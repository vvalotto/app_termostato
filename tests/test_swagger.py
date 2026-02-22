"""Tests de la configuración Swagger/Flasgger."""
import pytest

from app.configuracion.swagger_config import get_swagger_config, get_swagger_template
from app.configuracion.config import Config


class TestSwaggerConfig:
    """Tests para get_swagger_config()."""

    def test_retorna_dict(self):
        config = get_swagger_config()
        assert isinstance(config, dict)

    def test_tiene_specs_route(self):
        config = get_swagger_config()
        assert config["specs_route"] == "/docs/"

    def test_tiene_apispec_route(self):
        config = get_swagger_config()
        ruta = config["specs"][0]["route"]
        assert ruta == "/apispec.json"

    def test_swagger_ui_habilitado(self):
        config = get_swagger_config()
        assert config["swagger_ui"] is True

    def test_llamadas_independientes(self):
        c1 = get_swagger_config()
        c2 = get_swagger_config()
        assert c1 is not c2


class TestSwaggerTemplate:
    """Tests para get_swagger_template()."""

    def test_retorna_dict(self):
        template = get_swagger_template()
        assert isinstance(template, dict)

    def test_titulo_correcto(self):
        template = get_swagger_template()
        assert template["info"]["title"] == "API Termostato"

    def test_version_desde_config(self):
        template = get_swagger_template()
        assert template["info"]["version"] == Config.VERSION

    def test_tags_presentes(self):
        template = get_swagger_template()
        nombres = [tag["name"] for tag in template["tags"]]
        assert "Health" in nombres
        assert "Termostato" in nombres
        assert "Historial" in nombres

    def test_tres_tags(self):
        template = get_swagger_template()
        assert len(template["tags"]) == 3

    def test_llamadas_independientes(self):
        t1 = get_swagger_template()
        t2 = get_swagger_template()
        assert t1 is not t2


class TestSwaggerEndpoints:
    """Tests de integración vía HTTP."""

    def test_docs_retorna_200(self, client):
        response = client.get("/docs/")
        assert response.status_code == 200

    def test_apispec_retorna_200(self, client):
        response = client.get("/apispec.json")
        assert response.status_code == 200

    def test_apispec_tiene_titulo(self, client):
        response = client.get("/apispec.json")
        data = response.get_json()
        assert data["info"]["title"] == "API Termostato"

    def test_apispec_tiene_tag_health(self, client):
        response = client.get("/apispec.json")
        data = response.get_json()
        nombres = [t["name"] for t in data["tags"]]
        assert "Health" in nombres

    def test_apispec_tiene_tag_termostato(self, client):
        response = client.get("/apispec.json")
        data = response.get_json()
        nombres = [t["name"] for t in data["tags"]]
        assert "Termostato" in nombres

    def test_apispec_tiene_tag_historial(self, client):
        response = client.get("/apispec.json")
        data = response.get_json()
        nombres = [t["name"] for t in data["tags"]]
        assert "Historial" in nombres
