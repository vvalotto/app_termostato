"""
Punto de entrada de la API REST del termostato.
Lanza el servidor Flask con la configuración definida.
"""
from dotenv import load_dotenv

# Cargar variables de entorno desde .env (debe ser antes de importar Config)
load_dotenv()

from app.configuracion import Config
from app.servicios.api import create_app

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=Config.PORT, debug=Config.DEBUG)
