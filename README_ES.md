# Sistema Autónomo de Apuestas Deportivas

Un sistema completo en Python para monitoreo en tiempo real de eventos deportivos, análisis predictivo y ejecución automatizada de apuestas con gestión robusta de riesgo y salvaguardas éticas.

## Estructura del Proyecto

```
sports-betting-system/
├── src/
│   ├── data_acquisition/      # Obtención en tiempo real de datos de APIs
│   ├── ml_models/             # Modelos predictivos y análisis de cuotas
│   ├── execution/             # Ejecución automatizada de apuestas
│   ├── risk_management/       # Gestión de bankroll y seguridad
│   ├── dashboard/             # Panel de control (futuro)
│   └── utils.py               # Logging y utilidades
├── database/
│   └── schema.sql             # Esquema PostgreSQL
├── tests/                     # Pruebas unitarias e integración
├── docs/                      # Documentación de arquitectura y API
├── main.py                    # Orquestador del sistema
├── config.py                  # Gestión de configuración
├── requirements.txt           # Dependencias de Python
└── README_ES.md               # Este archivo
```

## Componentes Clave

### 1. Módulo de Adquisición de Datos
- **Monitoreo en tiempo real** de eventos deportivos
- **Integración multi-origen**: APIs de Sportradar, Betfair
- **Normalización de datos** y estandarización
- **Obtención de datos históricos** y almacenamiento

### 2. Modelos de Machine Learning
- **Predicción de resultados** usando Gradient Boosting y Regresión Logística
- **Extracción de características** de forma de equipo, lesiones, clima, etc.
- **Cálculo de probabilidades** con puntuación de confianza
- **Persistencia de modelos** (guardar/cargar modelos entrenados)

### 3. Módulo de Ejecución
- **Autenticación segura** con plataformas de apuestas
- **Colocación automatizada de apuestas** con validación
- **Comparación de cuotas** en múltiples casas de apuestas
- **Detección de arbitraje** para oportunidades sin riesgo

### 4. Gestión de Riesgo
- **Criterio de Kelly** para dimensionamiento óptimo de apuestas
- **Protección de bankroll** con límites diarios/semanales
- **Detección de racha de pérdidas** (pausa después de N pérdidas consecutivas)
- **Gestión de exposición** por deporte/equipo
- **Salvaguardas de juego responsable**

### 5. Cumplimiento y Auditoría
- **Logging detallado de decisiones** para transparencia
- **Cumplimiento regulatorio** (GDPR, KYC/AML)
- **Verificaciones de geolocalización** y verificación de edad
- **Pista de auditoría** de todas las apuestas y decisiones

## Instalación

### Requisitos Previos
- Python 3.9+
- PostgreSQL 12+ (para almacenamiento de datos)
- Redis (opcional, para caché)

### Configuración

1. **Clonar e instalar dependencias:**
```bash
cd sports-betting-system
pip install -r requirements.txt
```

2. **Configurar entorno:**
```bash
cp .env.example .env
# Editar .env con tus claves API y configuración
```

3. **Configurar base de datos:**
```bash
psql -U postgres -f database/schema.sql
```

4. **Ejecutar pruebas:**
```bash
pytest tests/ -v
```

## Características Principales

### 🎯 Análisis Predictivo
- Predicción de resultados con confianza de 60%+
- Modelos de aprendizaje automático entrenables
- Ajuste dinámico según desempeño histórico
- Análisis de valor de apuestas (expected value)

### 🛡️ Gestión de Riesgo
- Criterio de Kelly para dimensionamiento óptimo
- Límites diarios de pérdida (máximo 5% del bankroll)
- Límite máximo de apuesta única (máximo 2% del bankroll)
- Detección de racha de pérdidas (pausa automática)
- Juego responsable por defecto

### 💰 Arbitraje y Multi-Apuestas
- Detección de arbitraje de 2 vías (tenis, moneda)
- Detección de arbitraje de 3 vías (fútbol, baloncesto)
- Optimización de parlays con probabilidad garantizada
- Estrategias de cobertura completa del mercado
- Cobertura y hedging de apuestas

### 📊 Monitoreo en Tiempo Real
- Seguimiento de eventos en vivo
- Actualización de cuotas en tiempo real
- Detección de oportunidades de arbitraje
- Alertas de movimientos de mercado anormales

