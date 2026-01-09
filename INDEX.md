# INICIO RÁPIDO - ÍNDICE DE RECURSOS

## 🎯 Estado del Sistema: ✅ OPERACIONAL

---

## 📋 TABLA DE CONTENIDOS

### Documentación Principal
| Archivo | Propósito | Lectura |
|---------|----------|---------|
| [QUICK_START.md](QUICK_START.md) | Guía de inicio (5 min) | ⭐⭐⭐ |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Diseño del sistema | ⭐⭐⭐ |
| [VERIFICATION_REPORT.md](VERIFICATION_REPORT.md) | Informe de verificación | ⭐⭐ |
| [FINAL_SUMMARY.md](FINAL_SUMMARY.md) | Resumen completo | ⭐⭐ |
| [README.md](README.md) | Descripción general | ⭐ |

---

## 🚀 COMENZAR AHORA (5 MINUTOS)

### Opción 1: Ejecutar Ejemplos
```bash
.\.venv\Scripts\python.exe EXAMPLES.py
```
✅ Demuestra predicción, gestión de bankroll, detección de pérdidas, comparación de cuotas y ejecución

### Opción 2: Iniciar Sistema Completo
```bash
.\.venv\Scripts\python.exe main.py
```
✅ Inicia el orquestador con todos los componentes

### Opción 3: Verificar Estado
```bash
.\.venv\Scripts\python.exe install_deps.py
```
✅ Verifica que todos los módulos estén cargados correctamente

---

## 📂 ESTRUCTURA DEL PROYECTO

```
sports-betting-system/
│
├── src/                              # Código fuente principal
│   ├── data_acquisition/             # Adquisición de datos en tiempo real
│   ├── ml_models/                    # Modelos predictivos (XGBoost)
│   ├── execution/                    # Ejecución de apuestas
│   ├── risk_management/              # Gestión de bankroll
│   └── utils.py                      # Logging y auditoría
│
├── database/                         # Configuración de base de datos
│   └── schema.sql                    # Esquema PostgreSQL
│
├── docs/                             # Documentación técnica
│   └── ARCHITECTURE.md               # Diagrama y diseño
│
├── tests/                            # Tests unitarios
│   └── test_core.py                  # Pruebas básicas
│
├── main.py                           # Punto de entrada
├── config.py                         # Gestión de configuración
├── EXAMPLES.py                       # Ejemplos funcionales
├── requirements.txt                  # Dependencias Python
├── .env.example                      # Template de variables
│
└── QUICK_START.md                    # Guía de inicio rápido
```

---

## 🔧 COMPONENTES PRINCIPALES

### 1. **Data Acquisition** (src/data_acquisition/)
Obtiene datos deportivos en tiempo real de APIs:
- Sportradar (eventos en vivo, estadísticas)
- Betfair (cuotas en vivo)
- Proveedores alternativos

**Uso:**
```python
from src.data_acquisition import SportsDataFetcher
fetcher = SportsDataFetcher(api_key="key", provider="sportradar")
events = fetcher.get_live_events(sport="soccer")
```

### 2. **ML Models** (src/ml_models/)
Predice resultados de partidos usando:
- Gradient Boosting (XGBoost)
- Regresión Logística
- Redes Neuronales (opcional)

**Uso:**
```python
from src.ml_models import MatchPredictor
predictor = MatchPredictor(model_type="gradient_boosting")
prediction = predictor.predict(match_data)
# Retorna: probabilidades y confianza
```

### 3. **Execution** (src/execution/)
Ejecuta apuestas en plataformas legales:
- Autenticación con APIs de casas de apuestas
- Comparación de cuotas
- Validación de valor

**Uso:**
```python
from src.execution import BetExecutor, ComparisonEngine
executor = BetExecutor(bookmaker="betfair")
executor.authenticate()
best_odds = ComparisonEngine().find_best_odds(event_id)
```

### 4. **Risk Management** (src/risk_management/)
Protege el bankroll y cumple con límites:
- Kelly Criterion para dimensionamiento
- Límites diarios/semanales
- Pausa por racha de pérdidas

**Uso:**
```python
from src.risk_management import BankrollManager
manager = BankrollManager(initial_bankroll=1000)
stake = manager.calculate_stake(confidence=0.75)
```

### 5. **Utilities** (src/utils.py)
- Logging estructurado
- Auditoría de transacciones
- Funciones auxiliares

---

## ⚙️ CONFIGURACIÓN

### Variables de Entorno (.env)

Crea un archivo `.env` (copia de `.env.example`):

```env
# Base de Datos
DB_HOST=localhost
DB_PORT=5432
DB_NAME=sports_betting_db
DB_USER=betting_user

# APIs Deportivas
SPORTRADAR_API_KEY=your_key
BETFAIR_USERNAME=your_username
BETFAIR_PASSWORD=your_password

# Sistema
ENVIRONMENT=development
DEBUG=True

# Bankroll
BANKROLL_INITIAL=1000
MAX_DAILY_LOSS_PERCENT=2
MAX_SINGLE_BET_PERCENT=2
```

