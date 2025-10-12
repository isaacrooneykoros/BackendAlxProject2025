from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    RegisterView,NotificationSendView,
    OrderListCreateView, OrderDetailView,
    NotificationListView, NotificationUpdateView,
    OrderStatusUpdateView,NotificationCreateView
)

urlpatterns = [
    # Auth
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Orders
    path('orders/', OrderListCreateView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('orders/<int:pk>/status/', OrderStatusUpdateView.as_view(), name='order-status-update'),


    # Notifications
    path('notifications/', NotificationListView.as_view(), name='notifications'),
    path('notifications/<int:pk>/', NotificationUpdateView.as_view(), name='notification-update'),
    path('create/', NotificationCreateView.as_view(), name='notification-create'),
    path('notifications/send/', NotificationSendView.as_view(), name='notification-send'),  # 👈 New route
]
