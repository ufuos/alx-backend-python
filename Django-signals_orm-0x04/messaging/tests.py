
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

class SignalTestCase(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username="alice", password="password123")
        self.receiver = User.objects.create_user(username="bob", password="password123")

    def test_notification_created_on_message(self):
        message = Message.objects.create(sender=self.sender, receiver=self.receiver, content="Hello Bob!")
        notification = Notification.objects.get(user=self.receiver, message=message)
        self.assertEqual(notification.user, self.receiver)
        self.assertFalse(notification.is_read)
