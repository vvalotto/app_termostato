"""
Modelo de datos del termostato.
Define la clase Termostato que representa el estado del dispositivo.
"""
from datetime import datetime

from app.configuracion.config import Config


class Termostato:
    """
    Representa un termostato con sus propiedades de temperatura y estado.

    Attributes:
        temperatura_ambiente: Temperatura actual del ambiente (default: 20)
        temperatura_deseada: Temperatura objetivo configurada (default: 30)
        carga_bateria: Carga de la batería (default: 5.0)
        estado_climatizador: Estado del climatizador (default: "apagado")
        indicador: Indicador calculado segun nivel de bateria (NORMAL/BAJO/CRITICO)
    """

    def __init__(self, historial_repositorio=None, persistidor=None,
                 temperatura_ambiente_inicial=20, temperatura_deseada_inicial=24,
                 carga_bateria_inicial=5.0):
        """Inicializa el termostato con valores por defecto o configurados.

        Args:
            historial_repositorio: Repositorio para almacenar historial de temperaturas (opcional)
            persistidor: Persistidor para guardar estado en disco (opcional)
            temperatura_ambiente_inicial: Temperatura ambiente inicial (default: 20)
            temperatura_deseada_inicial: Temperatura deseada inicial (default: 24)
            carga_bateria_inicial: Carga de bateria inicial (default: 5.0)
        """
        self._historial_repositorio = historial_repositorio
        self._persistidor = persistidor
        self._temperatura_ambiente = temperatura_ambiente_inicial
        self._temperatura_deseada = temperatura_deseada_inicial
        self._carga_bateria = carga_bateria_inicial
        self._estado_climatizador = "apagado"

    @property
    def temperatura_ambiente(self):
        """Obtiene la temperatura ambiente actual."""
        return self._temperatura_ambiente

    @temperatura_ambiente.setter
    def temperatura_ambiente(self, valor):
        """Establece la temperatura ambiente (rango configurable)."""
        valor = int(valor)
        if not (Config.TEMPERATURA_AMBIENTE_MIN <= valor <= Config.TEMPERATURA_AMBIENTE_MAX):
            raise ValueError(
                f"temperatura_ambiente debe estar entre "
                f"{Config.TEMPERATURA_AMBIENTE_MIN} y {Config.TEMPERATURA_AMBIENTE_MAX}"
            )
        self._temperatura_ambiente = valor
        self._registrar_en_historial(valor)
        self._guardar_estado()

    @property
    def temperatura_deseada(self):
        """Obtiene la temperatura deseada configurada."""
        return self._temperatura_deseada

    @temperatura_deseada.setter
    def temperatura_deseada(self, valor):
        """Establece la temperatura deseada (rango configurable)."""
        valor = int(valor)
        if not (Config.TEMPERATURA_DESEADA_MIN <= valor <= Config.TEMPERATURA_DESEADA_MAX):
            raise ValueError(
                f"temperatura_deseada debe estar entre "
                f"{Config.TEMPERATURA_DESEADA_MIN} y {Config.TEMPERATURA_DESEADA_MAX}"
            )
        self._temperatura_deseada = valor
        self._guardar_estado()

    @property
    def carga_bateria(self):
        """Obtiene la carga de la batería."""
        return self._carga_bateria

    @carga_bateria.setter
    def carga_bateria(self, valor):
        """Establece la carga de la batería (rango configurable)."""
        valor = round(float(valor), 2)
        if not (Config.CARGA_BATERIA_MIN <= valor <= Config.CARGA_BATERIA_MAX):
            raise ValueError(
                f"carga_bateria debe estar entre "
                f"{Config.CARGA_BATERIA_MIN} y {Config.CARGA_BATERIA_MAX}"
            )
        self._carga_bateria = valor
        self._guardar_estado()

    @property
    def estado_climatizador(self):
        """Obtiene el estado del climatizador (encendido/enfriando/calentando)."""
        return self._estado_climatizador

    @estado_climatizador.setter
    def estado_climatizador(self, valor):
        """Establece el estado del climatizador."""
        self._estado_climatizador = str(valor)
        self._guardar_estado()

    @property
    def indicador(self):
        """Calcula el indicador de carga basado en el nivel de bateria.

        Returns:
            str: NORMAL si bateria > 3.5, BAJO si >= 2.5, CRITICO si < 2.5
        """
        if self._carga_bateria > Config.INDICADOR_UMBRAL_NORMAL:
            return "NORMAL"
        if self._carga_bateria >= Config.INDICADOR_UMBRAL_BAJO:
            return "BAJO"
        return "CRITICO"

    def _guardar_estado(self):
        """Persiste el estado actual si hay persistidor configurado."""
        if self._persistidor:
            datos = {
                'temperatura_ambiente': self._temperatura_ambiente,
                'temperatura_deseada': self._temperatura_deseada,
                'carga_bateria': self._carga_bateria,
                'estado_climatizador': self._estado_climatizador,
                'indicador': self.indicador
            }
            self._persistidor.guardar(datos)

    def cargar_estado(self):
        """Carga el estado desde el persistidor si existe."""
        if self._persistidor and self._persistidor.existe():
            datos = self._persistidor.cargar()
            if datos:
                self._temperatura_ambiente = datos.get('temperatura_ambiente', 20)
                self._temperatura_deseada = datos.get('temperatura_deseada', 24)
                self._carga_bateria = datos.get('carga_bateria', 5.0)
                self._estado_climatizador = datos.get('estado_climatizador', 'apagado')
                # indicador se calcula dinamicamente basado en carga_bateria

    def _registrar_en_historial(self, temperatura):
        """Registra una temperatura en el historial si hay repositorio configurado."""
        if self._historial_repositorio:
            from app.datos import RegistroTemperatura
            registro = RegistroTemperatura(
                temperatura=temperatura,
                timestamp=datetime.now()
            )
            self._historial_repositorio.agregar(registro)
