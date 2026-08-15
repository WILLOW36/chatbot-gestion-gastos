import json
import os

from google import genai
from google.genai import types


class GeminiService:
    """
    Servicio encargado de comunicarse con Google Gemini
    para extraer información estructurada de recibos.
    """

    DEFAULT_MODEL = "gemini-flash-lite-latest"

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "La variable de entorno GEMINI_API_KEY "
                "no está configurada."
            )

        self.client = genai.Client(
            api_key=api_key,
        )

        self.model_name = os.getenv(
            "GEMINI_MODEL",
            self.DEFAULT_MODEL,
        )

    def extract_receipt_data(
        self,
        image_bytes: bytes,
        mime_type: str = "mime_type",
    ) -> dict:
        """
        Analiza una imagen de recibo y devuelve
        los datos estructurados necesarios para un Expense.
        """

        response_schema = {
            "type": "OBJECT",
            "properties": {
                "nit": {
                    "type": "STRING",
                    "description": (
                        "NIT del establecimiento. "
                        "Cadena vacía si no es legible."
                    ),
                },
                "merchant_name": {
                    "type": "STRING",
                    "description": (
                        "Nombre del comercio o establecimiento. "
                        "Cadena vacía si no es legible."
                    ),
                },
                "amount": {
                    "type": "STRING",
                    "description": (
                        "Valor TOTAL del recibo. "
                        "Usar formato decimal, por ejemplo 25000.00. "
                        "Cadena vacía si no es legible."
                    ),
                },
                "description": {
                    "type": "STRING",
                    "description": (
                        "Descripción breve y útil del gasto. "
                        "Cadena vacía si no puede determinarse."
                    ),
                },
                "expense_date": {
                    "type": "STRING",
                    "description": (
                        "Fecha del gasto en formato YYYY-MM-DD. "
                        "Cadena vacía si no es legible."
                    ),
                },
            },
            "required": [
                "nit",
                "merchant_name",
                "amount",
                "description",
                "expense_date",
            ],
        }

        prompt = """
Analiza cuidadosamente la imagen del recibo.

Extrae exclusivamente la información necesaria
para registrar un gasto.

Reglas estrictas:

1. No inventes información.
2. Si un dato no aparece o no puede leerse correctamente,
   devuelve una cadena vacía.
3. El monto debe corresponder al valor TOTAL del recibo,
   cuando sea identificable.
4. La fecha debe utilizar el formato YYYY-MM-DD.
5. El NIT debe corresponder al establecimiento.
6. merchant_name debe contener el nombre del comercio.
7. description debe ser una descripción breve y útil del gasto.
8. No confundas subtotales, impuestos o descuentos con el total.
"""

        image_part = types.Part.from_bytes(
            data=image_bytes,
            mime_type=mime_type,
        )

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=[
                image_part,
                prompt,
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=response_schema,
            ),
        )

        return json.loads(response.text)