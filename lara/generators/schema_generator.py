"""Generador de schemas Pydantic"""
from pathlib import Path
from jinja2 import Environment, PackageLoader, select_autoescape
from typing import Dict, List

from lara.utils.file_utils import write_file, update_init_file
from lara.utils.string_utils import to_pascal_case
from lara.core.constants import DATETIME_COLUMNS


class SchemaGenerator:
    """Genera schemas Pydantic para validación"""
    
    def __init__(self, project_path: Path = None):
        """
        Inicializa el generador de schemas
        
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
    
    def generate(self, table: Dict) -> Path:
        """
        Genera schemas Pydantic (Create, Update, Response)
        
        Args:
            table: Diccionario con información de la tabla
        
        Returns:
            Path al archivo generado
        """
        table_name = table['name']
        class_name = to_pascal_case(table_name)
        
        # Preparar campos
        fields = self._prepare_fields(table['columns'])
        
        # Detectar si es tabla de autenticación
        is_auth_table = self._is_auth_table(table)
        
        # Detectar campos especiales
        has_timestamps = any(
            col['name'] in DATETIME_COLUMNS 
            for col in table['columns']
        )
        
        # Renderizar template
        template = self.env.get_template('schemas/pydantic_schema.py.jinja')
        content = template.render(
            class_name=class_name,
            table_name=table_name,
            fields=fields,
            is_auth_table=is_auth_table,
            has_timestamps=has_timestamps
        )
        
        # Guardar archivo
        output_path = self.project_path / "app" / "schemas" / f"{table_name}_schema.py"
        write_file(output_path, content)
        
        # Actualizar __init__.py
        init_path = self.project_path / "app" / "schemas" / "__init__.py"
        update_init_file(init_path, f"{table_name}_schema")
        
        return output_path
    
    def _prepare_fields(self, columns: List[Dict]) -> List[Dict]:
        """Prepara campos para los schemas"""
        fields = []
        
        for col in columns:
            # Saltar campos autogenerados en Create
            skip_in_create = col.get('primary_key') and col.get('autoincrement')
            skip_in_create = skip_in_create or col['name'] in ['created_at', 'updated_at']
            
            field_data = {
                'name': col['name'],
                'python_type': col.get('python_type', 'str'),
                'nullable': col.get('nullable', True),
                'primary_key': col.get('primary_key', False),
                'skip_in_create': skip_in_create,
                'max_length': col.get('length'),
                'is_email': 'email' in col['name'].lower(),
                'is_password': 'password' in col['name'].lower(),
                'is_timestamp': col['name'] in DATETIME_COLUMNS,
                'has_foreign_key': col.get('foreign_key') is not None
            }
            
            # Validaciones especiales
            if field_data['is_email']:
                field_data['validator'] = 'EmailStr'
            
            fields.append(field_data)
        
        return fields
    
    def _is_auth_table(self, table: Dict) -> bool:
        """Detecta si es una tabla de autenticación"""
        auth_names = ['users', 'user', 'usuarios', 'usuario']
        if table['name'].lower() in auth_names:
            return True
        
        password_cols = ['password', 'hashed_password', 'passwd']
        column_names = [col['name'].lower() for col in table['columns']]
        return any(pwd in column_names for pwd in password_cols)
