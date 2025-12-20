"""
Configuración global de la aplicación.
Provee una instancia compartida del termostato (patrón Singleton).
"""
from .termostato import Termostato


class Configurador:
    """
    Clase de configuración que mantiene la instancia global del termostato.

    Attributes:
        termostato: Instancia única del termostato compartida por toda la aplicación
    """
    termostato = Termostato()
