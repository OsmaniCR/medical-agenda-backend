# Medical Agenda - Sistema de Agendamiento Médico con Chatbot

Sistema completo de agendamiento médico con autenticación JWT y chatbot integrado con OpenAI que permite gestionar citas médicas mediante conversación natural.

## 🚀 Características

- **Autenticación JWT**: Sistema de login/registro con tokens JWT
- **API CRUD**: Endpoints completos para gestionar citas médicas
- **Chatbot Inteligente**: Asistente virtual con OpenAI que permite:
  - Agendar nuevas citas
  - Listar citas existentes
  - Modificar citas
  - Eliminar citas
- **Frontend Moderno**: Interfaz construida con React, TypeScript, Tailwind CSS
- **Backend Robusto**: API REST con Django y Django REST Framework

## 📋 Requisitos Previos

- **Docker** y **Docker Compose** (requerido para el backend)
- **Bun** (para gestión de dependencias de Node.js en el frontend)
- **Make** (opcional, pero recomendado para facilitar el desarrollo)

**Nota**: El backend está completamente dockerizado, por lo que no necesitas instalar Python, Poetry ni ninguna otra dependencia de Python en tu sistema local.

### Instalación de Make

Si no tienes Make instalado, puedes instalarlo según tu sistema operativo:

#### macOS

```bash
# Usando Homebrew (recomendado)
brew install make

# O usando Xcode Command Line Tools
xcode-select --install
```

#### Linux (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install build-essential
```

#### Linux (Fedora/RHEL/CentOS)

```bash
sudo dnf install make
# o
sudo yum install make
```

#### Windows

En Windows, Make no está disponible de forma nativa. Tienes varias opciones:

**Opción 1: Usar WSL (Windows Subsystem for Linux)**

```bash
# Instala WSL desde PowerShell (como administrador)
wsl --install

# Luego instala make dentro de WSL
sudo apt-get update
sudo apt-get install build-essential
```

**Opción 2: Usar Chocolatey**

```bash
# Instala Chocolatey primero (si no lo tienes)
# Luego instala make
choco install make
```

**Opción 3: Usar Git Bash**
Make viene incluido con Git for Windows. Puedes usar los comandos del Makefile directamente en Git Bash.

**Nota**: Si no puedes instalar Make, puedes ejecutar los comandos manualmente. Ver la sección "Opción 1b: Ejecución Local (Manual)" más abajo.

## 🔧 Instalación y Configuración

### Backend

#### Opción 1: Ejecución Local (Recomendado - Usando Makefile)

**Setup inicial después de clonar el repositorio:**

1. **Crea el archivo `.env`** copiando desde `.env.example`:

   **Linux/macOS:**
   ```bash
   cd medical-agenda-backend
   cp .env.example .env
   ```

   **Windows (PowerShell):**
   ```powershell
   cd medical-agenda-backend
   Copy-Item .env.example .env
   ```

   **Windows (CMD):**
   ```cmd
   cd medical-agenda-backend
   copy .env.example .env
   ```

2. **Edita el archivo `.env`** y configura las variables necesarias:

   ```env
   # Requerido
   OPENAI_API_KEY=tu-api-key-de-openai
   SECRET_KEY=tu-secret-key-seguro
   ```

3. **Ejecuta el setup inicial:**

   ```bash
   make first-setup
   ```

   Este comando automáticamente:
   - Construye la imagen Docker
   - Inicia el contenedor
   - Ejecuta las migraciones
   - Crea el primer usuario (username: `admin`, password: `admin123`)

4. **Si necesitas reiniciar el contenedor después de editar el `.env`:**

   ```bash
   make restart
   ```

El backend estará disponible en `http://localhost:8000`

**Comandos útiles del Makefile:**

```bash
make help              # Muestra todos los comandos disponibles
make build             # Construye la imagen Docker
make run               # Inicia el servidor ASGI en modo foreground (ver logs en tiempo real)
make up                # Inicia los contenedores en modo background
make down              # Detiene los contenedores
make logs              # Muestra los logs
make restart           # Reinicia los contenedores
make shell             # Abre un shell en el contenedor
make migrate           # Ejecuta migraciones
make createsuperuser   # Crea un superusuario interactivo
make setup-first-user  # Crea el primer usuario (admin/admin123)
make test              # Ejecuta los tests
```

#### Ejecución Manual con Docker (sin Makefile)

1. Navega al directorio del backend:

```bash
cd medical-agenda-backend
```

2. Copia el archivo de ejemplo de variables de entorno:

   **Linux/macOS:**
   ```bash
   cp .env.example .env
   ```

   **Windows (PowerShell):**
   ```powershell
   Copy-Item .env.example .env
   ```

   **Windows (CMD):**
   ```cmd
   copy .env.example .env
   ```

