# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Flask REST API backend for a thermostat system (app_termostato). This is the backend component of a client-server architecture, consumed by the frontend `webapp_termostato`. Part of an academic/didactic case study demonstrating REST API design.

## Commands

**Run the server:**
```bash
python run.py
```
Server runs on http://localhost:5050 by default.

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Environment variables:**
- `PORT`: Server port (default: 5050)
- `DEBUG`: Debug mode (default: True)

## Architecture

```
run.py                      # Entry point - launches Flask server
├── app/                    # Application package
│   ├── __init__.py
│   ├── servicios/
│   │   └── api.py          # REST endpoints (Flask routes)
│   └── general/
│       ├── termostato.py   # Termostato model (data class with properties)
│       └── configurador.py # Singleton pattern - holds shared Termostato instance
├── tests/                  # Test cases
└── quality/                # Quality agent scripts and reports
```

**Key patterns:**
- `Configurador.termostato` provides a singleton Termostato instance shared across the API
- All API endpoints in `app/servicios/api.py` use this shared instance
- The Termostato class uses Python properties with setters for data validation (int/float conversion)

## API Endpoints

All endpoints under `/termostato/` support GET (retrieve) and POST (update):
- `/temperatura_ambiente/` - POST field: `ambiente`
- `/temperatura_deseada/` - POST field: `deseada`
- `/bateria/` - POST field: `bateria`
- `/estado_climatizador/` - POST field: `climatizador`
- `/indicador/` - POST field: `indicador`

Health check: `GET /comprueba/`

## Language

The codebase uses Spanish for variable names, comments, and API field names. Maintain this convention.

## Jira Integration (MCP)

Este proyecto está vinculado al proyecto Jira `app_termostato`. Usar las herramientas MCP de Atlassian para:

- **Buscar issues**: `mcp__atlassian__search` con query relacionado a "app_termostato"
- **Buscar con JQL**: `mcp__atlassian__searchJiraIssuesUsingJql` con `project = "app_termostato"`
- **Obtener issue específico**: `mcp__atlassian__getJiraIssue` con el issueIdOrKey (ej: APP-123)
- **Crear issues**: `mcp__atlassian__createJiraIssue` con projectKey="APP" (o la clave del proyecto)

Consultar Jira antes de implementar nuevas funcionalidades para verificar historias de usuario y requisitos.

## Quality Agent

Este proyecto incluye un ambiente agentico para calidad de codigo implementado en la rama `TER-17`.

### Estructura del Ambiente Agentico

```
.claude/
├── agents/
│   └── quality-agent.md      # Agente especializado en calidad
├── commands/
│   ├── quality-check.md      # Comando /quality-check
│   └── quality-report.md     # Comando /quality-report
└── settings.json             # Configuracion y umbrales

quality/
├── scripts/
│   ├── calculate_metrics.py  # Calcula LOC, CC, MI, Pylint
│   ├── validate_gates.py     # Valida quality gates
│   └── generate_report.py    # Genera reportes Markdown
├── reports/                  # Reportes generados (JSON y MD)
└── requirements.txt          # Dependencias del ambiente de calidad
```

### Metricas Medidas

| Metrica | Herramienta | Umbral | Descripcion |
|---------|-------------|--------|-------------|
| CC | `radon cc` | <= 10 | Complejidad Ciclomatica - caminos en el codigo |
| MI | `radon mi` | > 20 | Indice de Mantenibilidad (0-100) |
| Pylint | `pylint` | >= 8.0 | Score de calidad y estilo |
| LOC | `radon raw` | <= 50/funcion | Lineas de codigo por funcion |

### Comandos Disponibles

| Comando | Descripcion |
|---------|-------------|
| `/quality-check [path]` | Analisis rapido de calidad |
| `/quality-report` | Reporte completo en Markdown |

### Uso del Agente

El agente se activa automaticamente cuando:
- Se modifican archivos Python
- Se solicita "analizar calidad" o "verificar codigo"
- Se invoca explicitamente: "usar quality-agent"

### Ejecucion Manual de Scripts

```bash
# Instalar dependencias
pip install -r quality/requirements.txt

# Analizar modulo especifico
python quality/scripts/calculate_metrics.py app/general/

# Analizar todo el proyecto
python quality/scripts/calculate_metrics.py app/

# Validar quality gates
python quality/scripts/validate_gates.py quality/reports/quality_*.json

# Generar reporte Markdown
python quality/scripts/generate_report.py quality/reports/quality_*.json
```

### Interpretacion de Resultados

**Grados de Calidad:**
- **A**: Todos los gates pasan (3/3)
- **B**: 2/3 gates pasan
- **C**: 1/3 gates pasan
- **F**: Ningun gate pasa

