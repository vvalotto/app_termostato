# Plan de Implementación — Skill `implement-us`

**Proyecto:** app_termostato
**Epic:** Refactorización Deuda Técnica - Diseño
**Skill:** `implement-us` (claude-dev-kit)
**Perfil activo:** `flask-rest`
**Fecha:** 2026-02-21
**Estado:** 📋 Pendiente

---

## 1. Validación del Perfil `flask-rest`

Estado: ✅ **COMPATIBLE — sin cambios requeridos**

| Aspecto | Estado | Detalle |
|---------|--------|---------|
| Perfil instalado | ✅ | `flask-rest` en `.claude/config.json` |
| Arquitectura | ✅ | `layered` (capas: general / servicios / datos) |
| Test framework | ✅ | `pytest` con Flask test client |
| Componentes soportados | ✅ | Blueprint, Service, Repository, Model |
| Quality Gates | ✅ | Pylint ≥ 8.0, CC ≤ 10, MI ≥ 20, Coverage ≥ 95% |
| Formato de HUs | ✅ | 100% compatible (Historia / ACs / Tareas / DoD) |
| CLAUDE.md | ✅ | No modificado por el instalador |
| Ambiente de calidad previo | ✅ | Conservado (agents/, commands/, settings.json) |

> **Nota sobre cobertura:** El umbral de cobertura del skill es **95%**. Los tests actuales
> cubren bien el código existente (62 tests). Al refactorizar, se deberá extender la suite
> para mantener ese umbral. No es bloqueante, pero requiere atención en HU-001.

---

## 2. Orden de Implementación

```
HU-005 → HU-004 → HU-003 → HU-002 + HU-006 → HU-001 → HU-007 → HU-008
```

### Grafo de Dependencias

```
HU-004  HU-005  HU-006      ← sin dependencias (cualquier orden)
                 │
               HU-003        ← sin dependencias directas
                 │
               HU-002 ───────────────────────────────────────────┐
                 │                                                 │
               HU-001        ← REQUIERE HU-002               HU-008
                 │
               HU-007        ← REQUIERE HU-001
```

---

## 3. Fases de Implementación

### Fase 1 — Quick Wins (1 día) 🟢

Cambios pequeños, riesgo bajo, sin dependencias. Ideales para validar el flujo del skill.

| HU | Título | SP | Archivo/s afectados | Comando |
|----|--------|----|---------------------|---------|
| HU-005 | Refactorizar imports y code smells | 1 | `termostato.py`, `api.py` | `/implement-us HU-005` |
| HU-004 | Validar estado_climatizador | 2 | `termostato.py`, `config.py` | `/implement-us HU-004` |

**HU-005 — Detalle:**
- Mover import de `RegistroTemperatura` al top de `termostato.py` (actualmente en línea 143 dentro de método)
- Crear clase `AppState` en `api.py` para encapsular `_inicio_servidor` (variable global)
- Actualizar `comprueba()` para usar `app_state.inicio_servidor`

**HU-004 — Detalle:**
- Agregar constantes `ENCENDIDO`/`APAGADO` en módulo de configuración
- Agregar validación en setter de `estado_climatizador` que rechace valores inválidos

---

### Fase 2 — Reducir Duplicación (1 día) 🟡

| HU | Título | SP | Archivo/s afectados | Comando |
|----|--------|----|---------------------|---------|
| HU-003 | Eliminar duplicación en endpoints | 5 | `api.py` | `/implement-us HU-003` |

**HU-003 — Detalle:**
- Los 5 endpoints (`temperatura_ambiente`, `temperatura_deseada`, `bateria`, `estado_climatizador`, `indicador`) siguen el mismo patrón GET/POST (~200 LOC duplicadas)
- Crear función genérica o decorador `@endpoint_termostato` que centralice la lógica
- Tests de regresión obligatorios antes de merge

---

### Fase 3 — Desacoplar Arquitectura (2 días) 🔴

| HU | Título | SP | Archivo/s afectados | Prerequisito | Comando |
|----|--------|----|---------------------|--------------|---------|
| HU-002 | Eliminar Singleton en Configurador | 8 | `configurador.py`, `api.py` | ninguno | `/implement-us HU-002` |
| HU-006 | Extraer configuración Swagger | 3 | `api.py` → `swagger_config.py` | ninguno | `/implement-us HU-006` |

**HU-002 — Detalle:**
- Reemplazar patrón Singleton por Factory `create_termostato()`
- Introducir `create_app()` (application factory de Flask) para inyección de dependencias
- Breaking change potencial en tests que usan `Configurador.termostato` directamente

**HU-006 — Detalle (paralelo con HU-002):**
- Extraer configuración Swagger de `api.py` a módulo `app/configuracion/swagger_config.py`
- Riesgo bajo — refactoring estructural sin cambio de comportamiento

