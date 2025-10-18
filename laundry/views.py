from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import User, Order, Notification
from .serializers import (
    RegisterSerializer,
    OrderSerializer,
    OrderStatusUpdateSerializer,
    NotificationSerializer,
    NotificationCreateSerializer,
)

# -----------------------------
#  User Registration View
# -----------------------------
class RegisterView(generics.CreateAPIView):
    """
    Handles user registration.
    Accessible by anyone (no authentication required).
    """
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


# -----------------------------
#  Orders: List & Create
# -----------------------------
class OrderListCreateView(generics.ListCreateAPIView):
    """
    Customers: Can view their own orders and create new ones.
    Admin: Can view all orders.
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "admin":
            return Order.objects.all().order_by("-created_at")
        return Order.objects.filter(customer=user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


# -----------------------------
#  Order Detail / Update / Delete
# -----------------------------
class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Allows users to view details of a single order.
    Admin can edit or delete any order.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]


# -----------------------------
#  Admin: Update Order Status
# -----------------------------
class OrderStatusUpdateView(generics.UpdateAPIView):
    """
    Admin-only endpoint to update order status.
    """
    queryset = Order.objects.all()
    serializer_class = OrderStatusUpdateSerializer
    permission_classes = [permissions.IsAdminUser]


# -----------------------------
#  Notifications: List (User)
# -----------------------------
class NotificationListView(generics.ListAPIView):
    """
    Returns only notifications belonging to the authenticated user.
    Sorted by latest first.
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by("-timestamp")


# -----------------------------
#  Notifications: Mark as Read
# -----------------------------
class NotificationUpdateView(generics.UpdateAPIView):
    """
    Marks a notification as read.
    """
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(is_read=True)


# -----------------------------
#  Custom Permission: Admin or Staff
# -----------------------------
class IsAdminOrStaff(permissions.BasePermission):
    """
    Custom permission class allowing only admin/staff users.
    """
    def has_permission(self, request, view):
        return request.user and (request.user.role == "admin" or request.user.is_staff)


# -----------------------------
#  Admin: Create a Single Notification
# -----------------------------
class NotificationCreateView(generics.CreateAPIView):
    """
    Admin can create a notification for a specific user.
    """
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrStaff]

    def perform_create(self, serializer):
        serializer.save()


# -----------------------------
#  Admin: Send Notification to Any Customer
# -----------------------------
class NotificationSendView(generics.CreateAPIView):
    """
    Admin sends a notification to a specific user.
    """
    queryset = Notification.objects.all()
    serializer_class = NotificationCreateSerializer
    permission_classes = [permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Notification sent successfully!"}, status=status.HTTP_201_CREATED)


# -----------------------------
#  Admin: Bulk Notification Sender
# -----------------------------
class AdminSendNotificationView(generics.CreateAPIView):
    """
    Admin can send a message to all customers or a specific list of users.
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # ✅ Ensure only admins can perform this
        if request.user.role != "admin":
            return Response({"error": "Only admins can send notifications."}, status=403)

        message = request.data.get("message")
        user_ids = request.data.get("user_ids", None)  # list of user IDs
        send_to_all = request.data.get("send_to_all", False)

        if not message:
            return Response({"error": "Message field is required."}, status=400)

        # ✅ Get recipients
        if send_to_all:
            customers = User.objects.filter(role="customer")
        elif user_ids:
            customers = User.objects.filter(id__in=user_ids, role="customer")
        else:
            return Response({
                "error": "Provide either 'user_ids' (list) or set 'send_to_all' to true."
            }, status=400)

        # ✅ Bulk create notifications
        notifications = [
            Notification(user=customer, message=message)
            for customer in customers
        ]
        Notification.objects.bulk_create(notifications)

        return Response({
            "message": f"Notifications sent to {customers.count()} customer(s)."
        }, status=status.HTTP_201_CREATED)
