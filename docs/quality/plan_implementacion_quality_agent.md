# Plan de Implementacion: Ambiente Agentico para Calidad de Codigo

**Proyecto:** app_termostato
**Fecha:** 2025-12-18
**Basado en:** Tutorial Ambiente Agentico Calidad Python v1.0

---

## Resumen Ejecutivo

Este plan define las tareas necesarias para implementar un ambiente agentico de calidad de codigo en el proyecto `app_termostato`. El objetivo es automatizar la medicion de metricas de calidad (LOC, CC, MI, Pylint) y establecer quality gates que aseguren la calidad del codigo.

---

## Fases del Proyecto

| Fase | Descripcion | Tareas |
|------|-------------|--------|
| 1 | Preparacion del Entorno | 1.1 - 1.3 |
| 2 | Configuracion de Claude Code | 2.1 - 2.2 |
| 3 | Creacion del Agente de Calidad | 3.1 - 3.2 |
| 4 | Scripts de Medicion | 4.1 - 4.4 |
| 5 | Quality Gates y Comandos | 5.1 - 5.2 |
| 6 | Pruebas y Validacion | 6.1 - 6.3 |
| 7 | Documentacion y Cierre | 7.1 - 7.2 |

---

## Fase 1: Preparacion del Entorno

### Tarea 1.1: Instalar herramientas de metricas

**Objetivo:** Instalar radon, pylint y dependencias necesarias

**Acciones:**
- [ ] Agregar dependencias a requirements.txt o crear quality/requirements.txt
- [ ] Ejecutar `pip install radon pylint pytest pytest-cov`
- [ ] Verificar instalacion con `radon --version` y `pylint --version`

**Criterio de aceptacion:** Los comandos `radon cc`, `radon mi`, `radon raw` y `pylint` funcionan correctamente.

---

### Tarea 1.2: Crear estructura de directorios

**Objetivo:** Establecer la estructura de carpetas para el ambiente agentico

**Acciones:**
- [ ] Crear `.claude/agents/`
- [ ] Crear `.claude/commands/`
- [ ] Crear `quality/scripts/`
- [ ] Crear `quality/reports/`

**Estructura resultante:**
```
app_termostato/
├── .claude/
│   ├── agents/
│   └── commands/
├── app/
│   ├── general/
│   └── servicios/
├── quality/
│   ├── scripts/
│   └── reports/
└── tests/
```

---

### Tarea 1.3: Verificar herramientas con test rapido

**Objetivo:** Confirmar que radon y pylint funcionan con el codigo existente

**Acciones:**
- [ ] Ejecutar `radon cc app/general/ -a` para ver complejidad
- [ ] Ejecutar `radon mi app/general/ -s` para ver mantenibilidad
- [ ] Ejecutar `pylint app/general/ --score=yes` para ver score

**Criterio de aceptacion:** Se obtienen metricas del codigo existente sin errores.

---

## Fase 2: Configuracion de Claude Code

### Tarea 2.1: Crear archivo settings.json

**Objetivo:** Configurar umbrales de quality gates

**Archivo:** `.claude/settings.json`

**Contenido:**
```json
{
  "version": "1.0",
  "project_name": "app_termostato",
  "quality_gates": {
    "max_complexity": 10,
    "min_maintainability": 20,
    "min_pylint_score": 8.0,
    "max_function_lines": 50
  }
}
```

**Criterio de aceptacion:** Archivo JSON valido creado en `.claude/settings.json`.

---

### Tarea 2.2: Actualizar CLAUDE.md con instrucciones del agente

**Objetivo:** Documentar el uso del agente de calidad en CLAUDE.md

**Acciones:**
- [ ] Agregar seccion sobre quality-agent
- [ ] Documentar comandos disponibles
- [ ] Documentar umbrales configurados

---

## Fase 3: Creacion del Agente de Calidad

### Tarea 3.1: Crear quality-agent.md

**Objetivo:** Definir el agente especializado en calidad de codigo

**Archivo:** `.claude/agents/quality-agent.md`

**Contenido clave:**
- Nombre: quality-agent
- Descripcion: Cuando activarse automaticamente
- Herramientas: Read, Write, Edit, Bash, Glob, Grep
- Instrucciones: Workflow de analisis de 5 pasos
- Formato de reporte: Metricas + Quality Gates + Recomendaciones

**Criterio de aceptacion:** Agente responde correctamente a "Use quality-agent to analyze code".

---

### Tarea 3.2: Verificar deteccion del agente

**Objetivo:** Confirmar que Claude Code detecta el agente

**Acciones:**
- [ ] Reiniciar sesion de Claude Code
- [ ] Solicitar "analyze code quality"
- [ ] Verificar que se activa quality-agent

---

## Fase 4: Scripts de Medicion

### Tarea 4.1: Crear calculate_metrics.py

**Objetivo:** Script principal que calcula todas las metricas

**Archivo:** `quality/scripts/calculate_metrics.py`

**Funcionalidades:**
- Calcular LOC/SLOC con radon raw
- Calcular CC con radon cc
- Calcular MI con radon mi
- Calcular score con pylint
- Generar resumen y grade (A/B/C/F)
- Guardar resultado en JSON

**Criterio de aceptacion:**
```bash
python quality/scripts/calculate_metrics.py app/general/
# Genera quality/reports/quality_YYYYMMDD_HHMMSS.json
```

---

### Tarea 4.2: Crear validate_gates.py

**Objetivo:** Script que valida quality gates contra metricas

**Archivo:** `quality/scripts/validate_gates.py`

**Funcionalidades:**
- Cargar metricas desde JSON
- Comparar contra umbrales
- Retornar exit code 0 (pass) o 1 (fail)
- Mostrar estado de cada gate

