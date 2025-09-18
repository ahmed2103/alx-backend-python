from rest_framework import viewsets, permissions
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing conversations and creating new ones
    """
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'conversation_id'

    def get_queryset(self):
        """
        Filter conversations to only show those where the current user is a participant
        """
        return Conversation.objects.filter(
            participants=self.request.user
        ).prefetch_related('participants', 'messages__sender').distinct()


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing messages and sending new ones
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'message_id'

    def get_queryset(self):
        """
        Filter messages to only show those in conversations where the current user is a participant
        """
        user_conversations = Conversation.objects.filter(participants=self.request.user)
        return Message.objects.filter(
            conversation__in=user_conversations
        ).select_related('sender', 'conversation').order_by('-sent_at')