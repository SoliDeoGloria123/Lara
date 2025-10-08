"""Generador de proyectos FastAPI"""
from pathlib import Path
from jinja2 import Environment, PackageLoader, select_autoescape
from typing import Optional

from lara.utils.file_utils import write_file, ensure_directory


class ProjectGenerator:
    """Genera la estructura completa de un proyecto FastAPI"""
    
    def __init__(self, project_name: str, output_path: Optional[Path] = None):
        """
        Inicializa el generador de proyectos
        
        Args:
            project_name: Nombre del proyecto a crear
            output_path: Ruta donde crear el proyecto (default: directorio actual)
        """
        self.project_name = project_name
        self.output_path = output_path or Path.cwd()
        self.project_path = self.output_path / project_name
        
        # Configurar Jinja2
        self.env = Environment(
            loader=PackageLoader('lara', 'templates'),
            autoescape=select_autoescape(),
            trim_blocks=True,
            lstrip_blocks=True
        )
    
    def generate(self):
        """Genera toda la estructura del proyecto"""
        self._create_directories()
        self._generate_app_files()
        self._generate_config_files()
        self._generate_docs()
        self._init_git()
        return self.project_path
    
    def _create_directories(self):
        """Crea la estructura de directorios"""
        directories = [
            self.project_path / "app",
            self.project_path / "app" / "models",
            self.project_path / "app" / "schemas",
            self.project_path / "app" / "controllers",
            self.project_path / "app" / "routes",
            self.project_path / "app" / "middlewares",
            self.project_path / "app" / "utils",
            self.project_path / "tests",
        ]
        
        for directory in directories:
            ensure_directory(directory)
            
            # Crear __init__.py vacío
            init_file = directory / "__init__.py"
            if not init_file.exists():
                write_file(init_file, f'"""{directory.name} module"""\n')
    
    def _generate_app_files(self):
        """Genera archivos principales de la aplicación"""
        # main.py
        template = self.env.get_template('project/main.py.jinja')
        content = template.render(project_name=self.project_name)
        write_file(self.project_path / "app" / "main.py", content)
        
        # config.py
        template = self.env.get_template('project/config.py.jinja')
        content = template.render(project_name=self.project_name)
        write_file(self.project_path / "app" / "config.py", content)
        
        # database.py
        template = self.env.get_template('project/database.py.jinja')
        content = template.render()
        write_file(self.project_path / "app" / "database.py", content)
        
        # middlewares/auth_middleware.py
        template = self.env.get_template('middlewares/auth_middleware.py.jinja')
        content = template.render()
        write_file(self.project_path / "app" / "middlewares" / "auth_middleware.py", content)
        
        # utils/auth.py
        template = self.env.get_template('project/auth.py.jinja')
        content = template.render()
        write_file(self.project_path / "app" / "utils" / "auth.py", content)
        
        # Generar ejemplo de modelo User
        template = self.env.get_template('project/example_user_model.py.jinja')
        content = template.render()
        write_file(self.project_path / "app" / "models" / "user.py", content)
        
        # Generar ejemplo de schema User
        template = self.env.get_template('project/example_user_schema.py.jinja')
        content = template.render()
        write_file(self.project_path / "app" / "schemas" / "user.py", content)
        
        # Generar ejemplo de controller User
        template = self.env.get_template('project/example_user_controller.py.jinja')
        content = template.render()
        write_file(self.project_path / "app" / "controllers" / "user.py", content)
        
        # Generar ejemplo de rutas User
        template = self.env.get_template('project/example_user_routes.py.jinja')
        content = template.render()
        write_file(self.project_path / "app" / "routes" / "user.py", content)
    
    def _generate_config_files(self):
        """Genera archivos de configuración"""
        # requirements.txt
        template = self.env.get_template('project/requirements.txt.jinja')
        content = template.render()
        write_file(self.project_path / "requirements.txt", content)
        
        # .env.example
        template = self.env.get_template('project/env.example.jinja')
        content = template.render(project_name=self.project_name)
        write_file(self.project_path / ".env.example", content)
        
        # .gitignore
        template = self.env.get_template('project/gitignore.jinja')
        content = template.render()
        write_file(self.project_path / ".gitignore", content)
    
    def _generate_docs(self):
        """Genera documentación"""
        # README.md
        template = self.env.get_template('project/README.md.jinja')
        content = template.render(project_name=self.project_name)
        write_file(self.project_path / "README.md", content)
    
    def _init_git(self):
        """Inicializa repositorio git"""
        import subprocess
        
        try:
            subprocess.run(
                ['git', 'init'],
                cwd=self.project_path,
                capture_output=True,
                check=True
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Git no disponible o error al inicializar
            pass