### 🔒 Seguridad y Cumplimiento
- Autenticación segura con casas de apuestas
- Encriptación de datos sensibles
- Verificación de edad y geolocalización
- Cumplimiento GDPR y KYC/AML
- Auditoría completa de operaciones

## Modo de Ejecución

### Modo Paper Trading (por defecto)
```bash
PAPER_TRADING=True python main.py
```
- Simula apuestas sin dinero real
- Ideal para testing y validación
- Perfecto para backtesting de estrategias

### Modo Trading en Vivo
```bash
LIVE_TRADING=True python main.py
```
⚠️ **REQUIERE:**
- Validación completa de 24 horas en paper trading
- Configuración de claves API reales
- Revisión de todos los parámetros de riesgo

## Configuración de Variables de Entorno

Crear archivo `.env` con las siguientes variables:

```bash
# Base de Datos
DB_HOST=localhost
DB_PORT=5432
DB_NAME=sports_betting_db
DB_USER=betting_user
DB_PASSWORD=tu_contraseña_segura

# Claves API
SPORTRADAR_API_KEY=tu_clave_sportradar
BETFAIR_USERNAME=tu_usuario
BETFAIR_PASSWORD=tu_contraseña
BETFAIR_APP_KEY=tu_app_key

# Configuración del Sistema
ENVIRONMENT=development
PAPER_TRADING=True
LIVE_TRADING=False
LOG_LEVEL=INFO

# Umbrales de Riesgo
MAX_DAILY_LOSS_PERCENT=5.0
MAX_SINGLE_BET_PERCENT=2.0
MIN_CONFIDENCE_THRESHOLD=0.60
BANKROLL_INITIAL=1000.00

# Juego Responsable
PAUSE_AFTER_LOSS_STREAK=3
MAX_BETS_PER_DAY=20
GEOLOCATION_CHECK=True
AGE_VERIFICATION_REQUIRED=True

# Cumplimiento
REGION=EU
REGULATORY_FRAMEWORK=GDPR
AUDIT_LOGGING=True
```

## Estrategias Disponibles

### 1. Predicción de Resultados
```python
from src.ml_models.predictor import MatchPredictor

predictor = MatchPredictor(model_type="gradient_boosting")
probability = predictor.predict_probability(match_data)
```

### 2. Detección de Arbitraje
```python
from src.execution.arbitrage_engine import ArbitrageEngine

engine = ArbitrageEngine()
is_arbitrage, margin = engine.check_two_way_arbitrage(odds_a, odds_b)
```

### 3. Optimización de Parlays
```python
from src.execution.arbitrage_engine import MultiBetOptimizer

optimizer = MultiBetOptimizer()
best_combo = optimizer.find_best_combination(events, combination_size=3)
```

### 4. Estrategia de Cobertura Completa
```python
from src.execution.arbitrage_engine import CoverageStrategy

strategy = CoverageStrategy()
coverage = strategy.calculate_full_coverage(outcomes, bankroll)
```

### 5. Gestión de Bonus
```python
from src.risk_management.zero_investment import BonusManager

manager = BonusManager()
strategy = manager.calculate_bonus_strategy(bankroll)
```

## Ejemplos de Uso

### Ejemplo 1: Apuesta Simple con Validación
```python
from main import BettingSystemOrchestrator
from config import current_config

# Crear orquestador
system = BettingSystemOrchestrator(current_config)

# Autenticarse
if not system.authenticate():
    print("Error de autenticación")
    exit()

# Colocar apuesta
bet = {
    "sport": "soccer",
    "event": "Barcelona vs Real Madrid",
    "market": "win_draw_loss",
    "selection": "home",
    "odds": 1.85,
    "confidence": 0.72
}

result = system.place_bet(bet)
print(f"Apuesta colocada: {result}")
```

### Ejemplo 2: Arbitraje Automático
```python
from src.execution.arbitrage_engine import ArbitrageEngine

engine = ArbitrageEngine()

# Verificar arbitraje de 2 vías
is_arbitrage, margin = engine.check_two_way_arbitrage(1.90, 2.10)

if is_arbitrage and margin > 0.02:  # 2% mínimo
    stakes = engine.calculate_arbitrage_stakes(1000, [1.90, 2.10], 
                                              ["bookmaker_a", "bookmaker_b"],
                                              ["away", "home"])
    print(f"Oportunidad de arbitraje: {margin*100:.2f}%")
    print(f"Distribución de apuestas: {stakes}")
```

