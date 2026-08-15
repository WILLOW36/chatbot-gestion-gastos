from django.urls import path

from .views import (
    ConversationSessionView,
    ConversationView,
)

urlpatterns = [
    path(
        "",
        ConversationView.as_view(),
        name="conversation",
    ),
    path(
        "<str:session_key>/",
        ConversationSessionView.as_view(),
        name="conversation-session",
    ),
]