"""Constantes globales para Lara"""

# Tipos de bases de datos soportadas
DATABASE_TYPES = {
    'sqlite': 'SQLite',
    'postgresql': 'PostgreSQL',
    'mysql': 'MySQL',
    'mssql': 'SQL Server',
    'mongodb': 'MongoDB'
}

# Mapeo de tipos SQL a SQLAlchemy
SQL_TO_SQLALCHEMY = {
    'INTEGER': 'Integer',
    'BIGINT': 'BigInteger',
    'SMALLINT': 'SmallInteger',
    'VARCHAR': 'String',
    'TEXT': 'Text',
    'CHAR': 'String',
    'BOOLEAN': 'Boolean',
    'DECIMAL': 'Numeric',
    'NUMERIC': 'Numeric',
    'FLOAT': 'Float',
    'DOUBLE': 'Float',
    'REAL': 'Float',
    'DATE': 'Date',
    'DATETIME': 'DateTime',
    'TIMESTAMP': 'DateTime',
    'TIME': 'Time',
    'JSON': 'JSON',
    'JSONB': 'JSON',
    'BLOB': 'LargeBinary',
    'BINARY': 'LargeBinary',
}

# Mapeo de tipos SQL a Python/Pydantic
SQL_TO_PYTHON = {
    'INTEGER': 'int',
    'BIGINT': 'int',
    'SMALLINT': 'int',
    'VARCHAR': 'str',
    'TEXT': 'str',
    'CHAR': 'str',
    'BOOLEAN': 'bool',
    'DECIMAL': 'float',
    'NUMERIC': 'float',
    'FLOAT': 'float',
    'DOUBLE': 'float',
    'REAL': 'float',
    'DATE': 'datetime.date',
    'DATETIME': 'datetime.datetime',
    'TIMESTAMP': 'datetime.datetime',
    'TIME': 'datetime.time',
    'JSON': 'dict',
    'JSONB': 'dict',
}

# Columnas especiales que requieren imports adicionales
DATETIME_COLUMNS = ['created_at', 'updated_at', 'deleted_at']
