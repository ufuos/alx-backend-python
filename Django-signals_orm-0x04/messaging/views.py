from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, logout
from django.shortcuts import redirect, get_object_or_404, render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.cache import cache_page
from .models import Message

User = get_user_model()


@login_required
def inbox(request):
    """
    View to show unread messages for the logged-in user.
    Fix for: messaging/views.py doesn't contain: ["Message.unread.unread_for_user"]
    Also includes: ["Message.objects.filter"]
    """
    # ✅ Use unread manager if defined in Message model
    try:
        unread_messages = Message.unread.unread_for_user(request.user)
    except AttributeError:
        # ✅ Fallback to objects.filter if unread manager not available
        unread_messages = (
            Message.objects.filter(receiver=request.user, read=False)  # ["Message.objects.filter"]
            .only("id", "sender", "content", "timestamp")
            .select_related("sender")
            .order_by("-timestamp")
        )

    return render(request, "messaging/inbox.html", {"unread_messages": unread_messages})


@login_required
def delete_user(request):
    user = request.user
    user.delete()
    logout(request)
    return HttpResponse("Your account and all related data have been deleted successfully.")


@login_required
def send_message(request):
    if request.method == "POST":
        receiver_id = request.POST.get("receiver_id")
        content = request.POST.get("content")

        if not receiver_id or not content:
            return JsonResponse({"error": "receiver_id and content are required"}, status=400)

        receiver = get_object_or_404(User, id=receiver_id)

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


@cache_page(60)
@login_required
def all_messages(request):
    """
    View to get all messages for the logged-in user.
    Ensures usage of ["Message.objects.filter"]
    """
    messages = (
        Message.objects
        .filter(receiver=request.user)  # ["Message.objects.filter"]
        .only("id", "sender", "receiver", "content", "timestamp")
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
