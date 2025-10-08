"""Inspector para bases de datos SQL con soporte SQL Server Management Studio"""
from sqlalchemy import create_engine, inspect, MetaData, text
from sqlalchemy.engine import Inspector
from typing import List, Dict, Optional
import os
import urllib.parse
from pathlib import Path
from dotenv import load_dotenv

from lara.inspectors.base_inspector import BaseInspector
from lara.core.constants import SQL_TO_SQLALCHEMY, SQL_TO_PYTHON
from lara.utils.string_utils import extract_length_from_type


class SQLInspector(BaseInspector):
    """Inspector para bases de datos SQL (SQL Server, PostgreSQL, MySQL, SQLite)"""
    
    def __init__(self, database_url: Optional[str] = None, project_path: Optional[Path] = None):
        """
        Inicializa el inspector SQL
        
        Args:
            database_url: URL de conexión a la base de datos (formato SQLAlchemy o SQL Server Management Studio)
            project_path: Ruta al proyecto (para buscar .env y modelos)
        """
        self.project_path = project_path or Path.cwd()
        
        # Cargar .env si existe
        env_path = self.project_path / ".env"
        if env_path.exists():
            load_dotenv(env_path)
        
        # Obtener URL de la base de datos
        raw_url = database_url or os.getenv("DATABASE_URL")
        
        if not raw_url:
            raise ValueError(
                "No se encontró DATABASE_URL. "
                "Proporciona database_url o crea un archivo .env con DATABASE_URL"
            )
        
        # Convertir formato SQL Server Management Studio a SQLAlchemy si es necesario
        self.database_url = self._normalize_connection_string(raw_url)
        
        self.engine = None
        self.inspector: Optional[Inspector] = None
        self.dialect = self._detect_dialect(self.database_url)
    
    def _normalize_connection_string(self, connection_string: str) -> str:
        """
        Convierte connection string de SQL Server Management Studio a formato SQLAlchemy
        
        Ejemplos:
        - SSMS: "Data Source=localhost\SQLEXPRESS;Initial Catalog=master;User ID=sa;Password=pass123"
        - SQLAlchemy: "mssql+pyodbc://sa:pass123@localhost\SQLEXPRESS/master?driver=ODBC+Driver+17+for+SQL+Server"
        """
        # Si ya está en formato SQLAlchemy, devolverlo tal cual
        if '://' in connection_string:
            return connection_string
        
        # Es formato SSMS, convertir a SQLAlchemy
        parts = {}
        for part in connection_string.split(';'):
            if '=' in part:
                key, value = part.split('=', 1)
                parts[key.strip()] = value.strip()
        
        # Extraer componentes
        server = parts.get('Data Source', 'localhost')
        database = parts.get('Initial Catalog', 'master')
        user = parts.get('User ID', 'sa')
        password = parts.get('Password', '')
        
        # Construir URL de SQLAlchemy
        import urllib.parse
        password_encoded = urllib.parse.quote_plus(password)
        
        # Configurar driver y parámetros adicionales
        driver = "ODBC+Driver+17+for+SQL+Server"
        trust_cert = "yes" if "Trust Server Certificate=True" in connection_string else "no"
        
        url = (
            f"mssql+pyodbc://{user}:{password_encoded}@{server}/{database}"
            f"?driver={driver}&TrustServerCertificate={trust_cert}"
        )
        
        return url
    
    def _detect_dialect(self, url: str) -> str:
        """Detecta el tipo de base de datos desde la URL"""
        if url.startswith('sqlite'):
            return 'sqlite'
        elif url.startswith('postgresql'):
            return 'postgresql'
        elif url.startswith('mysql'):
            return 'mysql'
        elif url.startswith('mssql'):
            return 'mssql'
        else:
            return 'unknown'
    
    def connect(self) -> bool:
        """Establece conexión con la base de datos"""
        try:
            connect_args = {}
            if "sqlite" in self.database_url:
                connect_args = {"check_same_thread": False}
            
            self.engine = create_engine(self.database_url, connect_args=connect_args, echo=False)
            self.inspector = inspect(self.engine)
            
            # Test de conexión
            with self.engine.connect():
                pass
            
            return True
        except Exception as e:
            error_msg = str(e)
            
            # Mensajes de error más útiles
            if "pyodbc" in error_msg:
                raise ConnectionError(
                    f"Error al conectar con SQL Server: {e}\n\n"
                    "Asegúrate de tener instalado pyodbc y el driver ODBC:\n"
                    "  pip install pyodbc\n"
                    "  Descarga: https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server"
                )
            elif "psycopg2" in error_msg:
                raise ConnectionError(
                    f"Error al conectar con PostgreSQL: {e}\n\n"
                    "Instala el driver de PostgreSQL:\n"
                    "  pip install psycopg2-binary"
                )
            elif "pymysql" in error_msg or "MySQLdb" in error_msg:
                raise ConnectionError(
                    f"Error al conectar con MySQL: {e}\n\n"
                    "Instala el driver de MySQL:\n"
                    "  pip install pymysql"
                )
            else:
                raise ConnectionError(f"Error al conectar a la base de datos: {e}")
    
    def get_database_info(self) -> Dict:
        """Obtiene información sobre la base de datos conectada"""
        if not self.inspector:
            self.connect()
        
        # Parsear URL para obtener info
        url_parts = self.database_url.split('://')
        dialect = url_parts[0]
        
        db_info = {
            'type': dialect,
            'url': self.database_url
        }
        
        # Extraer host y database si no es SQLite
        if dialect != 'sqlite':
            try:
                rest = url_parts[1]
                if '@' in rest:
                    _, location = rest.split('@')
                    if '/' in location:
                        host, database = location.split('/')
                        db_info['host'] = host
                        db_info['database'] = database.split('?')[0]
            except:
                pass
        else:
            # SQLite: extraer nombre de archivo
            db_info['database'] = url_parts[1].replace('///', '')
        
        return db_info
    
    def get_tables(self) -> List[Dict]:
        """Obtiene todas las tablas con sus columnas y relaciones"""
        if not self.inspector:
            self.connect()
        
        tables = []
        
        for table_name in self.inspector.get_table_names():
            table_info = self._get_table_info(table_name)
            tables.append(table_info)
        
        return tables
    
    def _get_table_info(self, table_name: str) -> Dict:
        """Obtiene información completa de una tabla"""
        columns = []
        
        # Obtener columnas
        for column in self.inspector.get_columns(table_name):
            col_info = self._parse_column(table_name, column)
            columns.append(col_info)
        
        # Obtener relaciones
        relationships = self._get_relationships(table_name)
        
        return {
            'name': table_name,
            'columns': columns,
            'relationships': relationships
        }
    
    def _parse_column(self, table_name: str, column: Dict) -> Dict:
        """Parsea información de una columna"""
        type_str = str(column['type'])
        base_type, length = extract_length_from_type(type_str)
        
        col_info = {
            'name': column['name'],
            'type': type_str,
            'base_type': base_type,
            'length': length,
            'nullable': column['nullable'],
            'primary_key': column.get('primary_key', False),
            'autoincrement': column.get('autoincrement', False),
            'default': column.get('default'),
            'foreign_key': None,
            'sqlalchemy_type': self._map_to_sqlalchemy(base_type),
            'python_type': self._map_to_python(base_type)
        }
        
        # Detectar Foreign Keys
        fks = self.inspector.get_foreign_keys(table_name)
        for fk in fks:
            if column['name'] in fk['constrained_columns']:
                idx = fk['constrained_columns'].index(column['name'])
                ref_table = fk['referred_table']
                ref_col = fk['referred_columns'][idx]
                col_info['foreign_key'] = f"{ref_table}.{ref_col}"
                col_info['foreign_key_table'] = ref_table
                col_info['foreign_key_column'] = ref_col
        
        return col_info
    
    def _get_relationships(self, table_name: str) -> List[Dict]:
        """Detecta relaciones entre tablas"""
        relationships = []
        fks = self.inspector.get_foreign_keys(table_name)
        
        for fk in fks:
            for i, col in enumerate(fk['constrained_columns']):
                relationships.append({
                    'type': 'many_to_one',
                    'target_table': fk['referred_table'],
                    'foreign_key': col,
                    'target_column': fk['referred_columns'][i]
                })
        
        return relationships
    
    def _map_to_sqlalchemy(self, sql_type: str) -> str:
        """Mapea tipo SQL a tipo SQLAlchemy"""
        return SQL_TO_SQLALCHEMY.get(sql_type.upper(), 'String')
    
    def _map_to_python(self, sql_type: str) -> str:
        """Mapea tipo SQL a tipo Python"""
        return SQL_TO_PYTHON.get(sql_type.upper(), 'str')
    
    def get_existing_models(self) -> List[str]:
        """Obtiene lista de modelos ya existentes en app/models/"""
        models_dir = self.project_path / "app" / "models"
        
        if not models_dir.exists():
            return []
        
        existing = []
        for file in models_dir.glob("*_model.py"):
            # Extraer nombre de tabla del nombre de archivo
            model_name = file.stem.replace("_model", "")
            existing.append(model_name)
        
        return existing
    
    def is_auth_table(self, table_name: str) -> bool:
        """Detecta si una tabla es de autenticación/usuarios"""
        auth_tables = ['users', 'user', 'usuarios', 'usuario', 'accounts', 'account']
        return table_name.lower() in auth_tables
    
    def has_password_column(self, table: Dict) -> bool:
        """Verifica si una tabla tiene columna de password"""
        password_cols = ['password', 'passwd', 'pwd', 'contraseña', 'clave', 'hashed_password']
        column_names = [col['name'].lower() for col in table['columns']]
        return any(pwd in column_names for pwd in password_cols)
