from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Conversation(models.Model):
# optional: group messages into conversations/rooms
 participants = models.ManyToManyField(User, related_name='conversations')
title = models.CharField(max_length=255, blank=True)
created_at = models.DateTimeField(auto_now_add=True)


def __str__(self):
 return self.title or f"Conversation {self.pk}"


class Message(models.Model):
 sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
conversation = models.ForeignKey(Conversation, null=True, blank=True, on_delete=models.CASCADE, related_name='messages')
content = models.TextField()
timestamp = models.DateTimeField(auto_now_add=True)


# Self-referential FK to represent a reply
parent_message = models.ForeignKey(
'self',
null=True,
blank=True,
related_name='children',
on_delete=models.SET_NULL,
help_text='Reference the parent message when this is a reply.'
)


class Meta:
 ordering = ['timestamp']
indexes = [
models.Index(fields=['sender']),
models.Index(fields=['receiver']),
models.Index(fields=['parent_message']),
models.Index(fields=['conversation']),
]


def __str__(self):
 return f"Message {self.pk} from {self.sender}"