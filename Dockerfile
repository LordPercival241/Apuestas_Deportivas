FROM python:3.13-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Crear directorios necesarios
RUN mkdir -p logs/audit

# Exponer puerto (si es necesario)
EXPOSE 5000

# Variables de entorno por defecto
ENV ENVIRONMENT=production
ENV PAPER_TRADING=True
ENV LIVE_TRADING=False
ENV LOG_LEVEL=INFO

# Comando para ejecutar
CMD ["python", "main.py"]
