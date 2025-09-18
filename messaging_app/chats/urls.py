
from django.urls import path, include
from rest_framework import routers
from .views import ConversationViewSet, MessageViewSet

# Use DRF's router to auto-generate routes for ViewSets
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
]
