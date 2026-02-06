# [HU-006] Extraer configuración de Swagger

**Epic:** Refactorización Deuda Técnica - Diseño
**Prioridad:** 🟡 Media
**Estimación:** 3 Story Points
**Sprint:** TBD
**Jira:** TBD

---

## 📖 Historia de Usuario

**Como** desarrollador del sistema
**Quiero** separar la configuración de Swagger del archivo de endpoints
**Para** mejorar la organización del código y facilitar el mantenimiento de la documentación API

## 🎯 Criterios de Aceptación

- [ ] **AC1:** Configuración Swagger movida a `app/configuracion/swagger_config.py`
- [ ] **AC2:** api.py solo importa y usa la configuración
- [ ] **AC3:** Swagger UI funciona correctamente en /docs/
- [ ] **AC4:** Toda la documentación de endpoints se preserva
- [ ] **AC5:** Fácil agregar/modificar tags y metadata de Swagger
- [ ] **AC6:** api.py reducido en ~40 líneas

## 📋 Tareas Técnicas

- [ ] **T1:** Crear `app/configuracion/swagger_config.py`
- [ ] **T2:** Mover `swagger_config` dict al nuevo archivo
- [ ] **T3:** Mover `swagger_template` dict al nuevo archivo
- [ ] **T4:** Crear función `get_swagger_config()` y `get_swagger_template()`
- [ ] **T5:** Actualizar `api.py` para importar configuración
- [ ] **T6:** Verificar Swagger UI funciona
- [ ] **T7:** Actualizar tests si necesario
- [ ] **T8:** Code review

## 🔗 Contexto

**Problema identificado:**
- **Análisis:** [docs/analisis/2026-02-06_analisis_diseno.md](../../analisis/2026-02-06_analisis_diseno.md#12-api-py)
- **Code smell:** Configuración embebida en módulo funcional
- **Ubicación:** `app/servicios/api.py:28-63`
- **Impacto:** api.py mezcla endpoints con configuración

**Código actual:**

```python
# app/servicios/api.py:28-63 (35 líneas de configuración)
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            # ...
        }
    ],
    # ...
}

swagger_template = {
    "info": {
        "title": "API Termostato",
        # ...
    },
    # ...
}

swagger = Swagger(app_api, config=swagger_config, template=swagger_template)
```

**Solución propuesta:**

```python
# app/configuracion/swagger_config.py (NUEVO)
"""Configuración de Swagger/OpenAPI para documentación de API."""

from app.configuracion.config import Config


def get_swagger_config():
    """Retorna configuración de Swagger."""
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
    """Retorna template de Swagger con metadata de API."""
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


# app/servicios/api.py (REFACTORIZADO)
from flasgger import Swagger
from app.configuracion.swagger_config import get_swagger_config, get_swagger_template

# Configuración de Swagger
swagger = Swagger(
    app_api,
    config=get_swagger_config(),
    template=get_swagger_template()
)

# ✅ Reducción de ~35 líneas en api.py
```

**Archivos afectados:**
- `app/configuracion/swagger_config.py` (crear)
- `app/servicios/api.py` (refactorizar - eliminar config)
- `tests/test_api.py` (verificar /docs/ funciona)

## 📊 Métricas

**Antes:**
- **LOC en api.py:** 429
- **Configuración embebida:** 35 líneas
- **Separación de concerns:** ❌

**Después:**
- **LOC en api.py:** ~394 (-35)
- **LOC en swagger_config.py:** ~50 (nuevo)
- **Separación de concerns:** ✅

## 🔗 Referencias

- **Análisis de diseño:** [docs/analisis/2026-02-06_analisis_diseno.md](../../analisis/2026-02-06_analisis_diseno.md)
- **Jira:** TBD
- **Flasgger Docs:** https://github.com/flasgger/flasgger

## 🧪 Testing

**Escenarios a validar:**

### Tests de Integración - Swagger UI
```python
def test_swagger_ui_disponible(client):
    response = client.get('/docs/')
    assert response.status_code == 200

def test_swagger_json_disponible(client):
    response = client.get('/apispec.json')
    assert response.status_code == 200
    assert response.json['info']['title'] == 'API Termostato'

def test_swagger_tags_presentes(client):
    response = client.get('/apispec.json')
    tags = [tag['name'] for tag in response.json['tags']]
    assert 'Health' in tags
    assert 'Termostato' in tags
    assert 'Historial' in tags
```

### Tests de Regresión
- Swagger UI se renderiza correctamente
- Todos los endpoints documentados aparecen
- Tags y descripciones correctas

## ⚠️ Riesgos

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Swagger UI deja de funcionar | Baja | Medio | Tests automáticos de /docs/ |
| Documentación incompleta | Baja | Bajo | Verificar manualmente UI |

## 🚀 Despliegue

- [ ] **Requiere migración de datos:** NO
- [ ] **Breaking changes:** NO
- [ ] **Requiere actualizar frontend:** NO
- [ ] **Requiere actualizar docs:** SÍ (mencionar nueva estructura)

## 📝 Definición de Done (DoD)

- [ ] swagger_config.py creado
- [ ] api.py refactorizado
- [ ] Swagger UI funciona en /docs/
- [ ] Tests de Swagger creados
- [ ] Code review aprobado
- [ ] Documentación actualizada
- [ ] Branch mergeado a master

---

**Creado:** 2026-02-06
**Actualizado:** 2026-02-06
**Autor:** Equipo de Desarrollo