3. Edita el archivo `.env` y configura las variables necesarias

4. Construye y ejecuta el contenedor:

   **Docker Compose v2:**
   ```bash
   docker compose up --build
   ```

   **Docker Compose v1:**
   ```bash
   docker-compose up --build
   ```

El backend estará disponible en `http://localhost:8000`

**Comandos Docker útiles:**

```bash
docker-compose build              # Construye la imagen
docker-compose up -d              # Inicia los contenedores en segundo plano
docker-compose down               # Detiene los contenedores
docker-compose logs -f           # Muestra los logs
docker-compose restart            # Reinicia los contenedores
docker-compose exec backend bash  # Abre un shell en el contenedor
docker-compose exec backend python manage.py migrate  # Ejecuta migraciones
```

### Frontend

1. Navega al directorio del frontend:

```bash
cd medical-agenda-frontend
```

2. Copia el archivo de ejemplo de variables de entorno:

```bash
cp .env.example .env
```

3. (Opcional) Edita el archivo `.env` si necesitas cambiar la URL de la API:

```bash
VITE_API_BASE_URL=http://localhost:8000/api
```

4. Instala las dependencias con Bun:

```bash
bun install
```

5. Inicia el servidor de desarrollo:

```bash
bun run dev
```

El frontend estará disponible en `http://localhost:5173`

## 📁 Estructura del Proyecto

```
medical-agenda/
├── medical-agenda-backend/
│   ├── apps/
│   │   ├── login/              # App de autenticación
│   │   │   ├── authentication.py  # Lógica JWT
│   │   │   ├── views.py        # Endpoints de login/registro
│   │   │   └── serializers.py  # Serializers de autenticación
│   │   └── medical_appointment/ # App de citas médicas
│   │       ├── models.py       # Modelo MedicalAppointment
│   │       ├── views.py        # Endpoints CRUD
│   │       ├── serializers.py  # Serializers de citas
│   │       ├── chatbot.py      # Lógica del chatbot con OpenAI
│   │       └── chatbot_views.py # Endpoint del chat
│   └── core/
│       └── settings.py          # Configuración Django
└── medical-agenda-frontend/
    ├── src/
    │   ├── pages/
    │   │   ├── Login.tsx        # Página de login/registro
    │   │   └── Chat.tsx         # Interfaz del chatbot
    │   ├── components/
    │   │   └── ProtectedRoute.tsx # Componente de protección de rutas
    │   ├── store/
    │   │   └── authStore.ts     # Store de autenticación con Zustand
    │   └── lib/
    │       └── api.ts           # Cliente API
```

## 🔌 Endpoints de la API

### Autenticación

- `POST /api/auth/register/` - Registro de nuevo usuario
- `POST /api/auth/login/` - Inicio de sesión

### Citas Médicas

- `GET /api/appointments/list/` - Listar todas las citas del usuario
- `POST /api/appointments/create/` - Crear una nueva cita
- `PUT /api/appointments/<id>/update/` - Actualizar una cita
- `DELETE /api/appointments/<id>/delete/` - Eliminar una cita

### Chatbot

- `POST /api/chat/` - Enviar mensaje al chatbot

**Ejemplo de request al chatbot:**

```json
{
  "message": "Agenda una cita para mañana a las 10:00 por dolor de cabeza",
  "conversation_history": []
}
```

## 🎨 Tecnologías Utilizadas

### Backend

- Django 6.0
- Django REST Framework
- ASGI (Uvicorn) - Servidor asíncrono
- PyJWT (autenticación JWT)
- OpenAI API (chatbot)
- django-cors-headers (CORS)
- python-decouple (variables de entorno)
- Docker (containerización)

### Frontend

- React 19
- TypeScript
- Vite
- Tailwind CSS
- Zustand (gestión de estado)
- React Router (routing)
- TanStack React Query (gestión de datos)
- Jose (JWT decoding)

## 🔐 Autenticación

El sistema utiliza JWT (JSON Web Tokens) para la autenticación. Los tokens se almacenan en el localStorage del navegador y se incluyen automáticamente en las peticiones mediante el header `Authorization: Bearer <token>`.

## 💬 Uso del Chatbot

El chatbot puede entender comandos en lenguaje natural. Ejemplos:

- "Agenda una cita para el 15 de diciembre a las 14:30 por revisión general"
- "Muéstrame mis citas"
- "Cambia la fecha de mi cita número 1 al 20 de diciembre"
- "Elimina la cita número 2"

## 🧪 Pruebas

Para probar el sistema:

1. Inicia ambos servidores (backend y frontend)
2. Accede a `http://localhost:5173`
3. Regístrate o inicia sesión
4. Comienza a chatear con el asistente para gestionar tus citas

