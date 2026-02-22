"""
Fixtures compartidos para los tests de la API del termostato.
Usa Application Factory Pattern para inyección de dependencias.
"""
import pytest
from unittest.mock import MagicMock

from app.servicios.api import create_app
from app.configuracion.factory import TermostatoFactory


@pytest.fixture
def termostato_real():
    """Fixture que provee una instancia real de Termostato para tests."""
    return TermostatoFactory.crear_termostato()


@pytest.fixture
def app(termostato_real):
    """Fixture que crea una app Flask con instancia de Termostato real."""
    flask_app = create_app(termostato=termostato_real)
    flask_app.config['TESTING'] = True
    return flask_app


@pytest.fixture
def client(app):
    """Fixture que provee el cliente de pruebas de Flask."""
    with app.test_client() as c:
        yield c
