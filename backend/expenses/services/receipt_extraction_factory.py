import os


class ReceiptExtractionFactory:
    """
    Crea el proveedor de extracción configurado
    mediante la variable de entorno AI_PROVIDER.
    """

    @staticmethod
    def create():
        provider = os.getenv(
            "AI_PROVIDER",
            "mock",
        ).strip().lower()

        if provider == "mock":
            from expenses.services.mock_receipt_service import (
                MockReceiptExtractionService,
            )

            return MockReceiptExtractionService()

        if provider == "gemini":
            from expenses.services.gemini_service import (
                GeminiService,
            )

            return GeminiService()

        raise ValueError(
            f"AI_PROVIDER no soportado: {provider}"
        )