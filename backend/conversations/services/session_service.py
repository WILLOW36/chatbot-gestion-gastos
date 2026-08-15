from conversations.models import ConversationSession
from drivers.models import Driver
from expenses.models import Expense


class SessionService:
    """
    Gestiona la creación y recuperación de sesiones
    persistentes del chatbot.
    """

    @staticmethod
    def get_or_create_session(
        session_key: str,
    ) -> ConversationSession:
        """
        Obtiene una sesión existente o crea una nueva.

        El uso de get_or_create permite que una misma sesión
        no tenga que ser creada manualmente por el cliente.
        """

        session, _ = ConversationSession.objects.get_or_create(
            session_key=session_key,
        )

        return session
    
    @staticmethod
    def update_step(
        session: ConversationSession,
        step: str,
    ) -> ConversationSession:
        """
        Actualiza el estado actual de una conversación.
        """

        session.current_step = step
        session.save(
            update_fields=[
                "current_step",
                "updated_at",
            ]
        )

        return session
    
    @staticmethod
    def assign_driver(
        session: ConversationSession,
        driver: Driver,
    ) -> ConversationSession:
        """
        Asocia un conductor a la sesión y persiste la relación.
        """

        session.driver = driver

        session.save(
            update_fields=[
                "driver",
                "updated_at",
            ]
        )

        return session
    
    def set_pending_expense(
        self,
        session: ConversationSession,
        expense: Expense | None,
    ) -> ConversationSession:
        """
        Asocia un gasto pendiente a la sesión actual.

        Esto permite saber qué gasto está esperando
        confirmación por parte del conductor.
        """

        session.pending_expense = expense
        session.save(
            update_fields=[
                "pending_expense",
                "updated_at",
            ]
        )

        return session