# 🚀 Ejemplo de Uso Rápido - Lara CLI v2

## Caso de Uso: Competencia Senasoft

Tienes **3 horas** para crear un backend completo con autenticación. Tu compañero hace el frontend (React). 

### 📋 Escenario

Base de datos MongoDB Atlas ya existe con estas colecciones:
- `usuarios` (email, password, nombre, rol)
- `cursos` (titulo, descripcion, precio, instructor_id)
- `inscripciones` (usuario_id, curso_id, fecha, estado)

**String de conexión:**
```
mongodb+srv://juanjuanddev:hR7m3QxGgMf5BOKv@cluster0.mnzsa9g.mongodb.net/EDUSTREAM?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true
```

---

## ⚡ Paso a Paso (2-3 minutos)

### 1️⃣ Crear proyecto (10 segundos)

```bash
lara create edustream_api
cd edustream_api
```

### 2️⃣ Configurar base de datos (20 segundos)

Editar `.env`:

```bash
DATABASE_TYPE=mongodb
MONGODB_URL=mongodb+srv://juanjuanddev:hR7m3QxGgMf5BOKv@cluster0.mnzsa9g.mongodb.net/EDUSTREAM?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true
SECRET_KEY=super-secret-key-change-in-production
```

### 3️⃣ Analizar base de datos (5 segundos)

```bash
lara get-database
```

**Output esperado:**

```
🔍 Analizando base de datos...

🔌 Conectando a MongoDB...
✅ Conexión exitosa a MongoDB
   Cluster: cluster0.mnzsa9g.mongodb.net
   Database: EDUSTREAM
   Colecciones: 3

✅ Se encontraron 3 colecciones:

┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┓
┃ 🔐📋 usuarios (Documents: 23)                                    ┃
┣━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━╋━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━┫
┃ Campo              ┃ Tipo          ┃ Requerido ┃ Notas              ┃
┣━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━╋━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━┫
┃ _id                ┃ ObjectId      ┃     ✅    ┃ PK                 ┃
┃ nombre             ┃ str           ┃     ✅    ┃ ─                  ┃
┃ email              ┃ EmailStr      ┃     ✅    ┃ 📧 Email, UNIQUE   ┃
┃ password           ┃ str           ┃     ✅    ┃ 🔒 Password hash   ┃
┃ rol                ┃ str           ┃     ❌    ┃ ─                  ┃
┃ fecha_registro     ┃ datetime      ┃     ✅    ┃ ─                  ┃
┗━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━┻━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━┛

  Relaciones detectadas:
    ❌ Ninguna

┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┓
┃ 📋 cursos (Documents: 45)                                        ┃
┣━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━╋━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━┫
┃ Campo              ┃ Tipo          ┃ Requerido ┃ Notas              ┃
┣━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━╋━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━┫
┃ _id                ┃ ObjectId      ┃     ✅    ┃ PK                 ┃
┃ titulo             ┃ str           ┃     ✅    ┃ ─                  ┃
┃ descripcion        ┃ str           ┃     ✅    ┃ ─                  ┃
┃ precio             ┃ float         ┃     ✅    ┃ ─                  ┃
┃ instructor_id      ┃ ObjectId      ┃     ✅    ┃ FK → usuarios      ┃
┃ duracion_horas     ┃ int           ┃     ✅    ┃ ─                  ┃
┗━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━┻━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━┛

  Relaciones detectadas:
    🔗 instructor_id → usuarios._id

┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┓
┃ 📋 inscripciones (Documents: 156)                                ┃
┣━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━╋━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━┫
┃ Campo              ┃ Tipo          ┃ Requerido ┃ Notas              ┃
┣━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━╋━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━┫
┃ _id                ┃ ObjectId      ┃     ✅    ┃ PK                 ┃
┃ usuario_id         ┃ ObjectId      ┃     ✅    ┃ FK → usuarios      ┃
┃ curso_id           ┃ ObjectId      ┃     ✅    ┃ FK → cursos        ┃
┃ fecha_inscripcion  ┃ datetime      ┃     ✅    ┃ ─                  ┃
┃ estado             ┃ str           ┃     ✅    ┃ ─                  ┃
┗━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━┻━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━┛

  Relaciones detectadas:
    🔗 usuario_id → usuarios._id
    🔗 curso_id → cursos._id

╭───────────────── ⚡ Sistema de Autenticación Disponible ─────────────────╮
│                                                                           │
│ 🔐 DETECCIÓN ESPECIAL:                                                   │
│                                                                           │
│ Se detectó colección de autenticación: usuarios                          │
│ Con 'lara sync-models' se generará automáticamente:                      │
│   • Sistema completo de autenticación JWT                                │
│   • Endpoints /register y /login                                         │
│   • Hash automático de contraseñas                                       │
│   • Middleware de autenticación                                          │
╰───────────────────────────────────────────────────────────────────────────╯

⚠️  Se detectaron 3 colecciones SIN modelos:
  • usuarios
  • cursos
  • inscripciones

💡 Ejecuta 'lara sync-models' para generarlos automáticamente
```

