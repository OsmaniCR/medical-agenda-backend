.PHONY: help build up down logs restart shell migrate setup-first-user first-setup clean check-docker env-file

# Variables - Detecta automáticamente docker compose o docker-compose
DOCKER_COMPOSE := $(shell which docker-compose >/dev/null 2>&1 && echo docker-compose || echo "docker compose")
SERVICE := backend

# Verifica que Docker esté instalado
check-docker:
	@if ! command -v docker >/dev/null 2>&1; then \
		echo "❌ Docker no está instalado o no está en el PATH"; \
		echo "📖 Instala Docker desde: https://www.docker.com/products/docker-desktop/"; \
		exit 1; \
	fi
	@if ! docker info >/dev/null 2>&1; then \
		echo "❌ Docker no está corriendo. Por favor, inicia Docker Desktop"; \
		exit 1; \
	fi

help: ## Muestra esta ayuda
	@echo "Comandos disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Docker - Comandos principales
build: check-docker ## Construye la imagen Docker
	$(DOCKER_COMPOSE) build

run: ## Inicia el servidor ASGI
	$(DOCKER_COMPOSE) up $(SERVICE)

up: ## Inicia los contenedores Docker
	$(DOCKER_COMPOSE) up -d

down: ## Detiene los contenedores Docker
	$(DOCKER_COMPOSE) down

logs: ## Muestra los logs de los contenedores
	$(DOCKER_COMPOSE) logs -f $(SERVICE)

restart: ## Reinicia los contenedores Docker
	$(DOCKER_COMPOSE) restart $(SERVICE)

shell: ## Abre un shell en el contenedor Docker
	$(DOCKER_COMPOSE) exec $(SERVICE) bash

# Base de datos
migrate: ## Ejecuta migraciones en el contenedor Docker
	$(DOCKER_COMPOSE) exec $(SERVICE) python manage.py makemigrations
	$(DOCKER_COMPOSE) exec $(SERVICE) python manage.py migrate

migrate-reset: ## Resetea la base de datos (¡CUIDADO: elimina todos los datos!)
	@echo "⚠️  Esto eliminará todos los datos de la base de datos"
	@read -p "¿Estás seguro? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		$(DOCKER_COMPOSE) exec $(SERVICE) rm -f db.sqlite3; \
		$(DOCKER_COMPOSE) exec $(SERVICE) python manage.py migrate; \
		echo "✅ Base de datos reseteada"; \
	fi

# Usuarios
createsuperuser: ## Crea un superusuario de forma interactiva
	$(DOCKER_COMPOSE) exec $(SERVICE) python manage.py createsuperuser

setup-first-user: ## Crea el primer usuario de forma no interactiva (username: admin, password: admin123)
	@echo "🔐 Creando primer usuario..."
	@echo "   Username: admin"
	@echo "   Password: admin123"
	@echo "   Email: admin@example.com"
	@$(DOCKER_COMPOSE) exec $(SERVICE) python manage.py shell -c "from django.contrib.auth.models import User; \
		User.objects.filter(username='admin').exists() or \
		User.objects.create_superuser('admin', 'admin@example.com', 'admin123') and \
		print('✅ Usuario admin creado exitosamente') or \
		print('ℹ️  El usuario admin ya existe')"
	@echo ""
	@echo "⚠️  IMPORTANTE: Cambia la contraseña después del primer login"

# Setup inicial
env-file: ## Crea el archivo .env desde .env.example si no existe
	@if [ ! -f .env ]; then \
		if [ ! -f .env.example ]; then \
			echo "❌ Error: No se encontró el archivo .env.example"; \
			exit 1; \
		fi; \
		cp .env.example .env; \
		echo "✅ Archivo .env creado desde .env.example"; \
		echo "⚠️  IMPORTANTE: Edita el archivo .env y configura OPENAI_API_KEY y SECRET_KEY"; \
	else \
		echo "ℹ️  El archivo .env ya existe, no se modificará"; \
	fi

first-setup: check-docker env-file build up migrate setup-first-user ## Setup completo para nuevos desarrolladores
	@echo ""
	@echo "🎉 ¡Setup inicial completado!"
	@echo ""
	@echo "📋 Próximos pasos:"
	@echo "   1. Edita el archivo .env y configura:"
	@echo "      - OPENAI_API_KEY (requerido)"
	@echo "      - SECRET_KEY (recomendado cambiar)"
	@echo "   2. El servidor ya está corriendo en http://localhost:8000"
	@echo "   3. Si necesitas reiniciar, usa 'make restart'"
	@echo ""
	@echo "👤 Credenciales del primer usuario:"
	@echo "   Username: admin"
	@echo "   Password: admin123"
	@echo "   ⚠️  Cambia la contraseña después del primer login"

# Testing
test: ## Ejecuta los tests en el contenedor Docker
	$(DOCKER_COMPOSE) exec $(SERVICE) python manage.py test

# Utilidades
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
