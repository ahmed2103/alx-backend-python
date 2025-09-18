from rest_framework import serializers
from .models import User, Message, Conversation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'



class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(read_only=True)
    class Meta:
        model = Conversation
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    conversation = ConversationSerializer(read_only=True)
    class Meta:
        model = Message
        fields = '__all__'
