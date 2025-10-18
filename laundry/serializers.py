from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Order, Notification


# -----------------------------
#  User Registration Serializer
# -----------------------------
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role', 'phone_number']

    def create(self, validated_data):
        """Create a new user with a hashed password"""
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            role=validated_data.get('role', 'customer'),
            phone_number=validated_data.get('phone_number', '')
        )
        return user


# -----------------------------
#  User Login Serializer
# -----------------------------
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """Authenticate user credentials"""
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid username or password.")
        return user


# -----------------------------
#  Order Serializer
# -----------------------------
class OrderSerializer(serializers.ModelSerializer):
    customer_username = serializers.CharField(source='customer.username', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'customer', 'customer_username', 'service_type', 'status',
            'pickup_address', 'delivery_address', 'total_price',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['customer', 'status', 'created_at', 'updated_at']

    def create(self, validated_data):
        """Attach the currently authenticated user as the customer."""
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['customer'] = request.user
        return super().create(validated_data)


# -----------------------------
#  Order Status Update Serializer
# -----------------------------
class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']


# -----------------------------
#  Notification Serializer
# -----------------------------
class NotificationSerializer(serializers.ModelSerializer):
    # Allow admin to specify which user receives the notification (by ID)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user',
        write_only=True
    )

    # Display the username of the recipient in responses
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'user_id', 'username', 'message', 'is_read', 'timestamp']
        read_only_fields = ['is_read', 'timestamp']

    def validate(self, data):
        """Ensure only admins can send notifications"""
        request = self.context.get('request')
        if request and request.user.role != 'admin':
            raise serializers.ValidationError("Only admins can send notifications.")
        return data


# -----------------------------
#  Notification Create Serializer (for admin use)
# -----------------------------
class NotificationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['user', 'message']
