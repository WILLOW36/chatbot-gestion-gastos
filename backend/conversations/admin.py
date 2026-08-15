from django.contrib import admin

from .models import ConversationSession


@admin.register(ConversationSession)
class ConversationSessionAdmin(admin.ModelAdmin):
    list_display = (
        "session_key",
        "driver",
        "current_step",
        "pending_expense",
        "updated_at",
    )
    list_filter = ("current_step",)
    search_fields = ("session_key",)