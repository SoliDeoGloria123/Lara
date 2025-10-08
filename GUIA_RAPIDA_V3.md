# 🚀 Guía Rápida - Lara v3.0

## ⚡ Inicio Ultra Rápido (1 minuto)

```bash
# 1. Crear proyecto
lara create mi_backend
  📝 ¿Deseas configurar una base de datos ahora? [Y/n]: y
  📝 Connection string: mongodb+srv://user:pass@cluster.mongodb.net/DB
  
  ⏳ Creando entorno virtual...
      ✅ Entorno virtual creado
  ⏳ Instalando dependencias...
      ✅ Dependencias instaladas
  ⏳ Configurando .env...
      ✅ .env configurado con tu base de datos
  ⏳ Finalizando configuración...
      ✅ Proyecto completamente configurado!

# 2. Entrar y analizar BD
cd mi_backend
lara get-database

# 3. Generar código
lara sync-models

# 4. Iniciar servidor
lara start
```

**¡Listo!** Tu API está en: http://localhost:8000/docs

---

## 📋 Comandos Principales

### `lara create <nombre>`
Crea proyecto con **configuración automática completa**.

```bash
lara create senasoft2024
```

**¿Qué hace?**
1. ✅ Pregunta connection string (opcional)
2. ✅ Crea estructura del proyecto
3. ✅ Crea `venv` automáticamente
4. ✅ Instala dependencias automáticamente
5. ✅ Configura `.env` con tu BD

**Omitir setup automático:**
```bash
lara create mi_proyecto --skip-setup
```

### `lara start`
Inicia el servidor FastAPI.

```bash
lara start
```

**Opciones:**
```bash
lara start --host 0.0.0.0 --port 3000  # Custom host/port
lara start --no-reload                  # Sin auto-reload
```

### `lara get-database`
Analiza tu base de datos.

```bash
lara get-database                                    # Interactivo o desde .env
lara get-database -c "mongodb+srv://..."             # Con parámetro
```

### `lara sync-models`
Genera modelos, schemas, controllers y routes.

```bash
lara sync-models
```

---

## 🎯 Escenarios de Uso

### 🏆 Competencia (Senasoft, Hackathon)

**Con BD proporcionada:**
```bash
lara create hackathon2024
  Connection string: [PEGAR CLUSTER AQUÍ]
cd hackathon2024
lara get-database
lara sync-models
lara start
```

**Sin BD al inicio:**
```bash
lara create hackathon2024
  ¿Deseas configurar BD ahora? [Y/n]: n
cd hackathon2024
# ...más tarde cuando tengas la BD...
lara get-database -c "connection_string"
lara sync-models
lara start
```

### 💻 Desarrollo Normal

**Setup rápido:**
```bash
lara create mi_api
  Connection string: postgresql://localhost/midb
cd mi_api
lara start
```

### 🧪 Pruebas/Experimentos

**Sin configuración automática:**
```bash
lara create test_api --skip-setup
cd test_api
# Configurar manualmente según necesites
```

---

## 🔌 Connection Strings Soportados

### MongoDB
```bash
mongodb+srv://user:pass@cluster.mongodb.net/database
mongodb://localhost:27017/database
```

### PostgreSQL
```bash
postgresql://user:pass@localhost:5432/database
postgresql://user:pass@host.com/database?ssl=true
```

### MySQL
```bash
mysql://user:pass@localhost:3306/database
mysql+pymysql://user:pass@localhost:3306/database
```

### SQL Server
```bash
mssql+pyodbc://user:pass@localhost/database?driver=ODBC+Driver+17+for+SQL+Server
Data Source=localhost\\SQLEXPRESS;Initial Catalog=DB;...
```

### SQLite (desarrollo)
```bash
sqlite:///./database.db
```

---

## 📝 Estructura de Proyecto Generado

```
mi_proyecto/
├── venv/                    # ✨ Creado automáticamente
│   ├── bin/                 # (Scripts/ en Windows)
│   └── lib/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app
│   ├── config.py            # Configuración
│   ├── database.py          # Conexión BD
│   ├── models/              # Modelos SQLAlchemy
│   ├── schemas/             # Schemas Pydantic
│   ├── controllers/         # CRUD controllers
│   ├── routes/              # API routes
│   ├── middlewares/         # Middlewares (JWT, CORS)
│   └── utils/               # Utilidades (auth, etc)
├── tests/
│   └── __init__.py
├── .env                     # ✨ Configurado automáticamente
├── .env.example
├── .gitignore
├── requirements.txt         # ✨ Ya instalado
└── README.md
```

