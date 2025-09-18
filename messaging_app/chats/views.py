from .models import Conversation, Message
from rest_framework.response import Response
from rest_framework import viewsets, status, permissions
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)



class MessageViewSet(viewsets.ModelViewSet):
    """viewSet for listing messages and make new one"""
    serializer_class = MessageSerializer
    lookup_field = 'message_id'

    def get_queryset(self):
        """
        Filter messages to only show those in conversations where the current user is a participant
        """
        user_conversations = Conversation.objects.filter(participants=self.request.user)
        return Message.objects.filter(
            conversation__in=user_conversations
        ).select_related('sender', 'conversation').order_by('-sent_at')