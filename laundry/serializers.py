from rest_framework import serializers
from .models import User, Order, Notification
from django.contrib.auth import authenticate

# Register serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role', 'phone_number']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            role=validated_data.get('role', 'customer'),
            phone_number=validated_data.get('phone_number', '')
        )
        return user


# Login serializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid username or password")
        return user


# Order serializer
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['customer', 'created_at', 'updated_at']

class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']


class NotificationSerializer(serializers.ModelSerializer):
    # Allow admin to specify which user receives the notification
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
        request = self.context.get('request')
        if request and request.user.role != 'admin':
            raise serializers.ValidationError("Only admins can send notifications.")
        return data

class NotificationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['user', 'message']  # Admin specifies which user gets the notification
