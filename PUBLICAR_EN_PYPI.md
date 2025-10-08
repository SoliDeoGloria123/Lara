# 📦 Guía para Publicar Lara en PyPI

## 🎯 Prerequisitos

### 1. Crear cuenta en PyPI

1. Ve a: https://pypi.org/account/register/
2. Crea tu cuenta
3. Verifica tu email

### 2. Crear cuenta en TestPyPI (para pruebas)

1. Ve a: https://test.pypi.org/account/register/
2. Crea tu cuenta
3. Verifica tu email

### 3. Generar API Tokens

#### Para PyPI (producción):
1. Ve a: https://pypi.org/manage/account/token/
2. Click en "Add API token"
3. Token name: `lara-cli-token`
4. Scope: `Entire account` (o específico para lara-cli después de la primera subida)
5. **Copia el token** (pypi-AgE...) - ¡No lo perderás!

#### Para TestPyPI (pruebas):
1. Ve a: https://test.pypi.org/manage/account/token/
2. Mismo proceso
3. Guarda el token

### 4. Configurar tokens localmente

Crea el archivo `~/.pypirc`:

```bash
nano ~/.pypirc
```

Contenido:
```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmcC... # TU TOKEN DE PYPI

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-AgENdGVzdC5weXBpLm9yZ... # TU TOKEN DE TESTPYPI
```

Proteger el archivo:
```bash
chmod 600 ~/.pypirc
```

## 📋 Verificar que todo está listo

### 1. Verificar pyproject.toml

```bash
cd /home/juan/Lara
cat pyproject.toml
```

Verificar:
- ✅ `name = "lara-cli"` (debe ser único en PyPI)
- ✅ `version = "3.0.0"` (incrementar en cada release)
- ✅ `description` está completo
- ✅ `readme = "README.md"` existe
- ✅ `license = {text = "MIT"}`
- ✅ `authors` con tu info
- ✅ `dependencies` listadas

### 2. Verificar README.md

```bash
head -20 README.md
```

Debe tener:
- ✅ Título claro
- ✅ Descripción
- ✅ Badges
- ✅ Instalación
- ✅ Uso rápido

### 3. Verificar LICENSE

```bash
cat LICENSE
```

Debe existir y ser MIT.

### 4. Verificar estructura

```bash
tree -L 2 -I '__pycache__|*.pyc|venv'
```

Estructura correcta:
```
/home/juan/Lara/
├── lara/
│   ├── __init__.py
│   ├── __version__.py
│   ├── cli.py
│   ├── generators/
│   ├── inspectors/
│   ├── templates/
│   └── utils/
├── pyproject.toml
├── README.md
├── LICENSE
└── assets/
    └── logo.png
```

## 🔧 Instalar herramientas de build

```bash
pip install --upgrade pip
pip install --upgrade build twine
```

**Qué hace cada una:**
- `build`: Genera los archivos de distribución (wheel y sdist)
- `twine`: Sube los archivos a PyPI de forma segura

## 🧪 Publicar en TestPyPI (PRUEBA PRIMERO)

### 1. Limpiar builds anteriores

```bash
cd /home/juan/Lara
rm -rf dist/ build/ *.egg-info
```

### 2. Crear distribución

```bash
python -m build
```

Esto crea:
- `dist/lara_cli-3.0.0-py3-none-any.whl` (wheel)
- `dist/lara-cli-3.0.0.tar.gz` (source distribution)

### 3. Verificar el paquete

```bash
twine check dist/*
```

Debe decir: `PASSED`

### 4. Subir a TestPyPI

```bash
twine upload --repository testpypi dist/*
```

O si no configuraste `.pypirc`:
```bash
twine upload --repository-url https://test.pypi.org/legacy/ dist/* \
  --username __token__ \
  --password pypi-AgEN... # Tu token de TestPyPI
```

### 5. Probar instalación desde TestPyPI

```bash
# En un nuevo terminal o venv
python -m venv test_env
source test_env/bin/activate
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ lara-cli

# Probar
lara version
lara create test_project
```

Si funciona, **¡estás listo para PyPI real!** 🎉

## 🚀 Publicar en PyPI (PRODUCCIÓN)

### 1. Asegurarte que todo está actualizado

