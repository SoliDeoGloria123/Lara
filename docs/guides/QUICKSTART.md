# 🛠️ Guía Rápida de Comandos Lara

## 📦 Instalación

```bash
# Instalación global desde PyPI (cuando esté publicado)
pip install lara-cli

# Instalación en modo desarrollo
git clone https://github.com/SoliDeoGloria123/Lara.git
cd Lara
pip install -e .

# Verificar instalación
lara version
```

## 🎯 Comandos Principales

### `lara create <nombre>`
Crea un nuevo proyecto FastAPI completo.

```bash
# Crear proyecto en directorio actual
lara create mi_api

# Crear en ruta específica
lara create mi_api --path /ruta/personalizada

# Ver ayuda
lara create --help
```

**Genera:**
- ✅ Estructura de carpetas completa
- ✅ Archivos de configuración
- ✅ Middlewares (Auth, CORS)
- ✅ Utils (JWT helpers)
- ✅ .env.example
- ✅ requirements.txt
- ✅ README.md
- ✅ .gitignore

---

### `lara get-database`
Analiza la base de datos y muestra su estructura.

```bash
# Analizar BD configurada en .env
lara get-database

# Ver ayuda
lara get-database --help
```

**Requiere:**
- Archivo `.env` en el directorio actual
- Variable `DATABASE_URL` configurada

**Muestra:**
- 📊 Tipo de base de datos
- 📋 Lista de tablas
- 🔑 Columnas con tipos
- 🔗 Foreign Keys
- ⚠️ Tablas sin modelos

---

### `lara sync-models`
Sincroniza modelos con la base de datos (comando más importante).

```bash
# Sincronización interactiva
lara sync-models

# Ver ayuda
lara sync-models --help
```

**Proceso interactivo:**
1. Detecta tablas nuevas
2. Pregunta si generar modelos → Sí/No
3. Pregunta si generar schemas → Sí/No
4. Pregunta si generar controllers → Sí/No
5. Pregunta si generar routes → Sí/No
6. Actualiza main.py automáticamente

**Genera:**
- 🗄️ Modelos SQLAlchemy
- 📝 Schemas Pydantic (Create, Update, Response)
- 🎮 Controllers CRUD
- 🛣️ Routes FastAPI
- 🔐 Auth completo si detecta tabla de usuarios

---

### `lara create-api <nombre>`
Genera API para un recurso específico (sin BD).

```bash
# Generar API manualmente
lara create-api producto

# Ver ayuda
lara create-api --help
```

**Nota:** Actualmente redirige a `sync-models` para generar desde BD.

---

### `lara generate-middleware <nombre>`
Genera un middleware personalizado.

```bash
# Generar middleware
lara generate-middleware rate_limit

# Otros ejemplos
lara generate-middleware logging
lara generate-middleware cache
lara generate-middleware security

# Ver ayuda
lara generate-middleware --help
```

**Genera:**
- Archivo de middleware en `app/middlewares/`
- Template básico con estructura correcta

**Recordar:** Registrar manualmente en `main.py`

---

### `lara version`
Muestra la versión de Lara.

```bash
lara version
```

---

## 🔄 Flujo de Trabajo Típico

### Escenario 1: Proyecto Nuevo con BD Existente

```bash
# 1. Crear proyecto
lara create ecommerce_api
cd ecommerce_api

# 2. Setup entorno
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt

# 3. Configurar BD
cp .env.example .env
nano .env  # Editar DATABASE_URL

# 4. Analizar BD
lara get-database

# 5. Generar todo
lara sync-models
# Responder 'y' a todo

# 6. Ejecutar
uvicorn app.main:app --reload

# 7. Abrir docs
# http://localhost:8000/docs
```

### Escenario 2: Competencia de Programación

```bash
# Setup ultra-rápido (2 minutos)
lara create senasoft2024 && cd senasoft2024
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt psycopg2-binary
echo "DATABASE_URL=postgresql://user:pass@host:5432/db" > .env
lara sync-models  # Responder 'y' a todo
uvicorn app.main:app --reload --host 0.0.0.0
```

### Escenario 3: Agregar Nuevas Tablas

```bash
# 1. Agregar tabla en la BD
# (SQL o herramienta de BD)

# 2. Ver cambios
lara get-database

# 3. Sincronizar solo lo nuevo
lara sync-models
# Solo generará modelos para tablas nuevas

# 4. Reiniciar servidor
# Ctrl+C y uvicorn app.main:app --reload
```

---

## 📝 Configuración de .env

### SQLite (Desarrollo)
```env
DATABASE_URL=sqlite:///./app.db
```

### PostgreSQL
```env
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/nombre_db
```

### MySQL
```env
DATABASE_URL=mysql+pymysql://usuario:contraseña@localhost:3306/nombre_db
```

### SQL Server
```env
DATABASE_URL=mssql+pymssql://usuario:contraseña@localhost:1433/nombre_db
```

### MongoDB (Experimental)
```env
MONGODB_URL=mongodb://localhost:27017/nombre_db
```

