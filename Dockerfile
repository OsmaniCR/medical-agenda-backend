FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Copy poetry files
COPY pyproject.toml poetry.lock ./

# Configure poetry to not create virtual environment
RUN poetry config virtualenvs.create false

# Install dependencies
# --no-root evita que Poetry intente instalar el proyecto actual como paquete
# (los archivos del proyecto se copian después)
RUN poetry install --no-root

# Copy project files
COPY . .

# Collect static files (if needed)
# RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run migrations and start ASGI server
CMD ["sh", "-c", "python manage.py migrate && uvicorn core.asgi:application --host 0.0.0.0 --port 8000"]

