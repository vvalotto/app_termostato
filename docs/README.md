# Documentación - app_termostato

Índice general de documentación del proyecto.

## 📁 Estructura

```
docs/
├── analisis/                    # Análisis y auditorías de código
├── mantenimiento/               # Gestión de deuda técnica
│   ├── historias_usuario/       # HUs de refactoring (formato Jira-ready)
│   └── decisiones_arquitectura/ # ADRs (Architecture Decision Records)
└── desarrollo/                  # Guías para contributors
```

## 🔍 Análisis y Auditorías

Auditorías técnicas puntuales del código, análisis de diseño, métricas de calidad.

📂 **[Ver análisis →](./analisis/)**

**Últimos análisis:**
- [2026-02-06: Análisis de Diseño SOLID](./analisis/2026-02-06_analisis_diseno.md) - Evaluación de principios SOLID, cohesión, acoplamiento y code smells

## 🔧 Mantenimiento y Deuda Técnica

Gestión activa de deuda técnica: historias de usuario, plan de refactorización, decisiones arquitectónicas.

📂 **[Ver mantenimiento →](./mantenimiento/)**

**Épicas activas:**
- **Refactorización Diseño:** 8 HUs identificadas (3 alta, 3 media, 2 baja prioridad)

**Decisiones arquitectónicas:**
- ADRs documentados con contexto y rationale

## 👨‍💻 Desarrollo

Guías para contributors: setup, testing, arquitectura, convenciones.

📂 **[Ver desarrollo →](./desarrollo/)**

## 📊 Estado del Proyecto

**Última auditoría:** 2026-02-06
**Calificación diseño:** C+ (6.5/10)
**Deuda técnica:** 8 HUs pendientes (~50 story points)

### Métricas Actuales

| Módulo | Cohesión | Acoplamiento | Nota |
|--------|----------|--------------|------|
| `termostato.py` | ⭐⭐ | Alto 🔴 | D |
| `api.py` | ⭐⭐⭐ | Alto 🔴 | C |
| `config.py` | ⭐⭐⭐⭐⭐ | Bajo ✅ | A |

## 🚀 Quick Links

- [CLAUDE.md](../CLAUDE.md) - Instrucciones para Claude Code
- [Quality Agent](../quality/) - Scripts de métricas de calidad
- [Tests](../tests/) - Suite de tests

---

**Última actualización:** 2026-02-06
