# 📋 Ejemplos de Uso de Lara

## Ejemplo 1: API Simple de Productos

### 1. Crear proyecto

```bash
lara create tienda_api
cd tienda_api
```

### 2. Configurar base de datos

Editar `.env`:
```env
DATABASE_URL=sqlite:///./tienda.db
```

### 3. Crear tabla en la BD

```python
# create_tables.py
import sqlite3

conn = sqlite3.connect('tienda.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10,2) NOT NULL,
    stock INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

conn.commit()
conn.close()
```

### 4. Sincronizar con Lara

```bash
lara get-database
lara sync-models
```

### 5. Ejecutar

```bash
uvicorn app.main:app --reload
```

## Ejemplo 2: API con Autenticación

### 1. Crear proyecto

```bash
lara create auth_api
cd auth_api
```

### 2. Crear tabla de usuarios

```sql
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    nombre VARCHAR(100),
    rol VARCHAR(50) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 3. Sincronizar (Lara detecta automáticamente la tabla de auth)

```bash
lara sync-models
```

### 4. Usar los endpoints de autenticación

```bash
# Registrar usuario
curl -X POST http://localhost:8000/api/usuarios/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "secretpassword123",
    "nombre": "Juan Pérez"
  }'

# Login (obtener token)
curl -X POST http://localhost:8000/api/usuarios/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=secretpassword123"

# Acceder a perfil (con token)
curl http://localhost:8000/api/usuarios/me \
  -H "Authorization: Bearer <tu_token_aqui>"
```

## Ejemplo 3: Competencia Senasoft

### Escenario: Te dan una base de datos PostgreSQL

```bash
# 1. Crear proyecto
lara create senasoft2024
cd senasoft2024

# 2. Instalar dependencias
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install psycopg2-binary  # Driver PostgreSQL

# 3. Configurar .env con credenciales proporcionadas
cat > .env << EOF
DATABASE_URL=postgresql://senasoft:password@db.server.com:5432/competencia
SECRET_KEY=$(openssl rand -hex 32)
EOF

# 4. Analizar base de datos
lara get-database

# 5. Generar TODO el código
lara sync-models
# Responder 'y' a todas las preguntas

# 6. Ejecutar
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Tiempo total: ~3 minutos** ⚡

## Ejemplo 4: Múltiples Tablas con Relaciones

### Base de datos

```sql
CREATE TABLE categorias (
    id INTEGER PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

CREATE TABLE productos (
    id INTEGER PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    categoria_id INTEGER,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);

CREATE TABLE pedidos (
    id INTEGER PRIMARY KEY,
    usuario_id INTEGER NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    estado VARCHAR(50) DEFAULT 'pendiente',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE pedido_items (
    id INTEGER PRIMARY KEY,
    pedido_id INTEGER NOT NULL,
    producto_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);
```

### Sincronizar

```bash
lara sync-models
```

Lara generará automáticamente:
- ✅ 4 modelos con relaciones
- ✅ 12 schemas Pydantic
- ✅ 4 controllers CRUD
- ✅ 4 routers FastAPI
- ✅ ~24 endpoints

## Ejemplo 5: Generar Middleware Personalizado

```bash
lara generate-middleware rate_limit
```

Genera:
```python
# app/middlewares/rate_limit_middleware.py
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Tu lógica aquí
        response = await call_next(request)
        return response
```

Registrar en `main.py`:
```python
from app.middlewares.rate_limit_middleware import RateLimitMiddleware

app.add_middleware(RateLimitMiddleware)
```

## Endpoints Generados Automáticamente

Para cada modelo, Lara genera:

```
GET    /api/{recursos}/              # Listar todos
GET    /api/{recursos}/{id}          # Obtener por ID
POST   /api/{recursos}/              # Crear nuevo
PUT    /api/{recursos}/{id}          # Actualizar
DELETE /api/{recursos}/{id}          # Eliminar
GET    /api/{recursos}/search/?q=... # Buscar
```

Más endpoints de autenticación:
```
POST   /api/usuarios/register        # Registro
POST   /api/usuarios/token           # Login
GET    /api/usuarios/me              # Perfil actual
```

## Personalización Post-Generación

Lara genera código base que puedes personalizar:

### Agregar validaciones personalizadas

```python
# app/schemas/producto_schema.py
from pydantic import validator

class ProductoCreate(ProductoBase):
    @validator('precio')
    def precio_positivo(cls, v):
        if v <= 0:
            raise ValueError('El precio debe ser positivo')
        return v
```

### Agregar lógica de negocio

```python
# app/controllers/producto_controller.py
class ProductoController:
    @staticmethod
    def create(db: Session, data: ProductoCreate):
        # Validación adicional
        if data.stock < 0:
            raise HTTPException(400, "Stock no puede ser negativo")
        
        db_record = Producto(**data.dict())
        db.add(db_record)
        db.commit()
        return db_record
```

### Agregar filtros personalizados

```python
# app/routes/producto_routes.py
@router.get("/categoria/{categoria_id}")
def get_by_categoria(categoria_id: int, db: Session = Depends(get_db)):
    return db.query(Producto).filter(
        Producto.categoria_id == categoria_id
    ).all()
```

## Tips para Competencias

1. **Usa SQLite en desarrollo** → Rápido y sin configuración
2. **Genera TODO con sync-models** → No pierdas tiempo escribiendo código repetitivo
3. **Personaliza después** → Primero genera la base, luego personaliza
4. **Lee los comentarios** → Lara deja TODOs donde debes personalizar
5. **Usa /docs** → FastAPI genera documentación automática

## Comandos Útiles

```bash
# Ver estructura de BD
lara get-database

# Regenerar todo
lara sync-models

# Crear proyecto rápido
lara create api && cd api && pip install -r requirements.txt

# Ejecutar con auto-reload
uvicorn app.main:app --reload --host 0.0.0.0

# Ver logs de la aplicación
uvicorn app.main:app --log-level debug
```
