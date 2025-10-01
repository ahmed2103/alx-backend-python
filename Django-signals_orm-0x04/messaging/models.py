from django.db import models
from django.contrib.auth import get_user_model
from .managers import UnreadMessagesManager
User = get_user_model()

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField(null=False, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    parent_message = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="replies")
    read = models.BooleanField(default=False)

    objects = models.Manager()  # The default manager.
    unread = UnreadMessagesManager()  # Custom manager for unread messages.



class Notification(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)

class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="history")
    timestamp = models.DateTimeField(auto_now_add=True)
    old_content = models.TextField(null=False, blank=False)
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="edited_messages")



