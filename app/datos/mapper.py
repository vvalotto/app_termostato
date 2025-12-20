"""
Mapper para convertir entre objetos de dominio y diccionarios.
"""
from datetime import datetime

from app.datos.registro import RegistroTemperatura


class HistorialMapper:
    """Convierte entre RegistroTemperatura y diccionarios."""

    def a_dict(self, registro: RegistroTemperatura) -> dict:
        """Convierte un RegistroTemperatura a diccionario para respuesta JSON."""
        return {
            'temperatura': registro.temperatura,
            'timestamp': registro.timestamp.isoformat()
        }

    def desde_dict(self, datos: dict) -> RegistroTemperatura:
        """Convierte un diccionario a RegistroTemperatura."""
        return RegistroTemperatura(
            temperatura=datos['temperatura'],
            timestamp=datetime.fromisoformat(datos['timestamp'])
        )
