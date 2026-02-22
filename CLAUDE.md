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
run.py                          # Entry point - launches Flask server
├── app/
│   ├── configuracion/
│   │   ├── config.py           # Centralized config (env vars)
│   │   ├── factory.py          # TermostatoFactory — creates instances
│   │   └── swagger_config.py   # Flasgger config
│   ├── general/
│   │   ├── termostato.py       # Facade — stable public interface
│   │   ├── termostato_modelo.py# @dataclass — pure data
│   │   ├── validators.py       # TermostatoValidator — range validation
│   │   └── calculadores.py     # Strategy Pattern — indicator calculation
│   ├── servicios/
│   │   ├── api.py              # create_app() — Application Factory Pattern
│   │   ├── decorators.py       # @endpoint_termostato — eliminates GET/POST duplication
│   │   ├── errors.py           # error_response() — uniform error format
│   │   └── termostato_service.py # TermostatoService — orchestration
│   └── datos/                  # Repositories, persistidor, mappers
├── tests/                      # Test suite (164 unit/integration + 64 system tests)
└── quality/                    # Quality agent scripts and reports
```

**Key patterns:**
- `create_app()` in `api.py` implements the Application Factory Pattern with dependency injection
- `TermostatoFactory` creates independent Termostato instances (replaces old Singleton)
- `Termostato` acts as a Facade delegating to Validator, Service, and Calculator
- `@endpoint_termostato` decorator centralizes GET/POST logic across all endpoints
- Strategy Pattern in `calculadores.py` allows swapping indicator algorithm without modifying Termostato

## API Endpoints

Health check: `GET /comprueba/`
Full state: `GET /termostato/`
History: `GET /termostato/historial/?limite=N`

Individual endpoints — GET (retrieve) and POST (update) unless noted:
- `/termostato/temperatura_ambiente/` - POST field: `ambiente` (int, 0-50)
- `/termostato/temperatura_deseada/` - POST field: `deseada` (int, 15-30)
- `/termostato/bateria/` - POST field: `bateria` (float, 0.0-5.0)
- `/termostato/estado_climatizador/` - POST field: `climatizador` (apagado|encendido|enfriando|calentando)
- `/termostato/indicador/` - GET only (calculated from battery level, not writable)

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
├── arquitectura/                # Arquitectura del sistema (C4 + detalle de módulos)
├── mantenimiento/               # Deuda técnica, HUs, ADRs, plans, reports
│   ├── historias_usuario/       # HUs de refactoring (Jira-ready)
│   ├── decisiones_arquitectura/ # ADRs
│   ├── plans/                   # Planes de implementación por HU
│   └── reports/                 # Reportes de HUs completadas
├── quality/                     # Reportes y planes del agente de calidad
├── testing/                     # Plan de testing de sistema
└── tutoriales/                  # Tutoriales y guías de herramientas
```

### Estado de Deuda Técnica

**Epic "Refactorización Deuda Técnica - Diseño" — CERRADA**
- 7/8 HUs completadas | 37 SP implementados | HU-008 descartada (over-engineering)
- Código post-refactoring: Pylint=8.89, CC=1.69, MI=90.15 — Quality Gates 3/3

**Acceso rápido:**
- [📋 Roadmap y estado](docs/mantenimiento/README.md)
- [📝 Historias de usuario](docs/mantenimiento/historias_usuario/)
- [🏛️ ADRs](docs/mantenimiento/decisiones_arquitectura/)
- [📄 Análisis original](docs/analisis/2026-02-06_analisis_diseno.md)

### Workflows Recomendados

**Al implementar nueva funcionalidad:**
1. Consultar Jira (`project = "app_termostato"`) para verificar HU y requisitos
2. Crear branch: `feature/TER-XXX-descripcion` o `test/`, `docs/`, `bugfix/`
3. Ejecutar `/quality-check` antes de hacer commit
4. Abrir PR con `/pr`

**Al tomar decisiones arquitectónicas:**
1. Consultar [ADRs existentes](docs/mantenimiento/decisiones_arquitectura/)
2. Si es decisión nueva, crear `ADR-XXX.md` siguiendo formato de ADR-001
