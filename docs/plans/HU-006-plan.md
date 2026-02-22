# Plan de Implementación: HU-006 - Extraer configuración Swagger

**Patrón:** Flask REST (Layered)
**Producto:** app_termostato
**Estimación HU:** 3 SP
**Estimación Total:** 35 min
**BDD:** No aplica (refactoring estructural sin cambio de comportamiento)

---

## Análisis del código actual

`api.py` contiene ~35 líneas de configuración Swagger embebidas en `create_app()`:
- `_swagger_config` — dict con configuración de Flasgger
- `_swagger_template` — dict con metadata de la API (título, versión, tags)

Ambos deben vivir en `app/configuracion/swagger_config.py`.

---

## Tareas

### T1 - Crear `app/configuracion/swagger_config.py` (10 min)
- [ ] Función `get_swagger_config()` → retorna dict de configuración Flasgger
- [ ] Función `get_swagger_template()` → retorna dict con metadata de API

### T2 - Refactorizar `api.py` (10 min)
- [ ] Eliminar `_swagger_config` y `_swagger_template` de `api.py`
- [ ] Importar `get_swagger_config`, `get_swagger_template` desde `swagger_config`
- [ ] Actualizar llamada a `Swagger()` dentro de `create_app()`

### T3 - Tests de Swagger (10 min)
- [ ] `tests/test_swagger.py` (crear)
  - GET `/docs/` retorna 200
  - GET `/apispec.json` retorna spec válida con título correcto
  - Tags `Health`, `Termostato`, `Historial` presentes

### T4 - Quality check (5 min)
- [ ] Ejecutar `/quality-check app/`

---

## Archivos afectados

| Archivo | Acción |
|---------|--------|
| `app/configuracion/swagger_config.py` | Crear |
| `app/servicios/api.py` | Modificar (eliminar config embebida) |
| `tests/test_swagger.py` | Crear |

---

**Estado:** ✅ COMPLETADO (4/4 tareas)
**Creado:** 2026-02-22
**Completado:** 2026-02-22
