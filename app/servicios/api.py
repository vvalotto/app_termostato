"""
API REST del termostato.
Expone endpoints para consultar y modificar el estado del termostato.
"""
import logging

from flask import Flask, request, jsonify

from app.general.configurador import Configurador
from app.servicios.errors import error_response

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Instancia la aplicación de servicios Flask
app_api = Flask(__name__)

# Configuración inicial del termostato
termostato = Configurador.termostato


@app_api.errorhandler(404)
def not_found_error(error):
    """Manejador de error 404 - Recurso no encontrado."""
    logger.warning("404 - Recurso no encontrado: %s", request.path)
    return error_response(404, "Recurso no encontrado", f"Ruta: {request.path}")


@app_api.errorhandler(500)
def internal_server_error(error):
    """Manejador de error 500 - Error interno del servidor."""
    logger.error("500 - Error interno: %s", error)
    return error_response(500, "Error interno del servidor")


@app_api.route("/comprueba/", methods=["GET"])
def comprueba():
    """Endpoint de health check para verificar que el servidor responde."""
    return "OK!", 200


@app_api.route("/termostato/", methods=["GET"])
def obtener_termostato():
    """GET: Obtiene el estado completo del termostato."""
    logger.info("GET /termostato/ -> 200")
    return jsonify({
        'temperatura_ambiente': termostato.temperatura_ambiente,
        'temperatura_deseada': termostato.temperatura_deseada,
        'carga_bateria': termostato.carga_bateria,
        'estado_climatizador': termostato.estado_climatizador,
        'indicador': termostato.indicador
    })


@app_api.route("/termostato/temperatura_ambiente/", methods=["GET", "POST"])
def obtener_temperatura_ambiente():
    """
    GET: Obtiene la temperatura ambiente actual.
    POST: Establece la temperatura ambiente. Requiere JSON: {"ambiente": valor}
    """
    if request.method == 'POST':
        datos = request.get_json()
        if not datos or "ambiente" not in datos:
            logger.warning("POST /termostato/temperatura_ambiente/ - Campo requerido faltante")
            return error_response(400, "Campo requerido faltante", "Se requiere campo 'ambiente'")
        try:
            termostato.temperatura_ambiente = datos["ambiente"]
        except ValueError as e:
            logger.warning("POST /termostato/temperatura_ambiente/ - %s", e)
            return error_response(400, "Valor fuera de rango", str(e))
        logger.info("POST /termostato/temperatura_ambiente/ -> 201")
        return jsonify({'mensaje': 'dato registrado'}), 201
    else:
        logger.info("GET /termostato/temperatura_ambiente/ -> 200")
        return jsonify({'temperatura_ambiente': termostato.temperatura_ambiente})


@app_api.route("/termostato/temperatura_deseada/", methods=["GET", "POST"])
def obtener_temperatura_deseada():
    """
    GET: Obtiene la temperatura deseada configurada.
    POST: Establece la temperatura deseada. Requiere JSON: {"deseada": valor}
    """
    if request.method == 'POST':
        datos = request.get_json()
        if not datos or "deseada" not in datos:
            logger.warning("POST /termostato/temperatura_deseada/ - Campo requerido faltante")
            return error_response(400, "Campo requerido faltante", "Se requiere campo 'deseada'")
        try:
            termostato.temperatura_deseada = datos["deseada"]
        except ValueError as e:
            logger.warning("POST /termostato/temperatura_deseada/ - %s", e)
            return error_response(400, "Valor fuera de rango", str(e))
        logger.info("POST /termostato/temperatura_deseada/ -> 201")
        return jsonify({'mensaje': 'dato registrado'}), 201
    else:
        logger.info("GET /termostato/temperatura_deseada/ -> 200")
        return jsonify({'temperatura_deseada': termostato.temperatura_deseada})


@app_api.route("/termostato/bateria/", methods=["GET", "POST"])
def obtener_carga_bateria():
    """
    GET: Obtiene la carga de la batería.
    POST: Establece la carga de batería. Requiere JSON: {"bateria": valor}
    """
    if request.method == 'POST':
        datos = request.get_json()
        if not datos or "bateria" not in datos:
            logger.warning("POST /termostato/bateria/ - Campo requerido faltante")
            return error_response(400, "Campo requerido faltante", "Se requiere campo 'bateria'")
        try:
            termostato.carga_bateria = datos["bateria"]
        except ValueError as e:
            logger.warning("POST /termostato/bateria/ - %s", e)
            return error_response(400, "Valor fuera de rango", str(e))
        logger.info("POST /termostato/bateria/ -> 201")
        return jsonify({'mensaje': 'dato registrado'}), 201
    else:
        logger.info("GET /termostato/bateria/ -> 200")
        return jsonify({'carga_bateria': termostato.carga_bateria})


@app_api.route("/termostato/estado_climatizador/", methods=["GET", "POST"])
def obtener_estado_climatizador():
    """
    GET: Obtiene el estado del climatizador (encendido/enfriando/calentando).
    POST: Establece el estado del climatizador. Requiere JSON: {"climatizador": valor}
    """
    if request.method == 'POST':
        datos = request.get_json()
        if not datos or "climatizador" not in datos:
            logger.warning("POST /termostato/estado_climatizador/ - Campo requerido faltante")
            return error_response(400, "Campo requerido faltante", "Se requiere campo 'climatizador'")
        termostato.estado_climatizador = datos["climatizador"]
        logger.info("POST /termostato/estado_climatizador/ -> 201")
        return jsonify({'mensaje': 'dato registrado'}), 201
    else:
        logger.info("GET /termostato/estado_climatizador/ -> 200")
        return jsonify({'estado_climatizador': termostato.estado_climatizador})


@app_api.route("/termostato/indicador/", methods=["GET", "POST"])
def obtener_indicador():
    """
    GET: Obtiene el indicador de carga del dispositivo.
    POST: Establece el indicador de carga. Requiere JSON: {"indicador": valor}
    """
    if request.method == 'POST':
        datos = request.get_json()
        if not datos or "indicador" not in datos:
            logger.warning("POST /termostato/indicador/ - Campo requerido faltante")
            return error_response(400, "Campo requerido faltante", "Se requiere campo 'indicador'")
        termostato.indicador = datos["indicador"]
        logger.info("POST /termostato/indicador/ -> 201")
        return jsonify({'mensaje': 'dato registrado'}), 201
    else:
        logger.info("GET /termostato/indicador/ -> 200")
        return jsonify({'indicador': termostato.indicador})
