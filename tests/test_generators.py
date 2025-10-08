"""Tests para generadores"""
import pytest
from pathlib import Path
import tempfile
import shutil

from lara.generators.project_generator import ProjectGenerator
from lara.generators.model_generator import ModelGenerator
from lara.generators.schema_generator import SchemaGenerator


@pytest.fixture
def temp_dir():
    """Fixture para crear un directorio temporal"""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path)


def test_project_generator(temp_dir):
    """Test para generar un proyecto completo"""
    project_name = "test_project"
    generator = ProjectGenerator(project_name, temp_dir)
    generator.generate()
    
    project_path = temp_dir / project_name
    
    # Verificar estructura de directorios
    assert project_path.exists()
    assert (project_path / "app").exists()
    assert (project_path / "app" / "models").exists()
    assert (project_path / "app" / "schemas").exists()
    assert (project_path / "app" / "controllers").exists()
    assert (project_path / "app" / "routes").exists()
    
    # Verificar archivos principales
    assert (project_path / "app" / "main.py").exists()
    assert (project_path / "app" / "config.py").exists()
    assert (project_path / "app" / "database.py").exists()
    assert (project_path / "requirements.txt").exists()
    assert (project_path / ".env.example").exists()
    assert (project_path / ".gitignore").exists()
    assert (project_path / "README.md").exists()


def test_model_generator(temp_dir):
    """Test para generar un modelo"""
    # Crear estructura básica
    (temp_dir / "app" / "models").mkdir(parents=True)
    
    table = {
        'name': 'usuarios',
        'columns': [
            {
                'name': 'id',
                'type': 'INTEGER',
                'sqlalchemy_type': 'Integer',
                'primary_key': True,
                'nullable': False,
                'autoincrement': True
            },
            {
                'name': 'nombre',
                'type': 'VARCHAR(100)',
                'sqlalchemy_type': 'String',
                'length': 100,
                'primary_key': False,
                'nullable': False
            },
            {
                'name': 'email',
                'type': 'VARCHAR(255)',
                'sqlalchemy_type': 'String',
                'length': 255,
                'primary_key': False,
                'nullable': False,
                'unique': True
            }
        ],
        'relationships': []
    }
    
    generator = ModelGenerator(temp_dir)
    output_path = generator.generate(table)
    
    assert output_path.exists()
    assert output_path.name == "usuarios_model.py"
    
    # Verificar contenido básico
    content = output_path.read_text()
    assert "class Usuarios(Base):" in content
    assert "__tablename__ = \"usuarios\"" in content
    assert "id = Column" in content
    assert "nombre = Column" in content


def test_schema_generator(temp_dir):
    """Test para generar schemas Pydantic"""
    # Crear estructura básica
    (temp_dir / "app" / "schemas").mkdir(parents=True)
    
    table = {
        'name': 'productos',
        'columns': [
            {
                'name': 'id',
                'type': 'INTEGER',
                'python_type': 'int',
                'primary_key': True,
                'nullable': False,
                'autoincrement': True
            },
            {
                'name': 'nombre',
                'type': 'VARCHAR(200)',
                'python_type': 'str',
                'length': 200,
                'primary_key': False,
                'nullable': False
            },
            {
                'name': 'precio',
                'type': 'DECIMAL',
                'python_type': 'float',
                'primary_key': False,
                'nullable': False
            }
        ]
    }
    
    generator = SchemaGenerator(temp_dir)
    output_path = generator.generate(table)
    
    assert output_path.exists()
    assert output_path.name == "productos_schema.py"
    
    # Verificar contenido
    content = output_path.read_text()
    assert "class ProductosBase(BaseModel):" in content
    assert "class ProductosCreate(" in content
    assert "class ProductosUpdate(BaseModel):" in content
    assert "class ProductosResponse(" in content
