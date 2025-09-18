
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, creating, and retrieving conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    @action(detail=True, methods=["post"])
    def send_message(self, request, pk=None):
        """
        Custom endpoint to send a message to an existing conversation.
        Example: POST /conversations/{id}/send_message/
        """
        conversation = self.get_object()
        data = request.data.copy()
        data["conversation"] = conversation.id
        serializer = MessageSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating messages.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
