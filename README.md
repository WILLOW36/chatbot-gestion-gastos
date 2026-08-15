# Chatbot de Gestión de Gastos

Aplicación web desarrollada como proyecto personal sobre una experiencia real paraque se puedan registrar gastos de conductores mediante un chatbot.

El usuario se identifica con su número de cédula, selecciona la opción de registrar un gasto y envía una foto del recibo. La aplicación utiliza Google Gemini para extraer los datos principales del comprobante y luego permite confirmar el gasto antes de guardarlo.

## ¿Qué hace?

* Identifica al conductor por número de cédula.
* Permite registrar un gasto desde una fotografía.
* Extrae automáticamente NIT, comercio, monto, descripción y fecha.
* Mantiene el estado de la conversación.
* Guarda los gastos en la base de datos.
* Permite confirmar el registro desde el chatbot.

## Tecnologías

**Backend**

* Python
* Django
* Django REST Framework
* SQLite

**Frontend**

* React
* Vite
* JavaScript
* CSS

**IA**

* Google Gemini API
* SDK `google-genai`
* Modelo configurado mediante `GEMINI_MODEL`

## Cómo funciona

```text
Cédula
  ↓
Menú
  ↓
Registrar gasto
  ↓
Foto del recibo
  ↓
Google Gemini
  ↓
Datos extraídos
  ↓
Confirmación
  ↓
Gasto registrado
```

## Ejecutar el proyecto

### 1. Clonar

```bash
git clone <URL_DEL_REPOSITORIO>
cd chatbot
```

### 2. Configurar Gemini

Crear el archivo `.env` en la raíz:

```env
GEMINI_API_KEY=tu_clave_de_gemini
GEMINI_MODEL=gemini-flash-lite-latest
```

No subir nunca el archivo `.env` al repositorio.

### 3. Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Backend:

`http://127.0.0.1:8000/`

### 4. Frontend

En otra terminal:

```powershell
cd frontend
npm install
npm run dev
```

En PowerShell, si `npm` está bloqueado por la política de ejecución:

```powershell
npm.cmd install
npm.cmd run dev
```

Frontend:

`http://localhost:5173/`

## Probar el chatbot

Para probar rápidamente el flujo se puede utilizar la imagen:

```text
backend/test_images/recibo_prueba.jpg
```

Flujo de prueba:

```text
Hola
  ↓
123456789
  ↓
1
  ↓
Enviar recibo
  ↓
Revisar datos extraídos
  ↓
Confirmar
```

Durante el desarrollo se utilizó como conductor de prueba:

```text
Cédula: 123456789
Nombre: Juan Perez
```

## API principal

```text
POST /api/conversations/
```

Recibe mensajes e imágenes del chatbot.

```text
GET /api/conversations/<session_key>/
```

Permite consultar el estado actual de una sesión.

## Estructura

```text
chatbot/
├── backend/
│   ├── conversations/
│   ├── drivers/
│   ├── expenses/
│   ├── test_images/
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   └── package.json
│
├── .env.example
├── .gitignore
└── README.md
```

## Estado del proyecto

Actualmente el MVP funciona de extremo a extremo:

* React conectado con Django REST.
* Identificación de conductores.
* Registro de gastos.
* Carga de recibos.
* Extracción de información con Gemini.
* Persistencia en SQLite.
* Confirmación del gasto.

## Próximas mejoras

* Mejorar el flujo de rechazo y nueva fotografía.
* Manejo más robusto de errores de Gemini.
* Pruebas automatizadas.
* Mejoras de sesión y recuperación de conversaciones.
* Preparación para despliegue.

## Nota

Es un proyecto desarrollado Full Stack y está preparado actualmente para ejecución local y debe complementarse con controles adicionales antes de utilizarse en producción.


