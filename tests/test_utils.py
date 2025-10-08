"""Tests para utilidades"""
import pytest
from lara.utils.string_utils import (
    to_snake_case,
    to_pascal_case,
    to_camel_case,
    pluralize,
    singularize,
    extract_length_from_type
)


def test_to_snake_case():
    """Test conversión a snake_case"""
    assert to_snake_case("ProductoDetalle") == "producto_detalle"
    assert to_snake_case("usuario-admin") == "usuario_admin"
    assert to_snake_case("MiClaseEspecial") == "mi_clase_especial"
    assert to_snake_case("API_KEY") == "api_key"


def test_to_pascal_case():
    """Test conversión a PascalCase"""
    assert to_pascal_case("producto_detalle") == "ProductoDetalle"
    assert to_pascal_case("usuario-admin") == "UsuarioAdmin"
    assert to_pascal_case("mi_clase_especial") == "MiClaseEspecial"


def test_to_camel_case():
    """Test conversión a camelCase"""
    assert to_camel_case("producto_detalle") == "productoDetalle"
    assert to_camel_case("usuario_admin") == "usuarioAdmin"
    assert to_camel_case("mi_clase_especial") == "miClaseEspecial"


def test_pluralize():
    """Test pluralización"""
    assert pluralize("producto") == "productos"
    assert pluralize("category") == "categories"
    assert pluralize("box") == "boxes"
    assert pluralize("tomato") == "tomatoes"


def test_singularize():
    """Test singularización"""
    assert singularize("productos") == "producto"
    assert singularize("categories") == "category"
    assert singularize("boxes") == "box"


def test_extract_length_from_type():
    """Test extracción de longitud de tipo SQL"""
    base_type, length = extract_length_from_type("VARCHAR(255)")
    assert base_type == "VARCHAR"
    assert length == 255
    
    base_type, length = extract_length_from_type("INTEGER")
    assert base_type == "INTEGER"
    assert length is None
    
    base_type, length = extract_length_from_type("CHAR(10)")
    assert base_type == "CHAR"
    assert length == 10
