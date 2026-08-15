from conversations.models import ConversationSession
from conversations.constants import (
    AWAITING_IMAGE_MESSAGE,
    GOODBYE_MESSAGE,
    GREETING_MESSAGE,
    INVALID_DRIVER_MESSAGE,
    INVALID_MENU_OPTION_MESSAGE,
    MENU_MESSAGE,
)

from conversations.services.session_service import SessionService
from drivers.services.driver_service import DriverService
from expenses.services.expense_service import ExpenseService
from expenses.services.gemini_service import GeminiService


class ConversationService:
    """
    Coordina el flujo principal de una conversación.

    Esta clase no debería contener detalles de HTTP.
    Su responsabilidad es ejecutar las reglas de negocio
    relacionadas con el estado de la conversación.
    """

    def __init__(self):
        """
        Inicializa las dependencias necesarias para gestionar
        la conversación.
        """

        self.session_service = SessionService()
        self.driver_service = DriverService()
        self.expense_service = ExpenseService()
        self.gemini_service = GeminiService()

    def process_message(
        self,
        session_key: str,
        message: str,
        image=None,
    ) -> dict:
        """
        Procesa un mensaje de texto estado actual de la conversación recibido por el chatbot.

        En esta primera implementación solamente garantizamos
        que exista una sesión y devolvemos su estado actual.
        """

        session = self.session_service.get_or_create_session(
            session_key=session_key,
        )
        
        if session.current_step == ConversationSession.Step.GREETING:
            return self._handle_greeting(session)

        if (
            session.current_step
            == ConversationSession.Step.AWAITING_CEDULA
        ):
            return self._handle_identification(
                session=session,
                identification_number=message,
            )

        if session.current_step == ConversationSession.Step.MENU:
            return self._handle_menu(
                session=session,
                option=message,
            )

        if (
            session.current_step
            == ConversationSession.Step.AWAITING_IMAGE
        ):
            return self._handle_receipt_image(
                session=session,
                image=image,
            )
        
        if (
            session.current_step
            == ConversationSession.Step.CONFIRMING
        ):
            return self._handle_confirmation(
                session=session,
                option=message,
            )
            
        return {
            "session_key": session.session_key,
            "current_step": session.current_step,
            "message": "El flujo solicitado todavía no está implementado.",
        }

    def _handle_greeting(
        self,
        session: ConversationSession,
    ) -> dict:
        """
        Procesa el saludo inicial de la conversación.
        """

        self.session_service.update_step(
            session=session,
            step=ConversationSession.Step.AWAITING_CEDULA,
        )

        return {
            "session_key": session.session_key,
            "current_step": ConversationSession.Step.AWAITING_CEDULA,
            "message": GREETING_MESSAGE,
        }

    def _handle_identification(
        self,
        session: ConversationSession,
        identification_number: str,
    ) -> dict:
        """
        Busca un conductor activo utilizando su identificación.
        """

        driver = self.driver_service.find_active_driver_by_identification(
            identification_number=identification_number,
        )

        if driver is None:
            return {
                "session_key": session.session_key,
                "current_step": session.current_step,
                "message": INVALID_DRIVER_MESSAGE,
            }

        self.session_service.assign_driver(
            session=session,
            driver=driver,
        )

        self.session_service.update_step(
            session=session,
            step=ConversationSession.Step.MENU,
        )

        return {
            "session_key": session.session_key,
            "current_step": ConversationSession.Step.MENU,
            "message": MENU_MESSAGE.format(
                driver_name=driver.full_name,
            ),
        }

    def _handle_menu(
        self,
        session: ConversationSession,
        option: str,
    ) -> dict:
        """
        Procesa la opción seleccionada por el conductor.
        """

        normalized_option = option.strip()

        if normalized_option == "1":
            self.session_service.update_step(
                session=session,
                step=ConversationSession.Step.AWAITING_IMAGE,
            )

            return {
                "session_key": session.session_key,
                "current_step": (
                    ConversationSession.Step.AWAITING_IMAGE
                ),
                "message": AWAITING_IMAGE_MESSAGE,
            }

        if normalized_option == "2":
            self.session_service.update_step(
                session=session,
                step=ConversationSession.Step.DONE,
            )

            return {
                "session_key": session.session_key,
                "current_step": ConversationSession.Step.DONE,
                "message": GOODBYE_MESSAGE,
            }

        return {
            "session_key": session.session_key,
            "current_step": session.current_step,
            "message": INVALID_MENU_OPTION_MESSAGE,
        }
        
    def _handle_receipt_image(
        self,
        session: ConversationSession,
        image,
    ) -> dict:
        """
        Procesa la imagen del recibo enviada por el conductor.
        Flujo:

        1. Validar imagen.
        2. Validar conductor.
        3. Leer imagen.
        4. Crear Expense.
        5. Enviar imagen a Gemini.
        6. Actualizar Expense.
        7. Asociar Expense a la sesión.
        8. Cambiar estado a CONFIRMING
        """

        if image is None:
            return {
                "session_key": session.session_key,
                "current_step": session.current_step,
                "message": (
                    "Por favor, envía una imagen del recibo."
                ),
            }
            

        if session.driver is None:
            return {
                "session_key": session.session_key,
                "current_step": session.current_step,
                "message": (
                    "No se encontró un conductor asociado "
                    "a esta sesión."
                ),
            }
            
        image_bytes = image.read()
        
        if not image_bytes:
            return {
                "session_key": session.session_key,
                "current_step": session.current_step,
                "message": (
                    "La imagen recibida está vacía."
                ),
            }

        expense = self.expense_service.create_pending_expense(
            driver=session.driver,
            receipt_image=image,
        )
        
        extracted_data = (
            self.gemini_service.extract_receipt_data(
                image_bytes=image_bytes,
                mime_type=image.content_type,
            )
        )

        expense = self.expense_service.update_from_extraction(
            expense=expense,
            extracted_data=extracted_data,
        )

        self.session_service.set_pending_expense(
            session=session,
            expense=expense,
        )

        self.session_service.update_step(
            session=session,
            step=ConversationSession.Step.CONFIRMING,
        )

        return {
            "session_key": session.session_key,
            "current_step": ConversationSession.Step.CONFIRMING,
            "message": (
                "Recibo recibido correctamente. "
                "Estamos procesando la información."
            ),
            "data": {
                "expense_id": expense.id,
                "nit": expense.nit,
                "merchant_name": expense.merchant_name,
                "amount": (
                    str(expense.amount)
                    if expense.amount is not None
                    else None
                ),
                "description": expense.description,
                "expense_date": (
                    expense.expense_date.isoformat()
                    if expense.expense_date
                    else None
                ),
            },
        }
        
    def _handle_confirmation(
        self,
        session: ConversationSession,
        option: str,
    ) -> dict:
        """
        Procesa la confirmación o rechazo del gasto
        extraído del recibo.
        """

        if session.pending_expense is None:
            return {
                "session_key": session.session_key,
                "current_step": session.current_step,
                "message": (
                    "No existe un gasto pendiente "
                    "de confirmación."
                ),
            }

        normalized_option = option.strip()

        expense = session.pending_expense

        if normalized_option == "1":
            self.expense_service.confirm_expense(
                expense=expense,
            )

            self.session_service.set_pending_expense(
                session=session,
                expense=None,
            )

            self.session_service.update_step(
                session=session,
                step=ConversationSession.Step.DONE,
            )

            return {
                "session_key": session.session_key,
                "current_step": ConversationSession.Step.DONE,
                "message": (
                    "Gasto confirmado correctamente. "
                    "Gracias."
                ),
            }

        if normalized_option == "2":
            self.expense_service.reject_expense(
                expense=expense,
            )

            self.session_service.set_pending_expense(
                session=session,
                expense=None,
            )

            self.session_service.update_step(
                session=session,
                step=ConversationSession.Step.DONE,
            )

            return {
                "session_key": session.session_key,
                "current_step": ConversationSession.Step.DONE,
                "message": (
                    "Gasto rechazado correctamente."
                ),
            }

        return {
            "session_key": session.session_key,
            "current_step": session.current_step,
            "message": (
                "Opción no válida. "
                "Responde 1 para confirmar "
                "o 2 para rechazar."
            ),
        }
        
