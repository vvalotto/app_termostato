"""
Implementacion de persistencia en archivo JSON.
"""
import json
import os
from typing import Optional

from app.datos.persistidor import TermostatoPersistidor


class TermostatoPersistidorJSON(TermostatoPersistidor):
    """Persistidor que guarda el estado en un archivo JSON."""

    def __init__(self, ruta: str = "data/termostato_estado.json"):
        self._ruta = ruta

    def guardar(self, datos: dict) -> None:
        """Guarda el estado en archivo JSON."""
        directorio = os.path.dirname(self._ruta)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio)
        with open(self._ruta, 'w', encoding='utf-8') as archivo:
            json.dump(datos, archivo, indent=2, ensure_ascii=False)

    def cargar(self) -> Optional[dict]:
        """Carga el estado desde archivo JSON."""
        if not self.existe():
            return None
        with open(self._ruta, 'r', encoding='utf-8') as archivo:
            return json.load(archivo)

    def existe(self) -> bool:
        """Verifica si existe el archivo de estado."""
        return os.path.exists(self._ruta)
