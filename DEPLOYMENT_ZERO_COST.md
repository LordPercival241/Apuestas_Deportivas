# Despliegue Gratuito - Zero Cost Deployment Guide

## 🚀 Opciones de Hosting GRATUITO

### 1. **Railway.app** ⭐ (RECOMENDADO)
- **Costo**: Gratuito ($5/mes crédito incluido)
- **Ideal para**: Bots 24/7
- **Specs**: 0.5GB RAM, suficiente para nuestro sistema

```bash
# 1. Registrarse en railway.app
# 2. Conectar GitHub
# 3. Crear nuevo proyecto
# 4. Seleccionar este repositorio
# 5. Listo - se deploya automáticamente
```

### 2. **Heroku** (Alternativa)
- **Costo**: Gratuito (limitado)
- **Nota**: Reducción de dynos gratuitos pero aún disponible

```bash
heroku create mi-arbitrage-bot
git push heroku main
```

### 3. **GitHub Actions** (Para bots)
- **Costo**: 100% GRATUITO
- **Ideal**: Ejecutar bots programados
- **Límite**: 2000 minutos/mes

### 4. **PythonAnywhere**
- **Costo**: Versión gratuita disponible
- **Ideal**: Scripts que corren periódicamente

---

## 📝 OPCIÓN 1: Railway.app (Paso a Paso)

### Paso 1: Crear Archivo `railway.toml`
```toml
[build]
builder = "dockerfile"

[deploy]
startCommand = "python main.py"
```

### Paso 2: Crear `Dockerfile`
```dockerfile
FROM python:3.13

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Variables de entorno (serán configuradas en Railway)
ENV ENVIRONMENT=production
ENV PAPER_TRADING=False
ENV LIVE_TRADING=False

CMD ["python", "main.py"]
```

### Paso 3: Archivo `.env` (Variables Seguras)
```env
# API Keys (configurar en Railway dashboard)
SPORTRADAR_API_KEY=your_key_here
BETFAIR_USERNAME=your_username
BETFAIR_PASSWORD=your_password
BETFAIR_APP_KEY=your_app_key

# Base de datos (usar PostgreSQL gratuito)
DB_HOST=db.railway.internal
DB_PORT=5432
DB_NAME=sports_betting_db
DB_USER=postgres
DB_PASSWORD=auto-generated-by-railway

# Sistema
ENVIRONMENT=production
PAPER_TRADING=True
LIVE_TRADING=False
LOG_LEVEL=INFO
```

### Paso 4: Despliegue en Railway
```bash
# 1. Instalar CLI de Railway
npm install -g @railway/cli

# 2. Login
railway login

# 3. Crear proyecto
railway init

# 4. Desplegar
railway up
```

---

## 📝 OPCIÓN 2: GitHub Actions (Completamente Gratis)

### Crear `.github/workflows/betting-bot.yml`

```yaml
name: Betting Bot 24/7

on:
  schedule:
    # Ejecutar cada hora
    - cron: '0 * * * *'
  push:
    branches: [main]

jobs:
  run-bot:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.13'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run betting bot
      env:
        SPORTRADAR_API_KEY: ${{ secrets.SPORTRADAR_API_KEY }}
        BETFAIR_USERNAME: ${{ secrets.BETFAIR_USERNAME }}
        BETFAIR_PASSWORD: ${{ secrets.BETFAIR_PASSWORD }}
        BETFAIR_APP_KEY: ${{ secrets.BETFAIR_APP_KEY }}
        DB_HOST: ${{ secrets.DB_HOST }}
        DB_USER: ${{ secrets.DB_USER }}
        DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
      run: python main.py
    
    - name: Log results
      if: always()
      run: |
        echo "Bot execution completed"
        # Enviar notificación de resultados
```

### Agregar Secrets en GitHub
```bash
# En GitHub > Settings > Secrets and variables > Actions

# Agregar:
- SPORTRADAR_API_KEY
- BETFAIR_USERNAME
- BETFAIR_PASSWORD
- BETFAIR_APP_KEY
- DB_HOST
- DB_USER
- DB_PASSWORD
```

---

## 🗄️ Base de Datos Gratuita

### Opción 1: PostgreSQL Gratuito (Railway)
```bash
# En Railway dashboard:
# 1. Agregar servicio PostgreSQL
# 2. Automáticamente conectado a tu app
# Costo: $0
```

