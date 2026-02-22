"""
Configuración de Flasgger/Swagger para la API REST del termostato.
"""
from app.configuracion.config import Config


def get_swagger_config():
    """Retorna la configuración de Flasgger."""
    return {
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


def get_swagger_template():
    """Retorna el template con metadata de la API."""
    return {
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
