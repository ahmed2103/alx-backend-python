from .models import Conversation, Message
from rest_framework.response import Response
from rest_framework import viewsets, status, permissions
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    """viewSet for listing conversations and make new one"""
    serializer_class = ConversationSerializer
    queryset = Conversation.objects.all()
    lookup_field = 'conversation_id'

class MessageViewSet(viewsets.ModelViewSet):
    """viewSet for listing messages and make new one"""
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    lookup_field = 'message_id'
