"""Clase base abstracta para inspectores de base de datos"""
from abc import ABC, abstractmethod
from typing import List, Dict
from pathlib import Path


class BaseInspector(ABC):
    """Clase base para inspectores de base de datos"""
    
    @abstractmethod
    def connect(self) -> bool:
        """Establece conexión con la base de datos"""
        pass
    
    @abstractmethod
    def get_tables(self) -> List[Dict]:
        """
        Obtiene todas las tablas/colecciones de la base de datos
        
        Returns:
            Lista de diccionarios con información de tablas:
            [
                {
                    'name': 'usuarios',
                    'columns': [
                        {
                            'name': 'id',
                            'type': 'INTEGER',
                            'nullable': False,
                            'primary_key': True,
                            'autoincrement': True,
                            'foreign_key': None
                        },
                        ...
                    ],
                    'relationships': [
                        {
                            'type': 'many_to_one',
                            'target_table': 'roles',
                            'foreign_key': 'rol_id'
                        },
                        ...
                    ]
                },
                ...
            ]
        """
        pass
    
    @abstractmethod
    def get_existing_models(self) -> List[str]:
        """
        Obtiene lista de modelos ya existentes en el proyecto
        
        Returns:
            Lista de nombres de tablas que ya tienen modelo
        """
        pass
    
    def get_missing_models(self) -> List[Dict]:
        """
        Obtiene tablas que no tienen modelo generado
        
        Returns:
            Lista de tablas sin modelo
        """
        all_tables = self.get_tables()
        existing_models = self.get_existing_models()
        
        return [
            table for table in all_tables 
            if table['name'] not in existing_models
        ]
