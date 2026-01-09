# Guía de Despliegue en Español - Costo 0

## 📋 Índice Rápido
- [Opción 1: Railway.app (Recomendado)](#opción-1-railwayapp-recomendado)
- [Opción 2: GitHub Actions](#opción-2-github-actions)
- [Opción 3: Heroku](#opción-3-heroku)
- [Opción 4: PythonAnywhere](#opción-4-pythonanywhere)
- [Troubleshooting](#troubleshooting)

---

## Opción 1: Railway.app (Recomendado) ⭐

Railway.app es la opción **más fácil** y tiene **$5 de crédito gratuito** (suficiente para 1-2 meses).

### Paso 1: Preparar GitHub

```bash
# 1. Ir a https://github.com y crear repositorio
# Nombre: sports-betting-system
# Visibilidad: Public o Private

# 2. En tu terminal local
git init
git add .
git commit -m "Initial commit: Sports betting system"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/sports-betting-system.git
git push -u origin main

# 3. Verificar en GitHub que todo subió
# Ir a https://github.com/TU_USUARIO/sports-betting-system
```

### Paso 2: Crear Cuenta Railway

```bash
# 1. Ir a https://railway.app
# 2. Click "Start Free"
# 3. Login con GitHub
# 4. Autorizar Railway a acceder a repositorios
# 5. ¡Listo! Tienes $5 de crédito gratuito
```

### Paso 3: Desplegar en Railway

**En Railway Dashboard:**

```bash
1. Click "New Project"
2. Click "Deploy from GitHub repo"
3. Seleccionar: TU_USUARIO / sports-betting-system
4. Click "Deploy"

Railway automáticamente:
  ✅ Lee el Dockerfile
  ✅ Construye la imagen
  ✅ Despliega la aplicación
  ✅ Expone en URL pública
```

### Paso 4: Configurar Base de Datos

**En Railway Dashboard:**

```bash
1. En tu proyecto
2. Click "+ Add Service"
3. Seleccionar "PostgreSQL"
4. Click "Create"

Railway automáticamente:
  ✅ Crea base de datos
  ✅ Proporciona credenciales
  ✅ Las variables se cargan en tu app
```

### Paso 5: Configurar Secretos

**En Railway Dashboard → Variables:**

```bash
SPORTRADAR_API_KEY=tu_api_key
BETFAIR_USERNAME=tu_usuario
BETFAIR_PASSWORD=tu_contraseña
BETFAIR_APP_KEY=tu_app_key
ENVIRONMENT=production
PAPER_TRADING=True
LIVE_TRADING=False
```

### Paso 6: Verificar Despliegue

**En Railway Dashboard → Logs:**

```
✅ Python app deployed
✅ Dependencies installed
✅ Bot running
```

### Paso 7: Bot Ejecutándose 24/7

Railway **mantiene tu app ejecutándose continuamente** gracias a:

```
- scheduler.py ejecuta cada 6 horas
- Bot revisa oportunidades de arbitraje
- Coloca apuestas automáticamente (en PAPER_TRADING)
- Logs guardados en storage
```

**Costo Total:** $0 (usas el crédito gratuito)

---

## Opción 2: GitHub Actions

GitHub Actions ejecuta tu bot **gratis** (2000 minutos/mes).

### Paso 1: Preparar Secretos

**En GitHub → Settings → Secrets and variables → Actions:**

```bash
1. Click "New repository secret"

Agregar cada variable:
- SPORTRADAR_API_KEY
- BETFAIR_USERNAME
- BETFAIR_PASSWORD
- BETFAIR_APP_KEY
- DB_HOST (si usas DB externa)
- DB_USER
- DB_PASSWORD
```

### Paso 2: Workflow ya Configurado

El archivo `.github/workflows/betting-bot.yml` ya está configurado:

```yaml
on:
  schedule:
    - cron: '0 */6 * * *'  # Cada 6 horas
  workflow_dispatch:       # O manualmente

jobs:
  betting-bot:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.13'
      - run: pip install -r requirements.txt
      - run: |
          export SPORTRADAR_API_KEY=${{ secrets.SPORTRADAR_API_KEY }}
          export BETFAIR_USERNAME=${{ secrets.BETFAIR_USERNAME }}
          # ... más variables ...
          python main.py
```

### Paso 3: Ver Ejecuciones

**En GitHub → Actions:**

```bash
1. Seleccionar workflow "Betting Bot"
2. Ver historial de ejecuciones
3. Click en cualquiera para ver logs
4. Ver duración y status
```

### Paso 4: Activar Manualmente

**Para ejecutar ahora sin esperar 6 horas:**

```bash
GitHub → Actions → Betting Bot → Run workflow → Run
```

**Costo Total:** $0 (plan gratuito)

**Limitación:** 2000 minutos/mes = ~40 ejecutiones × 6 horas

---

## Opción 3: Heroku

Heroku ofrece **free tier limitado** pero sigue siendo opción.

### Paso 1: Crear Cuenta Heroku

```bash
# 1. Ir a https://www.heroku.com/
# 2. Sign up
# 3. Instalar Heroku CLI:
#    Windows: https://devcenter.heroku.com/articles/heroku-cli
#    Mac: brew tap heroku/brew && brew install heroku
#    Linux: curl https://cli-assets.heroku.com/install.sh | sh
```

### Paso 2: Loguear en Heroku

```bash
heroku login
# Abre navegador, introduce credenciales
```

### Paso 3: Crear App

```bash
heroku create sports-betting-app
# Retorna: https://sports-betting-app.herokuapp.com
```

### Paso 4: Agregar PostgreSQL

```bash
heroku addons:create heroku-postgresql:hobby-dev
# Hobby-dev es GRATIS
```

### Paso 5: Configurar Secretos

```bash
heroku config:set SPORTRADAR_API_KEY=tu_clave
heroku config:set BETFAIR_USERNAME=tu_usuario
heroku config:set BETFAIR_PASSWORD=tu_contraseña
heroku config:set BETFAIR_APP_KEY=tu_app_key
heroku config:set PAPER_TRADING=True
```

### Paso 6: Desplegar

```bash
# Agregar Procfile si no existe
echo "web: python main.py" > Procfile
git add Procfile
git commit -m "Add Procfile"

# Desplegar
git push heroku main
```

### Paso 7: Ver Logs

```bash
heroku logs --tail
```

**Costo Total:** $0 (free tier)

**Nota:** Free tier se "duerme" después de 30 minutos inactividad. Actualizar cada 30 minutos es necesario.

---

## Opción 4: PythonAnywhere

PythonAnywhere es **específico para Python** y ofrece plan gratuito.

### Paso 1: Crear Cuenta

```bash
# 1. Ir a https://www.pythonanywhere.com/
# 2. Sign up (gratis)
# 3. Confirmar email
```

### Paso 2: Clonar Repositorio

**En PythonAnywhere → Bash console:**

```bash
git clone https://github.com/TU_USUARIO/sports-betting-system.git
cd sports-betting-system
mkvirtualenv --python=/usr/bin/python3.9 betting
pip install -r requirements.txt
```

### Paso 3: Crear Archivo .env

**En PythonAnywhere → Files:**

```bash
# Crear archivo: sports-betting-system/.env
SPORTRADAR_API_KEY=tu_clave
BETFAIR_USERNAME=tu_usuario
BETFAIR_PASSWORD=tu_contraseña
BETFAIR_APP_KEY=tu_app_key
PAPER_TRADING=True
LIVE_TRADING=False
DB_HOST=localhost
# ... resto de variables ...
```

### Paso 4: Crear Scheduled Task

**En PythonAnywhere → Web → Scheduled tasks:**

```bash
1. Click "Add new scheduled task"
2. Hora: 00:00 (medianoche)
3. Comando: /home/TU_USUARIO/.virtualenvs/betting/bin/python /home/TU_USUARIO/sports-betting-system/main.py
4. Click "Save"
```

Repetir para más horas si quieres ejecuciones frecuentes.

### Paso 5: Ver Logs

**En PythonAnywhere → Web → Scheduled tasks:**

```bash
Click en tarea → Ver output/errors
```

**Costo Total:** $0 (plan gratuito limitado)

---

## Comparación de Opciones

| Opción | Facilidad | Costo | Uptime | Mantenimiento |
|--------|-----------|-------|--------|--------------|
| **Railway** | ⭐⭐⭐⭐⭐ | $0 (crédito) | 99.9% | Mínimo |
| **GitHub Actions** | ⭐⭐⭐⭐ | $0 | 99.5% | Mínimo |
| **Heroku** | ⭐⭐⭐ | $0* | 99%* | Bajo |
| **PythonAnywhere** | ⭐⭐⭐ | $0* | 99%* | Bajo |

*Con limitaciones de free tier

### Recomendación
🏆 **Railway.app** es la mejor opción para este proyecto:
- Crédito gratuito de $5 (1-2 meses)
- Despliegue automático desde GitHub
- PostgreSQL incluido
- Muy fácil de usar
- Soporte excelente

---

## Proceso Completo en 5 Minutos

### Railway.app Express Setup

```bash
# 1. Terminal local (2 min)
git add .
git commit -m "Ready for deployment"
git push origin main

# 2. Railway Dashboard (3 min)
# - New Project
# - Deploy from GitHub
# - Add PostgreSQL
# - Add Variables (SPORTRADAR_API_KEY, etc.)
# - Deploy

# ✅ Bot ejecutándose en 5 minutos
```

---

## Monitorear Bot Ejecutándose

### Railway.app

```bash
# Logs en tiempo real
Dashboard → Deployments → Logs

# Buscar errores
grep ERROR logs/
```

### GitHub Actions

```bash
# Ver ejecuciones
GitHub → Actions → Betting Bot

# Logs detallados
Click en ejecución → View logs
```

### Local Terminal

```bash
# Ver logs locales mientras pruebas
tail -f logs/betting_system.log
```

---

## Troubleshooting

### Error: "ModuleNotFoundError"

```bash
# En Railway/Heroku:
# Asegurarse que requirements.txt está actualizado
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push origin main

# Railway redeploya automáticamente
```

### Error: "API Key invalid"

```bash
# Verificar en dashboard que variable está correcta
# Importante: esperar 2-3 minutos después de agregar variable
# Railway necesita reiniciar app para cargar nuevas variables
```

### Error: "Connection refused" PostgreSQL

```bash
# Si PostgreSQL no está disponible:
# 1. Railway: Agregar PostgreSQL service
# 2. Heroku: heroku addons:create heroku-postgresql:hobby-dev
# 3. Local: sudo service postgresql start

# Esperar 1-2 minutos para inicializar
```

### Error: "PAPER_TRADING not set"

```bash
# Asegurarse que variable existe en .env
PAPER_TRADING=True

# O en Railway/Heroku
# Agregar manualmente en dashboard
```

### App Sin Respuesta

```bash
# Problema común: free tier se "duerme"
# Solución: Usar Railway (mantiene app activo)
# O: Configurar healthcheck para mantener activo
```

---

## Verificar Que Funciona

### Después de Desplegar

```bash
# 1. Ver logs (debe decir "Bot running")
# 2. Esperar 6 horas para siguiente ejecución automática
# 3. O ejecutar manualmente en GitHub Actions

# Señales de éxito:
✅ Bot started successfully
✅ System authenticated
✅ Checking arbitrage opportunities
✅ No opportunities found (o "Found X opportunities")
```

### Testing Local Primero

```bash
# Antes de desplegar:
PAPER_TRADING=True SPORTRADAR_API_KEY=tu_clave python main.py

# Debe ejecutarse sin errores
```

---

## Próximos Pasos

1. ✅ Seleccionar opción de despliegue (Railway recomendado)
2. ✅ Crear repositorio GitHub
3. ✅ Push código
4. ✅ Crear cuenta en plataforma despliegue
5. ✅ Conectar repositorio
6. ✅ Agregar variables de entorno
7. ✅ Desplegar
8. ✅ Verificar logs
9. ✅ Ejecutar 24h en PAPER_TRADING
10. ✅ (Opcional) Cambiar a LIVE_TRADING

---

## Support & Recursos

### Documentación Oficial

- Railway: https://docs.railway.app/
- GitHub Actions: https://docs.github.com/en/actions
- Heroku: https://devcenter.heroku.com/
- PythonAnywhere: https://www.pythonanywhere.com/help/

### Comunidad

- GitHub Issues: https://github.com/TU_USUARIO/sports-betting-system/issues
- Stack Overflow: Tag `deployment python`
- Reddit: r/Python, r/DevOps

### Contacto Soporte

- Railway Support: https://support.railway.app/
- GitHub Support: https://github.com/support

---

**Última actualización:** Enero 2026  
**Versión:** 1.0  
**Costo Total:** $0
