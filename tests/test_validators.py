"""Tests unitarios de TermostatoValidator."""
import pytest

from app.general.validators import TermostatoValidator


@pytest.fixture
def validator():
    return TermostatoValidator()


class TestValidarTemperaturaAmbiente:

    def test_valor_valido_retorna_int(self, validator):
        assert validator.validar_temperatura_ambiente(25) == 25

    def test_convierte_string_a_int(self, validator):
        assert validator.validar_temperatura_ambiente("30") == 30

    def test_limite_minimo_valido(self, validator):
        assert validator.validar_temperatura_ambiente(0) == 0

    def test_limite_maximo_valido(self, validator):
        assert validator.validar_temperatura_ambiente(50) == 50

    def test_por_debajo_minimo_lanza_error(self, validator):
        with pytest.raises(ValueError, match="temperatura_ambiente"):
            validator.validar_temperatura_ambiente(-1)

    def test_por_encima_maximo_lanza_error(self, validator):
        with pytest.raises(ValueError, match="temperatura_ambiente"):
            validator.validar_temperatura_ambiente(51)


class TestValidarTemperaturaDeseada:

    def test_valor_valido_retorna_int(self, validator):
        assert validator.validar_temperatura_deseada(22) == 22

    def test_convierte_string_a_int(self, validator):
        assert validator.validar_temperatura_deseada("20") == 20

    def test_limite_minimo_valido(self, validator):
        assert validator.validar_temperatura_deseada(15) == 15

    def test_limite_maximo_valido(self, validator):
        assert validator.validar_temperatura_deseada(30) == 30

    def test_por_debajo_minimo_lanza_error(self, validator):
        with pytest.raises(ValueError, match="temperatura_deseada"):
            validator.validar_temperatura_deseada(14)

    def test_por_encima_maximo_lanza_error(self, validator):
        with pytest.raises(ValueError, match="temperatura_deseada"):
            validator.validar_temperatura_deseada(31)


class TestValidarCargaBateria:

    def test_valor_valido_retorna_float(self, validator):
        assert validator.validar_carga_bateria(3.5) == 3.5

    def test_convierte_int_a_float(self, validator):
        result = validator.validar_carga_bateria(4)
        assert isinstance(result, float)
        assert result == 4.0

    def test_limite_minimo_valido(self, validator):
        assert validator.validar_carga_bateria(0.0) == 0.0

    def test_limite_maximo_valido(self, validator):
        assert validator.validar_carga_bateria(5.0) == 5.0

    def test_por_debajo_minimo_lanza_error(self, validator):
        with pytest.raises(ValueError, match="carga_bateria"):
            validator.validar_carga_bateria(-0.1)

    def test_por_encima_maximo_lanza_error(self, validator):
        with pytest.raises(ValueError, match="carga_bateria"):
            validator.validar_carga_bateria(5.1)


class TestValidarEstadoClimatizador:

    def test_apagado_valido(self, validator):
        assert validator.validar_estado_climatizador("apagado") == "apagado"

    def test_encendido_valido(self, validator):
        assert validator.validar_estado_climatizador("encendido") == "encendido"

    def test_enfriando_valido(self, validator):
        assert validator.validar_estado_climatizador("enfriando") == "enfriando"

    def test_calentando_valido(self, validator):
        assert validator.validar_estado_climatizador("calentando") == "calentando"

    def test_normaliza_mayusculas(self, validator):
        assert validator.validar_estado_climatizador("APAGADO") == "apagado"

    def test_normaliza_espacios(self, validator):
        assert validator.validar_estado_climatizador("  apagado  ") == "apagado"

    def test_estado_invalido_lanza_error(self, validator):
        with pytest.raises(ValueError, match="estado_climatizador"):
            validator.validar_estado_climatizador("standby")

    def test_vacio_lanza_error(self, validator):
        with pytest.raises(ValueError, match="estado_climatizador"):
            validator.validar_estado_climatizador("")
