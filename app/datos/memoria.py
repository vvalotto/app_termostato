"""
Implementacion en memoria del repositorio de historial.
"""
from typing import List, Optional

from app.datos.registro import RegistroTemperatura
from app.datos.repositorio import HistorialRepositorio


class HistorialRepositorioMemoria(HistorialRepositorio):
    """Repositorio de historial que almacena en memoria."""

    MAX_REGISTROS = 100

    def __init__(self):
        self._registros: List[RegistroTemperatura] = []

    def agregar(self, registro: RegistroTemperatura) -> None:
        """Agrega un registro al inicio (mas reciente primero)."""
        self._registros.insert(0, registro)
        if len(self._registros) > self.MAX_REGISTROS:
            self._registros = self._registros[:self.MAX_REGISTROS]

    def obtener(self, limite: Optional[int] = None) -> List[RegistroTemperatura]:
        """Obtiene registros, opcionalmente limitados."""
        if limite is None:
            return self._registros.copy()
        return self._registros[:limite]

    def cantidad(self) -> int:
        """Retorna la cantidad de registros almacenados."""
        return len(self._registros)

    def limpiar(self) -> None:
        """Elimina todos los registros."""
        self._registros = []
