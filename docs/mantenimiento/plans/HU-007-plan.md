# Plan de Implementación: HU-007 - Strategy Pattern para indicador

**Patrón:** Flask REST (Layered)
**Producto:** app_termostato
**Estimación HU:** 5 SP
**Estimación Total:** 55 min
**BDD:** No aplica (refactoring — no cambia comportamiento de la API)

---

## Estado previo (HU-001 ya implementó)

- ✅ `IndicadorCalculator` (ABC) en `app/general/calculadores.py`
- ✅ `IndicadorCalculatorTresNiveles` en `app/general/calculadores.py`
- ✅ `test_calculadores.py` con 8 tests de `IndicadorCalculatorTresNiveles`

## Lo que falta

- `Termostato.__init__` hardcodea `IndicadorCalculatorTresNiveles` — no acepta DI
- `IndicadorCalculatorCincoNiveles` no implementada (AC3)
- Factory no soporta inyectar calculador (AC4)
- Tests de DI + 5 niveles ausentes (AC6)
- Documentación de cómo agregar estrategias (AC7)

---

## Tareas

### T1 - Agregar `IndicadorCalculatorCincoNiveles` a `calculadores.py` (10 min)
- [ ] 5 niveles: EXCELENTE (>4.5), BUENO (>3.5), NORMAL (>2.5), BAJO (>1.5), CRITICO

### T2 - Habilitar DI en `Termostato` (10 min)
- [ ] Agregar parámetro `indicador_calc=None` a `Termostato.__init__`
- [ ] Pasar `indicador_calc` a `TermostatoService` (ya lo soporta)
- [ ] Default: `IndicadorCalculatorTresNiveles()` — sin breaking changes

### T3 - Actualizar `factory.py` (5 min)
- [ ] Agregar parámetro `indicador_calc=None` a `TermostatoFactory.crear_termostato()`
- [ ] Pasar al constructor de `Termostato`

### T4 - Tests (15 min)
- [ ] `test_calculadores.py` — agregar tests de `IndicadorCalculatorCincoNiveles`
- [ ] `tests/test_termostato.py` — agregar tests de DI (estrategia inyectada funciona)

### T5 - Documentar en `docs/desarrollo/ARQUITECTURA.md` (10 min)
- [ ] Sección "Cómo agregar una nueva estrategia de indicador"
- [ ] Ejemplo con `IndicadorCalculatorCincoNiveles`

### T6 - Regresión + quality check (5 min)
- [ ] `pytest tests/` — todos pasan
- [ ] `/quality-check app/`

---

## Archivos afectados

| Archivo | Acción |
|---------|--------|
| `app/general/calculadores.py` | Agregar `IndicadorCalculatorCincoNiveles` |
| `app/general/termostato.py` | Agregar parámetro `indicador_calc` |
| `app/configuracion/factory.py` | Agregar parámetro `indicador_calc` |
| `tests/test_calculadores.py` | Agregar tests 5 niveles |
| `tests/test_termostato.py` | Agregar tests de DI |
| `docs/desarrollo/ARQUITECTURA.md` | Crear / actualizar |

**Sin cambios en:** `api.py`, `conftest.py`, `termostato_service.py`, `test_api.py`

---

**Estado:** ✅ COMPLETADO (6/6 tareas)
**Creado:** 2026-02-22
