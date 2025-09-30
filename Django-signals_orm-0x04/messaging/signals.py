from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification

@receiver(post_save, sender=Message)
def send_notification(sender, instance, created, **kwargs):
    if created:
        notification = Notification.objects.create(owner=instance.receiver, message=instance)

