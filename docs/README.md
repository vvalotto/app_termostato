# Documentación — app_termostato

Índice general de documentación del proyecto.

## Estructura

```
docs/
├── analisis/                    # Análisis y auditorías técnicas puntuales
├── arquitectura/                # Arquitectura del sistema (C4 + detalle de módulos)
├── mantenimiento/               # Deuda técnica, HUs, ADRs, planes y reportes
│   ├── historias_usuario/       # HUs de refactoring (formato Jira-ready)
│   ├── decisiones_arquitectura/ # ADRs (Architecture Decision Records)
│   ├── plans/                   # Planes de implementación por HU
│   └── reports/                 # Reportes de HUs completadas
├── quality/                     # Reportes y configuración del agente de calidad
├── testing/                     # Plan de testing de sistema
└── tutoriales/                  # Tutoriales y guías de herramientas
```

---

## Arquitectura

Documentación de la arquitectura del sistema: modelo C4, estructura de módulos, patrones de diseño y principios SOLID aplicados.

**[Ver arquitectura →](./arquitectura/)**

- [Arquitectura del sistema (módulos y patrones)](./arquitectura/ARQUITECTURA.md)
- [Modelo C4 (contexto, contenedores, componentes)](./arquitectura/arquitectura_c4.md)

---

## Análisis y Auditorías

Auditorías técnicas puntuales: diseño, calidad, cohesión, acoplamiento.

**[Ver análisis →](./analisis/)**

| Fecha | Tipo | Calificación |
|-------|------|-------------|
| 2026-02-06 | Diseño SOLID | C+ (6.5/10) → resuelto mediante refactoring |

---

## Mantenimiento y Deuda Técnica

Gestión de deuda técnica: HUs, ADRs, planes y reportes de implementación.

**[Ver mantenimiento →](./mantenimiento/)**

**Epic "Refactorización Deuda Técnica" — CERRADA**

| Estado | HUs | SP |
|--------|-----|----|
| Completadas | 7/8 | 37 |
| Descartadas | 1/8 (HU-008 over-engineering) | — |

ADRs documentados: ADR-001 (Factory vs Singleton), ADR-002 (DI Container descartado)

---

## Quality

Reportes de calidad y configuración del agente de métricas.

**[Ver quality →](./quality/)**

**Última ejecución (2025-12-21):** Grado A — CC=1.69, MI=90.15, Pylint=8.89

---

## Testing

Plan de testing de sistema y guías de ejecución.

**[Ver testing →](./testing/)**

- [Plan de testing de sistema](./testing/plan_testing_sistema.md) — 54 casos especificados, 64 tests automatizados

---

## Tutoriales

**[Ver tutoriales →](./tutoriales/)**

- [Tutorial: Ambiente Agéntico de Calidad Python](./tutoriales/Tutorial%20Ambiente%20Agentico%20Calidad%20Python.md)

---

## Estado del Proyecto

| Dimensión | Estado |
|-----------|--------|
| Versión | 1.2.0 |
| Quality Gates | 3/3 (Pylint=8.89, CC=1.69, MI=90.15) |
| Tests | 164 unitarios/integración + 64 sistema |
| Deuda técnica | Épica cerrada (7/8 HUs) |
| Despliegue | Google Cloud Run — us-central1 |

**Última actualización:** 2026-02-22
