from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, Notification

@receiver(post_save, sender=Order)
def order_status_notification(sender, instance, created, **kwargs):
    if not created:
        message = f"Your order #{instance.id} status has been updated to '{instance.status}'."
        Notification.objects.create(user=instance.customer, message=message)
