"""
Capa de gestion de datos.
Provee repositorios, mappers y persistidores.
"""
from app.datos.registro import RegistroTemperatura
from app.datos.repositorio import HistorialRepositorio
from app.datos.mapper import HistorialMapper
from app.datos.memoria import HistorialRepositorioMemoria
from app.datos.persistidor import TermostatoPersistidor
from app.datos.persistidor_json import TermostatoPersistidorJSON

__all__ = [
    'RegistroTemperatura',
    'HistorialRepositorio',
    'HistorialMapper',
    'HistorialRepositorioMemoria',
    'TermostatoPersistidor',
    'TermostatoPersistidorJSON',
]
