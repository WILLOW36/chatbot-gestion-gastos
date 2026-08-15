from django.contrib import admin

from .models import Driver


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = (
        "identification_number",
        "full_name",
        "phone",
        "is_active",
        "created_at",
    )
    list_filter = ("is_active",)
    search_fields = ("identification_number", "full_name")