# Quality Report Command

Genera un reporte completo de calidad de codigo en formato Markdown.

## Uso

```
/quality-report
```

## Instrucciones para el Agente

Cuando el usuario ejecute este comando, debes:

1. **Ejecutar analisis completo del proyecto**:
   ```bash
   python scripts/metrics/calculate_metrics.py .
   ```

2. **Leer el archivo JSON generado** en `reports/quality_*.json` (el mas reciente)

3. **Generar un reporte Markdown detallado** que incluya:

### Estructura del Reporte

```markdown
# Reporte de Calidad de Codigo

**Proyecto:** app_termostato
**Fecha:** [fecha actual]
**Grado General:** [A/B/C/F]

## Resumen Ejecutivo

- Quality Gates Pasados: X/3
- Issues Bloqueantes: N

## Metricas de Tamanio

| Metrica | Valor |
|---------|-------|
| Total LOC | XXX |
| Source LOC | XXX |
| Comentarios | XX% |

## Analisis de Complejidad

| Metrica | Valor |
|---------|-------|
| CC Promedio | X.X |
| CC Maximo | X |
| Funcion mas compleja | [nombre] |

### Distribucion por Grado
- A (1-5): XX funciones
- B (6-10): XX funciones
- C (11-20): XX funciones

## Indice de Mantenibilidad

| Metrica | Valor |
|---------|-------|
| MI Promedio | XX.X |
| MI Minimo | XX.X |
| Modulos bajo umbral | X |

## Analisis Pylint

| Metrica | Valor |
|---------|-------|
| Score | X.X/10 |
| Errores | X |
| Warnings | X |

## Estado de Quality Gates

| Gate | Estado | Valor | Umbral |
|------|--------|-------|--------|
| Complejidad | PASS/FAIL | X.X | <= 10 |
| Mantenibilidad | PASS/FAIL | XX.X | > 20 |
| Pylint | PASS/FAIL | X.X | >= 8.0 |

## Recomendaciones

[Lista de mejoras sugeridas basadas en los gates fallidos]
```

4. **Guardar el reporte** en `reports/quality_report_[fecha].md`

5. **Mostrar resumen al usuario** con ubicacion del archivo generado

## Notas

- Este comando es util para documentacion y revisiones de codigo
- El reporte puede compartirse con el equipo
- Usar antes de releases o pull requests importantes
