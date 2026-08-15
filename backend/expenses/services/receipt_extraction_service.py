from decimal import Decimal, InvalidOperation
from datetime import datetime

from django.db import transaction

from expenses.models import Expense
from expenses.services.gemini_service import GeminiService


class ReceiptExtractionService:
    """
    Coordina la extracción de información de un recibo
    utilizando Gemini y la actualización del Expense.
    """

    def __init__(self):
        self.gemini_service = GeminiService()

    @transaction.atomic
    def extract_and_update(
        self,
        expense: Expense,
    ) -> Expense:
        """
        Extrae los datos del recibo y actualiza el Expense.
        """

        expense.receipt_image.open("rb")

        try:
            image_bytes = expense.receipt_image.read()
        finally:
            expense.receipt_image.close()

        mime_type = self._get_mime_type(
            expense.receipt_image.name
        )

        extracted_data = self.gemini_service.extract_receipt_data(
            image_bytes=image_bytes,
            mime_type=mime_type,
        )

        expense.nit = extracted_data.get("nit", "").strip()

        expense.merchant_name = extracted_data.get(
            "merchant_name",
            "",
        ).strip()

        expense.description = extracted_data.get(
            "description",
            "",
        ).strip()

        expense.amount = self._parse_amount(
            extracted_data.get("amount", "")
        )

        expense.expense_date = self._parse_date(
            extracted_data.get("expense_date", "")
        )

        expense.save(
            update_fields=[
                "nit",
                "merchant_name",
                "description",
                "amount",
                "expense_date",
            ]
        )

        return expense

    @staticmethod
    def _parse_amount(value: str):
        """
        Convierte el monto recibido de Gemini
        a Decimal.
        """

        if not value:
            return None

        try:
            return Decimal(value)
        except (InvalidOperation, ValueError):
            return None

    @staticmethod
    def _parse_date(value: str):
        """
        Convierte YYYY-MM-DD a date.
        """

        if not value:
            return None

        try:
            return datetime.strptime(
                value,
                "%Y-%m-%d",
            ).date()
        except ValueError:
            return None

    @staticmethod
    def _get_mime_type(file_name: str) -> str:
        """
        Determina el MIME type básico a partir
        de la extensión del archivo.
        """

        extension = file_name.lower().split(".")[-1]

        mime_types = {
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "png": "image/png",
            "webp": "image/webp",
        }

        return mime_types.get(
            extension,
            "application/octet-stream",
        )