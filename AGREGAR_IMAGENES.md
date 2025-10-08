# 📸 Cómo agregar tus imágenes al proyecto

## Imágenes necesarias:

### 1. Logo del proyecto
**Archivo:** `assets/logo.png`
**Estado:** ✅ Ya existe (placeholder)
**Acción:** Reemplazar con el logo oficial (la imagen "F" blanca)

```bash
# Si tienes el logo en tu computadora:
cp /ruta/al/logo.png /home/juan/Lara/assets/logo.png
```

### 2. Foto del autor
**Archivo:** `assets/author.jpg`
**Estado:** ⚠️ Pendiente
**Acción:** Agregar tu foto

```bash
# Guardar tu foto:
cp /ruta/a/tu/foto.jpg /home/juan/Lara/assets/author.jpg
```

## 🎨 Recomendaciones

### Para el logo (logo.png):
- Formato: PNG con fondo transparente
- Tamaño: 300x300 px o similar
- El logo se muestra en 120px de ancho en el README

### Para la foto del autor (author.jpg):
- Formato: JPG o PNG
- Tamaño: 300x300 px o 500x500 px
- La foto se muestra en 150px de ancho
- Se verá redonda (círculo) automáticamente

## 📋 Después de agregar las imágenes

```bash
cd /home/juan/Lara

# Ver las imágenes
ls -lh assets/

# Commit
git add assets/
git commit -m "feat: Agregar logo oficial y foto del autor"
git push origin Lara
```

## 🖼️ Dónde aparecerán

**Logo (`assets/logo.png`):**
- ✓ README.md principal (parte superior)
- ✓ PyPI (cuando publiques)
- ✓ GitHub (en la página del repositorio)

**Foto del autor (`assets/author.jpg`):**
- ✓ README.md (sección Créditos)
- ✓ Muestra quién creó Lara

## ✅ Verificar que se vean bien

Después de agregarlas, abre el README en GitHub o VSCode para verificar:

```bash
# Ver en VSCode
code README.md

# O push y ver en GitHub
git push origin Lara
# Luego ir a: https://github.com/SoliDeoGloria123/Lara
```
