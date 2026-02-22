"""
Tests unitarios para TermostatoFactory.
HU-002: Eliminar Singleton en Configurador
"""
import pytest
from unittest.mock import MagicMock

from app.configuracion.factory import TermostatoFactory
from app.general.termostato import Termostato
from app.datos import HistorialRepositorioMemoria, HistorialMapper, TermostatoPersistidorJSON


class TestTermostatoFactoryCrearTermostato:
    """Tests para el método crear_termostato()."""

    def test_retorna_instancia_termostato(self):
        """Factory retorna una instancia de Termostato."""
        termostato = TermostatoFactory.crear_termostato()
        assert isinstance(termostato, Termostato)

    def test_dos_llamadas_retornan_instancias_independientes(self):
        """Cada llamada retorna una instancia diferente (no singleton)."""
        t1 = TermostatoFactory.crear_termostato()
        t2 = TermostatoFactory.crear_termostato()
        assert t1 is not t2

    def test_instancias_no_comparten_estado(self):
        """Modificar una instancia no afecta a la otra."""
        t1 = TermostatoFactory.crear_termostato()
        t2 = TermostatoFactory.crear_termostato()
        t1.temperatura_ambiente = 30
        assert t2.temperatura_ambiente != 30

    def test_acepta_historial_repositorio_customizado(self):
        """Factory acepta repositorio de historial customizado."""
        repo_mock = MagicMock()
        repo_mock.obtener.return_value = []
        termostato = TermostatoFactory.crear_termostato(
            historial_repositorio=repo_mock
        )
        assert isinstance(termostato, Termostato)

    def test_acepta_persistidor_customizado(self):
        """Factory acepta persistidor customizado."""
        persistidor_mock = MagicMock()
        persistidor_mock.cargar.return_value = None
        termostato = TermostatoFactory.crear_termostato(
            persistidor=persistidor_mock
        )
        assert isinstance(termostato, Termostato)


class TestTermostatoFactoryDependencias:
    """Tests para los métodos de creación de dependencias."""

    def test_crear_historial_repositorio_retorna_instancia(self):
        """Retorna instancia de HistorialRepositorioMemoria."""
        repo = TermostatoFactory.crear_historial_repositorio()
        assert isinstance(repo, HistorialRepositorioMemoria)

    def test_crear_historial_repositorio_instancias_independientes(self):
        """Cada llamada retorna una instancia diferente."""
        r1 = TermostatoFactory.crear_historial_repositorio()
        r2 = TermostatoFactory.crear_historial_repositorio()
        assert r1 is not r2

    def test_crear_historial_mapper_retorna_instancia(self):
        """Retorna instancia de HistorialMapper."""
        mapper = TermostatoFactory.crear_historial_mapper()
        assert isinstance(mapper, HistorialMapper)

    def test_crear_persistidor_retorna_instancia(self):
        """Retorna instancia de TermostatoPersistidorJSON."""
        persistidor = TermostatoFactory.crear_persistidor()
        assert isinstance(persistidor, TermostatoPersistidorJSON)


class TestCreateApp:
    """Tests para el Application Factory Pattern en api.py."""

    def test_create_app_retorna_flask_app(self):
        """create_app() retorna una aplicación Flask."""
        from app.servicios.api import create_app
        from flask import Flask
        app = create_app()
        assert isinstance(app, Flask)

    def test_create_app_con_termostato_inyectado(self):
        """create_app() acepta termostato por inyección de dependencias."""
        from app.servicios.api import create_app
        termostato_mock = MagicMock()
        termostato_mock.temperatura_ambiente = 22
        termostato_mock.indicador = 'NORMAL'
        app = create_app(termostato=termostato_mock)
        app.config['TESTING'] = True
        with app.test_client() as client:
            response = client.get('/termostato/indicador/')
            assert response.status_code == 200

    def test_dos_apps_no_comparten_estado(self):
        """Dos instancias de app tienen termostatos independientes."""
        from app.servicios.api import create_app
        t1 = TermostatoFactory.crear_termostato()
        t2 = TermostatoFactory.crear_termostato()
        app1 = create_app(termostato=t1)
        app2 = create_app(termostato=t2)
        app1.config['TESTING'] = True
        app2.config['TESTING'] = True

        with app1.test_client() as c1:
            c1.post('/termostato/temperatura_ambiente/', json={'ambiente': 35})

        with app2.test_client() as c2:
            response = c2.get('/termostato/temperatura_ambiente/')
            data = response.get_json()
            assert data['temperatura_ambiente'] != 35
