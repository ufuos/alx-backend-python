from django.contrib import admin
from .models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
 list_display = ('id', 'title', 'created_at')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
 list_display = ('id', 'sender', 'receiver', 'timestamp', 'parent_message')
list_filter = ('sender', 'receiver')