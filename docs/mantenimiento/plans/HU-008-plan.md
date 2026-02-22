# Plan de Implementación: HU-008 - Crear DI Container

**Patrón:** Flask REST (Layered)
**Producto:** app_termostato
**Estimación HU:** 8 SP
**Estimación Total:** 75 min
**BDD:** No aplica (refactoring — no cambia comportamiento de la API)

---

## Contexto previo

Las HUs anteriores ya implementaron DI de forma efectiva:
- `TermostatoFactory` — crea dependencias sin Singleton
- `create_app(termostato=None, ...)` — Application Factory con DI
- `conftest.py` — fixtures que usan `create_app(termostato=mock)`

**Decisión de alcance:** La HU propone refactorizar `api.py`, `run.py` y `conftest.py` para usar el container, pero esos archivos ya funcionan correctamente con DI. El riesgo de breaking changes supera el beneficio.

**Enfoque adoptado:** Agregar `DIContainer` como herramienta disponible sin romper la infraestructura existente. El container convive con `TermostatoFactory` y `create_app()`.

---

## Tareas

### T1 - Crear `app/configuracion/di_container.py` (30 min)
- [ ] `class DIContainer` con lazy singleton via `_singletons: dict`
  - `get_config()` — retorna `Config`
  - `get_historial_repositorio()` — singleton
  - `get_historial_mapper()` — singleton
  - `get_persistidor()` — singleton
  - `get_indicador_calc()` — singleton (`IndicadorCalculatorTresNiveles`)
  - `get_termostato()` — singleton con resolución transitiva
  - `reset()` — limpia singletons (útil en testing)
- [ ] `class TestDIContainer(DIContainer)` — permite inyectar mocks via `set_mock(nombre, mock)`
  - Sobreescribe `get_*` para retornar mocks si están configurados

### T2 - Tests unitarios `tests/test_di_container.py` (25 min)
- [ ] DIContainer retorna Config
- [ ] historial_repositorio es singleton (misma instancia en dos llamadas)
- [ ] get_termostato() resuelve dependencias transitivamente
- [ ] reset() limpia singletons (nueva instancia después de reset)
- [ ] TestDIContainer permite inyectar mock de persistidor
- [ ] TestDIContainer permite inyectar mock de historial_repositorio

### T3 - Actualizar `docs/desarrollo/ARQUITECTURA.md` (10 min)
- [ ] Sección "DIContainer — cuándo usarlo vs TermostatoFactory"
- [ ] Ejemplo de uso en producción y testing

### T4 - Regresión + quality check (10 min)
- [ ] `pytest tests/` — todos pasan
- [ ] `/quality-check app/`

---

## Archivos afectados

| Archivo | Acción |
|---------|--------|
| `app/configuracion/di_container.py` | Crear |
| `tests/test_di_container.py` | Crear |
| `docs/desarrollo/ARQUITECTURA.md` | Actualizar |

**Sin cambios en:** `api.py`, `run.py`, `conftest.py`, tests existentes

---

## Criterios de Aceptación verificados

| AC | Verificación |
|----|-------------|
| AC1: DIContainer con métodos por dependencia | `di_container.py` con 6 métodos `get_*` |
| AC2: Factory/Container integrados | DIContainer usa mismas dependencias que Factory |
| AC3: Fácil crear container de testing | `TestDIContainer.set_mock(nombre, mock)` |
| AC4: Resolución transitiva | `get_termostato()` llama `get_historial_repositorio()` etc. |
| AC5: Singletons | `_singletons` dict con lazy init |
| AC6: Documentación | `ARQUITECTURA.md` actualizado |
| AC7: Tests con mocks | `test_di_container.py` usa `TestDIContainer` |

---

**Estado:** ❌ DESCARTADA
**Motivo:** Over-engineering — HU-001 (TermostatoService) y HU-002 (Application Factory) ya cubren la necesidad. Ver ADR-002.
**Creado:** 2026-02-22
**Descartada:** 2026-02-22
