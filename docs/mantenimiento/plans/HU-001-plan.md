# Plan de Implementación: HU-001 - Refactorizar clase Termostato (God Object)

**Patrón:** Flask REST (Layered)
**Producto:** app_termostato
**Estimación HU:** 13 SP
**Estimación Total:** 2h 20min
**BDD:** No aplica (refactoring interno sin cambio de comportamiento de la API)

---

## Análisis del código actual

`termostato.py` tiene 164 LOC y 6 responsabilidades en una sola clase:
1. **Modelo de datos** — almacena `_temperatura_ambiente`, `_temperatura_deseada`, `_carga_bateria`, `_estado_climatizador`
2. **Validación** — 4 setters con lógica de validación de rangos
3. **Cálculo de indicador** — property `indicador` con lógica condicional
4. **Persistencia** — `_guardar_estado()` y `cargar_estado()`
5. **Historial** — `_registrar_en_historial()`
6. **Orquestación** — setters combinan validación + persistencia + historial

**Estrategia:** Extraer responsabilidades a módulos especializados. `Termostato` mantiene su interfaz pública (mismos setters/getters/métodos) pero delega internamente a los nuevos componentes. Sin breaking changes en api.py, conftest.py ni factory.py.

---

## Tareas

### T1 - Crear `app/general/termostato_modelo.py` (10 min)
- [ ] `@dataclass class TermostatoModelo` con los 4 campos del estado
- [ ] Sin lógica — solo datos

### T2 - Crear `app/general/validators.py` (15 min)
- [ ] `class TermostatoValidator`
  - `validar_temperatura_ambiente(valor: int) -> int`
  - `validar_temperatura_deseada(valor: int) -> int`
  - `validar_carga_bateria(valor: float) -> float`
  - `validar_estado_climatizador(valor: str) -> str`
- [ ] Cada método hace conversión de tipo + validación de rango + raise ValueError si falla
- [ ] Misma lógica que los setters actuales (extraer, no cambiar)

### T3 - Crear `app/general/calculadores.py` (15 min)
- [ ] `class IndicadorCalculator(ABC)` con método abstracto `calcular(carga_bateria: float) -> str`
- [ ] `class IndicadorCalculatorTresNiveles(IndicadorCalculator)` — implementación actual
- [ ] Misma lógica que el property `indicador` actual

### T4 - Crear `app/servicios/termostato_service.py` (25 min)
- [ ] `class TermostatoService` — orquesta modelo, validator, persistidor, historial, calculador
- [ ] Métodos explícitos de actualización:
  - `actualizar_temperatura_ambiente(valor) -> None`
  - `actualizar_temperatura_deseada(valor) -> None`
  - `actualizar_carga_bateria(valor) -> None`
  - `actualizar_estado_climatizador(valor) -> None`
  - `obtener_indicador() -> str`
  - `cargar_estado() -> None`
- [ ] Cada método: valida → actualiza modelo → persiste → registra historial (si aplica)

### T5 - Refactorizar `app/general/termostato.py` (20 min)
- [ ] `Termostato.__init__` crea `TermostatoValidator`, `IndicadorCalculatorTresNiveles`, y construye `TermostatoService` internamente
- [ ] Setters delegan a `TermostatoService.actualizar_*()`
- [ ] Property `indicador` delega a `TermostatoService.obtener_indicador()`
- [ ] `cargar_estado()` delega a `TermostatoService.cargar_estado()`
- [ ] **Interfaz pública idéntica** — sin breaking changes

### T6 - Tests nuevos (30 min)
- [ ] `tests/test_validators.py`
  - 8 tests: cada campo con valor válido + valor fuera de rango
- [ ] `tests/test_calculadores.py`
  - 4 tests: NORMAL (>3.5), BAJO (2.5-3.5), CRITICO (<2.5), valores límite
- [ ] `tests/test_termostato_service.py`
  - 6 tests: actualizar cada campo + cargar estado + obtener indicador

### T7 - Regresión + quality check (15 min)
- [ ] `pytest tests/` — todos deben pasar sin cambios
- [ ] `/quality-check app/`

---

## Archivos afectados

| Archivo | Acción |
|---------|--------|
| `app/general/termostato_modelo.py` | Crear |
| `app/general/validators.py` | Crear |
| `app/general/calculadores.py` | Crear |
| `app/servicios/termostato_service.py` | Crear |
| `app/general/termostato.py` | Refactorizar (misma API pública) |
| `tests/test_validators.py` | Crear |
| `tests/test_calculadores.py` | Crear |
| `tests/test_termostato_service.py` | Crear |

**Sin cambios en:** `api.py`, `conftest.py`, `factory.py`, `test_api.py`, `test_termostato.py`

---

## Criterios de Aceptación verificables

| AC | Verificación |
|----|-------------|
| AC1: Termostato modelo puro | `termostato_modelo.py` sin lógica de negocio |
| AC2: TermostatoValidator | `validators.py` con 4 métodos de validación |
| AC3: IndicadorCalculator | `calculadores.py` con ABC + implementación |
| AC4: TermostatoService | `termostato_service.py` orquesta todo |
| AC5: Tests existentes pasan | `pytest tests/` sin cambios → 100% pass |
| AC6: Cobertura >= 85% | Nuevos módulos cubiertos por test_validators + test_calculadores + test_termostato_service |
| AC7: CC Termostato <= 5 | Setters reducidos a una línea de delegación |
| AC8: Quality gates | CC ≤ 10, MI > 20, Pylint ≥ 8.0 |

---

**Estado:** ✅ COMPLETADO (7/7 tareas)
**Creado:** 2026-02-22
**Completado:** 2026-02-22