**Distribucion de Complejidad (CC):**
- A (1-5): Excelente - codigo simple
- B (6-10): Aceptable - complejidad moderada
- C (11-20): Riesgoso - considerar refactorizar
- D-F (21+): Critico - refactorizar obligatorio

### Configuracion

Los umbrales se configuran en `.claude/settings.json`:

```json
{
  "quality_gates": {
    "max_complexity": 10,
    "min_maintainability": 20,
    "min_pylint_score": 8.0,
    "max_function_lines": 50
  }
}
```

### Estado Actual del Proyecto

Ultima ejecucion (2025-12-19):
- **app/general/**: Grado A (CC=1.08, MI=100.0, Pylint=9.67)
- **app/servicios/**: Grado A (CC=2.88, MI=83.3, Pylint=8.6)

## Documentación de Mantenimiento

Este proyecto mantiene documentación estructurada en la carpeta `docs/` para análisis, mantenimiento y desarrollo.

### Estructura de Documentación

```
docs/
├── analisis/                    # Análisis y auditorías técnicas
│   ├── 2026-02-06_analisis_diseno.md
│   └── README.md
├── mantenimiento/               # Gestión de deuda técnica
│   ├── historias_usuario/       # HUs de refactoring (Jira-ready)
│   │   ├── HU-001_refactor_termostato.md
│   │   ├── HU-002_eliminar_singleton.md
│   │   └── ... (8 HUs totales)
│   ├── decisiones_arquitectura/ # ADRs
│   │   └── ADR-001_factory_vs_singleton.md
│   └── README.md
└── desarrollo/                  # Guías para contributors
    └── README.md
```

### Análisis de Diseño

**Último análisis:** 2026-02-06
**Enfoque:** Principios SOLID, Cohesión, Acoplamiento, Code Smells
**Calificación:** C+ (6.5/10)

**Acceso rápido:**
- [📄 Análisis completo](docs/analisis/2026-02-06_analisis_diseno.md)
- [📊 Índice de análisis](docs/analisis/README.md)

**Hallazgos principales:**
- 🔴 God Object en clase Termostato (6 responsabilidades)
- 🔴 Singleton anti-pattern en Configurador
- 🔴 Duplicación masiva en endpoints (~200 LOC)

### Deuda Técnica

**Epic activa:** Refactorización Deuda Técnica - Diseño
**Total:** 8 Historias de Usuario | ~50 Story Points

**Distribución por prioridad:**
- 🔴 **Alta:** 3 HUs (21 SP) - Refactorizar Termostato, Eliminar Singleton, Eliminar duplicación
- 🟡 **Media:** 3 HUs (6 SP) - Validaciones, imports, Swagger config
- 🟢 **Baja:** 2 HUs (13 SP) - Strategy Pattern, DI Container

**Acceso rápido:**
- [📋 Roadmap completo](docs/mantenimiento/README.md)
- [📝 Historias de usuario](docs/mantenimiento/historias_usuario/)
- [🏛️ Decisiones arquitectónicas (ADRs)](docs/mantenimiento/decisiones_arquitectura/)

### Sincronización con Jira

Las historias de usuario en `docs/mantenimiento/historias_usuario/` están en formato **Jira-ready**:

1. Crear Epic en Jira: "Refactorización Deuda Técnica - Diseño"
2. Migrar HUs de Markdown → Jira (copiar contenido)
3. Actualizar campo `Jira: TBD` en archivos locales con el ID asignado
4. Mantener estado sincronizado durante desarrollo

**Formato de HU:** Cada archivo `.md` contiene:
- Historia de usuario (Como... Quiero... Para...)
- Criterios de aceptación
- Tareas técnicas detalladas
- Contexto y referencias al análisis
- Escenarios de testing
- Métricas antes/después
- Riesgos y mitigaciones
- Definición de Done

### Workflows Recomendados

**Al trabajar en refactorización:**
1. Consultar [análisis de diseño](docs/analisis/2026-02-06_analisis_diseno.md) para contexto
2. Revisar HU correspondiente en [historias_usuario/](docs/mantenimiento/historias_usuario/)
3. Seguir criterios de aceptación y tareas técnicas
4. Ejecutar `/quality-check` antes de commit
5. Actualizar estado de HU al completar

**Al tomar decisiones arquitectónicas:**
1. Consultar [ADRs existentes](docs/mantenimiento/decisiones_arquitectura/)
2. Si es decisión nueva, crear ADR-XXX.md siguiendo formato de ADR-001
3. Referenciar ADR desde HU correspondiente