### Opción 2: MongoDB Atlas (Gratuito)
```bash
# 1. Registrarse en mongodb.com
# 2. Crear cluster gratuito
# 3. Obtener connection string
# Costo: $0 (hasta 5GB)
```

### Opción 3: SQLite (Local, más simple)
```python
# No necesita base de datos externa
# Almacena en archivo local
# Perfecto para desarrollo

SQLALCHEMY_DATABASE_URI = "sqlite:///sports_betting.db"
```

---

## 🔐 Manejar Credenciales Seguramente

### NUNCA guardes credenciales en GitHub

### Opción 1: Variables de Entorno en Railway
```bash
railway link          # Conectar a proyecto
railway env add SPORTRADAR_API_KEY xxxxx
railway env add BETFAIR_USERNAME xxxxx
```

### Opción 2: GitHub Secrets
```bash
# En GitHub > Settings > Secrets

# Agregar cada credencial como secret
# Luego referenciar como: ${{ secrets.NOMBRE }}
```

### Opción 3: Archivo `.env.local` (No subir a Git)
```bash
# .gitignore debe incluir:
.env
.env.local
*.key
credentials.json

# Crear .env localmente con tus credenciales
SPORTRADAR_API_KEY=tu_key
BETFAIR_USERNAME=tu_usuario
```

---

## 🎯 Configurar Credenciales de Apuestas

### Paso 1: Obtener API Keys

**Sportradar:**
```bash
# 1. Ir a: https://developer.sportradar.com/
# 2. Registrarse (gratis)
# 3. Crear aplicación
# 4. Copiar API Key
```

**Betfair:**
```bash
# 1. Ir a: https://developer.betfair.com/
# 2. Registrarse en cuenta
# 3. Generar App Key
# 4. Obtener certificado SSL
```

### Paso 2: Configurar en el Sistema

**Opción A: Railway**
```bash
railway env add SPORTRADAR_API_KEY "tu-key-aqui"
railway env add BETFAIR_USERNAME "tu-usuario"
railway env add BETFAIR_PASSWORD "tu-contraseña"
railway env add BETFAIR_APP_KEY "tu-app-key"
```

**Opción B: GitHub Actions**
```bash
# En GitHub Settings > Secrets > New repository secret
SPORTRADAR_API_KEY = tu-key-aqui
BETFAIR_USERNAME = tu-usuario
BETFAIR_PASSWORD = tu-contraseña
BETFAIR_APP_KEY = tu-app-key
```

**Opción C: Archivo .env Local**
```bash
# Crear archivo .env en raíz del proyecto
cat > .env << EOF
SPORTRADAR_API_KEY=tu-key-aqui
BETFAIR_USERNAME=tu-usuario
BETFAIR_PASSWORD=tu-contraseña
BETFAIR_APP_KEY=tu-app-key
DB_HOST=localhost
DB_PORT=5432
PAPER_TRADING=False
LIVE_TRADING=False
EOF

# Agregar a .gitignore (IMPORTANTE!)
echo ".env" >> .gitignore
```

---

## 📦 Setup Local (Testing)

```bash
# 1. Clonar proyecto
git clone https://github.com/tu-usuario/sports-betting-system.git
cd sports-betting-system

# 2. Crear virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# o
.venv\Scripts\activate     # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Crear .env local
cp .env.example .env
# Editar .env con tus credenciales

# 5. Ejecutar en papel trading
PAPER_TRADING=True python main.py

# 6. Ejecutar tests
pytest tests/ -v
```

---

## 🌍 Desplegar a Railway (Paso Completo)

### Paso 1: Preparar Proyecto
```bash
# Asegurarse que todo está en Git
git add .
git commit -m "Ready for deployment"
git push origin main
```

### Paso 2: Crear en Railway
```bash
# 1. Ir a railway.app
# 2. Click "New Project"
# 3. Seleccionar "Deploy from GitHub"
# 4. Conectar repositorio
# 5. Autorizar Railway en GitHub
```

### Paso 3: Configurar Variables
```bash
# En Railway Dashboard > Variables

# Agregar todas las variables de .env
SPORTRADAR_API_KEY = xxx
BETFAIR_USERNAME = xxx
BETFAIR_PASSWORD = xxx
BETFAIR_APP_KEY = xxx
ENVIRONMENT = production
PAPER_TRADING = False
LIVE_TRADING = False
```

