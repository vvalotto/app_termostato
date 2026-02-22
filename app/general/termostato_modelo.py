"""
Modelo de datos puro del termostato.
Representa el estado del dispositivo sin lógica de negocio.
"""
from dataclasses import dataclass


@dataclass
class TermostatoModelo:
    """Estado del termostato como modelo de datos puro."""
    temperatura_ambiente: int = 20
    temperatura_deseada: int = 24
    carga_bateria: float = 5.0
    estado_climatizador: str = "apagado"