---

### Fase 4 — Separar Responsabilidades (3 días) 🔴

| HU | Título | SP | Archivos resultantes | Prerequisito | Comando |
|----|--------|----|----------------------|--------------|---------|
| HU-001 | Refactorizar Termostato (God Object) | 13 | 4 nuevos módulos | **HU-002** | `/implement-us HU-001` |

**HU-001 — Detalle (mayor complejidad, ⭐):**

`app/general/termostato.py` → 4 componentes:

| Componente | Responsabilidad |
|------------|-----------------|
| `TermostatoModelo` | Solo almacenamiento de estado |
| `TermostatoValidador` | Rangos y conversiones de tipo |
| `IndicadorCalculador` | Lógica de cálculo del indicador |
| `TermostatoServicio` | Orquestador — coordina los anteriores |

> Los 36 tests de `test_termostato.py` deben seguir pasando sin modificación.

---

### Fase 5 — Patrones Avanzados (2 días) 🟢

| HU | Título | SP | Archivo/s afectados | Prerequisito | Comando |
|----|--------|----|---------------------|--------------|---------|
| HU-007 | Strategy Pattern para indicador | 5 | `estrategias_indicador.py` | **HU-001** | `/implement-us HU-007` |
| HU-008 | Crear DI Container | 8 | `di_container.py` | **HU-002** | `/implement-us HU-008` |

**HU-007 — Detalle:**
- Crear interfaz `EstrategiaIndicador` + implementaciones (`IndicadorNormal`, `IndicadorAhorro`, etc.)
- Extiende `IndicadorCalculador` de HU-001

**HU-008 — Detalle:**
- Centralizar toda la inyección de dependencias en `app/configuracion/di_container.py`
- Requiere Factory de HU-002

---

## 4. Resumen General

| Fase | HUs | SP | Días estimados | Riesgo |
|------|-----|----|----------------|--------|
| 1 — Quick Wins | HU-005, HU-004 | 3 | 1 | 🟢 Bajo |
| 2 — Duplicación | HU-003 | 5 | 1 | 🟡 Medio |
| 3 — Desacoplar | HU-002, HU-006 | 11 | 2 | 🔴 Alto |
| 4 — Responsabilidades | HU-001 | 13 | 3 | 🔴 Muy Alto |
| 5 — Patrones | HU-007, HU-008 | 13 | 2 | 🟢 Bajo |
| **Total** | **8 HUs** | **45 SP** | **~9 días** | |

---

## 5. Archivos Críticos

| Archivo | Rol | HUs que lo modifican |
|---------|-----|----------------------|
| `app/general/termostato.py` | God Object a refactorizar | HU-001, HU-004, HU-005 |
| `app/configuracion/configurador.py` | Singleton a eliminar | HU-002 |
| `app/servicios/api.py` | Duplicación + acoplamiento | HU-002, HU-003, HU-005, HU-006 |
| `tests/test_termostato.py` | 36 tests que deben seguir pasando | HU-001, HU-004 |
| `tests/test_api.py` | 26 tests de regresión | HU-002, HU-003 |
| `docs/mantenimiento/README.md` | Estado de HUs (actualizar al completar) | Todas |

---

## 6. Tracking de Tiempo

El kit registra automáticamente el tiempo en `.claude/tracking/HU-XXX-tracking.json`.

**Al iniciar cada HU**, ejecutar en Fase 0:
```python
from .claude.tracking.time_tracker import TimeTracker
tracker = TimeTracker("HU-XXX", "Título de la HU", puntos, "app_termostato")
tracker.start_tracking()
tracker.start_phase(0, "Validación de Contexto")
```

**Durante implementación (Fase 3)**, registrar cada tarea:
```python
tracker.start_task("task_001", "Descripción", "refactor", estimated_minutes=5)
# ... trabajo ...
tracker.end_task("task_001", file_created="app/general/termostato.py")
```

**Al finalizar (Fase 9)**:
```python
tracker.end_tracking()
```

**Archivos generados:**
```
.claude/tracking/
├── HU-005-tracking.json    ← tiempo por fase y tarea, varianza estimado vs real
├── HU-004-tracking.json
└── ...
```

> **HU-005:** tracking no registrado (omisión en primera ejecución). Aplica desde HU-004.

---

## 7. Flujo de Trabajo por HU (skill implement-us)

Cada `/implement-us HU-XXX` ejecuta 10 fases + commit de cierre:

