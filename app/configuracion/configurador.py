"""
Configuración global de la aplicación.
Provee una instancia compartida del termostato (patrón Singleton).
"""
from app.general.termostato import Termostato
from app.datos import (
    HistorialRepositorioMemoria,
    HistorialMapper,
    TermostatoPersistidorJSON
)
from app.configuracion.config import Config


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
        persistidor=persistidor,
        temperatura_ambiente_inicial=Config.TEMPERATURA_AMBIENTE_INICIAL,
        temperatura_deseada_inicial=Config.TEMPERATURA_DESEADA_INICIAL,
        carga_bateria_inicial=Config.CARGA_BATERIA_INICIAL
    )
    termostato.cargar_estado()
