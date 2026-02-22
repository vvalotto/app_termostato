"""Tests unitarios de IndicadorCalculator."""
import pytest

from app.general.calculadores import IndicadorCalculatorTresNiveles


@pytest.fixture
def calc():
    return IndicadorCalculatorTresNiveles()


class TestIndicadorCalculatorTresNiveles:

    def test_bateria_alta_retorna_normal(self, calc):
        assert calc.calcular(5.0) == "NORMAL"

    def test_bateria_sobre_umbral_normal_retorna_normal(self, calc):
        assert calc.calcular(3.6) == "NORMAL"

    def test_bateria_en_umbral_normal_retorna_bajo(self, calc):
        # 3.5 no es > 3.5, entonces es BAJO si >= 2.5
        assert calc.calcular(3.5) == "BAJO"

    def test_bateria_en_umbral_bajo_retorna_bajo(self, calc):
        assert calc.calcular(2.5) == "BAJO"

    def test_bateria_entre_umbrales_retorna_bajo(self, calc):
        assert calc.calcular(3.0) == "BAJO"

    def test_bateria_bajo_umbral_bajo_retorna_critico(self, calc):
        assert calc.calcular(2.4) == "CRITICO"

    def test_bateria_cero_retorna_critico(self, calc):
        assert calc.calcular(0.0) == "CRITICO"

    def test_retorna_string(self, calc):
        resultado = calc.calcular(4.0)
        assert isinstance(resultado, str)
