# messaging/manager.py
from django.db import models

class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        """
        Return only unread messages for the given user.
        Optimized with `.only()` to fetch minimal fields.
        """
        return (
            self.get_queryset()
            .filter(receiver=user, read=False)
            .only("id", "sender", "content", "timestamp")
        )
