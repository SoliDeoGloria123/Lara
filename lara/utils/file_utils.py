"""Utilidades para manejo de archivos"""
from pathlib import Path
from typing import Optional
import re


def ensure_directory(path: Path) -> None:
    """
    Asegura que un directorio exista, creándolo si es necesario
    
    Args:
        path: Ruta al directorio
    """
    path.mkdir(parents=True, exist_ok=True)


def write_file(path: Path, content: str) -> None:
    """
    Escribe contenido en un archivo, creando directorios si es necesario
    
    Args:
        path: Ruta al archivo
        content: Contenido a escribir
    """
    ensure_directory(path.parent)
    path.write_text(content, encoding='utf-8')


def read_file(path: Path) -> Optional[str]:
    """
    Lee el contenido de un archivo
    
    Args:
        path: Ruta al archivo
    
    Returns:
        Contenido del archivo o None si no existe
    """
    if not path.exists():
        return None
    return path.read_text(encoding='utf-8')


def append_to_file(path: Path, content: str) -> None:
    """
    Agrega contenido al final de un archivo
    
    Args:
        path: Ruta al archivo
        content: Contenido a agregar
    """
    existing_content = read_file(path) or ""
    write_file(path, existing_content + content)


def insert_import(file_path: Path, import_line: str) -> None:
    """
    Inserta un import en un archivo Python si no existe
    
    Args:
        file_path: Ruta al archivo Python
        import_line: Línea de import a insertar
    """
    content = read_file(file_path)
    if not content:
        return
    
    # Verificar si el import ya existe
    if import_line.strip() in content:
        return
    
    # Encontrar la posición después de los imports existentes
    lines = content.split('\n')
    insert_position = 0
    
    for i, line in enumerate(lines):
        if line.strip().startswith(('import ', 'from ')):
            insert_position = i + 1
        elif line.strip() and not line.strip().startswith('#'):
            break
    
    # Insertar el nuevo import
    lines.insert(insert_position, import_line)
    write_file(file_path, '\n'.join(lines))


def insert_router_registration(main_path: Path, router_name: str, prefix: str, tag: str) -> None:
    """
    Inserta el registro de un router en main.py
    
    Args:
        main_path: Ruta a main.py
        router_name: Nombre del módulo del router
        prefix: Prefijo de la ruta
        tag: Tag para la documentación
    """
    content = read_file(main_path)
    if not content:
        return
    
    # Import statement
    import_line = f"from app.routes import {router_name}"
    
    # Router registration
    registration_line = f'app.include_router({router_name}.router, prefix="{prefix}", tags=["{tag}"])'
    
    # Verificar si ya existe
    if import_line in content or registration_line in content:
        return
    
    lines = content.split('\n')
    
    # Insertar import después de otros imports de routes
    import_inserted = False
    for i, line in enumerate(lines):
        if 'from app.routes import' in line:
            lines.insert(i + 1, import_line)
            import_inserted = True
            break
    
    if not import_inserted:
        # Buscar después de imports generales
        for i, line in enumerate(lines):
            if line.startswith('app = FastAPI'):
                lines.insert(i, import_line)
                lines.insert(i, '')
                break
    
    # Insertar registro después de otros registros de routers
    registration_inserted = False
    for i, line in enumerate(lines):
        if 'app.include_router' in line:
            # Insertar después del último router
            j = i
            while j < len(lines) and ('app.include_router' in lines[j] or lines[j].strip() == ''):
                j += 1
            lines.insert(j, registration_line)
            registration_inserted = True
            break
    
    if not registration_inserted:
        # Buscar antes de @app.on_event o @app.get
        for i, line in enumerate(lines):
            if line.startswith('@app.'):
                lines.insert(i, '')
                lines.insert(i, registration_line)
                break
    
    write_file(main_path, '\n'.join(lines))


def update_init_file(init_path: Path, module_name: str) -> None:
    """
    Actualiza __init__.py para incluir un nuevo módulo
    
    Args:
        init_path: Ruta a __init__.py
        module_name: Nombre del módulo a importar
    """
    ensure_directory(init_path.parent)
    
    content = read_file(init_path) or ""
    
    if not content or content.strip() == "":
        # Crear nuevo __init__.py
        content = f'"""{init_path.parent.name} module"""\n\n'
    
    # Agregar import si no existe
    import_line = f"from .{module_name} import *\n"
    if import_line.strip() not in content:
        content += import_line
    
    write_file(init_path, content)
