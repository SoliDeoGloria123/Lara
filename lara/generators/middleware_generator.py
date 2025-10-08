"""Generador de middlewares"""
from pathlib import Path
from jinja2 import Environment, PackageLoader, select_autoescape

from lara.utils.file_utils import write_file


class MiddlewareGenerator:
    """Genera middlewares personalizados"""
    
    def __init__(self, project_path: Path = None):
        """
        Inicializa el generador de middlewares
        
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
    
    def generate_auth_middleware(self) -> Path:
        """Genera middleware de autenticación JWT"""
        template = self.env.get_template('middlewares/auth_middleware.py.jinja')
        content = template.render()
        
        output_path = self.project_path / "app" / "middlewares" / "auth_middleware.py"
        write_file(output_path, content)
        
        return output_path
    
    def generate_cors_middleware(self) -> Path:
        """Genera middleware de CORS"""
        template = self.env.get_template('middlewares/cors_middleware.py.jinja')
        content = template.render()
        
        output_path = self.project_path / "app" / "middlewares" / "cors_middleware.py"
        write_file(output_path, content)
        
        return output_path
    
    def generate_custom_middleware(self, name: str) -> Path:
        """
        Genera un middleware personalizado básico
        
        Args:
            name: Nombre del middleware
        
        Returns:
            Path al archivo generado
        """
        # Template básico para middleware personalizado
        content = f'''"""Middleware personalizado: {name}"""
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable


class {name.title().replace('_', '')}Middleware(BaseHTTPMiddleware):
    """Middleware {name}"""
    
    async def dispatch(self, request: Request, call_next: Callable):
        """
        Procesa la request antes y después de llegar al endpoint
        
        Args:
            request: Request de FastAPI
            call_next: Siguiente middleware/endpoint
        
        Returns:
            Response
        """
        # Lógica antes de procesar la request
        # ...
        
        # Procesar request
        response = await call_next(request)
        
        # Lógica después de procesar la request
        # ...
        
        return response
'''
        
        output_path = self.project_path / "app" / "middlewares" / f"{name}_middleware.py"
        write_file(output_path, content)
        
        return output_path
