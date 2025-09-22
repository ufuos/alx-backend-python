
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .filters import MessageFilter
from .pagination import MessagePagination
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, creating, and retrieving conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["participants"]  # filter by participants
    search_fields = ["title"]            # search by title if field exists
    ordering_fields = ["created_at"]     # order by creation time
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = MessagePagination
    filterset_class = MessageFilter

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation.
        Example: POST /conversations/
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation = serializer.save()
        return Response(
            ConversationSerializer(conversation).data,
            status=status.HTTP_201_CREATED,
        )

    @action(detail=True, methods=["post"])
    def send_message(self, request, pk=None):
        """
        Custom endpoint to send a message to an existing conversation.
        Example: POST /conversations/{id}/send_message/
        """
        conversation = self.get_object()
        # Ensure user is a participant
        if request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not a participant of this conversation."},
                status=status.HTTP_403_FORBIDDEN,
            )

        data = request.data.copy()
        data["conversation"] = conversation.id
        serializer = MessageSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(sender=request.user, conversation=conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get"])
    def messages(self, request, pk=None):
        """
        Retrieve all messages for a conversation.
        Example: GET /conversations/{id}/messages/
        """
        conversation = self.get_object()
        # Check if user is allowed to view
        if request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not authorized to view these messages."},
                status=status.HTTP_403_FORBIDDEN,
            )

        conversation_id = conversation.id
        messages = Message.objects.filter(conversation_id=conversation_id).order_by("timestamp")
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating messages.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["conversation", "sender"]  # filter by conversation or sender
    search_fields = ["content"]                    # search by message content
    ordering_fields = ["timestamp"]                # order by time sent

    def create(self, request, *args, **kwargs):
        """
        Create a new message.
        Example: POST /messages/
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        conversation_id = request.data.get("conversation")
        conversation = Conversation.objects.filter(id=conversation_id).first()
        if not conversation or request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not allowed to send messages in this conversation."},
                status=status.HTTP_403_FORBIDDEN,
            )

        message = serializer.save(sender=request.user, conversation=conversation)
        return Response(
            MessageSerializer(message).data,
            status=status.HTTP_201_CREATED,
        )
