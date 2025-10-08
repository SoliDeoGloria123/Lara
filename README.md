# 🚀 Lara - FastAPI CLI Generator

<div align="center">

![Lara Logo](https://img.shields.io/badge/Lara-FastAPI%20CLI-blue?style=for-the-badge&logo=fastapi)
[![Python](https://img.shields.io/badge/python-3.9+-blue?style=for-the-badge&logo=python)](https://www.python.org)
[![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)](LICENSE)
[![PyPI](https://img.shields.io/badge/PyPI-0.1.0-orange?style=for-the-badge&logo=pypi)](https://pypi.org)

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

### 1. Crear un Nuevo Proyecto

```bash
lara create mi_proyecto
cd mi_proyecto
```

Esto genera:
```
mi_proyecto/
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
├── .env.example
├── requirements.txt
└── README.md
```

### 2. Configurar y Ejecutar

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar base de datos
cp .env.example .env
# Editar .env con tu DATABASE_URL

# Ejecutar
uvicorn app.main:app --reload
```

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
Crea un nuevo proyecto FastAPI completo.

```bash
lara create mi_api
```

### `lara get-database`
Analiza la base de datos configurada en `.env` y muestra su estructura.

```bash
lara get-database
```

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
# 1. Crear proyecto
lara create senasoft2024
cd senasoft2024

# 2. Configurar entorno
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Configurar base de datos (te dan una BD existente)
cp .env.example .env
# Editar .env con credenciales

# 4. Analizar BD
lara get-database

# 5. Generar todo el código
lara sync-models
# Responder 'y' a todo

# 6. Ejecutar
uvicorn app.main:app --reload

# 7. Ver documentación automática
# http://localhost:8000/docs
```

**Tiempo total: ~2 minutos** ⚡

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

Desarrollado con ❤️ por [SoliDeoGloria123](https://github.com/SoliDeoGloria123)

Inspirado en:
- Laravel Artisan (PHP)
- Entity Framework Core CLI (.NET)
- Django Management Commands (Python)

---

## 📞 Soporte

- 🐛 **Issues**: [GitHub Issues](https://github.com/SoliDeoGloria123/Lara/issues)
- 📧 **Email**: contact@lara-cli.dev
- 💬 **Discussions**: [GitHub Discussions](https://github.com/SoliDeoGloria123/Lara/discussions)

---

<div align="center">

**⭐ Si te gusta Lara, dale una estrella en GitHub ⭐**

[Reportar Bug](https://github.com/SoliDeoGloria123/Lara/issues) •
[Solicitar Feature](https://github.com/SoliDeoGloria123/Lara/issues) •
[Documentación](https://github.com/SoliDeoGloria123/Lara#readme)

</div>
