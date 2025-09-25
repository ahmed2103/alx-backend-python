from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("you must provide email")
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    class Roles(models.TextChoices):
        GUEST = 'guest', 'Guest'
        HOST = 'host', 'HOST'
        ADMIN = 'admin', 'Admin'

    id = models.UUIDField(
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

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = UserManager()

    def __str__(self):
        return f"{self.email}+ {self.role}"

class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, unique=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    message_body = models.TextField(null= False)
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    sent_at = models.DateTimeField(auto_now_add=True)


