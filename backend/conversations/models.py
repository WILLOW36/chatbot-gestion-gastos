from django.db import models

from drivers.models import Driver
from expenses.models import Expense


class ConversationSession(models.Model):
    """
    Representa el estado actual de una conversación del chatbot.

    La sesión permite que el sistema recuerde en qué paso del flujo
    se encuentra el conductor entre diferentes solicitudes HTTP.
    """

    class Step(models.TextChoices):
        """
        Estados posibles de la máquina de estados del chatbot.
        """

        GREETING = "GREETING", "Saludo inicial"
        AWAITING_CEDULA = "AWAITING_CEDULA", "Esperando cedula"
        MENU = "MENU", "Menu de opciones"
        AWAITING_IMAGE = "AWAITING_IMAGE", "Esperando imagen del recibo"
        CONFIRMING = "CONFIRMING", "Confirmando datos extraidos"
        DONE = "DONE", "Conversacion finalizada"

    # Identificador único de la sesión de conversación.
    session_key = models.CharField(
        max_length=64,
        unique=True,
    )

    # El conductor puede ser NULL mientras todavía no se ha identificado.
    driver = models.ForeignKey(
        Driver,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="conversation_sessions",
    )

    # Estado actual de la máquina de estados del chatbot.
    current_step = models.CharField(
        max_length=30,
        choices=Step.choices,
        default=Step.GREETING,
    )

    # Gasto que actualmente está pendiente de confirmación.
    pending_expense = models.ForeignKey(
        Expense,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="pending_in_sessions",
    )

    # Fecha y hora de la última modificación de la sesión.
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        """
        Devuelve una representación legible de la sesión.
        """
        return f"{self.session_key} - {self.current_step}"
