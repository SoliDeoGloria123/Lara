"""Generador de controllers con lógica CRUD"""
from pathlib import Path
from jinja2 import Environment, PackageLoader, select_autoescape
from typing import Dict

from lara.utils.file_utils import write_file, update_init_file
from lara.utils.string_utils import to_pascal_case


class ControllerGenerator:
    """Genera controllers con operaciones CRUD"""
    
    def __init__(self, project_path: Path = None):
        """
        Inicializa el generador de controllers
        
        Args:
            project_path: Ruta al proyecto
        """
        self.project_path = project_path or Path.cwd()
        
        # Configurar Jinja2
        self.env = Environment(
            loader=PackageLoader('lara', 'templates'),
            autoescape=select_autoescape(),
            trim_blocks=True,
            lstrip_blocks=True
        )
    
    def generate(self, table: Dict, is_auth: bool = False) -> Path:
        """
        Genera un controller con CRUD completo
        
        Args:
            table: Diccionario con información de la tabla
            is_auth: Si es un controller de autenticación
        
        Returns:
            Path al archivo generado
        """
        table_name = table['name']
        class_name = to_pascal_case(table_name)
        
        # Seleccionar template
        if is_auth:
            template = self.env.get_template('controllers/auth_controller.py.jinja')
        else:
            template = self.env.get_template('controllers/crud_controller.py.jinja')
        
        # Renderizar
        content = template.render(
            class_name=class_name,
            table_name=table_name,
            model_name=f"{class_name}",
            is_auth=is_auth
        )
        
        # Guardar archivo
        output_path = self.project_path / "app" / "controllers" / f"{table_name}_controller.py"
        write_file(output_path, content)
        
        # Actualizar __init__.py
        init_path = self.project_path / "app" / "controllers" / "__init__.py"
        update_init_file(init_path, f"{table_name}_controller")
        
        return output_path
