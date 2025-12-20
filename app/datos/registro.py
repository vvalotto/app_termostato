"""
Modelo de dominio para registros de temperatura.
"""
from dataclasses import dataclass
from datetime import datetime


@dataclass
class RegistroTemperatura:
    """Representa un registro de temperatura en un momento dado."""
    temperatura: int
    timestamp: datetime
