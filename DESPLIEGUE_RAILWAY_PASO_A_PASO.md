# 🚀 GUÍA DE DESPLIEGUE A RAILWAY.APP

## ⏱️ Tiempo Total: 5-10 Minutos

### Paso 1: Ir a Railway.app (1 minuto)

```
1. Abre: https://railway.app
2. Click "Get Started"
3. Click "GitHub Login"
4. Autoriza Railway para acceder a tus repositorios
```

---

### Paso 2: Crear Nuevo Proyecto (2 minutos)

```
En Railway Dashboard:

1. Click "New Project"
2. Seleccionar: "Deploy from GitHub repo"
3. Buscar: "Apuestas_Deportivas" 
4. Click en tu repositorio: LordPercival241/Apuestas_Deportivas
5. Click "Deploy"

✅ Railway comienza a construir automáticamente desde Dockerfile
```

---

### Paso 3: Agregar PostgreSQL (2 minutos)

```
En Railway Dashboard > Tu Proyecto:

1. Click "+ New"
2. Seleccionar: "PostgreSQL"
3. Click "Create"

✅ Railway crea base de datos automáticamente
✅ Proporciona credenciales automáticamente
```

---

### Paso 4: Configurar Variables de Entorno (3 minutos)

**EN RAILWAY:**

```
En Railway Dashboard > Tu Proyecto > Variables:

Click "New Variable" para cada una:

SPORTRADAR_API_KEY = (dejar vacío por ahora, opcional)
BETFAIR_USERNAME = (dejar vacío por ahora, opcional)
BETFAIR_PASSWORD = (dejar vacío por ahora, opcional)
BETFAIR_APP_KEY = (dejar vacío por ahora, opcional)
ENVIRONMENT = production
PAPER_TRADING = True
LIVE_TRADING = False
LOG_LEVEL = INFO

NOTA: Las credenciales de PostgreSQL se cargan automáticamente
      Busca en Variables:
      - DATABASE_URL (automático)
      - PGHOST, PGPORT, PGUSER, PGPASSWORD (automáticos)
```

---

### Paso 5: Verificar Despliegue (2 minutos)

```
En Railway Dashboard:

1. Click en "Deployments" 
2. Ver el estado: "Building..." → "Deployed" ✅
3. Ver los logs en tiempo real

Deberías ver:
  ✅ Build started
  ✅ Installing dependencies
  ✅ Docker image created
  ✅ Container running
  ✅ Bot started
```

---

### Paso 6: Verificar que Funciona (1 minuto)

```
En Railway Dashboard > Logs:

Buscar estos mensajes:
  [INFO] System initializing...
  [INFO] Paper trading mode enabled
  [INFO] Checking for arbitrage opportunities...
  [INFO] Bot running

✅ Si ves estos mensajes: ¡BOT CORRIENDO EN PRODUCCIÓN!
```

---

## ✅ CHECKLIST DE DESPLIEGUE

```
[ ] Ir a Railway.app
[ ] Crear cuenta GitHub
[ ] Autorizar Railway
[ ] "New Project" → Deploy from GitHub
[ ] Seleccionar Apuestas_Deportivas
[ ] Click Deploy
[ ] Agregar PostgreSQL
[ ] Configurar variables
[ ] Ver logs de despliegue
[ ] Verificar "Bot running"
[ ] ¡LISTO!
```

---

## 💰 COSTO

```
Railway.app:        $0 ($5 crédito incluido)
PostgreSQL:         $0 (incluido)
Hosting:            $0
Git Deployment:     $0
Total Mensual:      $0
```

---

## 🎯 DESPUÉS DE DESPLEGAR

### El Bot Ahora:
✅ Corre 24/7 sin tu computadora  
✅ Ejecuta cada 6 horas automáticamente  
✅ Busca arbitrajes en tiempo real  
✅ Guarda logs en Railway  
✅ Monitorea eventos deportivos  

### Tu Repo en GitHub:
✅ GitHub Actions ejecuta cada 6 horas  
✅ Railway despliega cambios automáticamente  
✅ Logs disponibles en Railway Dashboard  

---

## 🔐 AGREGAR CREDENCIALES API (Después)

Cuando tengas claves API:

```
En Railway Dashboard > Variables:

SPORTRADAR_API_KEY = tu_clave_aqui
BETFAIR_USERNAME = tu_usuario
BETFAIR_PASSWORD = tu_contraseña
BETFAIR_APP_KEY = tu_app_key

✅ Railway reinicia automáticamente con nuevas variables
```

---

## 📊 MONITOREO EN RAILWAY

```
Railway Dashboard:

📈 Uso de recursos:
   - CPU: ~5-10% (muy bajo)
   - Memoria: ~100-200MB
   - Almacenamiento: ~1GB

📋 Logs en vivo:
   - Ver ejecución en tiempo real
   - Buscar errores
   - Monitorear salud

⚙️ Configuración:
   - Auto-deploy en git push
   - Auto-restart si falla
   - Backup automático de DB
```

---

## ❌ SI ALGO SALE MAL

### Error: "Deployment failed"
```
Ver logs en Railway
Usualmente: credenciales faltantes
Solución: Agregar variables faltantes
```

### Error: "Connection refused PostgreSQL"
```
Esperar 1-2 minutos para que DB inicie
Verificar DATABASE_URL está correcto
Reiniciar deployment
```

### Error: "Module not found"
```
Verificar requirements.txt en GitHub
Hacer git push con cambios
Railway redeploya automáticamente
```

---

## 🎓 PRÓXIMOS PASOS

### Día 1: Setup Básico
```
✅ Desplegar a Railway
✅ Verificar logs
✅ Confirmar "Bot running"
```

### Día 2: Obtener Credenciales
```
✅ Ir a https://developer.sportradar.com/
✅ Registrarse
✅ Crear aplicación
✅ Copiar API Key
✅ Agregar a Railway Variables
```

### Día 3: Habilitar Betfair
```
✅ Ir a https://developer.betfair.com/
✅ Aplicar para acceso API
✅ Esperar aprobación (24-48h)
✅ Configurar credenciales
✅ Cambiar PAPER_TRADING a False (después de validar)
```

---

## 📞 SOPORTE

### Railway Help
```
Docs: https://docs.railway.app/
Support: https://support.railway.app/
Status: https://status.railway.app/
```

### GitHub Help
```
Docs: https://docs.github.com/
Issues: Tu repositorio → Issues
```

---

## 🚀 ¡LISTO!

Todo está configurado. Solo necesitas:

1. Abrir: https://railway.app
2. GitHub Login
3. Deploy desde GitHub
4. Esperar 2-3 minutos
5. Ver logs confirmando "Bot running"

**¿DUDAS? Lee los logs en Railway Dashboard**

---

**Última actualización:** Enero 9, 2026  
**Versión:** 1.0  
**Tiempo de Setup:** 5-10 minutos
