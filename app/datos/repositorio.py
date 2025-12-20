"""
Interface abstracta para repositorios de historial.
Define el contrato que deben cumplir las implementaciones.
"""
from abc import ABC, abstractmethod
from typing import List, Optional

from app.datos.registro import RegistroTemperatura


class HistorialRepositorio(ABC):
    """Interface abstracta para el repositorio de historial de temperaturas."""

    @abstractmethod
    def agregar(self, registro: RegistroTemperatura) -> None:
        """Agrega un nuevo registro al historial."""
        pass

    @abstractmethod
    def obtener(self, limite: Optional[int] = None) -> List[RegistroTemperatura]:
        """Obtiene registros del historial, ordenados del mas reciente al mas antiguo."""
        pass

    @abstractmethod
    def cantidad(self) -> int:
        """Retorna la cantidad total de registros en el historial."""
        pass

    @abstractmethod
    def limpiar(self) -> None:
        """Elimina todos los registros del historial."""
        pass
