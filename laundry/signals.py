from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, Notification

@receiver(post_save, sender=Order)
def order_status_notification(sender, instance, created, **kwargs):
    if not created:
        message = f"Your order #{instance.id} status has been updated to '{instance.status}'."
        Notification.objects.create(user=instance.customer, message=message)

@receiver(post_save, sender=Order)
def send_order_status_notification(sender, instance, created, **kwargs):
    # Skip notification when order is first created
    if created:
        return

    # Create a notification message based on order status
    message = f"Hi {instance.customer.username}, your order #{instance.id} status has been updated to '{instance.status}'."

    # Create a notification for that customer
    Notification.objects.create(
        user=instance.customer,
        message=message
    )