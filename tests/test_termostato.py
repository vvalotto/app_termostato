"""
Tests unitarios para la clase Termostato.
TER-12: Tests unitarios del modelo
"""
from unittest.mock import Mock

import pytest

from app.general.termostato import Termostato


class TestTermostatoValoresDefault:
    """Tests para verificar valores por defecto del termostato."""

    def test_temperatura_ambiente_default(self):
        """Verifica que la temperatura ambiente por defecto es 20."""
        termostato = Termostato()
        assert termostato.temperatura_ambiente == 20

    def test_temperatura_deseada_default(self):
        """Verifica que la temperatura deseada por defecto es 24."""
        termostato = Termostato()
        assert termostato.temperatura_deseada == 24

    def test_carga_bateria_default(self):
        """Verifica que la carga de bateria por defecto es 5.0."""
        termostato = Termostato()
        assert termostato.carga_bateria == 5.0

    def test_estado_climatizador_default(self):
        """Verifica que el estado del climatizador por defecto es 'apagado'."""
        termostato = Termostato()
        assert termostato.estado_climatizador == "apagado"

    def test_indicador_default(self):
        """Verifica que el indicador por defecto es 'NORMAL'."""
        termostato = Termostato()
        assert termostato.indicador == "NORMAL"


class TestTemperaturaAmbiente:
    """Tests para la propiedad temperatura_ambiente."""

    def test_temperatura_ambiente_set_valido(self):
        """Verifica que se puede establecer un valor valido de temperatura ambiente."""
        termostato = Termostato()
        termostato.temperatura_ambiente = 25
        assert termostato.temperatura_ambiente == 25

    def test_temperatura_ambiente_set_minimo(self):
        """Verifica que se puede establecer el valor minimo (0)."""
        termostato = Termostato()
        termostato.temperatura_ambiente = 0
        assert termostato.temperatura_ambiente == 0

    def test_temperatura_ambiente_set_maximo(self):
        """Verifica que se puede establecer el valor maximo (50)."""
        termostato = Termostato()
        termostato.temperatura_ambiente = 50
        assert termostato.temperatura_ambiente == 50

    def test_temperatura_ambiente_set_invalido_menor(self):
        """Verifica que valores menores al minimo lanzan ValueError."""
        termostato = Termostato()
        with pytest.raises(ValueError) as excinfo:
            termostato.temperatura_ambiente = -1
        assert "temperatura_ambiente debe estar entre" in str(excinfo.value)

    def test_temperatura_ambiente_set_invalido_mayor(self):
        """Verifica que valores mayores al maximo lanzan ValueError."""
        termostato = Termostato()
        with pytest.raises(ValueError) as excinfo:
            termostato.temperatura_ambiente = 51
        assert "temperatura_ambiente debe estar entre" in str(excinfo.value)

    def test_temperatura_ambiente_conversion_a_int(self):
        """Verifica que valores float se convierten a int."""
        termostato = Termostato()
        termostato.temperatura_ambiente = 25.7
        assert termostato.temperatura_ambiente == 25
        assert isinstance(termostato.temperatura_ambiente, int)

    def test_temperatura_ambiente_conversion_string(self):
        """Verifica que valores string numericos se convierten a int."""
        termostato = Termostato()
        termostato.temperatura_ambiente = "30"
        assert termostato.temperatura_ambiente == 30


class TestTemperaturaDeseada:
    """Tests para la propiedad temperatura_deseada."""

    def test_temperatura_deseada_rango_valido(self):
        """Verifica que se puede establecer un valor dentro del rango (15-30)."""
        termostato = Termostato()
        termostato.temperatura_deseada = 22
        assert termostato.temperatura_deseada == 22

    def test_temperatura_deseada_rango_minimo(self):
        """Verifica que se puede establecer el valor minimo (15)."""
        termostato = Termostato()
        termostato.temperatura_deseada = 15
        assert termostato.temperatura_deseada == 15

    def test_temperatura_deseada_rango_maximo(self):
        """Verifica que se puede establecer el valor maximo (30)."""
        termostato = Termostato()
        termostato.temperatura_deseada = 30
        assert termostato.temperatura_deseada == 30

    def test_temperatura_deseada_invalido_menor(self):
        """Verifica que valores menores al minimo lanzan ValueError."""
        termostato = Termostato()
        with pytest.raises(ValueError) as excinfo:
            termostato.temperatura_deseada = 14
        assert "temperatura_deseada debe estar entre" in str(excinfo.value)

    def test_temperatura_deseada_invalido_mayor(self):
        """Verifica que valores mayores al maximo lanzan ValueError."""
        termostato = Termostato()
        with pytest.raises(ValueError) as excinfo:
            termostato.temperatura_deseada = 31
        assert "temperatura_deseada debe estar entre" in str(excinfo.value)


