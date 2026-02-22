"""
Servicio de orquestación del termostato.
Coordina validación, modelo, persistencia, historial y cálculo de indicadores.
"""
from datetime import datetime

from app.datos.registro import RegistroTemperatura
from app.general.calculadores import IndicadorCalculator
from app.general.termostato_modelo import TermostatoModelo
from app.general.validators import TermostatoValidator


class TermostatoService:
    """Orquesta las operaciones del termostato delegando a componentes especializados."""

    def __init__(self, modelo: TermostatoModelo, validator: TermostatoValidator,
                 indicador_calc: IndicadorCalculator, persistidor=None,
                 historial_repositorio=None):
        self._modelo = modelo
        self._validator = validator
        self._indicador_calc = indicador_calc
        self._persistidor = persistidor
        self._historial_repositorio = historial_repositorio

    def actualizar_temperatura_ambiente(self, valor) -> None:
        """Valida, actualiza, persiste y registra en historial."""
        self._modelo.temperatura_ambiente = self._validator.validar_temperatura_ambiente(valor)
        self._registrar_en_historial(self._modelo.temperatura_ambiente)
        self._guardar_estado()

    def actualizar_temperatura_deseada(self, valor) -> None:
        """Valida, actualiza y persiste."""
        self._modelo.temperatura_deseada = self._validator.validar_temperatura_deseada(valor)
        self._guardar_estado()

    def actualizar_carga_bateria(self, valor) -> None:
        """Valida, actualiza y persiste."""
        self._modelo.carga_bateria = self._validator.validar_carga_bateria(valor)
        self._guardar_estado()

    def actualizar_estado_climatizador(self, valor) -> None:
        """Valida, actualiza y persiste."""
        self._modelo.estado_climatizador = self._validator.validar_estado_climatizador(valor)
        self._guardar_estado()

    def obtener_indicador(self) -> str:
        """Calcula el indicador basado en la carga de batería actual."""
        return self._indicador_calc.calcular(self._modelo.carga_bateria)

    def cargar_estado(self) -> None:
        """Carga el estado desde el persistidor si existe."""
        if self._persistidor and self._persistidor.existe():
            datos = self._persistidor.cargar()
            if datos:
                self._modelo.temperatura_ambiente = datos.get('temperatura_ambiente', 20)
                self._modelo.temperatura_deseada = datos.get('temperatura_deseada', 24)
                self._modelo.carga_bateria = datos.get('carga_bateria', 5.0)
                self._modelo.estado_climatizador = datos.get('estado_climatizador', 'apagado')

    @property
    def modelo(self) -> TermostatoModelo:
        """Retorna el modelo de datos actual."""
        return self._modelo

    def _guardar_estado(self) -> None:
        """Persiste el estado actual si hay persistidor configurado."""
        if self._persistidor:
            datos = {
                'temperatura_ambiente': self._modelo.temperatura_ambiente,
                'temperatura_deseada': self._modelo.temperatura_deseada,
                'carga_bateria': self._modelo.carga_bateria,
                'estado_climatizador': self._modelo.estado_climatizador,
                'indicador': self.obtener_indicador()
            }
            self._persistidor.guardar(datos)

    def _registrar_en_historial(self, temperatura: int) -> None:
        """Registra la temperatura en el historial si hay repositorio configurado."""
        if self._historial_repositorio:
            registro = RegistroTemperatura(
                temperatura=temperatura,
                timestamp=datetime.now()
            )
            self._historial_repositorio.agregar(registro)