### Paso 4: Agregar PostgreSQL (Opcional)
```bash
# En Railway Dashboard
# 1. Click "New Service"
# 2. Seleccionar PostgreSQL
# 3. Conectar automáticamente
# Las variables se agregan automáticamente
```

### Paso 5: Desplegar
```bash
# Railway despliega automáticamente cuando haces push a main
# O en Dashboard > Triggers > Deploy
```

---

## 🤖 Configurar Bot Automático (24/7)

### Opción 1: Railway Cron Jobs
```bash
# En railway.toml
[build]
builder = "dockerfile"

[deploy]
startCommand = "python scheduler.py"
```

### Crear `scheduler.py`
```python
"""
Scheduler para ejecutar bot automáticamente
"""
import schedule
import time
from main import BettingSystemOrchestrator
from config import current_config

def run_bot():
    """Ejecutar el sistema de apuestas"""
    system = BettingSystemOrchestrator(current_config)
    system.authenticate()
    # Procesar eventos...
    print(f"Bot run completed at {time.time()}")

# Programar ejecuciones
schedule.every(1).hour.do(run_bot)      # Cada hora
# schedule.every(30).minutes.do(run_bot)  # Cada 30 minutos

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(60)
```

### Opción 2: GitHub Actions Scheduler
```yaml
# .github/workflows/betting-bot.yml
on:
  schedule:
    - cron: '0 */4 * * *'  # Cada 4 horas
    - cron: '0 0 * * *'    # Diariamente a medianoche
```

---

## 💰 Costos Totales

| Servicio | Costo |
|----------|-------|
| Railway App | $0 ($5 crédito gratis) |
| PostgreSQL | Incluido en Railway |
| GitHub Actions | $0 |
| Domain | $0 (opcional) |
| SSL/TLS | Incluido |
| **TOTAL** | **$0** |

---

## 🔍 Monitoreo y Logs

### Ver logs en Railway
```bash
railway logs
# o en Dashboard > Logs
```

### Ver logs locales
```bash
# Verificar archivo de logs
tail -f logs/system.log
```

### Enviar notificaciones (Gratis)
```python
# Notificar resultados por Telegram
import requests

def notify_telegram(message):
    token = "TU_TOKEN_BOT"
    chat_id = "TU_CHAT_ID"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": message})
```

---

## ✅ Checklist de Despliegue

- [ ] Código en GitHub
- [ ] .env.example sin credenciales reales
- [ ] .gitignore incluye .env
- [ ] Dockerfile listo
- [ ] requirements.txt actualizado
- [ ] Tests pasando (`pytest tests/ -v`)
- [ ] Credenciales de API obtenidas
- [ ] Railway account creada
- [ ] Variables de entorno configuradas
- [ ] Base de datos configurada
- [ ] Bot programado/scheduler listo
- [ ] Logs configurados
- [ ] Primeras ejecuciones testeadas

---

## 🚨 Troubleshooting

### Error: "ModuleNotFoundError"
```bash
# Solución: requirements.txt incompleto
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push
# Railway redeploya automáticamente
```

### Error: "API Key inválida"
```bash
# Verificar que la clave está bien configurada
railway env list
# Si falta, agregarla:
railway env add SPORTRADAR_API_KEY "tu-key"
```

### Bot no se ejecuta
```bash
# Verificar logs
railway logs

# Si hay errores, revisar main.py
# Asegurar que PAPER_TRADING=True para testing
```

---

## 📚 Recursos Gratuitos

- **Railway Docs**: https://docs.railway.app/
- **GitHub Actions**: https://github.com/features/actions
- **PostgreSQL Free**: https://www.postgresql.org/
- **Python Docs**: https://docs.python.org/3/
- **Betfair API Docs**: https://developer.betfair.com/
- **Sportradar Docs**: https://developer.sportradar.com/

---

## 🎯 Resumen

Para desplegar **gratis**:

1. **Usar Railway** ($0 con crédito gratuito)
2. **Guardar credenciales en Secrets** (Railway o GitHub)
3. **Usar PostgreSQL gratuito** (Incluido en Railway)
4. **Programar con GitHub Actions** (Completamente gratis)
5. **Monitorear con logs** (Incluido)

**Costo total: $0**

¡Listo para conectar tu bot a las casas de apuestas sin gastar en infraestructura!
