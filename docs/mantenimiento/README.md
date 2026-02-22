# Mantenimiento y Deuda Técnica

Gestión activa de deuda técnica, refactorizaciones y decisiones arquitectónicas.

## 📁 Estructura

```
mantenimiento/
├── historias_usuario/         # HUs de refactoring (Jira-ready)
│   ├── HU-001_refactor_termostato.md
│   ├── HU-002_eliminar_singleton.md
│   └── ...
└── decisiones_arquitectura/   # ADRs (Architecture Decision Records)
    └── ADR-001_factory_vs_singleton.md
```

## 🎯 Épicas Activas

### Epic: Refactorización Deuda Técnica - Diseño

**Origen:** [Análisis de Diseño 2026-02-06](../analisis/2026-02-06_analisis_diseno.md)
**Estado:** Planificación
**Total:** 8 HUs | ~50 Story Points

#### 🔴 Prioridad ALTA (21 SP)

| HU | Título | SP | Estado | Jira |
|----|--------|-------|--------|------|
| [HU-001](./historias_usuario/HU-001_refactor_termostato.md) | Refactorizar clase Termostato (God Object) | 13 | ✅ Completado | - |
| [HU-002](./historias_usuario/HU-002_eliminar_singleton.md) | Eliminar Singleton en Configurador | 8 | ✅ Completado | - |
| [HU-003](./historias_usuario/HU-003_eliminar_duplicacion_endpoints.md) | Eliminar duplicación en endpoints | 5 | ✅ Completado | - |

#### 🟡 Prioridad MEDIA (6 SP)

| HU | Título | SP | Estado | Jira |
|----|--------|-------|--------|------|
| [HU-004](./historias_usuario/HU-004_validar_estado_climatizador.md) | Validar estado_climatizador | 2 | ✅ Completado | - |
| [HU-005](./historias_usuario/HU-005_refactor_imports_estructura.md) | Refactorizar imports y estructura | 1 | ✅ Completado | - |
| [HU-006](./historias_usuario/HU-006_extraer_config_swagger.md) | Extraer configuración Swagger | 3 | ✅ Completado | - |

#### 🟢 Prioridad BAJA (13 SP)

| HU | Título | SP | Estado | Jira |
|----|--------|-------|--------|------|
| [HU-007](./historias_usuario/HU-007_strategy_indicador.md) | Strategy Pattern para indicador | 5 | ✅ Completado | - |
| [HU-008](./historias_usuario/HU-008_di_container.md) | Crear DI Container | 8 | 📋 Pendiente | - |

## 📐 Decisiones Arquitectónicas (ADRs)

| ID | Título | Estado | Fecha |
|----|--------|--------|-------|
| [ADR-001](./decisiones_arquitectura/ADR-001_factory_vs_singleton.md) | Factory Pattern vs Singleton | ✅ Aceptado | 2026-02-06 |

## 📊 Roadmap de Refactorización

### Fase 1: Quick Wins (1 día) 🎯
- HU-004: Validar estado_climatizador
- HU-005: Refactorizar imports

### Fase 2: Reducir Duplicación (1 día)
- HU-003: Eliminar duplicación endpoints

### Fase 3: Desacoplar (2 días)
- HU-002: Eliminar Singleton

### Fase 4: Separar Responsabilidades (3 días)
- HU-001: Refactorizar Termostato

### Fase 5: Patrones Avanzados (2 días)
- HU-006: Extraer config Swagger
- HU-007: Strategy Pattern indicador
- HU-008: DI Container

**Total estimado:** 9 días (~2 sprints)

## 🔄 Proceso de Sincronización con Jira

1. **Crear Epic en Jira:** "Refactorización Deuda Técnica - Diseño"
2. **Migrar HUs:** Copiar contenido de Markdown a Jira
3. **Actualizar ID:** Agregar ID de Jira en columna correspondiente
4. **Tracking:** Mantener estado sincronizado (Pendiente/En Progreso/Completado)

### Template de Epic Jira

```
Nombre: Refactorización Deuda Técnica - Diseño
Descripción: Resolver code smells y violaciones de SOLID identificados en análisis 2026-02-06
Origen: docs/analisis/2026-02-06_analisis_diseno.md
Story Points: 50
Prioridad: Alta
```

## 📈 Métricas de Progreso

**Completadas:** 7/8 (87.5%)
**En progreso:** 0/8 (0%)
**Pendientes:** 1/8 (12.5%)

**Story Points:**
- Completados: 37/50 (74%)
- Alta prioridad: 21/21 (100%) ✅
- Media prioridad: 6/6 (100%) ✅
- Baja prioridad: 5/13 (38%)

---

**Última actualización:** 2026-02-22
