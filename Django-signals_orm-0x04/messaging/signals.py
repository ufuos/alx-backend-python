from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Message, Notification
from .models import Message, MessageHistory

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    """Automatically create a notification when a new message is sent"""
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )
@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    # If updating (not creating a new message)
    if instance.pk:
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message.content != instance.content:
                # Save old content to history
                MessageHistory.objects.create(
                    message=old_message,
                    old_content=old_message.content
                )
                # Mark message as edited
                instance.edited = True
        except Message.DoesNotExist:
            pass
