from django.db import models


class Driver(models.Model):
    """
    Representa un conductor registrado en el sistema.

    La identificación del conductor es única y permite localizarlo
    durante el inicio de una conversación con el chatbot.
    """

    identification_number = models.CharField(
        max_length=20,
        unique=True,
        help_text="Número de cédula del conductor (identificador único)",
    )

    full_name = models.CharField(
        max_length=150,
        verbose_name="Nombre completo",
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Teléfono de contacto",
    )

    # Permite activar o desactivar un conductor sin eliminar su historial.
    is_active = models.BooleanField(default=True)

    # Fecha y hora en la que se creó el registro.
    created_at = models.DateTimeField(auto_now_add=True)

    # Fecha y hora de la última modificación del registro.
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Devuelve una representación legible del conductor.

        Esto será útil, por ejemplo, desde Django Admin.
        """
        return f"{self.identification_number} - {self.full_name}"