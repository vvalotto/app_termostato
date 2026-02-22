"""Tests unitarios de TermostatoService."""
import pytest
from unittest.mock import MagicMock

from app.general.calculadores import IndicadorCalculatorTresNiveles
from app.general.termostato_modelo import TermostatoModelo
from app.general.validators import TermostatoValidator
from app.servicios.termostato_service import TermostatoService


@pytest.fixture
def service():
    return TermostatoService(
        modelo=TermostatoModelo(),
        validator=TermostatoValidator(),
        indicador_calc=IndicadorCalculatorTresNiveles(),
    )


@pytest.fixture
def service_con_persistidor():
    persistidor = MagicMock()
    persistidor.existe.return_value = False
    return TermostatoService(
        modelo=TermostatoModelo(),
        validator=TermostatoValidator(),
        indicador_calc=IndicadorCalculatorTresNiveles(),
        persistidor=persistidor,
    )


class TestActualizarTemperaturaAmbiente:

    def test_valor_valido_actualiza_modelo(self, service):
        service.actualizar_temperatura_ambiente(30)
        assert service.modelo.temperatura_ambiente == 30

    def test_valor_invalido_lanza_error(self, service):
        with pytest.raises(ValueError):
            service.actualizar_temperatura_ambiente(99)

    def test_llama_persistidor_si_existe(self, service_con_persistidor):
        service_con_persistidor.actualizar_temperatura_ambiente(25)
        service_con_persistidor._persistidor.guardar.assert_called_once()


class TestActualizarTemperaturaDeseada:

    def test_valor_valido_actualiza_modelo(self, service):
        service.actualizar_temperatura_deseada(20)
        assert service.modelo.temperatura_deseada == 20

    def test_valor_invalido_lanza_error(self, service):
        with pytest.raises(ValueError):
            service.actualizar_temperatura_deseada(99)


class TestActualizarCargaBateria:

    def test_valor_valido_actualiza_modelo(self, service):
        service.actualizar_carga_bateria(3.0)
        assert service.modelo.carga_bateria == 3.0

    def test_valor_invalido_lanza_error(self, service):
        with pytest.raises(ValueError):
            service.actualizar_carga_bateria(10.0)


class TestActualizarEstadoClimatizador:

    def test_valor_valido_actualiza_modelo(self, service):
        service.actualizar_estado_climatizador("enfriando")
        assert service.modelo.estado_climatizador == "enfriando"

    def test_valor_invalido_lanza_error(self, service):
        with pytest.raises(ValueError):
            service.actualizar_estado_climatizador("modo_turbo")


class TestObtenerIndicador:

    def test_bateria_alta_retorna_normal(self, service):
        assert service.obtener_indicador() == "NORMAL"

    def test_bateria_baja_retorna_critico(self, service):
        service.actualizar_carga_bateria(1.0)
        assert service.obtener_indicador() == "CRITICO"


class TestCargarEstado:

    def test_sin_persistidor_no_falla(self, service):
        service.cargar_estado()  # no debe lanzar excepción

    def test_con_persistidor_carga_datos(self):
        persistidor = MagicMock()
        persistidor.existe.return_value = True
        persistidor.cargar.return_value = {
            'temperatura_ambiente': 28,
            'temperatura_deseada': 22,
            'carga_bateria': 2.0,
            'estado_climatizador': 'enfriando'
        }
        service = TermostatoService(
            modelo=TermostatoModelo(),
            validator=TermostatoValidator(),
            indicador_calc=IndicadorCalculatorTresNiveles(),
            persistidor=persistidor,
        )
        service.cargar_estado()
        assert service.modelo.temperatura_ambiente == 28
        assert service.modelo.estado_climatizador == "enfriando"
