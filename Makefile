.PHONY: help install setup migrate run createsuperuser shell test clean docker-build docker-up docker-down docker-logs docker-shell setup-first-user

# Variables
PYTHON := python
MANAGE := $(PYTHON) manage.py
POETRY := poetry
DOCKER_COMPOSE := docker-compose

help: ## Muestra esta ayuda
	@echo "Comandos disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Setup inicial
install: ## Instala las dependencias con Poetry
	$(POETRY) install --no-root

setup: install env-file migrate ## Setup completo: instala dependencias, crea .env y ejecuta migraciones
	@echo "✅ Setup completado!"
	@echo "📝 Recuerda editar el archivo .env con tus configuraciones"
	@echo "👤 Ejecuta 'make setup-first-user' para crear tu primer usuario"

env-file: ## Crea el archivo .env desde .env.example si no existe
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "✅ Archivo .env creado desde .env.example"; \
		echo "⚠️  IMPORTANTE: Edita el archivo .env y configura OPENAI_API_KEY y SECRET_KEY"; \
	else \
		echo "ℹ️  El archivo .env ya existe"; \
	fi

# Base de datos
migrate: ## Ejecuta las migraciones
	$(POETRY) run $(MANAGE) makemigrations
	$(POETRY) run $(MANAGE) migrate

migrate-reset: ## Resetea la base de datos (¡CUIDADO: elimina todos los datos!)
	@echo "⚠️  Esto eliminará todos los datos de la base de datos"
	@read -p "¿Estás seguro? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		rm -f db.sqlite3; \
		$(POETRY) run $(MANAGE) migrate; \
		echo "✅ Base de datos reseteada"; \
	fi

# Desarrollo
run: ## Ejecuta el servidor ASGI con Uvicorn
	$(POETRY) run uvicorn core.asgi:application --host 0.0.0.0 --port 8000 --reload

shell: ## Abre el shell de Django
	$(POETRY) run $(MANAGE) shell_plus

# Usuarios
createsuperuser: ## Crea un superusuario de forma interactiva
	$(POETRY) run $(MANAGE) createsuperuser

setup-first-user: ## Crea el primer usuario de forma no interactiva (username: admin, password: admin123)
	@echo "🔐 Creando primer usuario..."
	@echo "   Username: admin"
	@echo "   Password: admin123"
	@echo "   Email: admin@example.com"
	@$(POETRY) run $(MANAGE) shell -c "from django.contrib.auth.models import User; \
		User.objects.filter(username='admin').exists() or \
		User.objects.create_superuser('admin', 'admin@example.com', 'admin123') and \
		print('✅ Usuario admin creado exitosamente') or \
		print('ℹ️  El usuario admin ya existe')"
	@echo ""
	@echo "⚠️  IMPORTANTE: Cambia la contraseña después del primer login"

create-user: ## Crea un usuario normal (interactivo)
	@read -p "Username: " username; \
	read -p "Email: " email; \
	read -sp "Password: " password; \
	echo; \
	$(POETRY) run $(MANAGE) shell -c "from django.contrib.auth.models import User; \
		User.objects.create_user('$$username', '$$email', '$$password') and \
		print('✅ Usuario creado exitosamente')"

# Testing
test: ## Ejecuta los tests
	$(POETRY) run $(MANAGE) test

test-coverage: ## Ejecuta los tests con cobertura
	$(POETRY) run coverage run --source='.' $(MANAGE) test
	$(POETRY) run coverage report
	$(POETRY) run coverage html

# Docker
docker-build: ## Construye la imagen Docker
	$(DOCKER_COMPOSE) build

docker-up: ## Inicia los contenedores Docker
	$(DOCKER_COMPOSE) up -d

docker-down: ## Detiene los contenedores Docker
	$(DOCKER_COMPOSE) down

docker-logs: ## Muestra los logs de los contenedores
	$(DOCKER_COMPOSE) logs -f

docker-restart: ## Reinicia los contenedores Docker
	$(DOCKER_COMPOSE) restart

docker-shell: ## Abre un shell en el contenedor Docker
	$(DOCKER_COMPOSE) exec backend bash

docker-migrate: ## Ejecuta migraciones en el contenedor Docker
	$(DOCKER_COMPOSE) exec backend python manage.py makemigrations
	$(DOCKER_COMPOSE) exec backend python manage.py migrate

docker-createsuperuser: ## Crea un superusuario en el contenedor Docker
	$(DOCKER_COMPOSE) exec backend python manage.py createsuperuser

# Utilidades
collectstatic: ## Recolecta archivos estáticos
	$(POETRY) run $(MANAGE) collectstatic --noinput

lint: ## Ejecuta el linter (flake8, black, etc.)
	@echo "Ejecutando linters..."
	@$(POETRY) run flake8 . || echo "⚠️  flake8 no está instalado"
	@$(POETRY) run black --check . || echo "⚠️  black no está instalado"

format: ## Formatea el código con black
	@$(POETRY) run black . || echo "⚠️  black no está instalado"

clean: ## Limpia archivos temporales y cache
	find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} + 2>/dev/null || true
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	@echo "✅ Archivos temporales eliminados"

clean-db: ## Elimina la base de datos (¡CUIDADO!)
	@echo "⚠️  Esto eliminará la base de datos"
	@read -p "¿Estás seguro? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		rm -f db.sqlite3; \
		echo "✅ Base de datos eliminada"; \
	fi

# Comando completo para setup inicial después de clonar
first-setup: install env-file migrate setup-first-user ## Setup completo para nuevos desarrolladores
	@echo ""
	@echo "🎉 ¡Setup inicial completado!"
	@echo ""
	@echo "📋 Próximos pasos:"
	@echo "   1. Edita el archivo .env y configura:"
	@echo "      - OPENAI_API_KEY (requerido)"
	@echo "      - SECRET_KEY (recomendado cambiar)"
	@echo "   2. Ejecuta 'make run' para iniciar el servidor"
	@echo "   3. Accede a http://localhost:8000"
	@echo ""
	@echo "👤 Credenciales del primer usuario:"
	@echo "   Username: admin"
	@echo "   Password: admin123"
	@echo "   ⚠️  Cambia la contraseña después del primer login"

