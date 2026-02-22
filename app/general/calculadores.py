"""
Calculadores de indicadores del termostato.
Implementa el patrón Strategy para calcular el indicador de batería.
"""
from abc import ABC, abstractmethod

from app.configuracion.config import Config


class IndicadorCalculator(ABC):
    """Interfaz para calcular el indicador de carga de batería."""

    @abstractmethod
    def calcular(self, carga_bateria: float) -> str:
        """Calcula el indicador según la carga de batería.

        Args:
            carga_bateria: Nivel de carga de la batería

        Returns:
            str: Indicador calculado (ej: NORMAL, BAJO, CRITICO)
        """


class IndicadorCalculatorTresNiveles(IndicadorCalculator):
    """Calcula el indicador con tres niveles: NORMAL, BAJO, CRITICO."""

    def calcular(self, carga_bateria: float) -> str:
        """Retorna NORMAL si > 3.5, BAJO si >= 2.5, CRITICO en otro caso."""
        if carga_bateria > Config.INDICADOR_UMBRAL_NORMAL:
            return "NORMAL"
        if carga_bateria >= Config.INDICADOR_UMBRAL_BAJO:
            return "BAJO"
        return "CRITICO"


class IndicadorCalculatorCincoNiveles(IndicadorCalculator):
    """Calcula el indicador con cinco niveles: EXCELENTE, BUENO, NORMAL, BAJO, CRITICO."""

    def calcular(self, carga_bateria: float) -> str:
        """Retorna uno de 5 niveles según la carga de batería."""
        if carga_bateria > 4.5:
            return "EXCELENTE"
        if carga_bateria > 3.5:
            return "BUENO"
        if carga_bateria > 2.5:
            return "NORMAL"
        if carga_bateria > 1.5:
            return "BAJO"
        return "CRITICO"