---

## 🎨 Ejemplo Completo: E-commerce API

```bash
# 1. Crear proyecto
lara create ecommerce_api
  Connection string: postgresql://localhost/ecommerce

# 2. Esperar setup automático (~30 segundos)

# 3. Entrar al proyecto
cd ecommerce_api

# 4. Verificar tablas de la BD
lara get-database
  ✅ usuarios (id, email, password)
  ✅ productos (id, nombre, precio, stock)
  ✅ pedidos (id, usuario_id, fecha, total)
  ✅ pedido_items (id, pedido_id, producto_id, cantidad)

# 5. Generar todo el código
lara sync-models
  ¿Generar modelos? [Y/n]: y
  ¿Generar schemas? [Y/n]: y
  ¿Generar controllers? [Y/n]: y
  ¿Generar routes? [Y/n]: y
  
  ✅ 4 modelos generados
  ✅ 12 schemas generados
  ✅ 4 controllers generados
  ✅ 4 routers generados
  ✅ ~24 endpoints creados

# 6. Iniciar servidor
lara start
  🌐 http://localhost:8000
  📚 http://localhost:8000/docs

# 7. Endpoints disponibles automáticamente:
#    GET    /api/usuarios
#    POST   /api/usuarios
#    GET    /api/usuarios/{id}
#    PUT    /api/usuarios/{id}
#    DELETE /api/usuarios/{id}
#    (igual para productos, pedidos, pedido_items)
```

**Tiempo total:** ~2 minutos para tener una API completa funcionando 🚀

---

## 🔐 Autenticación JWT Automática

Si tu BD tiene tabla de usuarios con contraseña, Lara **detecta automáticamente** y genera:

✅ **Endpoints de auth:**
- `POST /api/auth/register` - Registrar usuario
- `POST /api/auth/token` - Login (obtener JWT)
- `GET /api/auth/me` - Perfil del usuario actual

✅ **Hash de contraseñas** con bcrypt

✅ **Middleware JWT** completo

✅ **Utilidades de auth** (create_token, verify_password)

---

## 💡 Tips

### Velocidad Máxima

```bash
# En lugar de responder cada pregunta de sync-models:
lara create proyecto && cd proyecto && \
lara get-database && \
yes | lara sync-models && \
lara start
```

### Ver logs del servidor

```bash
lara start  # Muestra logs en tiempo real
# Ctrl+C para detener
```

### Cambiar puerto si 8000 está ocupado

```bash
lara start --port 8001
```

### Sin base de datos (API desde cero)

```bash
lara create api_simple --skip-setup
cd api_simple
# Crear modelos manualmente en app/models/
lara start
```

---

## ⚙️ Configuración Manual (si usaste --skip-setup)

```bash
# Crear proyecto sin setup
lara create proyecto --skip-setup
cd proyecto

# Setup manual paso a paso
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
nano .env  # Editar DATABASE_URL

# Iniciar
lara start
```

---

## 🆘 Solución de Problemas

### "No se encontró app/main.py"
```bash
# Asegúrate de estar en la raíz del proyecto
cd mi_proyecto
lara start
```

### "No se encontró uvicorn"
```bash
# Instalar dependencias
pip install -r requirements.txt
```

### "Error de conexión a BD"
```bash
# Verificar .env
cat .env
# Actualizar connection string
nano .env
```

### Puerto 8000 ocupado
```bash
lara start --port 8001
```

---

## 📚 Recursos

- **Repositorio:** https://github.com/SoliDeoGloria123/Lara
- **Issues:** https://github.com/SoliDeoGloria123/Lara/issues
- **Documentación Completa:** Ver `README.md`
- **Cambios v3.0:** Ver `FLUJO_AUTOMATICO_V3.md`

---

## 🎉 ¡Listo para competir!

Con Lara v3.0 puedes crear un backend FastAPI completo en **menos de 2 minutos**.

**Perfecto para:**
- 🏆 Competencias de programación
- ⚡ Hackathons
- 🚀 Prototipos rápidos
- 💻 Desarrollo ágil

**¡Suerte en tu próxima competencia!** 🍀

---

**Versión:** 3.0.0  
**Fecha:** Octubre 2025  
**Autor:** SoliDeoGloria123
