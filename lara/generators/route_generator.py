"""Generador de routes FastAPI"""
from pathlib import Path
from jinja2 import Environment, PackageLoader, select_autoescape
from typing import Dict, List

from lara.utils.file_utils import write_file, update_init_file, insert_router_registration
from lara.utils.string_utils import to_pascal_case, pluralize


class RouteGenerator:
    """Genera routes FastAPI con endpoints CRUD"""
    
    def __init__(self, project_path: Path = None):
        """
        Inicializa el generador de routes
        
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
        Genera routes con endpoints CRUD
        
        Args:
            table: Diccionario con información de la tabla
            is_auth: Si es un router de autenticación
        
        Returns:
            Path al archivo generado
        """
        table_name = table['name']
        class_name = to_pascal_case(table_name)
        
        # Seleccionar template
        if is_auth:
            template = self.env.get_template('routes/auth_routes.py.jinja')
        else:
            template = self.env.get_template('routes/crud_routes.py.jinja')
        
        # Renderizar
        content = template.render(
            class_name=class_name,
            table_name=table_name,
            is_auth=is_auth
        )
        
        # Guardar archivo
        output_path = self.project_path / "app" / "routes" / f"{table_name}_routes.py"
        write_file(output_path, content)
        
        # Actualizar __init__.py
        init_path = self.project_path / "app" / "routes" / "__init__.py"
        update_init_file(init_path, f"{table_name}_routes")
        
        return output_path
    
    def update_main(self, tables: List[Dict]):
        """
        Actualiza main.py para registrar los routers generados
        
        Args:
            tables: Lista de tablas para las que se generaron routers
        """
        main_path = self.project_path / "app" / "main.py"
        
        if not main_path.exists():
            return
        
        for table in tables:
            table_name = table['name']
            router_name = f"{table_name}_routes"
            
            # Determinar prefijo y tag
            prefix = f"/api/{pluralize(table_name)}"
            tag = table_name
            
            # Insertar registro
            insert_router_registration(main_path, router_name, prefix, tag)
