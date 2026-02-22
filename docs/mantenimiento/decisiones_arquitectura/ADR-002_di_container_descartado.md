# ADR-002: DI Container descartado — Application Factory + TermostatoFactory son suficientes

**Estado:** ✅ Aceptado
**Fecha:** 2026-02-22
**HU relacionada:** HU-008

---

## Contexto

HU-008 propuso implementar un `DIContainer` centralizado para gestionar la inyección de dependencias del sistema.

## Decisión

**Se descarta HU-008.** No se implementará un DI Container explícito.

## Justificación

Al momento de evaluar HU-008, las HUs anteriores ya resolvieron el problema subyacente:

| Necesidad | Cubierta por |
|-----------|-------------|
| Centralizar creación de dependencias | `TermostatoFactory` (HU-002) |
| DI en producción | `create_app(termostato=None)` Application Factory (HU-002) |
| DI en tests con mocks | `conftest.py` + `create_app(termostato=Mock())` (HU-002) |
| Lazy singleton en Flask | Una app Flask por proceso — singleton implícito |
| Extensibilidad de estrategias | `IndicadorCalculator` ABC inyectable (HU-001, HU-007) |

Agregar `DIContainer` habría duplicado funcionalidad existente sumando ~150 LOC de infraestructura sin beneficio funcional.

La propia HU-008 advertía: *"DI Container puede ser over-engineering para un proyecto pequeño."*

## Consecuencias

- ✅ Menor complejidad — el sistema mantiene el mínimo necesario
- ✅ Sin deuda técnica adicional
- ✅ Los patrones existentes (Application Factory + Factory Method) son el estándar Flask
- ⚠️ Si el proyecto crece significativamente (>10 servicios), reconsiderar con una librería como `dependency-injector`