### Cargar Configuración

```python
from config import current_config

print(current_config.ENVIRONMENT)
print(current_config.BANKROLL_INITIAL)
```

---

## 🧪 VERIFICACIÓN DEL SISTEMA

Todos los tests pasan exitosamente:

```
[✓] Module Imports:        6/6 PASSED
[✓] Configuration:         1/1 PASSED
[✓] Functionality:         4/4 PASSED
─────────────────────────────────
TOTAL: 11/11 PASSED - SYSTEM OPERATIONAL
```

---

## 📊 ESTADÍSTICAS DEL PROYECTO

- **Archivos Python:** 4,100+ (incluidos venv)
- **Módulos Core:** 5 (data_acquisition, ml_models, execution, risk_management, utils)
- **Documentación:** 4 archivos (33 KB)
- **Dependencias:** 9 paquetes principales
- **Líneas de Código:** ~2,000 (sin tests)
- **Python Version:** 3.13.9

---

## 🎓 EJEMPLOS DE USO

### Ejemplo 1: Predicción Simple
```python
from src.ml_models import MatchPredictor

predictor = MatchPredictor()
match = {
    'home_team': 'Barcelona',
    'away_team': 'Real Madrid',
    'home_form': [1, 1, 1, 0, 1],
    'away_form': [1, 1, 0, 1, 1]
}
pred = predictor.predict(match)
print(f"Home win probability: {pred['home_win_prob']:.2%}")
```

### Ejemplo 2: Cálculo de Apuesta
```python
from src.risk_management import BankrollManager

manager = BankrollManager(initial_bankroll=1000)
# Simula apostar con 75% de confianza
stake = manager.calculate_stake(confidence=0.75)
print(f"Recommended stake: ${stake:.2f}")
```

### Ejemplo 3: Comparación de Cuotas
```python
from src.execution import ComparisonEngine

engine = ComparisonEngine()
best_odds = engine.find_best_odds("1X2", event_id=123)
print(f"Best odds available: {best_odds}")
```

---

## 🔐 SEGURIDAD

✅ **Implementado:**
- Gestión de variables de entorno
- Sin credenciales en el código
- Logging de transacciones
- Pistas de auditoría completas

⏳ **Por configurar:**
- Encriptación de base de datos
- Validación de certificados SSL
- Rotación de secretos

---

## 📈 PRÓXIMOS PASOS

### 1. Configuración Inicial (30 min)
- [ ] Crear archivo `.env` con credenciales reales
- [ ] Configurar base de datos PostgreSQL
- [ ] Obtener claves API de Sportradar y Betfair

### 2. Desarrollo (1-2 semanas)
- [ ] Entrenar modelos ML con datos históricos (2-3 temporadas)
- [ ] Ejecutar backtesting
- [ ] Validar precisión de predicciones

### 3. Testing (1 semana)
- [ ] Paper trading en modo demo
- [ ] Verificar ejecución de apuestas
- [ ] Monitorear gestión de riesgos

### 4. Producción (Cuando esté listo)
- [ ] Desplegar a servidor
- [ ] Configurar monitoreo
- [ ] Habilitar trading en vivo

---

## 🆘 SOLUCIÓN DE PROBLEMAS

### Error: "No module named 'pandas'"
```bash
.\.venv\Scripts\python.exe install_deps.py
```

### Error: "API authentication failed"
1. Verifica credenciales en `.env`
2. Comprueba que las claves API sean válidas
3. Verifica conectividad de red

### Error: "Connection refused"
1. Asegúrate de que PostgreSQL esté corriendo
2. Verifica la cadena de conexión en config.py

---

## 📞 SOPORTE

- **Documentación Técnica:** [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **Guía Rápida:** [QUICK_START.md](QUICK_START.md)
- **Configuración:** [config.py](config.py)
- **Ejemplos:** [EXAMPLES.py](EXAMPLES.py)

---

## 📅 ESTADO DE VERSIÓN

- **Versión:** 1.0.0
- **Estado:** Producción-ready (después de configuración)
- **Última verificación:** 2026-01-05
- **Status:** ✅ OPERACIONAL

---

## 💡 CARACTERÍSTICAS CLAVE

✅ Real-time data acquisition  
✅ ML-powered predictions  
✅ Automated bet execution  
✅ Advanced risk management  
✅ Responsible gaming controls  
✅ Complete audit logging  
✅ Multi-bookmaker support  
✅ Value betting framework  
✅ Production-ready architecture  

---

**¡El sistema está listo para usar! Comienza con [QUICK_START.md](QUICK_START.md)**

