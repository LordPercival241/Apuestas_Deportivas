# Guía de Configuración en Español

## 📋 Tabla de Contenidos
1. [Variables de Entorno](#variables-de-entorno)
2. [Configuración de Base de Datos](#configuración-de-base-de-datos)
3. [Claves API](#claves-api)
4. [Parámetros de Riesgo](#parámetros-de-riesgo)
5. [Juego Responsable](#juego-responsable)
6. [Despliegue](#despliegue)

---

## Variables de Entorno

### Crear archivo `.env`

```bash
cp .env.example .env
```

### Variables Completas

#### 🗄️ Base de Datos

| Variable | Valor Ejemplo | Descripción |
|----------|---------------|-------------|
| `DB_HOST` | `localhost` | Host del servidor PostgreSQL |
| `DB_PORT` | `5432` | Puerto de PostgreSQL |
| `DB_NAME` | `sports_betting_db` | Nombre de la base de datos |
| `DB_USER` | `betting_user` | Usuario de PostgreSQL |
| `DB_PASSWORD` | `contraseña_segura` | Contraseña del usuario |

#### 🔑 Claves API

| Variable | Donde Obtener | Pasos |
|----------|---------------|-------|
| `SPORTRADAR_API_KEY` | https://developer.sportradar.com/ | 1. Registrarse<br>2. Crear aplicación<br>3. Copiar API Key |
| `BETFAIR_USERNAME` | https://developer.betfair.com/ | Tu nombre de usuario Betfair |
| `BETFAIR_PASSWORD` | https://developer.betfair.com/ | Tu contraseña Betfair |
| `BETFAIR_APP_KEY` | https://developer.betfair.com/ | Generar en cuenta settings |

#### ⚙️ Sistema

| Variable | Valor | Opciones |
|----------|-------|----------|
| `ENVIRONMENT` | `development` | `development`, `production`, `testing` |
| `DEBUG` | `False` | `True`, `False` |
| `LOG_LEVEL` | `INFO` | `DEBUG`, `INFO`, `WARNING`, `ERROR` |

#### 🎮 Modo de Ejecución

| Variable | Valor Defecto | Notas |
|----------|---------------|-------|
| `PAPER_TRADING` | `True` | Simula apuestas sin dinero real |
| `LIVE_TRADING` | `False` | ⚠️ Requiere validación de 24h |
| `MIN_ODDS` | `1.50` | Cuota mínima para apostar |
| `MAX_ODDS` | `10.0` | Cuota máxima para apostar |

---

## Configuración de Base de Datos

### PostgreSQL Local

```bash
# 1. Instalar PostgreSQL
# Windows: https://www.postgresql.org/download/windows/
# Mac: brew install postgresql
# Linux: sudo apt-get install postgresql

# 2. Crear usuario
psql -U postgres
CREATE USER betting_user WITH PASSWORD 'contraseña_segura';

# 3. Crear base de datos
CREATE DATABASE sports_betting_db OWNER betting_user;

# 4. Cargar esquema
psql -U betting_user -d sports_betting_db -f database/schema.sql

# 5. Verificar
psql -U betting_user -d sports_betting_db -c "\dt"
```

### PostgreSQL en Railway.app (Recomendado)

```bash
# 1. Ir a https://railway.app
# 2. Crear nuevo proyecto
# 3. Agregar servicio PostgreSQL
# 4. Railway proporciona automáticamente:
#    - DB_HOST
#    - DB_PORT
#    - DB_NAME
#    - DB_USER
#    - DB_PASSWORD
# 5. Copiar a Railway environment variables
```

### SQLite (Para Testing)

```bash
# Cambiar en .env
DB_URI=sqlite:///sports_betting.db

# Crear base de datos automáticamente
python -c "from src.utils import init_db; init_db()"
```

---

## Claves API

### Sportradar API

**Pasos:**
1. Ir a https://developer.sportradar.com/
2. Registrarse con email
3. Crear aplicación
4. Seleccionar "free tier" (datos retrasados 24h)
5. Copiar API Key
6. Agregar a `.env`:
```bash
SPORTRADAR_API_KEY=tu_clave_aqui
```

**Endpoints Disponibles:**
- Soccer: Resultados, predicciones, lesiones
- Tennis: Puntuaciones en vivo, estadísticas
- Basketball: Marcadores, probabilidades
- American Football: Estadísticas, predicciones

**Rate Limit:** 50 requests/minuto en free tier

### Betfair API

**Pasos:**
1. Crear cuenta en https://www.betfair.com/
2. Ir a https://developer.betfair.com/
3. Aplicar para acceso API
4. Esperar aprobación (24-48 horas)
5. Generar App Key en account settings
6. Descargar certificado SSL
7. Agregar a `.env`:
```bash
BETFAIR_USERNAME=tu_usuario
BETFAIR_PASSWORD=tu_contraseña
BETFAIR_APP_KEY=tu_app_key
```

**Características:**
- API REST y Streaming
- Odds competitivas
- Arbitraje disponible
- Acceso a market data en vivo

**Rate Limit:** 1000 requests/minuto

---

## Parámetros de Riesgo

### Kelly Criterion

```bash
# Fracción de Kelly (por defecto: 1/4 Kelly para seguridad)
# Kelly % = (bp - q) / b, donde:
# - b = cuota - 1
# - p = probabilidad de ganar
# - q = probabilidad de perder

# Ejemplo: 60% probabilidad, cuota 1.70
# Kelly = (0.70 * 0.60 - 0.40) / 0.70 = 28.6%
# 1/4 Kelly = 7.1% del bankroll
```

### Límites de Bankroll

```bash
# Bankroll inicial
BANKROLL_INITIAL=1000.00

# Pérdida máxima diaria: 5% del bankroll
MAX_DAILY_LOSS_PERCENT=5.0

# Máximo por apuesta: 2% del bankroll
MAX_SINGLE_BET_PERCENT=2.0

# Ejemplo con bankroll $1000:
# Pérdida máxima diaria: $50
# Máximo por apuesta: $20
```

### Umbrales de Confianza

```bash
# Confianza mínima para apostar: 60%
MIN_CONFIDENCE_THRESHOLD=0.60

# Solo apuesta si modelo predice ≥60% de probabilidad
```

---

## Juego Responsable

### Racha de Pérdidas

```bash
# Pausar después de N pérdidas consecutivas
PAUSE_AFTER_LOSS_STREAK=3

# Ejemplo:
# - Pierdes 1: sistema activo ✅
# - Pierdes 2: sistema activo ✅
# - Pierdes 3: SISTEMA PAUSA ❌
# - Pausa de 1 hora
# - Reinicia automáticamente
```

### Límite Diario de Apuestas

```bash
# Máximo de apuestas por día
MAX_BETS_PER_DAY=20

# Ejemplo:
# Ya apostaste 20 veces hoy → No más apuestas hasta mañana
```

### Verificación de Edad

```bash
# Requerir verificación de edad
AGE_VERIFICATION_REQUIRED=True

# Países requieren verificación (18+)
```

### Geolocalización

```bash
# Verificar ubicación permitida
GEOLOCATION_CHECK=True

# Algunos países/regiones no permiten apuestas
# El sistema verifica la ubicación automáticamente
```

---

## Despliegue

### Local (Desarrollo)

```bash
# 1. Crear virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# o
.venv\Scripts\activate     # Windows

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Crear .env
cp .env.example .env
# Editar con tus datos

# 4. Ejecutar
python main.py
```

### Railway.app (Producción)

```bash
# 1. Push a GitHub
git push origin main

# 2. En Railway Dashboard
# - New Project
# - Deploy from GitHub
# - Seleccionar repositorio

# 3. Agregar PostgreSQL
# - Add Service → PostgreSQL

# 4. Configurar Environment Variables
# SPORTRADAR_API_KEY = ...
# BETFAIR_USERNAME = ...
# BETFAIR_PASSWORD = ...
# BETFAIR_APP_KEY = ...

# 5. Desplegar
# Railway despliega automáticamente
```

### Docker

```bash
# 1. Crear imagen
docker build -t sports-betting .

# 2. Ejecutar contenedor
docker run \
  -e PAPER_TRADING=True \
  -e SPORTRADAR_API_KEY=tu_clave \
  -e BETFAIR_USERNAME=tu_usuario \
  -e BETFAIR_PASSWORD=tu_contraseña \
  -e BETFAIR_APP_KEY=tu_app_key \
  -e DB_HOST=db_host \
  -e DB_USER=betting_user \
  -e DB_PASSWORD=tu_contraseña \
  sports-betting

# 3. Con docker-compose
docker-compose up -d
```

### GitHub Actions

```bash
# El workflow automático ejecuta cada 6 horas:
# 1. Checkout código
# 2. Instalar dependencias
# 3. Configurar variables desde secrets
# 4. Ejecutar main.py
# 5. Subir logs como artifacts

# Configurar Secrets en GitHub:
# Settings → Secrets and variables → Actions
# Agregar todos los SPORTRADAR_API_KEY, etc.
```

---

## Logging

### Niveles de Log

```bash
LOG_LEVEL=DEBUG     # Información detallada (desarrollo)
LOG_LEVEL=INFO      # Información general (normal)
LOG_LEVEL=WARNING   # Solo advertencias y errores
LOG_LEVEL=ERROR     # Solo errores
```

### Ubicación de Logs

```
logs/
├── betting_system.log      # Log principal
├── audit/
│   ├── bets.log           # Todas las apuestas
│   └── decisions.log      # Decisiones del sistema
└── errors.log             # Solo errores
```

### Ver Logs

```bash
# Ver log principal
tail -f logs/betting_system.log

# Ver apuestas realizadas
tail -f logs/audit/bets.log

# Buscar errores específicos
grep "ERROR" logs/betting_system.log

# Ver últimas 100 líneas
tail -100 logs/betting_system.log
```

---

## Seguridad

### Protección de Credenciales

✅ **HACER:**
```bash
# .env en .gitignore
echo ".env" >> .gitignore

# Usar GitHub Secrets para CI/CD
# Usar Railway Environment Variables para producción
# Cambiar contraseñas cada 3 meses
```

❌ **NO HACER:**
```bash
# Nunca subir .env a GitHub
# Nunca compartir claves API
# Nunca guardar contraseñas en código
# Nunca usar contraseñas débiles
```

### Best Practices

1. **Cambiar contraseñas regularmente**
   ```bash
   # Cada 3 meses cambiar credenciales
   ```

2. **Usar autenticación de dos factores**
   ```bash
   # En todas las casas de apuestas
   # En GitHub
   # En Railway.app
   ```

3. **Monitorear logs de auditoría**
   ```bash
   tail -f logs/audit/audit.log
   ```

4. **Hacer backups**
   ```bash
   # Copiar configuración
   cp .env .env.backup.$(date +%Y%m%d)
   ```

---

## Variables de Ejemplo Completo

### .env.example

```bash
# ===== BASE DE DATOS =====
DB_HOST=localhost
DB_PORT=5432
DB_NAME=sports_betting_db
DB_USER=betting_user
DB_PASSWORD=contraseña_muy_segura_123

# ===== API KEYS =====
SPORTRADAR_API_KEY=tu_api_key_sportradar
BETFAIR_USERNAME=tu_usuario_betfair
BETFAIR_PASSWORD=tu_contraseña_betfair
BETFAIR_APP_KEY=tu_app_key_betfair

# ===== SISTEMA =====
ENVIRONMENT=development
DEBUG=False
LOG_LEVEL=INFO

# ===== TRADING =====
PAPER_TRADING=True
LIVE_TRADING=False
MIN_ODDS=1.50
MAX_ODDS=10.0

# ===== RIESGO =====
BANKROLL_INITIAL=1000.00
MAX_DAILY_LOSS_PERCENT=5.0
MAX_SINGLE_BET_PERCENT=2.0
MIN_CONFIDENCE_THRESHOLD=0.60

# ===== JUEGO RESPONSABLE =====
PAUSE_AFTER_LOSS_STREAK=3
MAX_BETS_PER_DAY=20
GEOLOCATION_CHECK=True
AGE_VERIFICATION_REQUIRED=True

# ===== CUMPLIMIENTO =====
REGION=EU
REGULATORY_FRAMEWORK=GDPR
AUDIT_LOGGING=True

# ===== OPCIONAL =====
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
EMAIL_ALERTS=False
```

---

## Troubleshooting

### Error: "No such file or directory: '.env'"
```bash
cp .env.example .env
```

### Error: "ModuleNotFoundError: No module named 'src'"
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python main.py
```

### Error: "could not connect to server"
```bash
# PostgreSQL no está ejecutándose
# Linux: sudo service postgresql start
# Mac: brew services start postgresql
# Windows: Services → PostgreSQL → Start
```

### Error: "API Key invalid"
```bash
# Verificar que la clave sea correcta en .env
# Regenerar en plataforma de API
# Esperar 5 minutos para que se propague
```

### Error: "PAPER_TRADING is not defined"
```bash
export PAPER_TRADING=True
python main.py
```

---

## Próximos Pasos

1. ✅ Configurar variables de entorno
2. ✅ Configurar base de datos
3. ✅ Obtener claves API
4. ✅ Ejecutar localmente en paper trading
5. ✅ Validar por 24 horas
6. ✅ Desplegar en producción

---

**Última actualización:** Enero 2026  
**Versión:** 1.0
