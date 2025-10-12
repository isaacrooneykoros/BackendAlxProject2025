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
