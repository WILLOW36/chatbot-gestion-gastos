# Mensaje mostrado al iniciar una conversación.
GREETING_MESSAGE = (
    "¡Hola! Soy el asistente de gastos. "
    "Por favor, ingresa tu número de cédula."
)

# Mensaje mostrado cuando no se encuentra el conductor.
INVALID_DRIVER_MESSAGE = (
    "No encontramos un conductor activo con ese número de identificación. "
    "Verifica el número e inténtalo nuevamente."
)

# Menú principal del chatbot.
MENU_MESSAGE = (
    "Hola {driver_name}. ¿Qué deseas hacer?\n\n"
    "1. Registrar un gasto\n"
    "2. Salir"
)

# Mensaje cuando el usuario selecciona registrar un gasto.
AWAITING_IMAGE_MESSAGE = (
    "Perfecto. Por favor, envía una foto clara del recibo."
)

# Mensaje cuando la opción del menú no es válida.
INVALID_MENU_OPTION_MESSAGE = (
    "Opción no válida. Por favor, selecciona:\n\n"
    "1. Registrar un gasto\n"
    "2. Salir"
)

# Mensaje cuando el usuario decide terminar la conversación.
GOODBYE_MESSAGE = (
    "Gracias. ¡Hasta luego!"
)