### Variables Adicionales
```env
PROJECT_NAME=Mi API
SECRET_KEY=tu-clave-secreta-aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

---

## 🚀 Comandos de Ejecución

### Desarrollo
```bash
# Con auto-reload
uvicorn app.main:app --reload

# Con host y puerto específicos
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Con logs detallados
uvicorn app.main:app --reload --log-level debug
```

### Producción
```bash
# Con Gunicorn + Uvicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# Con múltiples workers
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## 🧪 Testing

```bash
# Ejecutar todos los tests
pytest

# Con verbose
pytest -v

# Con coverage
pytest --cov=app tests/

# Test específico
pytest tests/test_models.py

# Con output detallado
pytest -vv --tb=short
```

---

## 📦 Gestión de Dependencias

```bash
# Instalar dependencias
pip install -r requirements.txt

# Agregar nueva dependencia
pip install nombre-paquete
pip freeze > requirements.txt

# Dependencias de desarrollo
pip install -r requirements-dev.txt
```

### Dependencias Adicionales por BD

```bash
# PostgreSQL
pip install psycopg2-binary

# MySQL
pip install pymysql

# SQL Server
pip install pymssql

# MongoDB
pip install motor pymongo beanie
```

---

## 🔍 Debugging

### Ver estructura generada
```bash
# Listar archivos generados
find app -name "*.py" -type f

# Ver modelo generado
cat app/models/producto_model.py

# Ver schema generado
cat app/schemas/producto_schema.py

# Ver routes generadas
cat app/routes/producto_routes.py
```

### Verificar BD
```bash
# Con SQLite
sqlite3 app.db ".tables"

# Con psql
psql -h localhost -U usuario -d nombre_db -c "\dt"

# Con mycli (MySQL)
mycli -h localhost -u usuario nombre_db
```

### Logs de la aplicación
```bash
# Ver en tiempo real
uvicorn app.main:app --reload --log-level debug

# Redirigir a archivo
uvicorn app.main:app --reload > app.log 2>&1
```

---

## 🔧 Personalización Post-Generación

### Agregar validación personalizada
```python
# app/schemas/producto_schema.py
from pydantic import validator

class ProductoCreate(ProductoBase):
    @validator('precio')
    def precio_positivo(cls, v):
        if v <= 0:
            raise ValueError('El precio debe ser mayor a 0')
        return v
```

### Agregar endpoint personalizado
```python
# app/routes/producto_routes.py
@router.get("/destacados")
def get_destacados(db: Session = Depends(get_db)):
    return db.query(Producto).filter(Producto.destacado == True).all()
```

### Agregar lógica de negocio
```python
# app/controllers/producto_controller.py
@staticmethod
def aplicar_descuento(db: Session, id: int, porcentaje: float):
    producto = ProductoController.get_by_id(db, id)
    producto.precio = producto.precio * (1 - porcentaje/100)
    db.commit()
    return producto
```

---

## 📚 Recursos Útiles

### URLs Importantes
- **Docs interactivos**: http://localhost:8000/docs
- **Docs alternativos**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### Comandos de Ayuda
```bash
# Ayuda general
lara --help

# Ayuda de comando específico
lara create --help
lara get-database --help
lara sync-models --help
```

### Atajos Útiles
```bash
# Alias para desarrollo
alias laradev="uvicorn app.main:app --reload"
alias laratest="pytest -v"
alias laracov="pytest --cov=app tests/"

# Usar
laradev  # Iniciar servidor
laratest # Ejecutar tests
```

---

## 🎓 Tips y Trucos

1. **Usa SQLite para prototipado rápido** - No necesitas configurar servidor
2. **Genera primero, personaliza después** - No pierdas tiempo en boilerplate
3. **Lee /docs** - FastAPI genera documentación automática increíble
4. **Usa .env.example** - Para compartir config sin exponer credenciales
5. **Commit frecuente** - Lara inicializa git automáticamente
6. **Aprovecha el auto-reload** - uvicorn recarga cambios automáticamente
7. **Usa Rich para debug** - `from rich import print; print(objeto)`

---

## 🚨 Solución de Problemas Comunes

### "lara: command not found"
```bash
# Reinstalar
pip install -e .

# Verificar PATH
which lara
```

### "No se encontró .env"
```bash
# Crear desde ejemplo
cp .env.example .env
# Editar DATABASE_URL
```

### "Error al conectar a la BD"
```bash
# Verificar que el servidor esté corriendo
# Verificar credenciales en .env
# Instalar driver correcto (psycopg2, pymysql, etc)
```

### "Import error al ejecutar"
```bash
# Reinstalar dependencias
pip install -r requirements.txt

# Verificar que estás en el venv
which python
```

---

**¿Necesitas ayuda?**
- 📖 [README completo](README.md)
- 💡 [Ejemplos](EXAMPLES.md)
- 🔧 [Guía de instalación](INSTALL.md)
- 🐛 [Reportar issue](https://github.com/SoliDeoGloria123/Lara/issues)
