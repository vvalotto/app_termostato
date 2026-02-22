"""
Decoradores para endpoints REST del termostato.
Centraliza la lógica GET/POST común eliminando duplicación entre endpoints.
"""
import logging
from functools import wraps

from flask import request, jsonify

from app.servicios.errors import error_response

logger = logging.getLogger(__name__)


def endpoint_termostato(termostato, campo_modelo, campo_request, validar=True):
    """Decorador para endpoints GET/POST del termostato.

    Centraliza la lógica común: validación de campo requerido,
    actualización del modelo, manejo de ValueError y logging.

    Args:
        termostato: Instancia del modelo Termostato
        campo_modelo: Nombre del atributo en el modelo Termostato
                      (ej: 'temperatura_ambiente')
        campo_request: Nombre del campo en el JSON del request
                       (ej: 'ambiente')
        validar: Si True, captura ValueError y retorna 400.
                 Si False, deja pasar la excepción.
    """
    def decorator(func):
        @wraps(func)
        def wrapper():
            ruta = request.path

            if request.method == 'POST':
                datos = request.get_json()

                if not datos or campo_request not in datos:
                    logger.warning("POST %s - Campo requerido faltante", ruta)
                    return error_response(
                        400,
                        "Campo requerido faltante",
                        f"Se requiere campo '{campo_request}'"
                    )

                try:
                    setattr(termostato, campo_modelo, datos[campo_request])
                except ValueError as e:
                    if validar:
                        logger.warning("POST %s - %s", ruta, e)
                        return error_response(400, "Valor fuera de rango", str(e))
                    raise

                logger.info("POST %s -> 201", ruta)
                return jsonify({'mensaje': 'dato registrado'}), 201

            logger.info("GET %s -> 200", ruta)
            return jsonify({campo_modelo: getattr(termostato, campo_modelo)})

        return wrapper
    return decorator
