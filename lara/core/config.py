"""Configuración global de Lara"""
from pathlib import Path
from typing import Optional
import os
from dotenv import load_dotenv


class LaraConfig:
    """Configuración centralizada para Lara"""
    
    def __init__(self, project_path: Optional[Path] = None):
        self.project_path = project_path or Path.cwd()
        self._load_env()
    
    def _load_env(self):
        """Carga variables de entorno desde .env"""
        env_path = self.project_path / ".env"
        if env_path.exists():
            load_dotenv(env_path)
    
    @property
    def database_url(self) -> Optional[str]:
        """Obtiene la URL de la base de datos"""
        return os.getenv("DATABASE_URL")
    
    @property
    def mongodb_url(self) -> Optional[str]:
        """Obtiene la URL de MongoDB"""
        return os.getenv("MONGODB_URL")
    
    @property
    def app_path(self) -> Path:
        """Ruta al directorio app/"""
        return self.project_path / "app"
    
    @property
    def models_path(self) -> Path:
        """Ruta al directorio de modelos"""
        return self.app_path / "models"
    
    @property
    def schemas_path(self) -> Path:
        """Ruta al directorio de schemas"""
        return self.app_path / "schemas"
    
    @property
    def controllers_path(self) -> Path:
        """Ruta al directorio de controllers"""
        return self.app_path / "controllers"
    
    @property
    def routes_path(self) -> Path:
        """Ruta al directorio de routes"""
        return self.app_path / "routes"
    
    @property
    def middlewares_path(self) -> Path:
        """Ruta al directorio de middlewares"""
        return self.app_path / "middlewares"
    
    @property
    def utils_path(self) -> Path:
        """Ruta al directorio de utils"""
        return self.app_path / "utils"
