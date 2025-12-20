"""
API REST del termostato.
Expone endpoints para consultar y modificar el estado del termostato.
"""
from flask import Flask, make_response, request, jsonify

from app.general.configurador import Configurador

# Instancia la aplicación de servicios Flask
app_api = Flask(__name__)

# Configuración inicial del termostato
termostato = Configurador.termostato


@app_api.errorhandler(404)
def not_found_error(error):
    """Manejador de error 404 - Recurso no encontrado."""
    return make_response(jsonify({'error': 'No Encontrado'}), 404)


@app_api.errorhandler(500)
def internal_server_error(error):
    """Manejador de error 500 - Error interno del servidor."""
    return make_response(jsonify({'error': 'Error interno del servidor'}), 500)


@app_api.route("/comprueba/", methods=["GET"])
def comprueba():
    """Endpoint de health check para verificar que el servidor responde."""
    return "OK!", 200


@app_api.route("/termostato/", methods=["GET"])
def obtener_termostato():
    """GET: Obtiene el estado completo del termostato."""
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
            return jsonify({'error': 'Se requiere campo "ambiente"'}), 400
        try:
            termostato.temperatura_ambiente = datos["ambiente"]
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        return jsonify({'mensaje': 'dato registrado'}), 201
    else:
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
            return jsonify({'error': 'Se requiere campo "deseada"'}), 400
        try:
            termostato.temperatura_deseada = datos["deseada"]
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        return jsonify({'mensaje': 'dato registrado'}), 201
    else:
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
            return jsonify({'error': 'Se requiere campo "bateria"'}), 400
        try:
            termostato.carga_bateria = datos["bateria"]
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        return jsonify({'mensaje': 'dato registrado'}), 201
    else:
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
            return jsonify({'error': 'Se requiere campo "climatizador"'}), 400
        termostato.estado_climatizador = datos["climatizador"]
        return jsonify({'mensaje': 'dato registrado'}), 201
    else:
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
            return jsonify({'error': 'Se requiere campo "indicador"'}), 400
        termostato.indicador = datos["indicador"]
        return jsonify({'mensaje': 'dato registrado'}), 201
    else:
        return jsonify({'indicador': termostato.indicador})
