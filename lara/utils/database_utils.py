"""Utilidades para manejo de bases de datos"""
from typing import Optional
import re


def detect_database_type(database_url: str) -> str:
    """
    Detecta el tipo de base de datos desde la URL
    
    Args:
        database_url: URL de conexión a la base de datos
    
    Returns:
        Tipo de base de datos (sqlite, postgresql, mysql, mssql)
    """
    if database_url.startswith('sqlite'):
        return 'sqlite'
    elif database_url.startswith('postgresql'):
        return 'postgresql'
    elif database_url.startswith('mysql'):
        return 'mysql'
    elif database_url.startswith('mssql'):
        return 'mssql'
    else:
        return 'unknown'


def parse_database_url(database_url: str) -> dict:
    """
    Parsea una URL de base de datos en sus componentes
    
    Args:
        database_url: URL de conexión
    
    Returns:
        Dict con host, port, database, user, password
    """
    # Patrón: dialect://user:password@host:port/database
    pattern = r'(\w+)://(?:([^:]+):([^@]+)@)?([^:/]+)(?::(\d+))?/(.+)'
    match = re.match(pattern, database_url)
    
    if not match:
        return {
            'dialect': 'sqlite',
            'host': None,
            'port': None,
            'database': database_url.replace('sqlite:///', ''),
            'user': None,
            'password': None
        }
    
    dialect, user, password, host, port, database = match.groups()
    
    return {
        'dialect': dialect,
        'user': user,
        'password': password,
        'host': host,
        'port': int(port) if port else None,
        'database': database
    }


def needs_check_same_thread(database_url: str) -> bool:
    """
    Verifica si la base de datos necesita check_same_thread=False
    (Solo para SQLite)
    
    Args:
        database_url: URL de conexión
    
    Returns:
        True si es SQLite, False en caso contrario
    """
    return database_url.startswith('sqlite')


def get_driver_name(database_type: str) -> str:
    """
    Obtiene el nombre del driver recomendado para un tipo de BD
    
    Args:
        database_type: Tipo de base de datos
    
    Returns:
        Nombre del paquete driver
    """
    drivers = {
        'postgresql': 'psycopg2-binary',
        'mysql': 'pymysql',
        'mssql': 'pymssql',
        'sqlite': '',  # Incluido en Python
    }
    return drivers.get(database_type, '')
