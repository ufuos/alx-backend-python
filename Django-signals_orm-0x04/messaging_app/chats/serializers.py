from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """Serializer for Django User model (basic fields)."""

    class Meta:
        model = User
        fields = ["id", "username", "email"]


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for messages in a conversation."""
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ["id", "sender", "content", "timestamp"]


class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for conversations with nested users and messages."""
    name = serializers.CharField(required=True, max_length=255)
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ["id", "name", "participants", "messages", "last_message"]

    def get_last_message(self, obj):
        """Return the most recent message in the conversation."""
        last_msg = obj.messages.order_by("-timestamp").first()
        return MessageSerializer(last_msg).data if last_msg else None

    def validate_name(self, value):
        """Ensure the conversation name is not empty or too short."""
        if not value.strip():
            raise serializers.ValidationError("Conversation name cannot be empty.")
        if len(value) < 3:
            raise serializers.ValidationError("Conversation name must be at least 3 characters long.")
        return value
