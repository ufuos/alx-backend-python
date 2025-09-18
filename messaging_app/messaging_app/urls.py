"""
URL configuration for messaging_app project.
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from chats.views import ConversationViewSet, MessageViewSet  # fixed import

# Use DRF's router to auto-generate routes for ViewSets
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),          # ✅ API routes
    path('api-auth/', include('rest_framework.urls')),  # ✅ Added for browsable API login/logout
]
