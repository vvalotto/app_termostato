# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Flask REST API backend for a thermostat system (app_termostato). This is the backend component of a client-server architecture, consumed by the frontend `webapp_termostato`. Part of an academic/didactic case study demonstrating REST API design.

## Commands

**Run the server:**
```bash
python app.py
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
app.py                      # Entry point - launches Flask server
├── servicios/
│   └── api.py              # REST endpoints (Flask routes)
└── general/
    ├── termostato.py       # Termostato model (data class with properties)
    └── configurador.py     # Singleton pattern - holds shared Termostato instance
```

**Key patterns:**
- `Configurador.termostato` provides a singleton Termostato instance shared across the API
- All API endpoints in `servicios/api.py` use this shared instance
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
