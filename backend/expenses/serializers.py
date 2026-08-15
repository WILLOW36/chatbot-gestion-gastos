from rest_framework import serializers

from .models import Expense


class ExpenseSerializer(serializers.ModelSerializer):
    """
    Serializer responsable de representar y validar
    los datos básicos de un gasto.
    """

    class Meta:
        model = Expense
        fields = [
            "id",
            "driver",
            "receipt_image",
            "nit",
            "merchant_name",
            "amount",
            "description",
            "expense_date",
            "status",
            "created_at",
            "confirmed_at",
        ]
        read_only_fields = [
            "id",
            "status",
            "created_at",
            "confirmed_at",
        ]