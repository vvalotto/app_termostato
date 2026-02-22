"""
Factory para crear instancias del termostato y sus dependencias.
Reemplaza el patrón Singleton del Configurador con un Factory puro.
"""
from app.general.termostato import Termostato
from app.datos import (
    HistorialRepositorioMemoria,
    HistorialMapper,
    TermostatoPersistidorJSON
)
from app.configuracion.config import Config


class TermostatoFactory:
    """Factory puro para crear instancias de Termostato y sus dependencias.

    Permite inyección de dependencias y facilita el testing aislado.
    Cada llamada retorna una nueva instancia independiente (no singleton).
    """

    @staticmethod
    def crear_termostato(
        historial_repositorio=None,
        persistidor=None,
        config=None
    ) -> Termostato:
        """Crea una nueva instancia de Termostato con sus dependencias.

        Args:
            historial_repositorio: Repositorio de historial (default: en memoria)
            persistidor: Persistidor de estado (default: JSON)
            config: Clase de configuración (default: Config)

        Returns:
            Nueva instancia de Termostato con estado cargado
        """
        cfg = config or Config
        repo = historial_repositorio or TermostatoFactory.crear_historial_repositorio()
        persist = persistidor or TermostatoFactory.crear_persistidor()

        termostato = Termostato(
            historial_repositorio=repo,
            persistidor=persist,
            temperatura_ambiente_inicial=cfg.TEMPERATURA_AMBIENTE_INICIAL,
            temperatura_deseada_inicial=cfg.TEMPERATURA_DESEADA_INICIAL,
            carga_bateria_inicial=cfg.CARGA_BATERIA_INICIAL
        )
        termostato.cargar_estado()
        return termostato

    @staticmethod
    def crear_historial_repositorio() -> HistorialRepositorioMemoria:
        """Crea un nuevo repositorio de historial en memoria."""
        return HistorialRepositorioMemoria()

    @staticmethod
    def crear_historial_mapper() -> HistorialMapper:
        """Crea un nuevo mapper de historial."""
        return HistorialMapper()

    @staticmethod
    def crear_persistidor(ruta: str = None) -> TermostatoPersistidorJSON:
        """Crea un nuevo persistidor JSON.

        Args:
            ruta: Ruta del archivo JSON (default: ruta configurada)
        """
        return TermostatoPersistidorJSON(ruta) if ruta else TermostatoPersistidorJSON()
