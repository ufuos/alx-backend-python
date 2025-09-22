
from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation
    to access and modify its messages.
    """

    def has_permission(self, request, view):
        # Only allow authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Check if the user is a participant of the conversation
        related to the message or conversation object.
        """
        # Safe methods (GET, HEAD, OPTIONS) are always allowed if the user is a participant
        if request.method in permissions.SAFE_METHODS:
            if hasattr(obj, "conversation"):
                return request.user in obj.conversation.participants.all()
            if hasattr(obj, "participants"):
                return request.user in obj.participants.all()
            return False

        # For write methods (PUT, PATCH, DELETE), user must also be a participant
        if request.method in ["PUT", "PATCH", "DELETE"]:
            if hasattr(obj, "conversation"):
                return request.user in obj.conversation.participants.all()
            if hasattr(obj, "participants"):
                return request.user in obj.participants.all()
            return False

        return False
