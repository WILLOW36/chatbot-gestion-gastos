class MockReceiptExtractionService:
    """
    Proveedor local para pruebas y demostraciones.

    No realiza llamadas a servicios externos.
    """

    def extract_receipt_data(
        self,
        image_bytes: bytes,
        mime_type: str,
    ) -> dict:
        """
        Devuelve datos simulados de un recibo.

        La imagen se recibe para mantener el mismo contrato
        que tendría un proveedor real de extracción.
        """

        if not image_bytes:
            raise ValueError(
                "La imagen del recibo está vacía."
            )

        return {
            "nit": "900276962-1",
            "merchant_name": "D1 SAS",
            "amount": "66200.00",
            "description": "Compra de viveres y aseo",
            "expense_date": "2026-08-07",
        }