### Ejemplo 3: Optimización de Parlays
```python
from src.execution.arbitrage_engine import MultiBetOptimizer

optimizer = MultiBetOptimizer()

events = [
    {"team": "Team A", "probability": 0.65, "odds": 1.60},
    {"team": "Team B", "probability": 0.72, "odds": 1.45},
    {"team": "Team C", "probability": 0.58, "odds": 1.80},
]

best_parlay = optimizer.find_best_combination(events, combination_size=2)
print(f"Mejor parlay: {best_parlay}")
```

## API de Ejemplos

Ver archivo `ARBITRAGE_EXAMPLES.py` para 5 ejemplos ejecutables completos con:
- Apuestas deportivas simples
- Detección de arbitraje (tenis)
- Optimización de parlays
- Estrategia de cobertura completa
- Hedging y cobertura

## Despliegue

### Opción 1: Railway.app (Recomendado)
```bash
# 1. Subir código a GitHub
git push origin main

# 2. Conectar en railway.app
# Crear nuevo proyecto desde repositorio

# 3. Configurar variables
SPORTRADAR_API_KEY=...
BETFAIR_USERNAME=...
BETFAIR_PASSWORD=...
BETFAIR_APP_KEY=...

# 4. Desplegar
# Railway despliega automáticamente
```

### Opción 2: Docker Local
```bash
docker build -t sports-betting .
docker run -e PAPER_TRADING=True sports-betting
```

### Opción 3: GitHub Actions
```bash
# El workflow automático ejecuta cada 6 horas
# Ver .github/workflows/betting-bot.yml
```

## Seguridad

### Protección de Credenciales
- ✅ Nunca subir .env a GitHub
- ✅ Usar GitHub Secrets para credenciales
- ✅ Usar Railway Environment Variables
- ✅ Encriptación en tránsito (HTTPS)

### Mejores Prácticas
- Cambiar contraseñas regularmente
- Usar autenticación de dos factores en casas de apuestas
- Revisar logs de auditoría frecuentemente
- Mantener backups de configuración

## Pruebas

```bash
# Ejecutar todas las pruebas
pytest tests/ -v

# Ejecutar con cobertura
pytest tests/ --cov=src

# Ejecutar pruebas específicas
pytest tests/test_arbitrage.py -v
```

## Troubleshooting

### Error: "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Error: "API Key invalid"
- Verificar en .env que la clave es correcta
- Regenerar claves en plataforma de API

### Error: "Connection refused"
- Verificar PostgreSQL está ejecutándose
- Verificar credenciales de DB en .env

### Error: "PAPER_TRADING not defined"
```bash
export PAPER_TRADING=True
python main.py
```

## Monitoreo

Ver logs en:
- `logs/betting_system.log` - Log principal
- `logs/audit/audit.log` - Auditoría de apuestas

```bash
# Ver logs en tiempo real
tail -f logs/betting_system.log
```

## Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el repositorio
2. Crear rama para feature (`git checkout -b feature/nueva-caracteristica`)
3. Commit cambios (`git commit -am 'Add nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Crear Pull Request

## Licencia

MIT License - Ver LICENSE para detalles

## Disclaimer Legal

Este sistema está diseñado únicamente con fines educativos y de investigación. 

⚠️ **IMPORTANTE:**
- Las apuestas deportivas implican riesgo de pérdida de dinero
- No está garantizado que genere ganancias
- Antes de usar en modo LIVE_TRADING, entender completamente el sistema
- Cumplir con todas las regulaciones locales
- Apostar responsablemente

## Soporte

- 📧 Email: support@example.com
- 🐛 Issues: https://github.com/usuario/sports-betting-system/issues
- 💬 Discussions: https://github.com/usuario/sports-betting-system/discussions

## Roadmap

- [ ] Integración con más casas de apuestas (William Hill, 888)
- [ ] Dashboard web en tiempo real
- [ ] Análisis de arbitraje avanzado (Layer/Back automático)
- [ ] Predicción mejorada con Deep Learning
- [ ] Notificaciones Telegram/Email
- [ ] API REST pública
- [ ] Apps móvil (iOS/Android)

---

**Última actualización:** Enero 2026  
**Versión:** 2.0  
**Estado:** Producción
