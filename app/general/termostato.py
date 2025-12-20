"""
Modelo de datos del termostato.
Define la clase Termostato que representa el estado del dispositivo.
"""


class Termostato:
    """
    Representa un termostato con sus propiedades de temperatura y estado.

    Attributes:
        temperatura_ambiente: Temperatura actual del ambiente (default: 20)
        temperatura_deseada: Temperatura objetivo configurada (default: 30)
        carga_bateria: Carga de la batería (default: 5.0)
        estado_climatizador: Estado del climatizador (default: "apagado")
        indicador: Indicador de carga del dispositivo (default: "NORMAL")
    """

    def __init__(self):
        """Inicializa el termostato con valores por defecto."""
        self._temperatura_ambiente = 20
        self._temperatura_deseada = 24
        self._carga_bateria = 5.0
        self._estado_climatizador = "apagado"
        self._indicador = "NORMAL"

    @property
    def temperatura_ambiente(self):
        """Obtiene la temperatura ambiente actual."""
        return self._temperatura_ambiente

    @temperatura_ambiente.setter
    def temperatura_ambiente(self, valor):
        """Establece la temperatura ambiente (0-50°C)."""
        valor = int(valor)
        if not (0 <= valor <= 50):
            raise ValueError("temperatura_ambiente debe estar entre 0 y 50")
        self._temperatura_ambiente = valor

    @property
    def temperatura_deseada(self):
        """Obtiene la temperatura deseada configurada."""
        return self._temperatura_deseada

    @temperatura_deseada.setter
    def temperatura_deseada(self, valor):
        """Establece la temperatura deseada (15-30°C)."""
        valor = int(valor)
        if not (15 <= valor <= 30):
            raise ValueError("temperatura_deseada debe estar entre 15 y 30")
        self._temperatura_deseada = valor

    @property
    def carga_bateria(self):
        """Obtiene la carga de la batería."""
        return self._carga_bateria

    @carga_bateria.setter
    def carga_bateria(self, valor):
        """Establece la carga de la batería."""
        self._carga_bateria = round(float(valor), 2)

    @property
    def estado_climatizador(self):
        """Obtiene el estado del climatizador (encendido/enfriando/calentando)."""
        return self._estado_climatizador

    @estado_climatizador.setter
    def estado_climatizador(self, valor):
        """Establece el estado del climatizador."""
        self._estado_climatizador = str(valor)

    @property
    def indicador(self):
        """Obtiene el indicador de carga del dispositivo."""
        return self._indicador

    @indicador.setter
    def indicador(self, valor):
        """Establece el indicador de carga del dispositivo."""
        self._indicador = str(valor)
