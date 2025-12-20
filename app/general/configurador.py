"""
Configuración global de la aplicación.
Provee una instancia compartida del termostato (patrón Singleton).
"""
from .termostato import Termostato
from app.datos import (
    HistorialRepositorioMemoria,
    HistorialMapper,
    TermostatoPersistidorJSON
)


class Configurador:
    """
    Clase de configuración que mantiene la instancia global del termostato.

    Attributes:
        historial_repositorio: Repositorio para almacenar historial de temperaturas
        historial_mapper: Mapper para convertir registros a diccionarios
        persistidor: Persistidor para guardar estado en disco
        termostato: Instancia única del termostato compartida por toda la aplicación
    """
    historial_repositorio = HistorialRepositorioMemoria()
    historial_mapper = HistorialMapper()
    persistidor = TermostatoPersistidorJSON()
    termostato = Termostato(
        historial_repositorio=historial_repositorio,
        persistidor=persistidor
    )
    termostato.cargar_estado()
