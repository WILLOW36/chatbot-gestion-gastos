from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ConversationSession
from .serializers import (
    ConversationSerializer,
    ConversationSessionSerializer,
)
from .services.conversation_service import ConversationService

class ConversationView(APIView):
    """
    Endpoint principal para recibir interacciones del chatbot.

    En esta primera etapa solamente validamos la solicitud.
    La lógica de negocio será delegada posteriormente
    a ConversationService.
    """

    def post(self, request):
        """
        Recibe una interacción del usuario.

        Puede contener:
        - Un mensaje de texto.
        - Una imagen.

        La lógica de negocio todavía no se ejecuta aquí.
        """

        serializer = ConversationSerializer(
            data=request.data,
        )

        serializer.is_valid(raise_exception=True)
        
        service = ConversationService()
        
        result = service.process_message(
            session_key=serializer.validated_data["session_key"],
            message=serializer.validated_data.get("message", ""),
            image=serializer.validated_data.get("image"),
        )

        return Response(
            {
                "success": True,
                "message": "Request received successfully.",
                "data": result,
            },
            status=status.HTTP_200_OK,
        )
        
class ConversationSessionView(APIView):
    """
    Endpoint encargado de consultar el estado actual
    de una sesión de conversación.
    """

    def get(self, request, session_key):
        """
        Obtiene una sesión utilizando su session_key.
        """

        session = get_object_or_404(
            ConversationSession,
            session_key=session_key,
        )

        serializer = ConversationSessionSerializer(session)
        
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )