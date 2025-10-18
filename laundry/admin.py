from django.contrib import admin
from .models import User, Order, Notification


# --------------------------
# Custom User Admin
# --------------------------
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'role', 'phone_number', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'phone_number')
    ordering = ('id',)


# --------------------------
# Order Admin
# --------------------------
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'customer', 'service_type', 'status',
        'pickup_address', 'delivery_address', 'total_price',
        'created_at', 'updated_at'
    )
    list_filter = ('service_type', 'status', 'created_at')
    search_fields = ('customer__username', 'pickup_address', 'delivery_address')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')


# --------------------------
# Notification Admin
# --------------------------
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'message', 'is_read', 'timestamp')
    list_filter = ('is_read', 'timestamp')
    search_fields = ('user__username', 'message')
    ordering = ('-timestamp',)
    readonly_fields = ('timestamp',)
