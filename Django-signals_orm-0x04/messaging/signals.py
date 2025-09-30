from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification,MessageHistory

@receiver(post_save, sender=Message)
def send_notification(sender, instance, created, **kwargs):
    if created:
        notification = Notification.objects.create(owner=instance.receiver, message=instance)

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:
        old_message = Message.objects.get(pk=instance.pk)
        if old_message.content != instance.content:
            MessageHistory.objects.create(message=instance, old_content=old_message.content)
            instance.edited = True


