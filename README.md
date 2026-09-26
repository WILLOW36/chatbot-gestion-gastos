# Chatbot de Gestión de Gastos

Aplicación web Full Stack para registrar gastos de conductores mediante un chatbot.

El usuario se identifica, envía una foto del recibo, revisa los datos extraídos y confirma el gasto. El sistema también permite tomar una nueva foto si la información no es correcta.

## Tecnologías

- Python
- Django
- Django REST Framework
- React
- Vite
- JavaScript
- SQLite
- Google Gemini API
- Git / GitHub

## Arquitectura

```text
React
  ↓
Django REST API
  ↓
ConversationService
  ↓
ReceiptExtractionFactory
  ├── Mock
  └── Gemini
  ↓
ExpenseService
  ↓
SQLite
```

### Proveedores de extracción

El proyecto permite seleccionar el proveedor mediante `AI_PROVIDER`.

#### Modo demo

```env
AI_PROVIDER=mock
```

No requiere API externa y permite probar el proyecto localmente con datos simulados.

#### Modo Gemini

```env
AI_PROVIDER=gemini
GEMINI_API_KEY=tu_clave_de_gemini
GEMINI_MODEL=gemini-flash-lite-latest
```

## Instalación

### 1. Clonar

```bash
git clone https://github.com/WILLOW36/chatbot-gestion-gastos.git
cd chatbot-gestion-gastos
```

### 2. Configurar Backend

Crear `.env` en la raíz del proyecto.

Para probar localmente:

```env
AI_PROVIDER=mock
DJANGO_SECRET_KEY=tu_clave_secreta
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

Instalar dependencias:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### 3. Configurar Frontend

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

Aplicación disponible en:

```text
http://localhost:5173/
```

## Prueba rápida

Imagen de prueba:

```text
backend/test_images/recibo_prueba.jpg
```

Flujo:

```text
Hola
  ↓
123456789
  ↓
1. Registrar un gasto
  ↓
Enviar recibo
  ↓
Revisar datos
  ↓
Confirmar
```

Datos de prueba:

```text
Cédula: 123456789
Nombre: Juan Perez
```

En modo `mock` se utilizan datos simulados para demostrar el flujo completo.

## API

```text
POST /api/conversations/
GET  /api/conversations/<session_key>/
```

## Estado

MVP funcional de extremo a extremo con:

- [x] Identificación de conductores
- [x] Registro de gastos
- [x] Carga de recibos
- [x] Extracción de información
- [x] Confirmación y rechazo
- [x] Nueva fotografía
- [x] Persistencia en SQLite

Aplicación web desarrollada como proyecto personal sobre una experiencia real paraque se puedan registrar gastos de conductores mediante un chatbot.