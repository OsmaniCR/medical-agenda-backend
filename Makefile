.PHONY: help build up down logs restart shell migrate setup-first-user first-setup

# Variables
# Nota: Si tienes docker-compose (v1), cambia a "docker-compose"
# Si tienes docker compose (v2), usa "docker compose"
DOCKER_COMPOSE := docker compose
SERVICE := backend

help: ## Muestra esta ayuda
	@echo "Comandos disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Docker - Comandos principales
build: ## Construye la imagen Docker
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
	@echo "Ejecutando: docker compose exec backend rm -f /app/data/db.sqlite3"
	@echo "Ejecutando: docker compose exec backend python manage.py migrate"
	$(DOCKER_COMPOSE) exec $(SERVICE) rm -f /app/data/db.sqlite3
	$(DOCKER_COMPOSE) exec $(SERVICE) python manage.py migrate
	@echo "✅ Base de datos reseteada"

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

first-setup: build up migrate setup-first-user ## Setup completo para nuevos desarrolladores
	@echo ""
	@echo "🎉 ¡Setup inicial completado!"
	@echo ""
	@echo "📋 Próximos pasos:"
	@echo "   1. Asegúrate de tener el archivo .env configurado (ver README)"
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

