
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# ----------------------
# Custom Manager
# ----------------------
class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        return (
            self.get_queryset()
            .filter(receiver=user, read=False)  # ✅ correct fields
            .only("id", "sender", "receiver", "content", "timestamp")  # ✅ optimization
        )


class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_messages"
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)

    # track if edited
    edited_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="edited_messages",
    )

    # threaded conversations
    parent_message = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="replies",
        on_delete=models.CASCADE,
    )

    # ✅ managers
    objects = models.Manager()  # default
    unread = UnreadMessagesManager()  # custom

    # ✅ new field to track read/unread
    read = models.BooleanField(default=False)

    def __str__(self):
        if self.parent_message:
            return f"Reply by {self.sender} to {self.parent_message.id}: {self.content[:20]}"
        return f"From {self.sender} to {self.receiver}: {self.content[:20]}"


class Notification(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user} about message {self.message.id}"


class MessageHistory(models.Model):
    message = models.ForeignKey(
        Message, related_name="history", on_delete=models.CASCADE
    )
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="edit_history",
    )

    def __str__(self):
        return f"History of message {self.message.id} at {self.edited_at}"
