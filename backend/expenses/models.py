from django.db import models

from drivers.models import Driver


class Expense(models.Model):
    """
    Representa un gasto reportado por un conductor a partir
    de la fotografía de un recibo.

    Los datos extraídos del recibo pueden quedar vacíos inicialmente
    porque serán completados posteriormente mediante OCR/IA
    y confirmación del conductor.
    """

    class Status(models.TextChoices):
        """
        Estados posibles del ciclo de vida de un gasto.
        """

        PENDING = "PENDING", "Pendiente"
        CONFIRMED = "CONFIRMED", "Confirmado"
        REJECTED = "REJECTED", "Rechazado"

    # Relación entre el gasto y el conductor que lo reportó.
    # PROTECT evita eliminar un conductor que tenga historial de gastos.
    driver = models.ForeignKey(
        Driver,
        on_delete=models.PROTECT,
        related_name="expenses",
    )

    # Imagen del recibo que será procesada por OCR/IA.
    receipt_image = models.ImageField(
        upload_to="receipts/%Y/%m/%d/",
    )

    # Datos que serán extraídos del recibo.
    # Pueden estar vacíos inicialmente.
    nit = models.CharField(
        max_length=30,
        blank=True,
    )

    merchant_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Comercio",
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )

    description = models.CharField(
        max_length=255,
        blank=True,
    )

    expense_date = models.DateField(
        null=True,
        blank=True,
    )

    # Estado actual del proceso de confirmación.
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    # Fecha y hora en la que se creó el gasto.
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    # Fecha y hora en la que el conductor confirmó el gasto.
    # Permanece NULL mientras el gasto no haya sido confirmado.
    confirmed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    def __str__(self):
        """
        Devuelve una representación legible del gasto.
        """
        return f"{self.merchant_name or 'Unknown merchant'} - {self.amount or 0}"
