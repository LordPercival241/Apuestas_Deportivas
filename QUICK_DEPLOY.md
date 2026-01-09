# Quick Start - Despliegue en Railway (5 minutos)

## ✅ Opción Más Fácil: Railway.app

### Paso 1: Preparar Repositorio GitHub (1 min)

```bash
# 1. Push tu código a GitHub
git add .
git commit -m "Ready for deployment"
git push origin main

# 2. Verificar que .gitignore excluye .env
cat .gitignore | grep -i ".env"
# Debe mostrar: .env
```

### Paso 2: Crear Cuenta Railway (2 min)

```bash
# 1. Ir a https://railway.app
# 2. Click "Start Free"
# 3. GitHub Login
# 4. Autorizar Railway
```

### Paso 3: Desplegar (2 min)

En Railway Dashboard:
```bash
1. Click "New Project"
2. Seleccionar "Deploy from GitHub repo"
3. Elegir tu repositorio
4. Click "Deploy"

# ¡Ya está desplegando!
```

### Paso 4: Configurar Variables (Opcional pero importante)

```bash
En Railway Dashboard > Variables > Add:

SPORTRADAR_API_KEY=tu-api-key-aqui
BETFAIR_USERNAME=tu-usuario
BETFAIR_PASSWORD=tu-contraseña
BETFAIR_APP_KEY=tu-app-key
ENVIRONMENT=production
PAPER_TRADING=True
LIVE_TRADING=False
LOG_LEVEL=INFO
```

### Paso 5: Ver Logs

```bash
En Railway Dashboard > Deployments > Logs
```

---

## 🔐 Seguridad: Guardar Credenciales

**NUNCA** subas credenciales a GitHub!

### Opción 1: Railway Secrets (Más fácil)
```bash
# En Railway Dashboard
Variables > SPORTRADAR_API_KEY = valor

Las variables están encriptadas y seguras
```

### Opción 2: GitHub Secrets
```bash
# En GitHub > Settings > Secrets and variables > Actions

New repository secret:
- Nombre: SPORTRADAR_API_KEY
- Valor: tu-clave-aqui

Usar en workflows como: ${{ secrets.SPORTRADAR_API_KEY }}
```

### Opción 3: Local .env (Para testing)
```bash
# Crear archivo .env
echo "SPORTRADAR_API_KEY=tu-clave" > .env
echo ".env" >> .gitignore
git add .gitignore
git commit -m "Add .env to gitignore"
git push
```

---

## 🚀 Ejecutar Localmente Primero

Antes de desplegar, prueba localmente:

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
# Editar .env con tus datos

# 4. Ejecutar en paper trading (sin riesgo)
PAPER_TRADING=True python main.py

# 5. Ejecutar tests
pytest tests/ -v
```

---

## 📊 Arquitectura de Despliegue

```
GitHub Repository
        ↓
      Railway
        ↓
   ├─ Python App (main.py)
   ├─ PostgreSQL (opcional)
   └─ Logs & Monitoring
        ↓
   Betfair API
   Sportradar API
```

---

## 🤖 Ejecutar Automáticamente (24/7)

### Opción 1: Railway Cron
```bash
# En railway.toml
[deploy]
startCommand = "python scheduler.py"
```

Luego `scheduler.py` ejecuta cada 6 horas automáticamente.

### Opción 2: GitHub Actions
```bash
# .github/workflows/betting-bot.yml

on:
  schedule:
    - cron: '0 */6 * * *'  # Cada 6 horas

Ejecuta automáticamente en los servidores de GitHub
```

---

## 💰 Costos Finales

| Item | Costo |
|------|-------|
| Railway App | $0 ($5 crédito) |
| PostgreSQL | Incluido |
| GitHub | $0 |
| Hosting | $0 |
| **Total** | **$0** |

---

## ❌ Si Algo Falla

### Error: "ModuleNotFoundError"
```bash
# Solución
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push
# Railway redeploya automáticamente
```

### Error: "API Key invalid"
```bash
# Verificar en Railway
railway env list

# Actualizar si falta
railway env add SPORTRADAR_API_KEY "tu-key"
```

### Error: "Connection refused"
```bash
# Railway tarda ~1 min en iniciar
# Esperar y revisar logs:
railway logs
```

---

## 📝 Próximos Pasos

1. ✅ Repositorio en GitHub
2. ✅ Cuenta Railway creada
3. ✅ Variables configuradas
4. ✅ Despliegue iniciado
5. ⏳ Esperar ~2 minutos
6. ✅ Ver logs en Dashboard
7. ✅ Bot corriendo en 24/7

---

## 🔗 Links Útiles

- Railway: https://railway.app
- GitHub: https://github.com
- Documentación Railway: https://docs.railway.app/
- Python docs: https://docs.python.org/3/
- Betfair API: https://developer.betfair.com/

---

**¿Listo?**

```bash
git push origin main
# Ir a Railway Dashboard
# Click Deploy
# ¡Listo!
```
