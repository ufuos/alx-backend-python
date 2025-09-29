# chats/filters.py
import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    # Filter messages by user id (sender or recipient)
    sender = django_filters.NumberFilter(field_name="sender__id")
    recipient = django_filters.NumberFilter(field_name="recipient__id")
    
    # Filter messages by created_at datetime range
    start_date = django_filters.DateTimeFilter(field_name="created_at", lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name="created_at", lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['sender', 'recipient', 'start_date', 'end_date']
