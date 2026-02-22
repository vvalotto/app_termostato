"""
Facade del termostato.
Mantiene la interfaz pública original delegando a componentes especializados.
"""
from app.general.calculadores import IndicadorCalculatorTresNiveles
from app.general.termostato_modelo import TermostatoModelo
from app.general.validators import TermostatoValidator
from app.servicios.termostato_service import TermostatoService


class Termostato:
    """
    Facade del termostato con interfaz pública estable.

    Delega la lógica de validación, cálculo y persistencia a componentes
    especializados (TermostatoService, TermostatoValidator, IndicadorCalculator).

    Attributes:
        temperatura_ambiente: Temperatura actual del ambiente
        temperatura_deseada: Temperatura objetivo configurada
        carga_bateria: Carga de la batería
        estado_climatizador: Estado del climatizador
        indicador: Indicador calculado según nivel de batería (NORMAL/BAJO/CRITICO)
    """

    def __init__(self, historial_repositorio=None, persistidor=None,
                 temperatura_ambiente_inicial=20, temperatura_deseada_inicial=24,
                 carga_bateria_inicial=5.0):
        modelo = TermostatoModelo(
            temperatura_ambiente=temperatura_ambiente_inicial,
            temperatura_deseada=temperatura_deseada_inicial,
            carga_bateria=carga_bateria_inicial,
        )
        self._service = TermostatoService(
            modelo=modelo,
            validator=TermostatoValidator(),
            indicador_calc=IndicadorCalculatorTresNiveles(),
            persistidor=persistidor,
            historial_repositorio=historial_repositorio,
        )

    @property
    def temperatura_ambiente(self):
        """Obtiene la temperatura ambiente actual."""
        return self._service.modelo.temperatura_ambiente

    @temperatura_ambiente.setter
    def temperatura_ambiente(self, valor):
        """Establece la temperatura ambiente (rango configurable)."""
        self._service.actualizar_temperatura_ambiente(valor)

    @property
    def temperatura_deseada(self):
        """Obtiene la temperatura deseada configurada."""
        return self._service.modelo.temperatura_deseada

    @temperatura_deseada.setter
    def temperatura_deseada(self, valor):
        """Establece la temperatura deseada (rango configurable)."""
        self._service.actualizar_temperatura_deseada(valor)

    @property
    def carga_bateria(self):
        """Obtiene la carga de la batería."""
        return self._service.modelo.carga_bateria

    @carga_bateria.setter
    def carga_bateria(self, valor):
        """Establece la carga de la batería (rango configurable)."""
        self._service.actualizar_carga_bateria(valor)

    @property
    def estado_climatizador(self):
        """Obtiene el estado del climatizador."""
        return self._service.modelo.estado_climatizador

    @estado_climatizador.setter
    def estado_climatizador(self, valor):
        """Establece el estado del climatizador."""
        self._service.actualizar_estado_climatizador(valor)

    @property
    def indicador(self):
        """Calcula el indicador de carga basado en el nivel de batería."""
        return self._service.obtener_indicador()

    def cargar_estado(self):
        """Carga el estado desde el persistidor si existe."""
        self._service.cargar_estado()