```
Fase 0: Validación de contexto     (automático)
Fase 1: Escenarios BDD Gherkin     ← ⏸ APROBACIÓN USUARIO (ver criterio BDD abajo)
Fase 2: Plan de implementación     ← ⏸ APROBACIÓN USUARIO
Fase 3: Implementación del código  (automático, con tracking de tiempo)
Fase 4: Tests unitarios            (automático)
Fase 5: Tests de integración       (automático)
Fase 6: Validación BDD             (automático, solo si Fase 1 fue ejecutada)
Fase 7: Quality Gates              (automático — Pylint, CC, MI)
Fase 8: Actualización documentación ← ⏸ APROBACIÓN USUARIO
Fase 9: Reporte final              (automático)
── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ── ──
Commit ← ⏸ USUARIO VERIFICA Y CONFIRMA → commit por HU
```

**Formato de commit por HU:**
```
refactor(HU-XXX): <título de la HU>

- <archivo>: <cambio principal>
- <archivo>: <cambio principal>

Tests: N/N | Pylint: X.XX | CC: A | MI: A

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

### Criterio BDD (Fase 1)

> **BDD aplica solo cuando la HU cambia el comportamiento observable por el usuario/cliente del API.**
> Refactorings internos sin cambio de contrato externo → BDD se omite.

| HU | ¿BDD aplica? | Motivo |
|----|-------------|--------|
| HU-005 | ❌ No | Refactoring interno puro (mover imports, encapsular variable). El API se comporta exactamente igual. |
| HU-004 | ✅ Sí | Agrega validación en `POST /estado_climatizador/`. Cambia el contrato del endpoint: antes aceptaba cualquier valor, después rechaza valores inválidos. |
| HU-003 | ❌ No | Eliminación de duplicación interna. Los endpoints mantienen el mismo contrato. |
| HU-006 | ❌ No | Mover configuración Swagger a otro módulo. Sin cambio de comportamiento. |
| HU-002 | ❌ No | Cambio arquitectónico interno (Singleton → Factory). El API externo no cambia. |
| HU-001 | ❌ No | Separación de responsabilidades interna. Sin cambio de contrato externo. |
| HU-007 | ✅ Sí | Strategy Pattern para indicador puede introducir nuevos comportamientos de cálculo observables. Evaluar al implementar. |
| HU-008 | ❌ No | DI Container es infraestructura interna. Sin cambio de contrato externo. |

### Criterio ADR (Fase 0 — Validación)

> **En Fase 0 siempre revisar `docs/mantenimiento/decisiones_arquitectura/`** para verificar
> si existe un ADR que gobierne la HU. Si existe, la implementación debe seguirlo.

| HU | ADR relacionado | Impacto |
|----|----------------|---------|
| HU-005 | Ninguno | Sin restricción arquitectónica |
| HU-004 | Ninguno | Sin restricción arquitectónica |
| HU-003 | Ninguno | Sin restricción arquitectónica |
| HU-006 | Ninguno | Sin restricción arquitectónica |
| HU-002 | **ADR-001** ✅ | Usar Factory Pattern puro + `create_app()` con DI. No usar Singleton mejorado (❌ rechazado en ADR-001). |
| HU-001 | Derivado de ADR-001 | La separación de Termostato debe ser compatible con el Factory de HU-002. |
| HU-007 | Ninguno (crear ADR-002 si aplica) | Evaluar si la estrategia elegida requiere decisión arquitectónica formal. |
| HU-008 | ADR-001 (pospuso DI Container) | Retomar evaluación: ¿realmente necesario o over-engineering? |

---

## 8. Progreso

| HU | Título | SP | Estado | Fecha inicio | Fecha fin |
|----|--------|----|--------|--------------|-----------|
| HU-005 | Refactorizar imports y code smells | 1 | ✅ Completado | 2026-02-21 | 2026-02-21 |
| HU-004 | Validar estado_climatizador | 2 | ✅ Completado | 2026-02-21 | 2026-02-21 |
| HU-003 | Eliminar duplicación en endpoints | 5 | 📋 Pendiente | — | — |
| HU-006 | Extraer configuración Swagger | 3 | 📋 Pendiente | — | — |
| HU-002 | Eliminar Singleton en Configurador | 8 | 📋 Pendiente | — | — |
| HU-001 | Refactorizar Termostato (God Object) | 13 | 📋 Pendiente | — | — |
| HU-007 | Strategy Pattern para indicador | 5 | 📋 Pendiente | — | — |
| HU-008 | Crear DI Container | 8 | 📋 Pendiente | — | — |
| **Total** | | **45 SP** | **2/8 completadas** | | |

---

## 9. Primer Paso Recomendado

```
/implement-us HU-005
```

Es la HU más pequeña (1 SP), permite validar el flujo completo del skill con riesgo mínimo.

---

**Creado:** 2026-02-21
**Basado en:** [Análisis de diseño 2026-02-06](../analisis/2026-02-06_analisis_diseno.md)
**Referencia de HUs:** [historias_usuario/](./historias_usuario/)
