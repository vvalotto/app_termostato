"""
Validaciones del termostato.
Extrae la lógica de validación de rangos de la clase Termostato.
"""
from app.configuracion.config import Config


class TermostatoValidator:
    """Valida los valores del termostato antes de asignarlos al modelo."""

    def validar_temperatura_ambiente(self, valor) -> int:
        """Valida y convierte temperatura ambiente al rango configurado."""
        valor = int(valor)
        if not (Config.TEMPERATURA_AMBIENTE_MIN <= valor <= Config.TEMPERATURA_AMBIENTE_MAX):
            raise ValueError(
                f"temperatura_ambiente debe estar entre "
                f"{Config.TEMPERATURA_AMBIENTE_MIN} y {Config.TEMPERATURA_AMBIENTE_MAX}"
            )
        return valor

    def validar_temperatura_deseada(self, valor) -> int:
        """Valida y convierte temperatura deseada al rango configurado."""
        valor = int(valor)
        if not (Config.TEMPERATURA_DESEADA_MIN <= valor <= Config.TEMPERATURA_DESEADA_MAX):
            raise ValueError(
                f"temperatura_deseada debe estar entre "
                f"{Config.TEMPERATURA_DESEADA_MIN} y {Config.TEMPERATURA_DESEADA_MAX}"
            )
        return valor

    def validar_carga_bateria(self, valor) -> float:
        """Valida y convierte carga de batería al rango configurado."""
        valor = round(float(valor), 2)
        if not (Config.CARGA_BATERIA_MIN <= valor <= Config.CARGA_BATERIA_MAX):
            raise ValueError(
                f"carga_bateria debe estar entre "
                f"{Config.CARGA_BATERIA_MIN} y {Config.CARGA_BATERIA_MAX}"
            )
        return valor

    def validar_estado_climatizador(self, valor) -> str:
        """Valida el estado del climatizador contra los valores permitidos."""
        valor = str(valor).lower().strip()
        if valor not in Config.ESTADOS_CLIMATIZADOR_VALIDOS:
            raise ValueError(
                f"estado_climatizador debe ser uno de: "
                f"{', '.join(sorted(Config.ESTADOS_CLIMATIZADOR_VALIDOS))}. "
                f"Recibido: '{valor}'"
            )
        return valor
