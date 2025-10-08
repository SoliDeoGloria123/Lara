# 🚀 Lara - FastAPI CLI Generator

<div align="center">

<img src="assets/logo.png" alt="Lara Logo" width="120"/>

[![Python](https://img.shields.io/badge/python-3.9+-blue?style=for-the-badge&logo=python)](https://www.python.org)
[![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)](LICENSE)
[![PyPI](https://img.shields.io/badge/PyPI-3.0.1-orange?style=for-the-badge&logo=pypi)](https://pypi.org)

**Genera proyectos FastAPI completos en segundos** 🚀

Herramienta CLI diseñada para competencias de programación (Senasoft, hackathons, etc.) que permite crear APIs REST con FastAPI de forma rápida y profesional, similar a Laravel Artisan o Entity Framework Core CLI.

[Características](#-características) •
[Instalación](#-instalación) •
[Uso](#-uso-rápido) •
[Documentación](#-documentación)

</div>

---

## ✨ Características

### 🎯 Generación Rápida
- ✅ **Proyecto completo** en un solo comando
- ✅ **Estructura profesional** con mejores prácticas
- ✅ **Autenticación JWT** lista para usar
- ✅ **CORS configurado** automáticamente

### 🗄️ Sincronización con Base de Datos
- ✅ **Analiza tu BD existente** (PostgreSQL, MySQL, SQLite, SQL Server)
- ✅ **Detecta tablas automáticamente**
- ✅ **Genera modelos SQLAlchemy** con relaciones
- ✅ **Crea schemas Pydantic** (Create, Update, Response)
- ✅ **Genera controllers CRUD** completos
- ✅ **Genera routes FastAPI** con documentación

### 🔧 Flexibilidad
- ✅ **Detección inteligente** de tablas de autenticación
- ✅ **Generación interactiva** (elige qué generar)
- ✅ **Middlewares personalizados**
- ✅ **MongoDB** (opcional)

---

## 📦 Instalación

### Desde PyPI (recomendado)

```bash
pip install lara-cli
```

### Desde código fuente

```bash
git clone https://github.com/SoliDeoGloria123/Lara.git
cd Lara
pip install -e .
```

### Verificar instalación

```bash
lara version
```

---

## 🚀 Uso Rápido

### 1. Crear un Nuevo Proyecto (¡TODO AUTOMÁTICO!)

```bash
lara create mi_proyecto
```

**¡Eso es todo!** Lara automáticamente:
- ✅ Te pregunta el **connection string** de tu base de datos
- ✅ Crea la estructura del proyecto
- ✅ Crea el **entorno virtual** (venv)
- ✅ Instala las **dependencias** (requirements.txt)
- ✅ Configura el **.env** con tu base de datos

```
mi_proyecto/
├── venv/                    # ✅ Ya creado
├── app/
│   ├── main.py              # FastAPI app
│   ├── config.py            # Configuración
│   ├── database.py          # Conexión a BD
│   ├── models/              # Modelos SQLAlchemy
│   ├── schemas/             # Schemas Pydantic
│   ├── controllers/         # Lógica CRUD
│   ├── routes/              # Endpoints FastAPI
│   ├── middlewares/         # Middlewares (JWT, CORS)
│   └── utils/               # Utilidades (auth, etc)
├── tests/
├── .env                     # ✅ Ya configurado
├── requirements.txt
└── README.md
```

### 2. Iniciar el Servidor

```bash
cd mi_proyecto
lara start
```

¡Ya está corriendo! 🎉 Accede a: http://localhost:8000/docs

### 3. Sincronizar con Base de Datos Existente

```bash
# Analizar tu base de datos
lara get-database
```

Salida ejemplo:
```
🔍 Analizando base de datos...

✅ Conexión exitosa a POSTGRESQL
   Host: localhost:5432
   Database: mi_competencia_db

✅ Se encontraron 5 tablas:

📋 usuarios
   id: INTEGER (PK)
   email: VARCHAR(255) (NOT NULL, UNIQUE)
   hashed_password: VARCHAR(255) (NOT NULL)
   created_at: TIMESTAMP

📋 productos
   id: INTEGER (PK)
   nombre: VARCHAR(200) (NOT NULL)
   precio: DECIMAL(10,2) (NOT NULL)
   categoria_id: INTEGER (FK → categorias.id)

⚠️  Se detectaron 2 tablas SIN modelos:
  • productos
  • categorias

💡 Ejecuta 'lara sync-models' para generarlos
```

### 4. Generar Modelos Automáticamente

```bash
lara sync-models
```

**Flujo interactivo:**
```
🔄 Sincronizando con base de datos...

📋 Se encontraron 2 tablas nuevas:
  ⚠ productos
  ⚠ categorias

¿Desea generar modelos? [y/N]: y

✨ Generando modelos...
  ✅ app/models/productos_model.py
  ✅ app/models/categorias_model.py

¿Desea generar schemas Pydantic? [y/N]: y

✨ Generando schemas...
  ✅ app/schemas/productos_schema.py
  ✅ app/schemas/categorias_schema.py

¿Desea generar controllers CRUD? [y/N]: y

✨ Generando controllers...
  ✅ app/controllers/productos_controller.py
  ✅ app/controllers/categorias_controller.py

¿Desea generar routes? [y/N]: y

✨ Generando routes...
  ✅ app/routes/productos_routes.py
  ✅ app/routes/categorias_routes.py

🔧 Actualizando main.py...
  ✅ Routers registrados automáticamente

🎉 ¡Sincronización completada!

📝 Resumen:
  • 2 modelos generados
  • 6 schemas generados (Create, Update, Response)
  • 2 controllers generados
  • 2 routers generados
  • ~12 endpoints creados

💡 Ejecuta 'uvicorn app.main:app --reload'
```

---

## 📖 Comandos

### `lara create <nombre>`
Crea un nuevo proyecto FastAPI completo **con configuración automática**.

```bash
lara create mi_api
# Te pide: Connection string de tu BD
# ✨ Crea venv, instala deps, configura .env automáticamente
```

**Opciones:**
- `--skip-setup`: Omite la configuración automática (venv, deps, .env)

### `lara start`
Inicia el servidor FastAPI con uvicorn.

```bash
cd mi_proyecto
lara start
# Servidor en: http://localhost:8000
# Docs en: http://localhost:8000/docs
```

**Opciones:**
- `--host / -h`: Host del servidor (default: 127.0.0.1)
- `--port / -p`: Puerto del servidor (default: 8000)
- `--no-reload`: Desactiva auto-reload

### `lara get-database`
Analiza la base de datos y muestra su estructura.

```bash
lara get-database
# O con parámetro:
lara get-database -c "postgresql://user:pass@host/db"
```

**Métodos de conexión (en orden de prioridad):**
1. Parámetro `-c` / `--connection`
2. Variable en `.env` (MONGODB_URL o DATABASE_URL)
3. Input interactivo (te lo pide por terminal)

### `lara sync-models`
Sincroniza modelos con la base de datos y genera código automáticamente.

```bash
lara sync-models
```

### `lara generate-middleware <nombre>`
Genera un middleware personalizado.

```bash
lara generate-middleware rate_limit
```

### `lara version`
Muestra la versión de Lara.

```bash
lara version
```

---

## 🗄️ Bases de Datos Soportadas

- ✅ **SQLite** (desarrollo rápido)
- ✅ **PostgreSQL** (recomendado para producción)
- ✅ **MySQL / MariaDB**
- ✅ **SQL Server**
- ✅ **MongoDB** (experimental)

### Configuración en `.env`:

```env
# SQLite
DATABASE_URL=sqlite:///./app.db

# PostgreSQL
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# MySQL
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/dbname

# MongoDB (opcional)
MONGODB_URL=mongodb://localhost:27017/dbname
```

---

## 🔐 Autenticación JWT

Lara detecta automáticamente tablas de usuarios (`users`, `usuarios`) y genera:

✅ **Modelo con `hashed_password`**
✅ **Schemas con validación de email**
✅ **Controller con hash de contraseñas (bcrypt)**
✅ **Endpoints de autenticación** (`/register`, `/login`, `/me`)
✅ **Middleware JWT** completo
✅ **Utilidades de auth** (create_token, verify_password)

### Endpoints generados automáticamente:

```
POST /api/auth/register  # Registro de usuario
POST /api/auth/token     # Login (obtener token)
GET  /api/auth/me        # Perfil del usuario actual (requiere token)
```

---

## 📝 Ejemplo Completo

### Escenario: Competencia Senasoft

```bash
# 1. Crear proyecto (te pide el connection string)
lara create senasoft2024
# 📝 Connection string: [PEGAR EL CLUSTER/CONNECTION STRING AQUÍ]
# ⏳ Configurando... venv, deps, .env
# ✅ ¡Proyecto listo!

cd senasoft2024

# 2. Analizar BD
lara get-database

# 3. Generar todo el código
lara sync-models
# Responder 'y' a todo

# 4. Ejecutar
lara start

# 5. Ver documentación automática
# http://localhost:8000/docs
```

**Tiempo total: ~1 minuto** ⚡

### ¿Qué pasó detrás de escena?

Cuando ejecutaste `lara create`:
1. ✅ Creó la estructura completa del proyecto
2. ✅ Creó el entorno virtual (`python -m venv venv`)
3. ✅ Instaló todas las dependencias (`pip install -r requirements.txt`)
4. ✅ Configuró `.env` con tu connection string
5. ✅ Todo listo para `lara start`

---

## 🎨 Código Generado

### Modelo (SQLAlchemy)

```python
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Producto(Base):
    __tablename__ = "productos"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False)
    precio = Column(Float, nullable=False)
    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    
    categoria = relationship("Categoria", back_populates="productos")
```

### Schema (Pydantic)

```python
from pydantic import BaseModel, Field
from typing import Optional

class ProductoCreate(BaseModel):
    nombre: str = Field(..., max_length=200)
    precio: float = Field(..., gt=0)
    categoria_id: int

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    precio: Optional[float] = None
    categoria_id: Optional[int] = None

class ProductoResponse(BaseModel):
    id: int
    nombre: str
    precio: float
    categoria_id: int
    
    class Config:
        from_attributes = True
```

### Controller (CRUD)

```python
class ProductoController:
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Producto).offset(skip).limit(limit).all()
    
    @staticmethod
    def create(db: Session, data: ProductoCreate):
        db_producto = Producto(**data.dict())
        db.add(db_producto)
        db.commit()
        db.refresh(db_producto)
        return db_producto
    
    # + update, delete, get_by_id...
```

### Routes (FastAPI)

```python
@router.get("/", response_model=List[ProductoResponse])
def get_productos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return ProductoController.get_all(db, skip, limit)

@router.post("/", response_model=ProductoResponse, status_code=201)
def create_producto(data: ProductoCreate, db: Session = Depends(get_db)):
    return ProductoController.create(db, data)

# + PUT, DELETE, GET by ID...
```

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! 

1. Fork el proyecto
2. Crea tu rama (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

---

## 🌟 Créditos

<div align="center">

<img src="assets/creador.jpeg" alt="Juan - Creador de Lara" width="150" style="border-radius: 50%;"/>

### Desarrollado con ❤️ por Juan David - Alias Boajerges
**[SoliDeoGloria123](https://github.com/SoliDeoGloria123)**

*"Creando herramientas para que los desarrolladores se enfoquen en lo que realmente importa: resolver problemas."*

</div>

**Inspirado en:**
- 🎨 Laravel Artisan (PHP)
- ⚙️ Entity Framework Core CLI (.NET)
- 🐍 Django Management Commands (Python)

---

## 📞 Soporte

- 🐛 **Issues**: [GitHub Issues](https://github.com/SoliDeoGloria123/Lara/issues)
- 📧 **Email**: juan.juand.dev@gmail.com
- 💬 **Discussions**: [GitHub Discussions](https://github.com/SoliDeoGloria123/Lara/discussions)

---

<div align="center">

**⭐ Si te gusta Lara, dale una estrella en GitHub ⭐**

[Reportar Bug](https://github.com/SoliDeoGloria123/Lara/issues) •
[Solicitar Feature](https://github.com/SoliDeoGloria123/Lara/issues) •
[Documentación](https://github.com/SoliDeoGloria123/Lara#readme)

</div>
