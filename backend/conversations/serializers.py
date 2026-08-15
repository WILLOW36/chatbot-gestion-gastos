from rest_framework import serializers
from .models import ConversationSession

class ConversationSerializer(serializers.Serializer):
    """
    Serializer de entrada para las interacciones del chatbot.

    Este serializer valida únicamente la estructura y los datos
    recibidos. Las reglas de negocio pertenecen a los servicios.
    """

    session_key = serializers.CharField(
        max_length=64,
        required=True,
    )

    message = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    image = serializers.ImageField(
        required=False,
        allow_null=True,
    )

    def validate(self, attrs):
        """
        Valida que la petición contenga al menos una interacción:
        un mensaje o una imagen.
        """

        message = attrs.get("message", "").strip()
        image = attrs.get("image")

        if not message and image is None:
            raise serializers.ValidationError(
                "Debe proporcionar un mensaje o una imagen."
            )
            
        if message and image is not None:
            raise serializers.ValidationError(
                "No puede proporcionar un mensaje y una imagen "
                "en la misma solicitud."
            )

        return attrs
    
class ConversationSessionSerializer(serializers.ModelSerializer):
    """
    Serializer de salida para representar el estado actual
    de una sesión de conversación.
    """

    class Meta:
        model = ConversationSession
        fields = [
            "id",
            "session_key",
            "driver",
            "current_step",
            "pending_expense",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "session_key",
            "driver",
            "current_step",
            "pending_expense",
            "updated_at",
        ]