class TestCargaBateria:
    """Tests para la propiedad carga_bateria."""

    def test_carga_bateria_redondeo(self):
        """Verifica que la carga de bateria se redondea a 2 decimales."""
        termostato = Termostato()
        termostato.carga_bateria = 3.14159
        assert termostato.carga_bateria == 3.14

    def test_carga_bateria_redondeo_hacia_arriba(self):
        """Verifica redondeo hacia arriba cuando corresponde."""
        termostato = Termostato()
        termostato.carga_bateria = 2.555
        assert termostato.carga_bateria == 2.56

    def test_carga_bateria_rango_minimo(self):
        """Verifica que se puede establecer el valor minimo (0.0)."""
        termostato = Termostato()
        termostato.carga_bateria = 0.0
        assert termostato.carga_bateria == 0.0

    def test_carga_bateria_rango_maximo(self):
        """Verifica que se puede establecer el valor maximo (5.0)."""
        termostato = Termostato()
        termostato.carga_bateria = 5.0
        assert termostato.carga_bateria == 5.0

    def test_carga_bateria_invalido_negativo(self):
        """Verifica que valores negativos lanzan ValueError."""
        termostato = Termostato()
        with pytest.raises(ValueError) as excinfo:
            termostato.carga_bateria = -0.1
        assert "carga_bateria debe estar entre" in str(excinfo.value)

    def test_carga_bateria_invalido_mayor(self):
        """Verifica que valores mayores al maximo lanzan ValueError."""
        termostato = Termostato()
        with pytest.raises(ValueError) as excinfo:
            termostato.carga_bateria = 5.01
        assert "carga_bateria debe estar entre" in str(excinfo.value)

    def test_carga_bateria_conversion_int_a_float(self):
        """Verifica que valores int se convierten a float."""
        termostato = Termostato()
        termostato.carga_bateria = 3
        assert termostato.carga_bateria == 3.0
        assert isinstance(termostato.carga_bateria, float)


class TestEstadoClimatizador:
    """Tests para la propiedad estado_climatizador."""

    def test_estado_climatizador_valores(self):
        """Verifica que se pueden establecer diferentes estados."""
        termostato = Termostato()

        termostato.estado_climatizador = "encendido"
        assert termostato.estado_climatizador == "encendido"

        termostato.estado_climatizador = "enfriando"
        assert termostato.estado_climatizador == "enfriando"

        termostato.estado_climatizador = "calentando"
        assert termostato.estado_climatizador == "calentando"

        termostato.estado_climatizador = "apagado"
        assert termostato.estado_climatizador == "apagado"

    def test_estado_climatizador_conversion_a_string(self):
        """Verifica que valores no string se convierten a string."""
        termostato = Termostato()
        termostato.estado_climatizador = 123
        assert termostato.estado_climatizador == "123"
        assert isinstance(termostato.estado_climatizador, str)


class TestIndicador:
    """Tests para la propiedad indicador."""

    def test_indicador_valores(self):
        """Verifica que se pueden establecer diferentes valores de indicador."""
        termostato = Termostato()

        termostato.indicador = "NORMAL"
        assert termostato.indicador == "NORMAL"

        termostato.indicador = "BAJO"
        assert termostato.indicador == "BAJO"

        termostato.indicador = "CRITICO"
        assert termostato.indicador == "CRITICO"

    def test_indicador_conversion_a_string(self):
        """Verifica que valores no string se convierten a string."""
        termostato = Termostato()
        termostato.indicador = 456
        assert termostato.indicador == "456"


class TestInicializacionPersonalizada:
    """Tests para inicializacion con valores personalizados."""

    def test_inicializacion_con_valores_personalizados(self):
        """Verifica que se pueden pasar valores iniciales al constructor."""
        termostato = Termostato(
            temperatura_ambiente_inicial=25,
            temperatura_deseada_inicial=20,
            carga_bateria_inicial=3.5
        )
        assert termostato.temperatura_ambiente == 25
        assert termostato.temperatura_deseada == 20
        assert termostato.carga_bateria == 3.5


class TestPersistencia:
    """Tests para la funcionalidad de persistencia."""

    def test_guardar_estado_con_persistidor(self):
        """Verifica que se llama al persistidor cuando se modifica una propiedad."""
        mock_persistidor = Mock()
        termostato = Termostato(persistidor=mock_persistidor)

        termostato.temperatura_ambiente = 25

        mock_persistidor.guardar.assert_called()
        datos_guardados = mock_persistidor.guardar.call_args[0][0]
        assert datos_guardados['temperatura_ambiente'] == 25

    def test_cargar_estado_existente(self):
        """Verifica que se carga el estado desde el persistidor."""
        mock_persistidor = Mock()
        mock_persistidor.existe.return_value = True
        mock_persistidor.cargar.return_value = {
            'temperatura_ambiente': 30,
            'temperatura_deseada': 25,
            'carga_bateria': 4.0,
            'estado_climatizador': 'enfriando',
            'indicador': 'BAJO'
        }

        termostato = Termostato(persistidor=mock_persistidor)
        termostato.cargar_estado()

        assert termostato.temperatura_ambiente == 30
        assert termostato.temperatura_deseada == 25
        assert termostato.carga_bateria == 4.0
        assert termostato.estado_climatizador == 'enfriando'
        assert termostato.indicador == 'BAJO'

    def test_cargar_estado_sin_persistidor(self):
        """Verifica que no hay error al cargar estado sin persistidor."""
        termostato = Termostato()
        termostato.cargar_estado()  # No debe lanzar excepcion
        assert termostato.temperatura_ambiente == 20  # Mantiene default


class TestHistorial:
    """Tests para la funcionalidad de historial."""

    def test_registrar_en_historial_al_cambiar_temperatura(self):
        """Verifica que se registra en historial al cambiar temperatura ambiente."""
        mock_repositorio = Mock()
        termostato = Termostato(historial_repositorio=mock_repositorio)

        termostato.temperatura_ambiente = 25

        mock_repositorio.agregar.assert_called_once()
        registro = mock_repositorio.agregar.call_args[0][0]
        assert registro.temperatura == 25
