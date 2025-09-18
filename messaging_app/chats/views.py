from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing conversations and creating new ones
    """
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'conversation_id'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['participants__first_name', 'participants__last_name', 'participants__email']
    ordering_fields = ['created_at']
    ordering = ['-created_at']  # newest first

    def get_queryset(self):
        """
        Filter conversations to only show those where the current user is a participant
        """
        return (
            Conversation.objects.filter(participants=self.request.user)
            .prefetch_related('participants', 'messages__sender')
            .distinct()
        )

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with given participants
        """
        participants = request.data.get("participants", [])
        if not participants:
            return Response(
                {"error": "Participants list is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing messages and sending new ones
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'message_id'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['message_body', 'sender__first_name', 'sender__last_name']
    ordering_fields = ['sent_at']
    ordering = ['-sent_at']  # newest messages first

    def get_queryset(self):
        """
        Filter messages to only show those in conversations where the current user is a participant
        """
        user_conversations = Conversation.objects.filter(participants=self.request.user)
        return (
            Message.objects.filter(conversation__in=user_conversations)
            .select_related('sender', 'conversation')
            .order_by('-sent_at')
        )

    def create(self, request, *args, **kwargs):
        """
        Send a message in a conversation
        """
        conversation_id = request.data.get("conversation_id")
        message_body = request.data.get("message_body")

        if not conversation_id or not message_body:
            return Response(
                {"error": "conversation_id and message_body are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        conversation = get_object_or_404(Conversation, conversation_id=conversation_id)

        if request.user not in conversation.participants.all():
            return Response(
                {"error": "You are not a participant in this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )

        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            message_body=message_body
        )
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
