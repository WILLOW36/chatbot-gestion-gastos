from datetime import date
from decimal import Decimal, InvalidOperation
from django.db import transaction
from django.utils import timezone

from expenses.models import Expense
from drivers.models import Driver


class ExpenseService:
    """
    Gestiona las operaciones relacionadas con los gastos.

    Este servicio mantiene separada la lógica de negocio
    de las vistas HTTP y del flujo conversacional.
    """

    @transaction.atomic
    def create_pending_expense(
        self,
        driver: Driver,
        receipt_image,
    ) -> Expense:
        """
        Crea un gasto inicialmente pendiente.
        """

        expense = Expense.objects.create(
            driver=driver,
            receipt_image=receipt_image,
            status=Expense.Status.PENDING,
        )

        return expense

    @transaction.atomic
    def update_from_extraction(
        self,
        expense: Expense,
        extracted_data: dict,
    ) -> Expense:
        """
        Actualiza un gasto con los datos obtenidos
        mediante extracción de información del recibo por Gemini.
        """

        expense.nit = extracted_data.get(
            "nit",
            "",
        )

        expense.merchant_name = extracted_data.get(
            "merchant_name",
            "",
        )

        expense.description = extracted_data.get(
            "description",
            "",
        )

        amount = extracted_data.get("amount")

        if amount:
            try:
                expense.amount = Decimal(str(amount))
            except (InvalidOperation, ValueError):
                expense.amount = None
        else:
            expense.amount = None

        expense_date = extracted_data.get(
            "expense_date"
        )

        if expense_date:
            try:
                expense.expense_date = date.fromisoformat(
                    expense_date
                )
            except ValueError:
                expense.expense_date = None
        else:
            expense.expense_date = None

        expense.save(
            update_fields=[
                "nit",
                "merchant_name",
                "amount",
                "description",
                "expense_date",
            ]
        )

        return expense

    @staticmethod
    def _parse_amount(value: str):
        """
        Convierte el monto devuelto por Gemini
        a Decimal de forma segura.
        """

        if not value:
            return None

        try:
            return Decimal(str(value))
        except (InvalidOperation, ValueError):
            return None

    @staticmethod
    def _parse_date(value: str):
        """
        Convierte una fecha YYYY-MM-DD a date.
        """

        if not value:
            return None

        from datetime import date

        try:
            return date.fromisoformat(value)
        except ValueError:
            return None
        
    def confirm_expense(
        self,
        expense: Expense,
    ) -> Expense:
        """
        Confirma un gasto pendiente.
        """

        expense.status = Expense.Status.CONFIRMED
        expense.confirmed_at = timezone.now()

        expense.save(
            update_fields=[
                "status",
                "confirmed_at",
            ]
        )

        return expense
    
    def reject_expense(
        self,
        expense: Expense,
    ) -> Expense:
        """
        Rechaza un gasto pendiente.
        """

        expense.status = Expense.Status.REJECTED

        expense.save(
            update_fields=[
                "status",
            ]
        )

        return expense