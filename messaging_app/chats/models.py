from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    class Roles(models.TextChoices):
        GUEST = 'guest', 'Guest'
        HOST = 'host', 'HOST'
        ADMIN = 'admin', 'Admin'

    user_id = models.UUIDField(
        primary_key= True,
        default=uuid.uuid4,
        editable=False,
    )
    first_name = models.CharField(max_length=150, null=False, blank=False)
    last_name =models.CharField(max_length=150, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False, db_index=True)
    password_hash = models.CharField(max_length=255, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField(max_length=10, choices=Roles.choices, default=Roles.GUEST)
    created_at = models.DateTimeField(auto_now_add= True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.email}+ {self.role}"

class Conversation:
    conversation_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    participants = models.ManyToManyField(User, on_delete=models.CASCADE, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

class Message:
    message_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, unique=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    message_body = models.TextField(null= False)
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    sent_at = models.DateTimeField(auto_now_add=True)


