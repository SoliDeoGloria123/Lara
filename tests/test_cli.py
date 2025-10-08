"""Tests para el CLI"""
import pytest
from typer.testing import CliRunner
from lara.cli import app

runner = CliRunner()


def test_version():
    """Test comando version"""
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "Lara CLI" in result.stdout
    assert "0.1.0" in result.stdout


def test_create_project():
    """Test comando create (sin ejecutar realmente)"""
    # Solo verificar que el comando existe y es invocable
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "create" in result.stdout


def test_get_database_without_env():
    """Test get-database sin archivo .env"""
    result = runner.invoke(app, ["get-database"])
    assert result.exit_code == 1
    assert "No se encontró" in result.stdout or "error" in result.stdout.lower()
