"""
Capa de gestion de datos.
Provee repositorios y mappers para persistencia.
"""
from app.datos.registro import RegistroTemperatura
from app.datos.repositorio import HistorialRepositorio
from app.datos.mapper import HistorialMapper
from app.datos.memoria import HistorialRepositorioMemoria

__all__ = [
    'RegistroTemperatura',
    'HistorialRepositorio',
    'HistorialMapper',
    'HistorialRepositorioMemoria',
]
