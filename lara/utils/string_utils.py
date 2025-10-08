"""Utilidades para manipulación de strings"""
import re


def to_snake_case(text: str) -> str:
    """
    Convierte texto a snake_case
    
    Examples:
        >>> to_snake_case("ProductoDetalle")
        'producto_detalle'
        >>> to_snake_case("usuario-admin")
        'usuario_admin'
    """
    # Reemplazar guiones y espacios por guiones bajos
    text = text.replace('-', '_').replace(' ', '_')
    
    # Insertar guión bajo antes de mayúsculas
    text = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
    text = re.sub('([a-z0-9])([A-Z])', r'\1_\2', text)
    
    # Convertir a minúsculas y limpiar guiones bajos múltiples
    text = text.lower()
    text = re.sub('_+', '_', text)
    
    return text.strip('_')


def to_pascal_case(text: str) -> str:
    """
    Convierte texto a PascalCase
    
    Examples:
        >>> to_pascal_case("producto_detalle")
        'ProductoDetalle'
        >>> to_pascal_case("usuario-admin")
        'UsuarioAdmin'
    """
    text = to_snake_case(text)
    return ''.join(word.capitalize() for word in text.split('_'))


def to_camel_case(text: str) -> str:
    """
    Convierte texto a camelCase
    
    Examples:
        >>> to_camel_case("producto_detalle")
        'productoDetalle'
        >>> to_camel_case("usuario_admin")
        'usuarioAdmin'
    """
    pascal = to_pascal_case(text)
    return pascal[0].lower() + pascal[1:] if pascal else ''


def pluralize(word: str) -> str:
    """
    Pluraliza una palabra (inglés/español básico)
    
    Examples:
        >>> pluralize("producto")
        'productos'
        >>> pluralize("category")
        'categories'
    """
    word = word.lower()
    
    # Reglas para inglés
    if word.endswith('y') and len(word) > 1 and word[-2] not in 'aeiou':
        return word[:-1] + 'ies'
    elif word.endswith(('s', 'x', 'z', 'ch', 'sh')):
        return word + 'es'
    elif word.endswith('o') and len(word) > 1 and word[-2] not in 'aeiou':
        return word + 'es'
    else:
        return word + 's'


def singularize(word: str) -> str:
    """
    Singulariza una palabra (inglés/español básico)
    
    Examples:
        >>> singularize("productos")
        'producto'
        >>> singularize("categories")
        'category'
    """
    word = word.lower()
    
    if word.endswith('ies'):
        return word[:-3] + 'y'
    elif word.endswith('es') and len(word) > 2:
        if word[-3] in 'sxz' or word.endswith(('ches', 'shes')):
            return word[:-2]
        return word[:-1]
    elif word.endswith('s') and len(word) > 1:
        return word[:-1]
    
    return word


def extract_length_from_type(type_str: str) -> tuple[str, int | None]:
    """
    Extrae el tipo base y la longitud de un tipo SQL
    
    Examples:
        >>> extract_length_from_type("VARCHAR(255)")
        ('VARCHAR', 255)
        >>> extract_length_from_type("INTEGER")
        ('INTEGER', None)
    """
    match = re.match(r'(\w+)(?:\((\d+)\))?', type_str.upper())
    if match:
        base_type = match.group(1)
        length = int(match.group(2)) if match.group(2) else None
        return base_type, length
    return type_str.upper(), None
