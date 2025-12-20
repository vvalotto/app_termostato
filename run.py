"""
Punto de entrada de la API REST del termostato.
Lanza el servidor Flask con la configuración definida.
"""
import os

from app.servicios.api import app_api

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5050))
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    app_api.run(host='0.0.0.0', port=port, debug=debug)