```bash
cd /home/juan/Lara
git status  # Debe estar limpio
git log -1  # Ver último commit
```

### 2. Limpiar y rebuild

```bash
rm -rf dist/ build/ *.egg-info
python -m build
twine check dist/*
```

### 3. ¡SUBIR A PYPI!

```bash
twine upload dist/*
```

O sin `.pypirc`:
```bash
twine upload dist/* --username __token__ --password pypi-AgEI... # Tu token de PyPI
```

### 4. Verificar en PyPI

Ir a: https://pypi.org/project/lara-cli/

¡Debe aparecer tu proyecto! 🎊

### 5. Probar instalación

```bash
# En un nuevo terminal
pip install lara-cli

lara version
# Debe mostrar: Lara CLI version 3.0.0
```

## 🎉 ¡PUBLICADO!

Tu paquete ahora está disponible para todo el mundo:

```bash
pip install lara-cli
```

## 📝 Para futuras actualizaciones

### 1. Incrementar versión

```bash
# Editar lara/__version__.py
__version__ = "3.0.1"  # o 3.1.0, 4.0.0, etc.

# Editar pyproject.toml
version = "3.0.1"
```

### 2. Commit y tag

```bash
git add .
git commit -m "bump: version 3.0.1"
git tag v3.0.1
git push origin Lara
git push origin v3.0.1
```

### 3. Rebuild y upload

```bash
rm -rf dist/ build/ *.egg-info
python -m build
twine check dist/*
twine upload dist/*
```

## 🔍 Verificar información del paquete

```bash
# Ver metadata
tar -xzf dist/lara-cli-3.0.0.tar.gz
cat lara-cli-3.0.0/PKG-INFO

# Ver contenido del wheel
unzip -l dist/lara_cli-3.0.0-py3-none-any.whl
```

## 🐛 Solución de Problemas

### Error: "Package already exists"

El nombre `lara-cli` ya está tomado en PyPI.

**Solución:**
```bash
# Cambiar nombre en pyproject.toml
name = "lara-fastapi-cli"  # o "lara-generator", "fastapi-lara", etc.
```

Luego rebuild y upload.

### Error: "Invalid credentials"

**Solución:**
1. Verificar que el token está correcto en `.pypirc`
2. El token debe empezar con `pypi-AgE...`
3. Usar `__token__` como username

### Error: "README not found"

**Solución:**
```bash
# Verificar que README.md existe
ls -la README.md

# Verificar en pyproject.toml
readme = "README.md"
```

### Error: "Invalid version"

**Solución:**
```bash
# Versión debe seguir PEP 440
# Válidas: 1.0.0, 1.0.0a1, 1.0.0b2, 1.0.0rc1
# Inválidas: v1.0.0, 1.0, 1.0.0-alpha
```

## 📊 Estadísticas

Después de publicar, puedes ver:

- **Descargas:** https://pypistats.org/packages/lara-cli
- **Página del proyecto:** https://pypi.org/project/lara-cli/
- **Historial de versiones:** https://pypi.org/project/lara-cli/#history

## 🎯 Checklist Final

Antes de `twine upload dist/*`:

- [ ] Versión incrementada en `__version__.py` y `pyproject.toml`
- [ ] README.md actualizado
- [ ] CHANGELOG o notas de versión
- [ ] Todo commiteado a git
- [ ] Tag creado: `git tag v3.0.0`
- [ ] Probado en TestPyPI
- [ ] `twine check dist/*` pasa
- [ ] Logo actualizado en assets/logo.png

## 🔐 Seguridad

**NUNCA subas a git:**
- Tokens de PyPI
- Archivo `.pypirc`
- Variables de entorno con tokens

Agregar a `.gitignore`:
```
.pypirc
*.token
.env.pypi
```

## 📚 Referencias

- PyPI: https://pypi.org/
- TestPyPI: https://test.pypi.org/
- Guía oficial: https://packaging.python.org/tutorials/packaging-projects/
- Twine docs: https://twine.readthedocs.io/
- PEP 517/518: https://peps.python.org/pep-0517/

---

**¡Buena suerte con la publicación!** 🚀

Si tienes problemas, revisa esta guía paso a paso.
