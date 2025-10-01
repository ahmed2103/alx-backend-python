from django.db.models.query_utils import Q
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import logout
from .models import Message

def build_thread(message):
    thread = {
        'id': message.id,
        'sender': message.sender.username,
        'receiver': message.receiver.username,
        'content': message.content,
        'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'edited': message.edited
    }
    for reply in message.replies.all().select_related('sender', 'receiver'):
        thread['replies'].append(build_thread(reply))
    return thread


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_user(request):
    user = request.user
    user.delete()
    logout(request)
    return Response({"message": "User deleted successfully"},status=status.HTTP_204_NO_CONTENT)



@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_threaded_conversation(request):
    messages = (Message.objects.filter(sender=request.user)
                .select_related('sender', 'receiver')
                .prefetch_related('replies__sender', 'replies__receiver'))
    threads = []
    for message in messages.filter(parent_message__isnull=True):
        threads.append(build_thread(message))
    return Response(threads, status=status.HTTP_200_OK)



