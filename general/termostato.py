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
        carga_bateria: Nivel de carga de la batería (default: 5.0)
        estado_climatizador: Estado del climatizador (default: "apagado")
        nivel_de_carga: Nivel de carga del dispositivo (default: "0")
    """

    def __init__(self):
        """Inicializa el termostato con valores por defecto."""
        self._temperatura_ambiente = 20
        self._temperatura_deseada = 24
        self._carga_bateria = 5.0
        self._estado_climatizador = "apagado"
        self._nivel_de_carga = "normal"

    @property
    def temperatura_ambiente(self):
        """Obtiene la temperatura ambiente actual."""
        return self._temperatura_ambiente

    @temperatura_ambiente.setter
    def temperatura_ambiente(self, valor):
        """Establece la temperatura ambiente."""
        self._temperatura_ambiente = int(valor)

    @property
    def temperatura_deseada(self):
        """Obtiene la temperatura deseada configurada."""
        return self._temperatura_deseada

    @temperatura_deseada.setter
    def temperatura_deseada(self, valor):
        """Establece la temperatura deseada."""
        self._temperatura_deseada = int(valor)

    @property
    def carga_bateria(self):
        """Obtiene el nivel de carga de la batería."""
        return self._carga_bateria

    @carga_bateria.setter
    def carga_bateria(self, valor):
        """Establece el nivel de carga de la batería."""
        self._carga_bateria = round(float(valor), 2)

    @property
    def estado_climatizador(self):
        """Obtiene el estado del climatizador (encendido/apagado)."""
        return self._estado_climatizador

    @estado_climatizador.setter
    def estado_climatizador(self, valor):
        """Establece el estado del climatizador."""
        self._estado_climatizador = str(valor)

    @property
    def nivel_de_carga(self):
        """Obtiene el nivel de carga del dispositivo."""
        return self._nivel_de_carga

    @nivel_de_carga.setter
    def nivel_de_carga(self, valor):
        """Establece el nivel de carga del dispositivo."""
        self._nivel_de_carga = str(valor)
