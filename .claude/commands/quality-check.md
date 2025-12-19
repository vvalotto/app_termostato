# Quality Check Command

Ejecuta analisis completo de calidad de codigo Python.

## Uso

```
/quality-check [ruta]
```

Si no se especifica ruta, analiza todo el proyecto.

## Instrucciones para el Agente

Cuando el usuario ejecute este comando, debes:

1. **Identificar el objetivo**:
   - Si se proporciona `$ARGUMENTS`, usar esa ruta
   - Si no, analizar el directorio actual (`.`)

2. **Ejecutar el script de metricas**:
   ```bash
   python scripts/metrics/calculate_metrics.py $TARGET
   ```

3. **Mostrar el resumen al usuario** con:
   - Grado general (A/B/C/F)
   - Estado de cada quality gate (PASS/FAIL)
   - Metricas clave: CC promedio, MI promedio, Pylint score

4. **Si hay gates fallidos**, ejecutar validacion detallada:
   ```bash
   python scripts/metrics/validate_gates.py reports/quality_*.json
   ```

5. **Proporcionar recomendaciones** especificas para mejorar el codigo:
   - Indicar archivos/funciones problematicos
   - Sugerir acciones concretas de refactorizacion

## Ejemplo de Salida Esperada

```
ANALISIS DE CALIDAD - app_termostato
=====================================

Grado General: A
Quality Gates: 3/3 pasaron

Metricas:
- Complejidad (CC): 1.08 [PASS]
- Mantenibilidad (MI): 100.0 [PASS]
- Pylint Score: 9.67/10 [PASS]

Estado: Codigo cumple con todos los estandares de calidad.
```

## Variables Disponibles

- `$ARGUMENTS`: Argumentos pasados al comando (ej: ruta del archivo/directorio)
