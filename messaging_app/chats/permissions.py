
from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation
    to access its messages.
    """

    def has_permission(self, request, view):
        # Only allow authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Check if the user is a participant of the conversation
        related to the message or conversation object.
        """
        # If obj is a Message, check obj.conversation participants
        if hasattr(obj, "conversation"):
            return request.user in obj.conversation.participants.all()

        # If obj is a Conversation, check its participants directly
        if hasattr(obj, "participants"):
            return request.user in obj.participants.all()

        return False
