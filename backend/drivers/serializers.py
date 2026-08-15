from rest_framework import serializers

from .models import Driver


class DriverSerializer(serializers.ModelSerializer):
    """
    Serializer responsable de convertir objetos Driver
    a JSON y validar datos relacionados con conductores.
    """

    class Meta:
        model = Driver
        fields = [
            "id",
            "identification_number",
            "full_name",
            "phone",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]