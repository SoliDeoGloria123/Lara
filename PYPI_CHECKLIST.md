# 🚀 Checklist Rápido - Publicar en PyPI

## ✅ Lista de Verificación

### Antes de empezar:
- [ ] Cuenta en PyPI creada
- [ ] Email verificado
- [ ] Token de PyPI copiado

### Durante la configuración:
- [ ] Archivo `~/.pypirc` creado
- [ ] Token pegado correctamente
- [ ] Permisos configurados (chmod 600)

### Al publicar:
- [ ] Build creado sin errores
- [ ] Check de twine pasado
- [ ] Upload exitoso

### Después de publicar:
- [ ] Verificar en https://pypi.org/project/lara-cli/
- [ ] Probar instalación: `pip install lara-cli`
- [ ] Verificar versión: `lara version`

---

## 🔗 Links Importantes

- **Crear cuenta**: https://pypi.org/account/register/
- **Obtener token**: https://pypi.org/manage/account/token/
- **Ver proyecto**: https://pypi.org/project/lara-cli/

---

## 📝 Comandos Rápidos

```bash
# Configurar token
nano ~/.pypirc
chmod 600 ~/.pypirc

# Publicar
cd /home/juan/Lara
./publish.sh prod

# O manual:
python -m build
twine check dist/*
twine upload dist/*

# Verificar
pip install lara-cli
lara version
```

---

## ⚠️ Errores Comunes

**"The name 'lara-cli' already exists"**
→ Cambiar nombre en `pyproject.toml`

**"Invalid authentication"**
→ Revisar token en `~/.pypirc`

**"Version already exists"**
→ Incrementar versión en `pyproject.toml` y `lara/__version__.py`

---

## 🔄 Para Actualizar Después

1. Editar versión:
   ```bash
   # lara/__version__.py
   __version__ = "3.0.1"
   
   # pyproject.toml
   version = "3.0.1"
   ```

2. Commit y tag:
   ```bash
   git add .
   git commit -m "bump: version 3.0.1"
   git tag v3.0.1
   git push origin Lara --tags
   ```

3. Rebuild y publicar:
   ```bash
   rm -rf dist/ build/ *.egg-info
   python -m build
   twine upload dist/*
   ```

---

**¡Éxito!** 🎉
