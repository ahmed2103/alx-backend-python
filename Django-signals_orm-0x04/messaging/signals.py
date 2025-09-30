from django.db.models.signals import post_save, pre_save, post_delete
from django.db.models import Q
from django.dispatch import receiver
from .models import Message, Notification,MessageHistory
from django.contrib.auth import get_user_model

User = get_user_model()

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

@receiver(post_delete, sender=User)
def clean_user_related_data(sender, instance, **kwargs):
    Message.objects.filter(Q(sender = instance) | Q(receiver = instance)).delete()
    Notification.objects.filter(owner = instance).delete()
    MessageHistory.objects.filter(edited_by = instance).delete()


