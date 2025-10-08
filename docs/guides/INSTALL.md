# 🚀 Guía de Instalación de Lara

## Instalación Local (Desarrollo)

### 1. Clonar el repositorio

```bash
git clone https://github.com/SoliDeoGloria123/Lara.git
cd Lara
```

### 2. Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate    # Windows
```

### 3. Instalar en modo desarrollo

```bash
pip install -e .
```

### 4. Verificar instalación

```bash
lara version
lara --help
```

## Instalación desde PyPI (Recomendado para usuarios)

Una vez publicado en PyPI:

```bash
pip install lara-cli
```

## Uso Rápido

### Crear un proyecto nuevo

```bash
lara create mi_proyecto
cd mi_proyecto
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### Configurar base de datos en .env

```env
# SQLite (desarrollo)
DATABASE_URL=sqlite:///./app.db

# PostgreSQL (producción)
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# MySQL
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/dbname
```

### Analizar base de datos existente

```bash
lara get-database
```

### Sincronizar modelos con la BD

```bash
lara sync-models
```

### Ejecutar la aplicación

```bash
uvicorn app.main:app --reload
```

Visita http://localhost:8000/docs para ver la documentación interactiva.

## Publicar en PyPI

### 1. Instalar herramientas

```bash
pip install build twine
```

### 2. Crear cuenta en PyPI

- Visita https://pypi.org/account/register/
- Verifica tu email

### 3. Construir el paquete

```bash
python -m build
```

### 4. Subir a PyPI

```bash
# Test PyPI primero (recomendado)
twine upload --repository testpypi dist/*

# PyPI real
twine upload dist/*
```

## Desarrollo

### Instalar dependencias de desarrollo

```bash
pip install -r requirements-dev.txt
```

### Ejecutar tests

```bash
pytest tests/ -v
```

### Formatear código

```bash
black lara/
ruff check lara/
```

### Generar coverage

```bash
pytest --cov=lara tests/
```

## Solución de Problemas

### Error: "No module named 'lara'"

Asegúrate de haber instalado el paquete:
```bash
pip install -e .
```

### Error: "DATABASE_URL no encontrada"

Asegúrate de tener un archivo `.env` en la raíz de tu proyecto con:
```env
DATABASE_URL=sqlite:///./app.db
```

### Error al conectar a la base de datos

Verifica que:
1. La URL de conexión sea correcta
2. El servidor de BD esté corriendo
3. Tengas los drivers instalados (psycopg2, pymysql, etc)

## Contribuir

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Soporte

- **GitHub Issues**: https://github.com/SoliDeoGloria123/Lara/issues
- **Documentation**: https://github.com/SoliDeoGloria123/Lara#readme