## 🔐 Variables de Entorno

### Backend (.env)

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
CORS_ALLOW_CREDENTIALS=True

# JWT Settings
JWT_SECRET_KEY=your-jwt-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DELTA=86400

# OpenAI Settings (REQUERIDO)
OPENAI_API_KEY=your-openai-api-key-here
```

### Frontend (.env)

```env
# API Base URL
VITE_API_BASE_URL=http://localhost:8000/api
```

## 🛠️ Makefile - Comandos Rápidos

El backend incluye un Makefile con comandos útiles para facilitar el desarrollo. **Todos los comandos del Makefile usan solo Docker Compose** para garantizar portabilidad entre sistemas operativos (Linux, macOS, Windows).

**Nota sobre Docker Compose**: El Makefile está configurado para usar `docker compose` (v2) por defecto. Si tienes `docker-compose` (v1), edita el Makefile y cambia la línea 6 de `DOCKER_COMPOSE := docker compose` a `DOCKER_COMPOSE := docker-compose`.

### Setup Inicial (Después de Clonar)

**IMPORTANTE**: Antes de ejecutar `make first-setup`, debes crear el archivo `.env` manualmente:

**Linux/macOS:**
```bash
cd medical-agenda-backend
cp .env.example .env
```

**Windows (PowerShell):**
```powershell
cd medical-agenda-backend
Copy-Item .env.example .env
```

**Windows (CMD):**
```cmd
cd medical-agenda-backend
copy .env.example .env
```

Luego edita el `.env` y configura las variables necesarias (especialmente `OPENAI_API_KEY`).

Después ejecuta:
```bash
make first-setup
```

Este comando automáticamente:

- ✅ Construye la imagen Docker
- ✅ Inicia el contenedor
- ✅ Ejecuta migraciones
- ✅ Crea primer usuario (admin/admin123)

### Comandos Principales

```bash
make help              # Muestra todos los comandos disponibles
make first-setup       # Setup completo para nuevos desarrolladores
make build             # Construye la imagen Docker
make run               # Inicia el servidor ASGI en modo foreground (ver logs en tiempo real)
make up                # Inicia los contenedores en modo background
make down              # Detiene los contenedores
make logs              # Muestra los logs
make restart           # Reinicia los contenedores
make shell             # Abre shell en el contenedor
make migrate           # Ejecuta migraciones
make createsuperuser   # Crea superusuario (interactivo)
make setup-first-user  # Crea primer usuario (admin/admin123)
make test              # Ejecuta tests
```

### Limpieza Manual

Para limpiar archivos temporales de Python, ejecuta estos comandos según tu sistema:

**Linux/macOS:**
```bash
find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete
find . -type f -name "*.pyo" -delete
rm -rf .pytest_cache .coverage htmlcov
```

**Windows (PowerShell):**
```powershell
Get-ChildItem -Path . -Recurse -Filter __pycache__ | Remove-Item -Recurse -Force
Get-ChildItem -Path . -Recurse -Filter *.pyc | Remove-Item -Force
Get-ChildItem -Path . -Recurse -Filter *.pyo | Remove-Item -Force
Remove-Item -Path .pytest_cache,.coverage,htmlcov -Recurse -Force -ErrorAction SilentlyContinue
```

**Nota**: El Makefile solo contiene comandos de Docker Compose para garantizar portabilidad entre sistemas operativos.
```

## 🐳 Docker

El backend está completamente dockerizado. Todos los comandos del Makefile utilizan Docker internamente, por lo que no necesitas instalar Python, Poetry ni ninguna otra dependencia de Python en tu sistema local.

### Instalación de Docker

Si no tienes Docker instalado:

**macOS:**
- Descarga Docker Desktop desde: https://www.docker.com/products/docker-desktop/

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
```

**Windows:**
- Descarga Docker Desktop desde: https://www.docker.com/products/docker-desktop/
- O instala WSL2 y Docker dentro de WSL2

## 📝 Notas

- **Variables de entorno**: Todas las configuraciones sensibles ahora usan variables de entorno. Asegúrate de configurar el archivo `.env` antes de ejecutar.
- **OpenAI API Key**: Es requerida para que el chatbot funcione. Obtén una en [OpenAI Platform](https://platform.openai.com/).
- El sistema utiliza SQLite por defecto. Para producción, se recomienda usar PostgreSQL o MySQL.
- Los tokens JWT expiran después de 24 horas (configurable mediante `JWT_EXPIRATION_DELTA`).
- **Class-based Views**: Todas las vistas del backend están implementadas como class-based views siguiendo las mejores prácticas de Django REST Framework.

## 👤 Autor

Desarrollado como prueba técnica para RECSA
