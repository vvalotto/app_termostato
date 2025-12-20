"""
Interface abstracta para persistencia del estado del termostato.
"""
from abc import ABC, abstractmethod
from typing import Optional


class TermostatoPersistidor(ABC):
    """Interface para persistir el estado del termostato."""

    @abstractmethod
    def guardar(self, datos: dict) -> None:
        """Guarda el estado del termostato."""
        pass

    @abstractmethod
    def cargar(self) -> Optional[dict]:
        """Carga el estado del termostato. Retorna None si no existe."""
        pass

    @abstractmethod
    def existe(self) -> bool:
        """Verifica si existe un estado guardado."""
        pass
