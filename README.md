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

- Python 3.12+
- Poetry (para gestión de dependencias de Python)
- Bun (para gestión de dependencias de Node.js)
- Make (opcional, pero recomendado para facilitar el desarrollo)
- Base de datos SQLite (incluida por defecto)

### Instalación de Poetry

Si no tienes Poetry instalado, puedes instalarlo de las siguientes maneras:

#### Instalación Automática (Recomendado)

El comando `make first-setup` intentará instalar Poetry automáticamente si no está instalado.

#### Instalación Manual

**Todos los sistemas:**
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

**macOS (con Homebrew):**
```bash
brew install poetry
```

**Windows (con pip):**
```bash
pip install poetry
```

**Linux (con pip):**
```bash
pip install --user poetry
```

Después de instalar, asegúrate de agregar Poetry al PATH:
```bash
# Linux/macOS
export PATH="$HOME/.local/bin:$PATH"

# O añádelo permanentemente a tu ~/.bashrc o ~/.zshrc
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
```

**Verificar instalación:**
```bash
poetry --version
```

Para más información, visita: https://python-poetry.org/docs/#installation

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

```bash
cd medical-agenda-backend
make first-setup
```

Este comando automáticamente:

- Instala las dependencias
- Crea el archivo `.env` desde `.env.example`
- Ejecuta las migraciones
- Crea el primer usuario (username: `admin`, password: `admin123`)

**Edita el archivo `.env`** y configura las variables necesarias:

```bash
# Requerido
OPENAI_API_KEY=tu-api-key-de-openai
SECRET_KEY=tu-secret-key-seguro
```

**Inicia el servidor:**

```bash
make run
```

El backend estará disponible en `http://localhost:8000`

**Otros comandos útiles del Makefile:**

```bash
make help              # Muestra todos los comandos disponibles
make setup             # Setup básico (sin crear usuario)
make migrate           # Ejecuta migraciones
make createsuperuser   # Crea un superusuario interactivo
make setup-first-user  # Crea el primer usuario (admin/admin123)
make shell             # Abre el shell de Django
make test              # Ejecuta los tests
make clean             # Limpia archivos temporales
```

#### Opción 1b: Ejecución Local (Manual)

Si prefieres ejecutar los comandos manualmente:

1. Navega al directorio del backend:

```bash
cd medical-agenda-backend
```

2. Copia el archivo de ejemplo de variables de entorno:

```bash
cp .env.example .env
```

3. Edita el archivo `.env` y configura las variables necesarias

4. Instala las dependencias con Poetry:

```bash
poetry install
```

5. Activa el entorno virtual:

```bash
poetry shell
```

6. Ejecuta las migraciones:

```bash
python manage.py makemigrations
python manage.py migrate
```

7. Crea un superusuario:

```bash
python manage.py createsuperuser
```

8. Inicia el servidor de desarrollo:

```bash
python manage.py runserver
# o
uvicorn core.asgi:application --host 0.0.0.0 --port 8000 --reload
```

#### Opción 2: Ejecución con Docker

1. Navega al directorio del backend:

```bash
cd medical-agenda-backend
```

2. Copia el archivo de ejemplo de variables de entorno:

```bash
cp .env.example .env
```

3. Edita el archivo `.env` y configura las variables necesarias

4. Construye y ejecuta el contenedor:

```bash
# Usando Makefile
make docker-build
make docker-up

# O directamente con docker-compose
docker-compose up --build
```

El backend estará disponible en `http://localhost:8000`

**Comandos Docker útiles:**

```bash
make docker-build          # Construye la imagen
make docker-up            # Inicia los contenedores
make docker-down          # Detiene los contenedores
make docker-logs          # Muestra los logs
make docker-restart       # Reinicia los contenedores
make docker-shell         # Abre un shell en el contenedor
make docker-migrate       # Ejecuta migraciones en Docker
make docker-createsuperuser  # Crea superusuario en Docker
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

El backend incluye un Makefile con comandos útiles para facilitar el desarrollo.

### Setup Inicial (Después de Clonar)

```bash
cd medical-agenda-backend
make first-setup
```

Este comando hace todo automáticamente:

- ✅ Instala dependencias
- ✅ Crea archivo `.env`
- ✅ Ejecuta migraciones
- ✅ Crea primer usuario (admin/admin123)

### Comandos Principales

```bash
make help              # Muestra todos los comandos disponibles
make first-setup       # Setup completo para nuevos desarrolladores
make install           # Instala dependencias
make setup             # Setup básico (sin crear usuario)
make run               # Inicia servidor ASGI (uvicorn)
make migrate           # Ejecuta migraciones
make createsuperuser   # Crea superusuario (interactivo)
make setup-first-user  # Crea primer usuario (admin/admin123)
make shell             # Abre shell de Django
make test              # Ejecuta tests
make clean             # Limpia archivos temporales
```

### Comandos Docker

```bash
make docker-build      # Construye imagen Docker
make docker-up        # Inicia contenedores
make docker-down      # Detiene contenedores
make docker-logs      # Muestra logs
make docker-restart   # Reinicia contenedores
make docker-shell     # Abre shell en contenedor
make docker-migrate   # Ejecuta migraciones en Docker
```

## 🐳 Docker

El backend puede ejecutarse usando Docker. Para más información, consulta la sección de instalación del backend.

### Comandos Docker útiles

```bash
# Construir y ejecutar
docker-compose up --build

# Ejecutar en segundo plano
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener
docker-compose down
```

O usa los comandos del Makefile (ver sección anterior).

## 📝 Notas

- **Variables de entorno**: Todas las configuraciones sensibles ahora usan variables de entorno. Asegúrate de configurar el archivo `.env` antes de ejecutar.
- **OpenAI API Key**: Es requerida para que el chatbot funcione. Obtén una en [OpenAI Platform](https://platform.openai.com/).
- El sistema utiliza SQLite por defecto. Para producción, se recomienda usar PostgreSQL o MySQL.
- Los tokens JWT expiran después de 24 horas (configurable mediante `JWT_EXPIRATION_DELTA`).
- **Class-based Views**: Todas las vistas del backend están implementadas como class-based views siguiendo las mejores prácticas de Django REST Framework.

## 👤 Autor

Desarrollado como prueba técnica para RECSA
