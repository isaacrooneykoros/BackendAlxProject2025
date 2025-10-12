from django.contrib.auth.models import User
from rest_framework import generics, permissions
from .models import Order, Notification
from .serializers import (
    RegisterSerializer,
    OrderSerializer,
    NotificationSerializer,OrderStatusUpdateSerializer,NotificationCreateSerializer
)
from rest_framework.response import Response
from rest_framework import status


# Register View
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


# Orders List/Create
class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Order.objects.all()
        return Order.objects.filter(customer=user)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


# Order Detail/Update/Delete
class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

class OrderStatusUpdateView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderStatusUpdateSerializer
    permission_classes = [permissions.IsAdminUser]


# Notifications List
class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return only the current user's notifications, newest first
        return Notification.objects.filter(user=self.request.user).order_by('-timestamp')


# Mark Notification as Read
class NotificationUpdateView(generics.UpdateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(is_read=True)

class IsAdminOrStaff(permissions.BasePermission):
    """Allow only admin/staff users to send notifications."""
    def has_permission(self, request, view):
        return request.user and request.user.is_staff  # or request.user.is_superuser


#Notification Create
class NotificationCreateView(generics.CreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrStaff]

    def perform_create(self, serializer):
        serializer.save()  # admin will provide the user field in the request

# 🟩 Admin-only: Send notification to any customer
class NotificationSendView(generics.CreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationCreateSerializer
    permission_classes = [permissions.IsAdminUser]  # Restrict to admins only

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Notification sent successfully!"}, status=status.HTTP_201_CREATED)

class AdminSendNotificationView(generics.CreateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if request.user.role != 'admin':
            return Response({"error": "Only admins can send notifications."}, status=403)

        message = request.data.get('message')
        user_ids = request.data.get('user_ids', None)  # list of IDs or None
        send_to_all = request.data.get('send_to_all', False)

        if not message:
            return Response({"error": "Message field is required."}, status=400)

        if send_to_all:
            customers = User.objects.filter(role='customer')
        elif user_ids:
            customers = User.objects.filter(id__in=user_ids, role='customer')
        else:
            return Response({
                "error": "Provide either 'user_ids' (list) or set 'send_to_all' to true."
            }, status=400)

        notifications = [
            Notification(user=customer, message=message)
            for customer in customers
        ]
        Notification.objects.bulk_create(notifications)

        return Response({
            "message": f"Notifications sent to {customers.count()} customer(s)."
        }, status=status.HTTP_201_CREATED)
