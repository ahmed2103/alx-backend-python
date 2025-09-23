from django.core.exceptions import PermissionDenied
from rest_framework import viewsets, permissions, status, filters

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from django_filters.rest_framework import DjangoFilterBackend

class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing conversations and creating new ones
    """
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        """
        Filter conversations to only show those where the current user is a participant
        """
        user = self.request.user
        return Conversation.objects.filter(participants=user).prefetch_related('messages__sender')


    def perform_create(self, serializer):
        """
        Create a new conversation with the current user as a participant
        """

        user = self.request.user
        serializer.save(participants=[user])



class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing messages and sending new ones
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['message_body', 'sender__first_name', 'sender__last_name']
    ordering_fields = ['sent_at']

    def get_queryset(self):
        """
        Filter messages to only show those in conversations where the current user is a participant
        """
        conversation_pk = self.kwargs['conversation_pk']
        return Message.objects.filter(
            conversation__participants=self.request.user,
            conversation__pk=conversation_pk
        ).order_by('sent_at')

    def perform_create(self, serializer):
        """
        Send a message in a conversation
        """
        conversation_pk = self.kwargs['conversation_pk']
        try:
            conversation = self.request.user.conversations.get(pk=conversation_pk)
            serializer.save(sender=self.request.user, conversation=conversation)
        except Conversation.DoesNotExist:
            raise PermissionDenied("You are not a participant in this conversation.")

