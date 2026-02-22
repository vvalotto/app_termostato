"""
API REST del termostato.
Expone endpoints para consultar y modificar el estado del termostato.
"""
import logging
from datetime import datetime

from flask import Flask, request, jsonify
from flask_cors import CORS
from flasgger import Swagger

from app.configuracion import Config
from app.configuracion.configurador import Configurador
from app.servicios.decorators import endpoint_termostato
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
CORS(app_api)

# Configuracion de Swagger
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}

swagger_template = {
    "info": {
        "title": "API Termostato",
        "description": "API REST para control y monitoreo de termostato",
        "version": Config.VERSION,
        "contact": {
            "name": "Soporte",
            "email": "soporte@termostato.local"
        }
    },
    "basePath": "/",
    "schemes": ["http", "https"],
    "tags": [
        {"name": "Health", "description": "Endpoints de estado del sistema"},
        {"name": "Termostato", "description": "Control del termostato"},
        {"name": "Historial", "description": "Historial de temperaturas"}
    ]
}

swagger = Swagger(app_api, config=swagger_config, template=swagger_template)

# Configuración inicial del termostato
termostato = Configurador.termostato


class AppState:
    """Estado de la aplicación Flask."""
    def __init__(self):
        self.inicio_servidor = datetime.now()


app_state = AppState()


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
    """Health check del sistema.
    ---
    tags:
      - Health
    responses:
      200:
        description: Estado del sistema
        schema:
          type: object
          properties:
            status:
              type: string
              example: ok
            version:
              type: string
              example: 1.0.0
            uptime_seconds:
              type: integer
              example: 3600
            timestamp:
              type: string
              example: 2025-12-21T10:30:00
    """
    ahora = datetime.now()
    uptime = (ahora - app_state.inicio_servidor).total_seconds()
    logger.info("GET /comprueba/ -> 200")
    return jsonify({
        'status': 'ok',
        'version': Config.VERSION,
        'uptime_seconds': int(uptime),
        'timestamp': ahora.isoformat()
    })


@app_api.route("/termostato/", methods=["GET"])
def obtener_termostato():
    """Obtiene el estado completo del termostato.
    ---
    tags:
      - Termostato
    responses:
      200:
        description: Estado completo del termostato
        schema:
          type: object
          properties:
            temperatura_ambiente:
              type: integer
              example: 20
            temperatura_deseada:
              type: integer
              example: 24
            carga_bateria:
              type: number
              example: 5.0
            estado_climatizador:
              type: string
              example: apagado
            indicador:
              type: string
              example: NORMAL
    """
    logger.info("GET /termostato/ -> 200")
    return jsonify({
        'temperatura_ambiente': termostato.temperatura_ambiente,
        'temperatura_deseada': termostato.temperatura_deseada,
        'carga_bateria': termostato.carga_bateria,
        'estado_climatizador': termostato.estado_climatizador,
        'indicador': termostato.indicador
    })


@app_api.route("/termostato/historial/", methods=["GET"])
def obtener_historial():
    """Obtiene el historial de temperaturas ambiente.
    ---
    tags:
      - Historial
    parameters:
      - name: limite
        in: query
        type: integer
        required: false
        description: Numero maximo de registros a retornar
    responses:
      200:
        description: Historial de temperaturas
        schema:
          type: object
          properties:
            historial:
              type: array
              items:
                type: object
                properties:
                  temperatura:
                    type: integer
                  timestamp:
                    type: string
            total:
              type: integer
    """
    limite = request.args.get('limite', type=int)
    repositorio = Configurador.historial_repositorio
    mapper = Configurador.historial_mapper

    registros = repositorio.obtener(limite)
    historial = [mapper.a_dict(r) for r in registros]

    logger.info("GET /termostato/historial/ -> 200 (%d registros)", len(historial))
    return jsonify({
        'historial': historial,
        'total': repositorio.cantidad()
    })


@app_api.route("/termostato/temperatura_ambiente/", methods=["GET", "POST"])
@endpoint_termostato(termostato, "temperatura_ambiente", "ambiente")
def obtener_temperatura_ambiente():
    """Gestiona la temperatura ambiente.
    ---
    tags:
      - Termostato
    parameters:
      - name: body
        in: body
        required: false
        schema:
          type: object
          properties:
            ambiente:
              type: integer
              description: Temperatura ambiente (0-50)
              example: 25
    responses:
      200:
        description: Temperatura ambiente actual (GET)
        schema:
          type: object
          properties:
            temperatura_ambiente:
              type: integer
              example: 20
      201:
        description: Temperatura actualizada (POST)
        schema:
          type: object
          properties:
            mensaje:
              type: string
              example: dato registrado
      400:
        description: Error de validacion
        schema:
          type: object
          properties:
            error:
              type: object
              properties:
                codigo:
                  type: integer
                mensaje:
                  type: string
                detalle:
                  type: string
    """


@app_api.route("/termostato/temperatura_deseada/", methods=["GET", "POST"])
@endpoint_termostato(termostato, "temperatura_deseada", "deseada")
def obtener_temperatura_deseada():
    """Gestiona la temperatura deseada.
    ---
    tags:
      - Termostato
    parameters:
      - name: body
        in: body
        required: false
        schema:
          type: object
          properties:
            deseada:
              type: integer
              description: Temperatura deseada (15-30)
              example: 22
    responses:
      200:
        description: Temperatura deseada actual (GET)
        schema:
          type: object
          properties:
            temperatura_deseada:
              type: integer
              example: 24
      201:
        description: Temperatura actualizada (POST)
      400:
        description: Error de validacion
    """


@app_api.route("/termostato/bateria/", methods=["GET", "POST"])
@endpoint_termostato(termostato, "carga_bateria", "bateria")
def obtener_carga_bateria():
    """Gestiona la carga de bateria.
    ---
    tags:
      - Termostato
    parameters:
      - name: body
        in: body
        required: false
        schema:
          type: object
          properties:
            bateria:
              type: number
              description: Carga de bateria (0.0-5.0)
              example: 3.5
    responses:
      200:
        description: Carga de bateria actual (GET)
        schema:
          type: object
          properties:
            carga_bateria:
              type: number
              example: 5.0
      201:
        description: Bateria actualizada (POST)
      400:
        description: Error de validacion
    """


@app_api.route("/termostato/estado_climatizador/", methods=["GET", "POST"])
@endpoint_termostato(termostato, "estado_climatizador", "climatizador")
def obtener_estado_climatizador():
    """Gestiona el estado del climatizador.
    ---
    tags:
      - Termostato
    parameters:
      - name: body
        in: body
        required: false
        schema:
          type: object
          properties:
            climatizador:
              type: string
              description: "Estado válido: apagado, encendido, enfriando, calentando"
              example: enfriando
              enum: [apagado, encendido, enfriando, calentando]
    responses:
      200:
        description: Estado del climatizador (GET)
        schema:
          type: object
          properties:
            estado_climatizador:
              type: string
              example: apagado
      201:
        description: Estado actualizado (POST)
      400:
        description: Campo requerido faltante o estado inválido
    """


@app_api.route("/termostato/indicador/", methods=["GET"])
def obtener_indicador():
    """Obtiene el indicador de carga (calculado segun nivel de bateria).
    ---
    tags:
      - Termostato
    responses:
      200:
        description: Indicador actual calculado segun carga de bateria
        schema:
          type: object
          properties:
            indicador:
              type: string
              description: NORMAL (>3.5), BAJO (2.5-3.5), CRITICO (<2.5)
              example: NORMAL
    """
    logger.info("GET /termostato/indicador/ -> 200")
    return jsonify({'indicador': termostato.indicador})
