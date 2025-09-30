from django.db.models import signals
from django.dispatch import receiver
from .models import Message, Notification

@receiver(signals.post_save, sender=Message)
def send_notification(sender, instance, created, **kwargs):
    if created:
        notification = Notification(owner=instance.receiver, message=instance)
        notification.save()