### 4️⃣ Generar TODO el código (30 segundos - 1 minuto)

```bash
lara sync-models
```

El comando te hará preguntas interactivas:

```
🔄 Analizando base de datos...
✅ Conectado a: MongoDB (EDUSTREAM)

📊 Resumen:
  • Total colecciones: 3
  • Modelos existentes: 0
  • Nuevas colecciones: 3

🆕 Colecciones a procesar:
  1. usuarios (23 documentos) 🔐
  2. cursos (45 documentos)
  3. inscripciones (156 documentos)

─────────────────────────────────────────────────────────
🔐 DETECCIÓN ESPECIAL: Colección 'usuarios' encontrada!
─────────────────────────────────────────────────────────
Esta colección contiene credenciales de usuarios.

¿Desea generar sistema de autenticación completo? (s/n): s   👈 ¡SÍ!

✨ Sistema de autenticación:
  ✅ Generará endpoints /register y /login
  ✅ Implementará hash de contraseñas (bcrypt)
  ✅ Generará middleware JWT
  ✅ Creará utilidades de autenticación

¿Desea generar MODELOS para estas colecciones? (s/n): s   👈 ¡SÍ!

✨ Generando modelos...
  ✅ app/models/usuario_model.py
  ✅ app/models/curso_model.py
  ✅ app/models/inscripcion_model.py

¿Desea generar SCHEMAS Pydantic? (s/n): s   👈 ¡SÍ!

✨ Generando schemas...
  ✅ app/schemas/usuario_schema.py (UsuarioCreate, Update, Response, Login, Token)
  ✅ app/schemas/curso_schema.py
  ✅ app/schemas/inscripcion_schema.py

¿Desea generar CONTROLLERS CRUD? (s/n): s   👈 ¡SÍ!

✨ Generando controllers...
  ✅ app/controllers/usuario_controller.py (con register() y login())
  ✅ app/controllers/curso_controller.py
  ✅ app/controllers/inscripcion_controller.py

¿Desea generar ROUTES (endpoints FastAPI)? (s/n): s   👈 ¡SÍ!

✨ Generando routes...
  ✅ app/routes/usuario_routes.py
     • POST /register
     • POST /login
     • GET  /me
     • GET  / (lista)
     • GET  /{id}
     • PUT  /{id}
     • DELETE /{id}
  ✅ app/routes/curso_routes.py
  ✅ app/routes/inscripcion_routes.py

🔐 Generando sistema de autenticación...
  ✅ app/middlewares/auth_middleware.py
  ✅ app/utils/auth.py

🔧 Actualizando main.py...
  ✅ Routers registrados
  ✅ Startup event configurado

─────────────────────────────────────────────────────────
🎉 ¡SINCRONIZACIÓN COMPLETADA!
─────────────────────────────────────────────────────────

📊 Resumen:
  ✅ 3 modelos generados
  ✅ 9 schemas generados
  ✅ 3 controllers generados
  ✅ 3 routers generados
  ✅ 21 endpoints creados
  ✅ Sistema de autenticación JWT implementado
```

### 5️⃣ Instalar dependencias (1 minuto)

```bash
pip install -r requirements.txt
```

### 6️⃣ Ejecutar API (inmediato)

```bash
uvicorn app.main:app --reload
```

