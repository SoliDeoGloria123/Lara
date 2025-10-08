"""Generador de modelos SQLAlchemy y Beanie"""
from pathlib import Path
from jinja2 import Environment, PackageLoader, select_autoescape
from typing import Dict, List, Set

from lara.utils.file_utils import write_file, update_init_file
from lara.utils.string_utils import to_pascal_case, to_snake_case
from lara.core.constants import DATETIME_COLUMNS


class ModelGenerator:
    """Genera modelos para bases de datos"""
    
    def __init__(self, project_path: Path = None, db_type: str = 'sql'):
        """
        Inicializa el generador de modelos
        
        Args:
            project_path: Ruta al proyecto
            db_type: Tipo de base de datos ('sql' o 'mongodb')
        """
        self.project_path = project_path or Path.cwd()
        self.db_type = db_type
        
        # Configurar Jinja2
        self.env = Environment(
            loader=PackageLoader('lara', 'templates'),
            autoescape=select_autoescape(),
            trim_blocks=True,
            lstrip_blocks=True
        )
    
    def generate(self, table: Dict) -> Path:
        """
        Genera un modelo a partir de metadata de tabla
        
        Args:
            table: Diccionario con información de la tabla
        
        Returns:
            Path al archivo generado
        """
        if self.db_type == 'sql':
            return self._generate_sql_model(table)
        else:
            return self._generate_mongo_model(table)
    
    def _generate_sql_model(self, table: Dict) -> Path:
        """Genera un modelo SQLAlchemy"""
        table_name = table['name']
        class_name = to_pascal_case(table_name)
        
        # Detectar imports necesarios
        imports = self._detect_imports(table)
        
        # Preparar columnas
        columns = self._prepare_columns(table['columns'])
        
        # Preparar relaciones
        relationships = self._prepare_relationships(table)
        
        # Detectar si tiene timestamps
        has_timestamps = any(
            col['name'] in DATETIME_COLUMNS 
            for col in table['columns']
        )
        
        # Detectar si es tabla de autenticación
        is_auth_table = self._is_auth_table(table)
        
        # Renderizar template
        template = self.env.get_template('models/sql_model.py.jinja')
        content = template.render(
            class_name=class_name,
            table_name=table_name,
            columns=columns,
            relationships=relationships,
            imports=sorted(imports),
            has_timestamps=has_timestamps,
            is_auth_table=is_auth_table
        )
        
        # Guardar archivo
        output_path = self.project_path / "app" / "models" / f"{table_name}_model.py"
        write_file(output_path, content)
        
        # Actualizar __init__.py
        init_path = self.project_path / "app" / "models" / "__init__.py"
        update_init_file(init_path, f"{table_name}_model")
        
        return output_path
    
    def _generate_mongo_model(self, table: Dict) -> Path:
        """Genera un modelo Beanie para MongoDB"""
        collection_name = table['name']
        class_name = to_pascal_case(collection_name)
        
        # Preparar campos
        fields = []
        for col in table['columns']:
            if col['name'] == '_id':
                continue  # Beanie maneja _id automáticamente
            
            fields.append({
                'name': col['name'],
                'type': col.get('python_type', 'str'),
                'optional': col['nullable']
            })
        
        # Renderizar template
        template = self.env.get_template('models/mongo_model.py.jinja')
        content = template.render(
            class_name=class_name,
            collection_name=collection_name,
            fields=fields
        )
        
        # Guardar archivo
        output_path = self.project_path / "app" / "models" / f"{collection_name}_model.py"
        write_file(output_path, content)
        
        return output_path
    
    def _detect_imports(self, table: Dict) -> Set[str]:
        """Detecta los imports necesarios para el modelo"""
        imports = {'Column', 'Integer'}
        
        for col in table['columns']:
            sqlalchemy_type = col.get('sqlalchemy_type', 'String')
            imports.add(sqlalchemy_type)
            
            if col.get('foreign_key'):
                imports.add('ForeignKey')
        
        # Si hay relaciones, importar relationship
        if table.get('relationships'):
            imports.add('relationship')
        
        return imports
    
    def _prepare_columns(self, columns: List[Dict]) -> List[Dict]:
        """Prepara columnas para el template"""
        prepared = []
        
        for col in columns:
            col_data = {
                'name': col['name'],
                'type': col.get('sqlalchemy_type', 'String'),
                'length': col.get('length'),
                'primary_key': col.get('primary_key', False),
                'nullable': col.get('nullable', True),
                'unique': col.get('unique', False),
                'index': col.get('index', False) or col.get('primary_key', False),
                'foreign_key': col.get('foreign_key'),
                'default': col.get('default'),
                'autoincrement': col.get('autoincrement', False)
            }
            
            # Defaults especiales para timestamps
            if col['name'] == 'created_at':
                col_data['has_default'] = True
                col_data['default_value'] = 'datetime.utcnow'
            elif col['name'] == 'updated_at':
                col_data['has_default'] = True
                col_data['default_value'] = 'datetime.utcnow'
                col_data['onupdate'] = 'datetime.utcnow'
            
            prepared.append(col_data)
        
        return prepared
    
    def _prepare_relationships(self, table: Dict) -> List[Dict]:
        """Prepara relaciones para el template"""
        relationships = []
        
        for rel in table.get('relationships', []):
            target_table = rel['target_table']
            target_class = to_pascal_case(target_table)
            
            relationships.append({
                'name': to_snake_case(target_table),
                'target_class': target_class,
                'back_populates': table['name'],
                'type': rel.get('type', 'many_to_one')
            })
        
        return relationships
    
    def _is_auth_table(self, table: Dict) -> bool:
        """Detecta si es una tabla de autenticación"""
        auth_names = ['users', 'user', 'usuarios', 'usuario']
        if table['name'].lower() in auth_names:
            return True
        
        # Verificar si tiene columna de password
        password_cols = ['password', 'hashed_password', 'passwd', 'pwd']
        column_names = [col['name'].lower() for col in table['columns']]
        return any(pwd in column_names for pwd in password_cols)
