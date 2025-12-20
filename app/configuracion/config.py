"""
Configuracion centralizada del sistema.
Carga valores desde variables de entorno.
"""
import os


class Config:
    """Configuracion del sistema cargada desde variables de entorno."""

    # Servidor
    PORT = int(os.getenv('PORT', 5050))
    DEBUG = os.getenv('DEBUG', 'true').lower() == 'true'

    # Valores iniciales del termostato
    TEMPERATURA_AMBIENTE_INICIAL = int(os.getenv('TEMPERATURA_AMBIENTE_INICIAL', 20))
    TEMPERATURA_DESEADA_INICIAL = int(os.getenv('TEMPERATURA_DESEADA_INICIAL', 24))
    CARGA_BATERIA_INICIAL = float(os.getenv('CARGA_BATERIA_INICIAL', 5.0))

    # Rangos de validacion - Temperatura ambiente
    TEMPERATURA_AMBIENTE_MIN = int(os.getenv('TEMPERATURA_AMBIENTE_MIN', 0))
    TEMPERATURA_AMBIENTE_MAX = int(os.getenv('TEMPERATURA_AMBIENTE_MAX', 50))

    # Rangos de validacion - Temperatura deseada
    TEMPERATURA_DESEADA_MIN = int(os.getenv('TEMPERATURA_DESEADA_MIN', 15))
    TEMPERATURA_DESEADA_MAX = int(os.getenv('TEMPERATURA_DESEADA_MAX', 30))

    # Rangos de validacion - Bateria
    CARGA_BATERIA_MIN = float(os.getenv('CARGA_BATERIA_MIN', 0.0))
    CARGA_BATERIA_MAX = float(os.getenv('CARGA_BATERIA_MAX', 5.0))
