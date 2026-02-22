"""
Tests unitarios para el decorador endpoint_termostato.
HU-003: Eliminar duplicación en endpoints API
"""
import pytest
from unittest.mock import MagicMock

from app.servicios.api import app_api


@pytest.fixture
def client():
    """Fixture que proporciona el cliente de pruebas de Flask."""
    app_api.config['TESTING'] = True
    with app_api.test_client() as client:
        yield client


class TestDecoradorGet:
    """Tests para el comportamiento GET del decorador."""

    def test_get_temperatura_ambiente_retorna_valor(self, client):
        """GET retorna el valor actual del campo del modelo."""
        response = client.get('/termostato/temperatura_ambiente/')
        assert response.status_code == 200
        data = response.get_json()
        assert 'temperatura_ambiente' in data

    def test_get_temperatura_deseada_retorna_valor(self, client):
        """GET retorna el valor actual de temperatura deseada."""
        response = client.get('/termostato/temperatura_deseada/')
        assert response.status_code == 200
        data = response.get_json()
        assert 'temperatura_deseada' in data

    def test_get_bateria_retorna_valor(self, client):
        """GET retorna el valor actual de carga de bateria."""
        response = client.get('/termostato/bateria/')
        assert response.status_code == 200
        data = response.get_json()
        assert 'carga_bateria' in data

    def test_get_estado_climatizador_retorna_valor(self, client):
        """GET retorna el valor actual del estado del climatizador."""
        response = client.get('/termostato/estado_climatizador/')
        assert response.status_code == 200
        data = response.get_json()
        assert 'estado_climatizador' in data


class TestDecoradorPost:
    """Tests para el comportamiento POST del decorador."""

    def test_post_temperatura_ambiente_valida(self, client):
        """POST con valor valido retorna 201."""
        response = client.post(
            '/termostato/temperatura_ambiente/',
            json={'ambiente': 25}
        )
        assert response.status_code == 201
        assert response.get_json()['mensaje'] == 'dato registrado'

    def test_post_temperatura_deseada_valida(self, client):
        """POST con valor valido retorna 201."""
        response = client.post(
            '/termostato/temperatura_deseada/',
            json={'deseada': 22}
        )
        assert response.status_code == 201

    def test_post_bateria_valida(self, client):
        """POST con valor valido retorna 201."""
        response = client.post(
            '/termostato/bateria/',
            json={'bateria': 3.5}
        )
        assert response.status_code == 201

    def test_post_estado_climatizador_valido(self, client):
        """POST con estado valido retorna 201."""
        response = client.post(
            '/termostato/estado_climatizador/',
            json={'climatizador': 'encendido'}
        )
        assert response.status_code == 201


class TestDecoradorValidacion:
    """Tests para la validacion centralizada del decorador."""

    def test_post_sin_campo_requerido_retorna_400(self, client):
        """POST sin el campo requerido retorna 400."""
        response = client.post(
            '/termostato/temperatura_ambiente/',
            json={'campo_incorrecto': 99}
        )
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'ambiente' in data['error']['detalle']

    def test_post_sin_body_retorna_415(self, client):
        """POST sin Content-Type JSON retorna 415 (Flask rechaza antes del decorador)."""
        response = client.post('/termostato/temperatura_ambiente/')
        assert response.status_code == 415

    def test_post_body_vacio_retorna_400(self, client):
        """POST con body JSON vacio retorna 400."""
        response = client.post(
            '/termostato/temperatura_ambiente/',
            json={}
        )
        assert response.status_code == 400

    def test_post_valor_fuera_de_rango_retorna_400(self, client):
        """POST con valor fuera de rango retorna 400."""
        response = client.post(
            '/termostato/temperatura_ambiente/',
            json={'ambiente': 9999}
        )
        assert response.status_code == 400
        data = response.get_json()
        assert data['error']['mensaje'] == 'Valor fuera de rango'

    def test_post_estado_climatizador_invalido_retorna_400(self, client):
        """POST con estado de climatizador invalido retorna 400."""
        response = client.post(
            '/termostato/estado_climatizador/',
            json={'climatizador': 'estado_invalido'}
        )
        assert response.status_code == 400