**Criterio de aceptacion:**
```bash
python quality/scripts/validate_gates.py quality/reports/quality_*.json
# Exit code 0 si pasan todos los gates
```

---

### Tarea 4.3: Crear generate_report.py

**Objetivo:** Script que genera reporte Markdown legible

**Archivo:** `quality/scripts/generate_report.py`

**Funcionalidades:**
- Cargar metricas desde JSON
- Generar reporte Markdown detallado
- Incluir recomendaciones especificas
- Guardar en quality/reports/

**Criterio de aceptacion:**
```bash
python quality/scripts/generate_report.py quality/reports/quality_*.json
# Genera quality/reports/quality_YYYYMMDD_HHMMSS.md
```

---

### Tarea 4.4: Crear requirements.txt para scripts

**Objetivo:** Documentar dependencias de los scripts

**Archivo:** `quality/requirements.txt`

**Contenido:**
```
radon>=6.0.1
pylint>=3.0.0
pytest>=8.0.0
pytest-cov>=4.1.0
```

---

## Fase 5: Quality Gates y Comandos

### Tarea 5.1: Crear comando /quality-check

**Objetivo:** Comando personalizado para ejecutar analisis

**Archivo:** `.claude/commands/quality-check.md`

**Funcionalidad:**
- Ejecutar calculate_metrics.py
- Mostrar resumen
- Sugerir correcciones

**Uso:** `/quality-check [path]`

---

### Tarea 5.2: Crear comando /quality-report

**Objetivo:** Comando para generar reporte completo

**Archivo:** `.claude/commands/quality-report.md`

**Funcionalidad:**
- Ejecutar analisis completo
- Generar reporte Markdown
- Mostrar en consola

**Uso:** `/quality-report`

---

## Fase 6: Pruebas y Validacion

### Tarea 6.1: Ejecutar analisis completo del proyecto

**Objetivo:** Validar que todo funciona end-to-end

**Acciones:**
- [ ] Ejecutar `python quality/scripts/calculate_metrics.py .`
- [ ] Verificar generacion de JSON en quality/reports/
- [ ] Revisar metricas obtenidas

**Criterio de aceptacion:** Se genera reporte sin errores.

---

### Tarea 6.2: Probar quality gates

**Objetivo:** Verificar que los gates funcionan correctamente

**Acciones:**
- [ ] Ejecutar validate_gates.py
- [ ] Verificar exit codes
- [ ] Probar con codigo que falle (opcional)

---

### Tarea 6.3: Probar integracion con Claude Code

**Objetivo:** Validar el flujo completo con el agente

**Acciones:**
- [ ] Iniciar sesion de Claude Code
- [ ] Solicitar analisis de calidad
- [ ] Verificar que el agente ejecuta los scripts
- [ ] Revisar reporte generado

---

## Fase 7: Documentacion y Cierre

### Tarea 7.1: Actualizar documentacion

**Objetivo:** Documentar el sistema implementado

**Acciones:**
- [ ] Actualizar CLAUDE.md con instrucciones de uso
- [ ] Documentar umbrales y su justificacion
- [ ] Agregar ejemplos de uso

---

### Tarea 7.2: Crear issue de seguimiento en Jira (opcional)

**Objetivo:** Registrar la implementacion en Jira

**Acciones:**
- [ ] Crear epic o tarea en proyecto TER
- [ ] Documentar resultado del analisis inicial
- [ ] Planificar mejoras futuras

---

## Checklist de Verificacion Final

- [x] Herramientas instaladas (radon, pylint)
- [x] Estructura de directorios creada
- [x] Agente quality-agent.md funcional
- [x] Scripts de metricas funcionando
- [x] Quality gates configurados
- [x] Comandos personalizados creados
- [x] Documentacion actualizada
- [x] Prueba end-to-end exitosa

---

## Resultados de Pruebas (Fase 6)

**Fecha de ejecucion:** 2025-12-19

### Modulo: app/general/

| Metrica | Valor | Estado |
|---------|-------|--------|
| CC Promedio | 1.08 | [PASS] |
| MI Promedio | 100.0 | [PASS] |
| Pylint Score | 9.67/10 | [PASS] |
| Grado | A | - |

### Modulo: app/servicios/

| Metrica | Valor | Estado |
|---------|-------|--------|
| CC Promedio | 2.88 | [PASS] |
| MI Promedio | 83.3 | [PASS] |
| Pylint Score | 8.6/10 | [PASS] |
| Grado | A | - |

**Resultado:** Todos los quality gates pasaron. El codigo cumple con los estandares de calidad.

---

## Metricas Objetivo del Proyecto

Basado en el codigo actual de `app_termostato`, los objetivos son:

| Metrica | Objetivo | Resultado Actual | Estado |
|---------|----------|------------------|--------|
| CC promedio | <= 10 | 1.08 - 2.88 | [PASS] |
| MI promedio | > 20 | 83.3 - 100.0 | [PASS] |
| Pylint score | >= 8.0 | 8.6 - 9.67 | [PASS] |
| LOC por funcion | <= 50 | OK | [PASS] |

---

## Notas de Implementacion

1. **Idioma:** El codigo y comentarios siguen en espanol segun convencion del proyecto
2. **Integracion Jira:** Los reportes pueden vincularse a issues TER-*
3. **Extensibilidad:** La estructura permite agregar mas metricas en el futuro

---

**Documento creado:** 2025-12-18
**Ultima actualizacion:** 2025-12-19
**Autor:** Claude Code + Victor Valotto
**Estado:** Implementacion completada - Fases 1-6
