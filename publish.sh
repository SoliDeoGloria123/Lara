#!/bin/bash

# Script para publicar Lara en PyPI
# Uso: ./publish.sh [test|prod|both]

set -e

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Publicación de Lara CLI${NC}"
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "setup.py" ]; then
    echo -e "${RED}❌ Error: setup.py no encontrado${NC}"
    echo "Ejecuta este script desde la raíz del proyecto"
    exit 1
fi

# Limpiar builds anteriores
echo -e "${YELLOW}🧹 Limpiando builds anteriores...${NC}"
rm -rf build/ dist/ *.egg-info

# Verificar código
echo -e "${YELLOW}🔍 Verificando setup.py...${NC}"
python3 setup.py check

# Construir paquete
echo -e "${YELLOW}📦 Construyendo paquete...${NC}"
python3 -m build

# Verificar paquete
echo -e "${YELLOW}✅ Verificando paquete...${NC}"
twine check dist/*

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Error en la verificación del paquete${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Paquete construido y verificado correctamente${NC}"
echo ""

# Determinar destino
MODE=${1:-"ask"}

if [ "$MODE" == "ask" ]; then
    echo -e "${BLUE}¿Dónde deseas publicar?${NC}"
    echo "1) Test PyPI (recomendado primero)"
    echo "2) PyPI (producción)"
    echo "3) Ambos (Test PyPI primero, luego PyPI)"
    echo "4) Cancelar"
    read -p "Selecciona (1-4): " choice
    
    case $choice in
        1) MODE="test" ;;
        2) MODE="prod" ;;
        3) MODE="both" ;;
        4) echo "Cancelado"; exit 0 ;;
        *) echo -e "${RED}Opción inválida${NC}"; exit 1 ;;
    esac
fi

# Publicar en Test PyPI
if [ "$MODE" == "test" ] || [ "$MODE" == "both" ]; then
    echo ""
    echo -e "${YELLOW}📤 Subiendo a Test PyPI...${NC}"
    twine upload --repository testpypi dist/*
    
    if [ $? -eq 0 ]; then
        echo ""
        echo -e "${GREEN}✅ Publicado exitosamente en Test PyPI!${NC}"
        echo -e "${BLUE}Prueba con:${NC}"
        echo "  pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ lara-cli"
        echo ""
        
        if [ "$MODE" == "both" ]; then
            read -p "¿Continuar con PyPI real? (s/n): " continue
            if [[ ! "$continue" =~ ^([sS][íi]?)$ ]]; then
                exit 0
            fi
        else
            exit 0
        fi
    else
        echo -e "${RED}❌ Error al publicar en Test PyPI${NC}"
        exit 1
    fi
fi

# Publicar en PyPI real
if [ "$MODE" == "prod" ] || [ "$MODE" == "both" ]; then
    echo ""
    echo -e "${RED}⚠️  ATENCIÓN: Vas a publicar en PyPI REAL${NC}"
    read -p "¿Estás seguro? (escribe 'SI' para continuar): " confirm
    
    if [ "$confirm" != "SI" ]; then
        echo "Cancelado"
        exit 0
    fi
    
    echo ""
    echo -e "${YELLOW}📤 Subiendo a PyPI...${NC}"
    twine upload dist/*
    
    if [ $? -eq 0 ]; then
        echo ""
        echo -e "${GREEN}🎉 ¡Publicado exitosamente en PyPI!${NC}"
        echo ""
        echo -e "${BLUE}Los usuarios pueden instalar con:${NC}"
        echo "  pip install lara-cli"
        echo ""
        echo -e "${BLUE}Ver en PyPI:${NC}"
        echo "  https://pypi.org/project/lara-cli/"
        echo ""
    else
        echo -e "${RED}❌ Error al publicar en PyPI${NC}"
        exit 1
    fi
fi

echo -e "${GREEN}✅ Proceso completado${NC}"
