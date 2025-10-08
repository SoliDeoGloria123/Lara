# 🚀 Guía para Publicar Lara en PyPI

## Preparación Previa

### 1. Crear Cuenta en PyPI

1. Visita https://pypi.org/account/register/
2. Completa el formulario de registro
3. Verifica tu email
4. (Opcional) Configura 2FA para mayor seguridad

### 2. Crear Cuenta en Test PyPI (Recomendado)

1. Visita https://test.pypi.org/account/register/
2. Crea una cuenta separada
3. Úsala para probar antes de publicar en PyPI real

### 3. Instalar Herramientas

```bash
pip install --upgrade build twine
```

## Proceso de Publicación

### Paso 1: Verificar el Proyecto

```bash
cd /home/juan/Lara

# Verificar que todo funciona
lara version
lara --help

# Ejecutar tests
pytest tests/ -v

# Verificar que setup.py está correcto
python setup.py check
```

### Paso 2: Limpiar Builds Anteriores

```bash
rm -rf build/ dist/ *.egg-info
```

### Paso 3: Construir el Paquete

```bash
python -m build
```

Esto generará:
- `dist/lara-cli-0.1.0.tar.gz` (código fuente)
- `dist/lara_cli-0.1.0-py3-none-any.whl` (wheel)

### Paso 4: Verificar el Paquete

```bash
twine check dist/*
```

Debe mostrar:
```
Checking dist/lara-cli-0.1.0.tar.gz: PASSED
Checking dist/lara_cli-0.1.0-py3-none-any.whl: PASSED
```

### Paso 5: Probar en Test PyPI (RECOMENDADO)

```bash
twine upload --repository testpypi dist/*
```

Te pedirá:
- Username: tu_usuario_testpypi
- Password: tu_contraseña_testpypi

### Paso 6: Instalar desde Test PyPI

```bash
# En un nuevo entorno virtual
python -m venv test_env
source test_env/bin/activate

# Instalar desde Test PyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ lara-cli

# Probar
lara version
lara --help
```

### Paso 7: Publicar en PyPI Real

Si todo funciona en Test PyPI:

```bash
twine upload dist/*
```

Te pedirá:
- Username: tu_usuario_pypi
- Password: tu_contraseña_pypi

### Paso 8: Verificar Publicación

1. Visita https://pypi.org/project/lara-cli/
2. Verifica que la página se ve correctamente
3. Prueba la instalación:

```bash
pip install lara-cli
lara version
```

## Configuración de Tokens (Recomendado)

En lugar de usar username/password cada vez, configura tokens:

### 1. Crear Token en PyPI

1. Ve a https://pypi.org/manage/account/
2. Scroll hasta "API tokens"
3. Click "Add API token"
4. Scope: "Entire account" o "Project: lara-cli"
5. Copia el token (empieza con `pypi-`)

### 2. Configurar .pypirc

