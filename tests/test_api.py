"""
Tests de integracion para la API REST del termostato.
TER-13: Tests de integracion de API
"""
import pytest

from app.servicios.api import app_api


@pytest.fixture
def client():
    """Fixture que proporciona el cliente de pruebas de Flask."""
    app_api.config['TESTING'] = True
    with app_api.test_client() as client:
        yield client


class TestHealthCheck:
    """Tests para el endpoint de health check."""

    def test_comprueba_endpoint(self, client):
        """Verifica que el endpoint /comprueba/ responde correctamente."""
        response = client.get('/comprueba/')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ok'
        assert 'version' in data
        assert 'uptime_seconds' in data
        assert 'timestamp' in data

    def test_comprueba_formato_json(self, client):
        """Verifica que la respuesta es JSON valido."""
        response = client.get('/comprueba/')
        assert response.content_type == 'application/json'


class TestTermostatoEndpoint:
    """Tests para el endpoint unificado /termostato/."""

    def test_get_termostato_completo(self, client):
        """Verifica que GET /termostato/ retorna todas las propiedades."""
        response = client.get('/termostato/')
        assert response.status_code == 200
        data = response.get_json()
        assert 'temperatura_ambiente' in data
        assert 'temperatura_deseada' in data
        assert 'carga_bateria' in data
        assert 'estado_climatizador' in data
        assert 'indicador' in data


class TestTemperaturaAmbiente:
    """Tests para el endpoint /termostato/temperatura_ambiente/."""

    def test_get_temperatura_ambiente(self, client):
        """Verifica que GET retorna la temperatura ambiente."""
        response = client.get('/termostato/temperatura_ambiente/')
        assert response.status_code == 200
        data = response.get_json()
        assert 'temperatura_ambiente' in data
        assert isinstance(data['temperatura_ambiente'], int)

    def test_post_temperatura_ambiente_valido(self, client):
        """Verifica que POST con valor valido actualiza la temperatura."""
        response = client.post(
            '/termostato/temperatura_ambiente/',
            json={'ambiente': 25}
        )
        assert response.status_code == 201
        data = response.get_json()
        assert data['mensaje'] == 'dato registrado'

        # Verificar que se actualizo
        response = client.get('/termostato/temperatura_ambiente/')
        assert response.get_json()['temperatura_ambiente'] == 25

    def test_post_temperatura_ambiente_sin_json(self, client):
        """Verifica que POST sin JSON retorna error 415 (Unsupported Media Type)."""
        response = client.post('/termostato/temperatura_ambiente/')
        assert response.status_code == 415

    def test_post_temperatura_ambiente_json_vacio(self, client):
        """Verifica que POST con JSON vacio retorna error 400."""
        response = client.post(
            '/termostato/temperatura_ambiente/',
            json={}
        )
        assert response.status_code == 400
        data = response.get_json()
        assert data['error']['mensaje'] == 'Campo requerido faltante'

    def test_post_temperatura_ambiente_sin_campo(self, client):
        """Verifica que POST sin campo 'ambiente' retorna error 400."""
        response = client.post(
            '/termostato/temperatura_ambiente/',
            json={'otro_campo': 25}
        )
        assert response.status_code == 400
        data = response.get_json()
        assert data['error']['mensaje'] == 'Campo requerido faltante'

    def test_post_temperatura_ambiente_fuera_rango(self, client):
        """Verifica que POST con valor fuera de rango retorna error 400."""
        response = client.post(
            '/termostato/temperatura_ambiente/',
            json={'ambiente': 100}
        )
        assert response.status_code == 400
        data = response.get_json()
        assert data['error']['mensaje'] == 'Valor fuera de rango'


class TestTemperaturaDeseada:
    """Tests para el endpoint /termostato/temperatura_deseada/."""

    def test_get_temperatura_deseada(self, client):
        """Verifica que GET retorna la temperatura deseada."""
        response = client.get('/termostato/temperatura_deseada/')
        assert response.status_code == 200
        data = response.get_json()
        assert 'temperatura_deseada' in data

    def test_post_temperatura_deseada_valido(self, client):
        """Verifica que POST con valor valido actualiza la temperatura."""
        response = client.post(
            '/termostato/temperatura_deseada/',
            json={'deseada': 22}
        )
        assert response.status_code == 201

    def test_post_temperatura_deseada_sin_campo(self, client):
        """Verifica que POST sin campo 'deseada' retorna error 400."""
        response = client.post(
            '/termostato/temperatura_deseada/',
            json={'temperatura': 22}
        )
        assert response.status_code == 400

    def test_post_temperatura_deseada_fuera_rango(self, client):
        """Verifica que POST con valor fuera de rango (15-30) retorna error."""
        response = client.post(
            '/termostato/temperatura_deseada/',
            json={'deseada': 35}
        )
        assert response.status_code == 400


