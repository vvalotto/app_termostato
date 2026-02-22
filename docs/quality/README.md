# Quality — app_termostato

Reportes de calidad y documentación del agente de métricas.

## Documentos

| Archivo | Descripción |
|---------|-------------|
| [quality_report_20251221.md](./quality_report_20251221.md) | Reporte completo de calidad (2025-12-21) |
| [calidad_diseno_arquitectura.md](./calidad_diseno_arquitectura.md) | Análisis de calidad de diseño y arquitectura |
| [plan_implementacion_quality_agent.md](./plan_implementacion_quality_agent.md) | Plan de implementación del agente de calidad |

---

## Estado Actual

**Última ejecución:** 2025-12-21

| Módulo | CC | MI | Pylint | Grado |
|--------|----|----|--------|-------|
| `app/general/` | 1.08 | 100.0 | 9.67 | A |
| `app/servicios/` | 2.88 | 83.3 | 8.60 | A |

**Quality Gates (3/3):** CC ≤ 10 ✅ | MI > 20 ✅ | Pylint ≥ 8.0 ✅

---

## Comandos

```bash
# Análisis rápido
/quality-check [path]

# Reporte completo
/quality-report

# Scripts directos
python quality/scripts/calculate_metrics.py app/
python quality/scripts/validate_gates.py quality/reports/quality_*.json
python quality/scripts/generate_report.py quality/reports/quality_*.json
```

---

**Última actualización:** 2026-02-22