```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
✅ EDUSTREAM iniciado correctamente
📚 Docs: http://localhost:8000/docs
🔐 Auth endpoints: /api/auth/register, /api/auth/login
```

---

## 🎯 Resultado Final

### ✅ Endpoints generados automáticamente:

#### **Autenticación** (`/api/auth`)
- `POST /api/auth/register` - Registrar nuevo usuario
- `POST /api/auth/login` - Login y obtener JWT token
- `GET /api/auth/me` - Obtener usuario actual (requiere token)

#### **Usuarios** (`/api/usuarios`)
- `GET /api/usuarios/` - Lista todos (requiere auth)
- `GET /api/usuarios/{id}` - Obtener uno (requiere auth)
- `PUT /api/usuarios/{id}` - Actualizar (requiere auth)
- `DELETE /api/usuarios/{id}` - Eliminar (requiere auth)

#### **Cursos** (`/api/cursos`)
- `GET /api/cursos/` - Lista todos
- `POST /api/cursos/` - Crear (requiere auth)
- `GET /api/cursos/{id}` - Obtener uno
- `PUT /api/cursos/{id}` - Actualizar (requiere auth)
- `DELETE /api/cursos/{id}` - Eliminar (requiere auth)

#### **Inscripciones** (`/api/inscripciones`)
- `GET /api/inscripciones/` - Lista todas
- `POST /api/inscripciones/` - Crear (requiere auth)
- `GET /api/inscripciones/{id}` - Obtener una
- `PUT /api/inscripciones/{id}` - Actualizar (requiere auth)
- `DELETE /api/inscripciones/{id}` - Eliminar (requiere auth)

---

## 💻 Para tu compañero de Frontend

Dale estos ejemplos:

### 1. Registro

```javascript
// register.js
async function register(nombre, email, password) {
  const response = await fetch('http://localhost:8000/api/auth/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ nombre, email, password })
  });
  return response.json();
}
```

### 2. Login

```javascript
// login.js
async function login(email, password) {
  const response = await fetch('http://localhost:8000/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  const data = await response.json();
  
  // Guardar token
  if (data.access_token) {
    localStorage.setItem('token', data.access_token);
  }
  
  return data;
}
```

### 3. Peticiones autenticadas

```javascript
// cursos.js
async function getCursos() {
  const token = localStorage.getItem('token');
  
  const response = await fetch('http://localhost:8000/api/cursos/', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  return response.json();
}
```

---

## 🏆 Ventaja Competitiva

| Tarea | Tiempo Manual | Con Lara | Ahorro |
|-------|---------------|----------|--------|
| Setup inicial | 30-45 min | 10 seg | 180x |
| Modelos (3) | 30-45 min | 10 seg | 180x |
| Schemas (9) | 45-60 min | 10 seg | 270x |
| Controllers (3) | 60-90 min | 10 seg | 360x |
| Routes (21 endpoints) | 90-120 min | 10 seg | 540x |
| Sistema Auth JWT | 60-90 min | Automático | ∞ |
| **TOTAL** | **5-7 horas** | **2-3 min** | **100-210x** |

¡Con Lara, tienes **TODO** el backend listo en 3 minutos! 🚀

Te quedan **2 horas 57 minutos** para:
- Implementar lógica de negocio específica
- Optimizar queries
- Agregar validaciones custom
- Documentar
- Probar edge cases
- **¡GANAR LA COMPETENCIA!** 🏆

---

## 🎯 Ejemplo con SQL Server

Si usas SQL Server Management Studio:

```env
DATABASE_TYPE=mssql
DATABASE_URL=Data Source=localhost\SQLEXPRESS;Initial Catalog=CompetenciaDB;User ID=sa;Password=tuPassword123;Trust Server Certificate=True
```

Lara convierte automáticamente a formato SQLAlchemy. ✨

---

## 📚 Swagger UI

Abre http://localhost:8000/docs para ver toda la documentación interactiva. 

Prueba endpoints directamente desde el navegador. El botón **Authorize** 🔒 te permite ingresar el token JWT.

---

## 🎉 ¡Éxito en tu Competencia!

Con Lara pasas de **0 a API completa en 3 minutos**. 

**Enfócate en lo que importa: tu lógica de negocio.** 💪