class TestCargaBateria:
    """Tests para el endpoint /termostato/bateria/."""

    def test_get_carga_bateria(self, client):
        """Verifica que GET retorna la carga de bateria."""
        response = client.get('/termostato/bateria/')
        assert response.status_code == 200
        data = response.get_json()
        assert 'carga_bateria' in data

    def test_post_carga_bateria_valido(self, client):
        """Verifica que POST con valor valido actualiza la bateria."""
        response = client.post(
            '/termostato/bateria/',
            json={'bateria': 3.5}
        )
        assert response.status_code == 201

    def test_post_carga_bateria_sin_campo(self, client):
        """Verifica que POST sin campo 'bateria' retorna error 400."""
        response = client.post(
            '/termostato/bateria/',
            json={'carga': 3.5}
        )
        assert response.status_code == 400

    def test_post_carga_bateria_fuera_rango(self, client):
        """Verifica que POST con valor fuera de rango (0-5) retorna error."""
        response = client.post(
            '/termostato/bateria/',
            json={'bateria': 10.0}
        )
        assert response.status_code == 400


class TestEstadoClimatizador:
    """Tests para el endpoint /termostato/estado_climatizador/."""

    def test_get_estado_climatizador(self, client):
        """Verifica que GET retorna el estado del climatizador."""
        response = client.get('/termostato/estado_climatizador/')
        assert response.status_code == 200
        data = response.get_json()
        assert 'estado_climatizador' in data

    def test_post_estado_climatizador_valido(self, client):
        """Verifica que POST actualiza el estado del climatizador."""
        response = client.post(
            '/termostato/estado_climatizador/',
            json={'climatizador': 'enfriando'}
        )
        assert response.status_code == 201

        # Verificar que se actualizo
        response = client.get('/termostato/estado_climatizador/')
        assert response.get_json()['estado_climatizador'] == 'enfriando'

    def test_post_estado_climatizador_sin_campo(self, client):
        """Verifica que POST sin campo 'climatizador' retorna error 400."""
        response = client.post(
            '/termostato/estado_climatizador/',
            json={'estado': 'enfriando'}
        )
        assert response.status_code == 400


class TestIndicador:
    """Tests para el endpoint /termostato/indicador/."""

    def test_get_indicador(self, client):
        """Verifica que GET retorna el indicador."""
        response = client.get('/termostato/indicador/')
        assert response.status_code == 200
        data = response.get_json()
        assert 'indicador' in data

    def test_post_indicador_valido(self, client):
        """Verifica que POST actualiza el indicador."""
        response = client.post(
            '/termostato/indicador/',
            json={'indicador': 'BAJO'}
        )
        assert response.status_code == 201

    def test_post_indicador_sin_campo(self, client):
        """Verifica que POST sin campo 'indicador' retorna error 400."""
        response = client.post(
            '/termostato/indicador/',
            json={'valor': 'BAJO'}
        )
        assert response.status_code == 400


class TestHistorial:
    """Tests para el endpoint /termostato/historial/."""

    def test_get_historial(self, client):
        """Verifica que GET retorna el historial de temperaturas."""
        response = client.get('/termostato/historial/')
        assert response.status_code == 200
        data = response.get_json()
        assert 'historial' in data
        assert 'total' in data
        assert isinstance(data['historial'], list)

    def test_get_historial_con_limite(self, client):
        """Verifica que GET con parametro limite funciona."""
        response = client.get('/termostato/historial/?limite=5')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data['historial']) <= 5


class TestErrores:
    """Tests para manejo de errores."""

    def test_endpoint_no_existente_404(self, client):
        """Verifica que endpoints no existentes retornan 404."""
        response = client.get('/ruta/no/existente/')
        assert response.status_code == 404
        data = response.get_json()
        assert data['error']['mensaje'] == 'Recurso no encontrado'
        assert data['error']['codigo'] == 404

    def test_respuesta_error_formato_json(self, client):
        """Verifica que las respuestas de error son JSON valido."""
        response = client.get('/ruta/no/existente/')
        assert response.content_type == 'application/json'
        data = response.get_json()
        assert 'error' in data
        assert 'mensaje' in data['error']
        assert 'codigo' in data['error']