Crea/edita `~/.pypirc`:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-TU_TOKEN_AQUI

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-TU_TOKEN_TEST_AQUI
```

Permisos:
```bash
chmod 600 ~/.pypirc
```

Ahora puedes subir sin password:
```bash
twine upload dist/*
```

## Script Automatizado

Crea `publish.sh`:

```bash
#!/bin/bash

set -e

echo "🧹 Limpiando builds anteriores..."
rm -rf build/ dist/ *.egg-info

echo "🔍 Verificando código..."
python setup.py check

echo "📦 Construyendo paquete..."
python -m build

echo "✅ Verificando paquete..."
twine check dist/*

echo ""
echo "¿Deseas subir a Test PyPI primero? (s/n)"
read -r response
if [[ "$response" =~ ^([sS][íi]?)$ ]]; then
    echo "📤 Subiendo a Test PyPI..."
    twine upload --repository testpypi dist/*
    echo ""
    echo "✅ Publicado en Test PyPI!"
    echo "Prueba: pip install --index-url https://test.pypi.org/simple/ lara-cli"
    echo ""
    echo "¿Continuar con PyPI real? (s/n)"
    read -r response2
    if [[ ! "$response2" =~ ^([sS][íi]?)$ ]]; then
        exit 0
    fi
fi

echo "📤 Subiendo a PyPI..."
twine upload dist/*

echo ""
echo "🎉 ¡Publicado exitosamente!"
echo "Instala con: pip install lara-cli"
```

Hacerlo ejecutable:
```bash
chmod +x publish.sh
```

Usar:
```bash
./publish.sh
```

## Actualizar Versiones

### 1. Actualizar Versión

Edita `lara/__version__.py`:
```python
__version__ = "0.1.1"  # o la versión que corresponda
```

También actualiza en:
- `setup.py`
- `pyproject.toml`

### 2. Crear Tag de Git

```bash
git add .
git commit -m "Release v0.1.1"
git tag v0.1.1
git push origin main
git push origin v0.1.1
```

### 3. Publicar Nueva Versión

```bash
./publish.sh
```

## Versionado Semántico

Sigue [Semantic Versioning](https://semver.org/):

- **MAJOR** (1.0.0): Cambios incompatibles con versiones anteriores
- **MINOR** (0.1.0): Nuevas funcionalidades compatibles
- **PATCH** (0.0.1): Bug fixes

Ejemplos:
- `0.1.0` → Primera versión pública
- `0.1.1` → Bug fix
- `0.2.0` → Nueva funcionalidad (comando nuevo)
- `1.0.0` → Primera versión estable

## Mantener el Proyecto

### Actualizar README en PyPI

El README se actualiza automáticamente desde `README.md` al subir nueva versión.

### Responder Issues

Monitorea https://github.com/SoliDeoGloria123/Lara/issues

### Releases en GitHub

1. Ve a https://github.com/SoliDeoGloria123/Lara/releases
2. Click "Draft a new release"
3. Selecciona el tag (v0.1.0)
4. Título: "Lara v0.1.0 - Initial Release"
5. Describe cambios
6. Adjunta archivos de dist/ si quieres

## Checklist de Publicación

Antes de publicar, verifica:

- [ ] Todos los tests pasan
- [ ] README.md está actualizado
- [ ] CHANGELOG.md lista cambios (opcional pero recomendado)
- [ ] Versión actualizada en `__version__.py`, `setup.py`, `pyproject.toml`
- [ ] Licencia correcta (LICENSE)
- [ ] .gitignore excluye archivos sensibles
- [ ] Dependencias correctas en requirements.txt
- [ ] Code coverage > 70% (opcional)
- [ ] Documentación completa
- [ ] Ejemplos funcionan

## Estadísticas Post-Publicación

Monitorea:
- **Downloads**: https://pypistats.org/packages/lara-cli
- **Stars**: https://github.com/SoliDeoGloria123/Lara/stargazers
- **Issues**: https://github.com/SoliDeoGloria123/Lara/issues

## Promoción

Una vez publicado:

1. **Twitter/X**: Anuncia el lanzamiento
2. **Reddit**: r/Python, r/FastAPI
3. **Dev.to**: Escribe un artículo
4. **Hacker News**: Submit
5. **LinkedIn**: Post profesional

## Solución de Problemas

### Error: "403 Forbidden"
- Verifica credenciales
- Asegúrate de que el paquete no existe ya con ese nombre

### Error: "400 Bad Request"
- Verifica que setup.py y pyproject.toml están correctos
- Verifica que README.md es válido Markdown

### Error: "Filename already exists"
- Ya subiste esa versión
- Incrementa el número de versión

### Warning: "long_description is not formatted correctly"
- Verifica sintaxis de README.md
- Usa `twine check dist/*` antes de subir

## Comandos Útiles

```bash
# Ver paquetes instalados
pip list | grep lara

# Desinstalar
pip uninstall lara-cli

# Instalar versión específica
pip install lara-cli==0.1.0

# Ver información del paquete
pip show lara-cli

# Ver archivos instalados
pip show -f lara-cli
```

## Recursos

- **PyPI**: https://pypi.org/
- **Test PyPI**: https://test.pypi.org/
- **Packaging Guide**: https://packaging.python.org/
- **Twine Docs**: https://twine.readthedocs.io/
- **Semantic Versioning**: https://semver.org/

---

**¡Listo para publicar! 🚀**

Una vez publicado, cualquier persona podrá instalar Lara con:
```bash
pip install lara-cli
```

Y usarlo inmediatamente:
```bash
lara create mi_proyecto
```
