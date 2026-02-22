# Plan de Implementación: HU-003 - Eliminar duplicación en endpoints API

**Patrón:** Flask REST (Layered)
**Producto:** app_termostato
**Estimación HU:** 5 SP
**Estimación Total:** 1h 30min
**BDD:** No aplica (refactorización sin cambio de comportamiento)

---

## Análisis del código actual

Los endpoints `temperatura_ambiente`, `temperatura_deseada`, `bateria` y `estado_climatizador`
repiten el siguiente patrón ~30 líneas c/u:

```
POST: validar campo → setattr(termostato, ...) → manejar ValueError → return 201
GET:  getattr(termostato, ...) → return 200
```

El endpoint `indicador` y `obtener_termostato` son solo GET, no participan de la duplicación.

**Diferencias entre endpoints:**

| Endpoint            | campo_modelo        | campo_request | valida ValueError |
|---------------------|---------------------|---------------|-------------------|
| temperatura_ambiente| temperatura_ambiente| ambiente      | ✅ Sí             |
| temperatura_deseada | temperatura_deseada | deseada       | ✅ Sí             |
| bateria             | carga_bateria       | bateria       | ✅ Sí             |
| estado_climatizador | estado_climatizador | climatizador  | ✅ Sí             |

---

## Componentes a implementar

### T1 - Crear decorador `endpoint_termostato` (15 min)
- [x] `app/servicios/decorators.py` (crear)
  - Decorador `endpoint_termostato(campo_modelo, campo_request, validar=True)`
  - Maneja lógica GET/POST genérica
  - Centraliza validación de campo requerido
  - Centraliza manejo de ValueError
  - Centraliza logging

### T2 - Refactorizar `temperatura_ambiente` (5 min)
- [x] `app/servicios/api.py` — función `obtener_temperatura_ambiente`
  - Aplicar `@endpoint_termostato("temperatura_ambiente", "ambiente")`
  - Conservar docstring Swagger intacto
  - Cuerpo de función queda vacío (`pass`)

### T3 - Refactorizar `temperatura_deseada` (5 min)
- [x] `app/servicios/api.py` — función `obtener_temperatura_deseada`
  - Aplicar `@endpoint_termostato("temperatura_deseada", "deseada")`

### T4 - Refactorizar `bateria` (5 min)
- [x] `app/servicios/api.py` — función `obtener_carga_bateria`
  - Aplicar `@endpoint_termostato("carga_bateria", "bateria")`

### T5 - Refactorizar `estado_climatizador` (5 min)
- [x] `app/servicios/api.py` — función `obtener_estado_climatizador`
  - Aplicar `@endpoint_termostato("estado_climatizador", "climatizador")`

### T6 - Tests unitarios del decorador (20 min)
- [x] `tests/test_decorators.py` (crear)
  - GET retorna valor correcto del termostato
  - POST actualiza valor correctamente → 201
  - POST sin campo requerido → 400
  - POST con ValueError → 400
  - Logging se invoca correctamente

### T7 - Tests de regresión (15 min)
- [x] Ejecutar `tests/test_api.py` existente sin modificación
  - Todos los tests deben pasar sin cambios
  - Verificar códigos HTTP idénticos
  - Verificar formato JSON de respuestas idéntico

### T8 - Quality check (10 min)
- [x] Ejecutar `/quality-check app/servicios/`
  - Pylint ≥ 8.0
  - CC ≤ 10
  - MI > 20

---

## Archivos afectados

| Archivo | Acción |
|---------|--------|
| `app/servicios/decorators.py` | Crear |
| `app/servicios/api.py` | Modificar (4 endpoints) |
| `tests/test_decorators.py` | Crear |

## Métricas esperadas

| Métrica | Antes | Después |
|---------|-------|---------|
| LOC en api.py | ~440 | ~280 |
| Duplicación | ~120 LOC | ~0 |
| LOC en decorators.py | — | ~50 |

---

**Estado:** ✅ COMPLETADO
**Creado:** 2026-02-22
**Completado:** 2026-02-22

---

## Métricas de Tiempo

| Tarea | Estimado | Real | Varianza |
|-------|----------|------|----------|
| T1 - Crear decorators.py | 15 min | 1 min | -14 min |
| T2-T5 - Refactorizar endpoints | 20 min | 2 min | -18 min |
| T6 - Tests unitarios | 20 min | 5 min | -15 min |
| T7 - Tests regresión | 15 min | 1 min | -14 min |
| T8 - Quality check | 10 min | 1 min | -9 min |
| **Total** | **80 min** | **10 min** | **-70 min** |

## Lecciones Aprendidas

- ✅ El decorador con `termostato` como parámetro explícito facilita el testing (DI)
- ⚠️ Flask retorna 415 (no 400) cuando POST no lleva `Content-Type: application/json` — el test debe reflejarlo
- 💡 El patrón `@wraps(func)` es esencial para preservar los docstrings de Swagger
