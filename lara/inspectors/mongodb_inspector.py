"""Inspector para MongoDB con análisis profundo de documentos"""
from typing import List, Dict, Optional, Any, Set
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import os
from dotenv import load_dotenv

from lara.inspectors.base_inspector import BaseInspector


class MongoDBInspector(BaseInspector):
    """Inspector para MongoDB Atlas y Compass con detección inteligente de esquemas"""
    
    def __init__(self, mongodb_url: Optional[str] = None, project_path: Optional[Path] = None):
        """
        Inicializa el inspector MongoDB
        
        Args:
            mongodb_url: URL de conexión a MongoDB Atlas/Compass
            project_path: Ruta al proyecto
        """
        self.project_path = project_path or Path.cwd()
        
        # Cargar .env si existe
        env_path = self.project_path / ".env"
        if env_path.exists():
            load_dotenv(env_path)
        
        self.mongodb_url = mongodb_url or os.getenv("MONGODB_URL") or os.getenv("DATABASE_URL")
        
        if not self.mongodb_url:
            raise ValueError(
                "No se encontró MONGODB_URL o DATABASE_URL. "
                "Crea un archivo .env con: MONGODB_URL=mongodb+srv://..."
            )
        
        self.client = None
        self.db = None
        self.db_name = None
    
    def connect(self) -> bool:
        """Establece conexión con MongoDB"""
        try:
            from pymongo import MongoClient
            from pymongo.server_api import ServerApi
            
            # Extraer nombre de la base de datos desde la URL
            # mongodb+srv://user:pass@cluster.mongodb.net/DATABASE?options
            url_parts = self.mongodb_url.split('/')
            if len(url_parts) >= 4:
                self.db_name = url_parts[3].split('?')[0]
            else:
                raise ValueError("URL de MongoDB inválida. Formato esperado: mongodb+srv://.../<database>")
            
            # Configurar cliente con opciones para Atlas
            if 'mongodb+srv://' in self.mongodb_url:
                # MongoDB Atlas
                self.client = MongoClient(
                    self.mongodb_url,
                    server_api=ServerApi('1'),
                    serverSelectionTimeoutMS=5000,
                    connectTimeoutMS=10000
                )
            else:
                # MongoDB local o compass
                self.client = MongoClient(self.mongodb_url)
            
            self.db = self.client[self.db_name]
            
            # Test de conexión con ping
            self.client.admin.command('ping')
            
            return True
        except ImportError:
            raise ImportError(
                "pymongo no está instalado. "
                "Instálalo con: pip install pymongo"
            )
        except Exception as e:
            raise ConnectionError(f"Error al conectar a MongoDB: {e}")
    
    def get_database_info(self) -> Dict:
        """Obtiene información sobre la base de datos conectada"""
        if not self.db:
            self.connect()
        
        # Obtener estadísticas de la base de datos
        stats = self.db.command("dbStats")
        
        return {
            'type': 'mongodb',
            'name': self.db_name,
            'url': self.mongodb_url.split('@')[1].split('/')[0] if '@' in self.mongodb_url else 'localhost',
            'collections_count': stats.get('collections', 0),
            'data_size': stats.get('dataSize', 0),
            'storage_size': stats.get('storageSize', 0),
            'indexes': stats.get('indexes', 0)
        }
    
    def get_tables(self) -> List[Dict]:
        """Obtiene todas las colecciones de MongoDB con análisis profundo"""
        if not self.db:
            self.connect()
        
        collections = []
        
        for collection_name in self.db.list_collection_names():
            # Filtrar colecciones del sistema
            if collection_name.startswith('system.'):
                continue
                
            collection_info = self._analyze_collection(collection_name)
            collections.append(collection_info)
        
        return collections
    
    def _analyze_collection(self, collection_name: str, sample_size: int = 100) -> Dict:
        """
        Analiza la estructura de una colección analizando múltiples documentos
        
        Args:
            collection_name: Nombre de la colección
            sample_size: Número de documentos a analizar para inferir esquema
        """
        collection = self.db[collection_name]
        
        # Obtener conteo de documentos
        doc_count = collection.count_documents({})
        
        if doc_count == 0:
            return {
                'name': collection_name,
                'document_count': 0,
                'columns': [],
                'relationships': [],
                'indexes': []
            }
        
        # Analizar múltiples documentos para inferir esquema completo
        samples = list(collection.find().limit(min(sample_size, doc_count)))
        
        # Detectar todos los campos y sus tipos
        field_info = self._analyze_fields(samples)
        
        # Detectar relaciones (campos que terminan en _id)
        relationships = self._detect_relationships(field_info, collection_name)
        
        # Obtener índices
        indexes = self._get_indexes(collection)
        
        # Convertir a formato de columnas
        columns = []
        for field_name, info in field_info.items():
            columns.append({
                'name': field_name,
                'type': info['type'],
                'python_type': info['python_type'],
                'nullable': info['nullable'],
                'required': info['required'],
                'primary_key': field_name == '_id',
                'unique': field_name in [idx['field'] for idx in indexes if idx.get('unique', False)],
                'foreign_key': info.get('foreign_key'),
                'foreign_key_table': info.get('foreign_key_table'),
                'is_array': info['is_array'],
                'is_object': info['is_object'],
                'sample_values': info['sample_values'][:3]  # Primeros 3 valores de ejemplo
            })
        
        return {
            'name': collection_name,
            'document_count': doc_count,
            'columns': columns,
            'relationships': relationships,
            'indexes': indexes
        }
    
    def _analyze_fields(self, documents: List[Dict]) -> Dict[str, Dict]:
        """
        Analiza campos de múltiples documentos para determinar tipos y requerimientos
        """
        field_info = defaultdict(lambda: {
            'types': set(),
            'null_count': 0,
            'present_count': 0,
            'sample_values': []
        })
        
        total_docs = len(documents)
        
        for doc in documents:
            # Aplanar documento para obtener todos los campos
            flat_doc = self._flatten_dict(doc)
            
            for field_name, value in flat_doc.items():
                info = field_info[field_name]
                info['present_count'] += 1
                
                if value is None:
                    info['null_count'] += 1
                else:
                    field_type = self._infer_type(value)
                    info['types'].add(field_type)
                    
                    # Guardar valores de muestra (máximo 5)
                    if len(info['sample_values']) < 5:
                        info['sample_values'].append(str(value)[:50])  # Limitar longitud
        
        # Convertir a formato final
        result = {}
        for field_name, info in field_info.items():
            # Determinar tipo principal (el más común)
            main_type = list(info['types'])[0] if info['types'] else 'str'
            
            result[field_name] = {
                'type': main_type,
                'python_type': self._mongo_to_python_type(main_type),
                'nullable': info['null_count'] > 0,
                'required': info['present_count'] == total_docs and info['null_count'] == 0,
                'is_array': main_type == 'list',
                'is_object': main_type == 'dict',
                'sample_values': info['sample_values']
            }
            
            # Detectar si es foreign key (campos que terminan en _id)
            if field_name.endswith('_id') and field_name != '_id':
                referenced_collection = field_name.replace('_id', '') + 's'  # Pluralizar
                result[field_name]['foreign_key'] = f"{referenced_collection}._id"
                result[field_name]['foreign_key_table'] = referenced_collection
        
        return result
    
    def _flatten_dict(self, d: Dict, parent_key: str = '', sep: str = '.') -> Dict:
        """Aplana un diccionario anidado"""
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            
            if isinstance(v, dict) and not self._is_special_type(v):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        
        return dict(items)
    
    def _is_special_type(self, value: Any) -> bool:
        """Detecta si es un tipo especial de MongoDB (ObjectId, datetime, etc.)"""
        type_name = type(value).__name__
        return type_name in ['ObjectId', 'datetime', 'Decimal128', 'Binary', 'Code']
    
    def _infer_type(self, value: Any) -> str:
        """Infiere el tipo de dato desde un valor"""
        from bson import ObjectId
        
        if value is None:
            return 'str'
        elif isinstance(value, bool):
            return 'bool'
        elif isinstance(value, int):
            return 'int'
        elif isinstance(value, float):
            return 'float'
        elif isinstance(value, str):
            # Detectar si es email
            if '@' in value and '.' in value:
                return 'email'
            # Detectar si es password (hash bcrypt/argon2)
            if value.startswith('$2b$') or value.startswith('$argon2'):
                return 'password'
            return 'str'
        elif isinstance(value, datetime):
            return 'datetime'
        elif isinstance(value, ObjectId):
            return 'ObjectId'
        elif isinstance(value, dict):
            return 'dict'
        elif isinstance(value, list):
            return 'list'
        else:
            return 'str'
    
    def _mongo_to_python_type(self, mongo_type: str) -> str:
        """Convierte tipo de MongoDB a tipo Python"""
        type_map = {
            'str': 'str',
            'int': 'int',
            'float': 'float',
            'bool': 'bool',
            'datetime': 'datetime',
            'ObjectId': 'ObjectId',
            'dict': 'Dict',
            'list': 'List',
            'email': 'EmailStr',
            'password': 'str'
        }
        return type_map.get(mongo_type, 'str')
    
    def _detect_relationships(self, field_info: Dict, collection_name: str) -> List[Dict]:
        """Detecta relaciones implícitas en campos que terminan con _id"""
        relationships = []
        
        for field_name, info in field_info.items():
            if field_name.endswith('_id') and field_name != '_id':
                # Inferir nombre de colección referenciada
                ref_name = field_name.replace('_id', '')
                ref_collection = ref_name + 's'  # Pluralizar (simplificado)
                
                relationships.append({
                    'type': 'many_to_one',
                    'field': field_name,
                    'target_collection': ref_collection,
                    'target_field': '_id'
                })
        
        return relationships
    
    def _get_indexes(self, collection) -> List[Dict]:
        """Obtiene los índices de una colección"""
        indexes = []
        
        for index in collection.list_indexes():
            index_info = {
                'name': index['name'],
                'keys': list(index['key'].keys()),
                'field': list(index['key'].keys())[0] if len(index['key']) == 1 else None,
                'unique': index.get('unique', False),
                'sparse': index.get('sparse', False)
            }
            indexes.append(index_info)
        
        return indexes
    
    def get_existing_models(self) -> List[str]:
        """Obtiene lista de modelos existentes"""
        models_dir = self.project_path / "app" / "models"
        
        if not models_dir.exists():
            return []
        
        existing = []
        for file in models_dir.glob("*_model.py"):
            model_name = file.stem.replace("_model", "")
            existing.append(model_name)
        
        return existing
    
    def is_auth_collection(self, collection_name: str) -> bool:
        """Detecta si una colección es de autenticación/usuarios"""
        auth_names = ['users', 'user', 'usuarios', 'usuario', 'accounts', 'account']
        return collection_name.lower() in auth_names
    
    def has_password_field(self, collection_info: Dict) -> bool:
        """Verifica si una colección tiene campo de password"""
        password_fields = ['password', 'passwd', 'pwd', 'contraseña', 'clave', 'hashed_password', 'hash']
        column_names = [col['name'].lower() for col in collection_info['columns']]
        return any(pwd in column_names for pwd in password_fields)
