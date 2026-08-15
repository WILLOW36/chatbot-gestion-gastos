from django.contrib import admin

from .models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "driver",
        "merchant_name",
        "amount",
        "expense_date",
        "status",
        "created_at",
    )
    list_filter = ("status", "expense_date")
    search_fields = ("merchant_name", "nit", "driver__full_name")
    readonly_fields = ("receipt_image_preview",)

    def receipt_image_preview(self, obj):
        from django.utils.html import format_html
        if obj.receipt_image:
            return format_html(
                '<img src="{}" style="max-height: 400px;" />',
                obj.receipt_image.url,
            )
        return "Sin imagen"