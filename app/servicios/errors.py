"""
Manejo de errores estandarizado para la API REST.
Provee funciones y formatos consistentes para respuestas de error.
"""
from flask import make_response, jsonify


def error_response(codigo, mensaje, detalle=None):
    """
    Genera una respuesta de error estandarizada.

    Args:
        codigo: Codigo HTTP del error (400, 404, 500, etc.)
        mensaje: Mensaje descriptivo del error
        detalle: Informacion adicional sobre el error (opcional)

    Returns:
        Response: Respuesta Flask con formato JSON estandarizado
    """
    error_dict = {
        'error': {
            'codigo': codigo,
            'mensaje': mensaje
        }
    }
    if detalle:
        error_dict['error']['detalle'] = detalle
    return make_response(jsonify(error_dict), codigo)
