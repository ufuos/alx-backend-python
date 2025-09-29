
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, logout
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.cache import cache_page   # ✅ import cache_page
from .models import Message

User = get_user_model()


@login_required
def delete_user(request):
    """
    View to allow a logged-in user to delete their own account.
    """
    user = request.user
    user.delete()   # This will trigger post_delete signal
    logout(request)
    return HttpResponse("Your account and all related data have been deleted successfully.")


@login_required
def send_message(request):
    """
    View for sending a message from the logged-in user (sender)
    to another user (receiver).
    """
    if request.method == "POST":
        receiver_id = request.POST.get("receiver_id")
        content = request.POST.get("content")

        if not receiver_id or not content:
            return JsonResponse({"error": "receiver_id and content are required"}, status=400)

        receiver = get_object_or_404(User, id=receiver_id)

        # Save the message
        message = Message.objects.create(
            sender=request.user,
            receiver=receiver,
            content=content
        )

        return JsonResponse({
            "message": "Message sent successfully",
            "id": message.id,
            "sender": request.user.username,
            "receiver": receiver.username,
            "content": message.content,
            "timestamp": message.timestamp,
        }, status=201)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@cache_page(60)         # ✅ explicitly cache for 60 seconds
@login_required
def inbox(request):
    """
    View to get all messages for the logged-in user.
    Uses select_related to optimize sender/receiver queries.
    """
    messages = (
        Message.objects
        .filter(receiver=request.user)
        .select_related("sender", "receiver")
        .order_by("-timestamp")
    )

    data = [
        {
            "id": msg.id,
            "sender": msg.sender.username,
            "receiver": msg.receiver.username,
            "content": msg.content,
            "timestamp": msg.timestamp,
        }
        for msg in messages
    ]

    return JsonResponse({"messages": data}, status=200)
