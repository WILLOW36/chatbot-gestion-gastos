from typing import Protocol


class ReceiptExtractionProvider(Protocol):
    """
    Contrato que deben cumplir los proveedores
    encargados de extraer información de un recibo.
    """

    def extract_receipt_data(
        self,
        image_bytes: bytes,
        mime_type: str,
    ) -> dict:
        ...