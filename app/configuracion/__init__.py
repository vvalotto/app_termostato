"""
Modulo de configuracion del sistema.
"""
from app.configuracion.config import Config

# Configurador se importa de forma diferida para evitar import circular
# con termostato.py que necesita Config
# Usar: from app.configuracion.configurador import Configurador

__all__ = ['Config']


def get_configurador():
    """Retorna la clase Configurador de forma diferida."""
    from app.configuracion.configurador import Configurador
    return Configurador
