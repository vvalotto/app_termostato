# Guías de Desarrollo

Documentación para contributors y desarrolladores del proyecto.

## 📚 Contenido

Esta sección contendrá:

- **CONTRIBUTING.md** - Cómo contribuir al proyecto
- **TESTING.md** - Estrategias de testing y cómo ejecutar tests
- **ARQUITECTURA.md** - Visión general de la arquitectura del sistema
- **CONVENCIONES.md** - Estándares de código y naming conventions

## 🚀 Quick Start

```bash
# Clonar repositorio
git clone <repo-url>

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
python run.py

# Ejecutar tests
pytest

# Ejecutar quality checks
python quality/scripts/calculate_metrics.py app/
```

## 🏗️ Arquitectura (Resumen)

```
run.py
├── app/
│   ├── servicios/api.py          # REST endpoints (Flask)
│   ├── general/termostato.py     # Modelo de datos
│   ├── configuracion/
│   │   ├── config.py             # Configuración desde env vars
│   │   └── configurador.py       # Factory/Singleton (⚠️ en refactoring)
│   └── datos/                    # Repositorios y persistencia
│       ├── repositorio.py        # Interface ABC
│       ├── memoria.py            # Implementación en memoria
│       └── persistidor_json.py   # Persistencia JSON
└── tests/                        # Tests unitarios e integración
```

## 🧪 Testing

```bash
# Tests unitarios
pytest tests/

# Tests con cobertura
pytest --cov=app tests/

# Tests específicos
pytest tests/test_termostato.py
```

**Cobertura actual:** TBD
**Target:** >= 80%

## 📏 Quality Gates

| Métrica | Umbral | Actual |
|---------|--------|--------|
| CC (Complejidad) | <= 10 | ⚠️ 15 (termostato.py) |
| MI (Mantenibilidad) | > 20 | ✅ Pasa |
| Pylint | >= 8.0 | ✅ 9.67 (general/), 8.6 (servicios/) |
| LOC/función | <= 50 | ✅ Pasa |

Ver [Quality Reports](../../quality/reports/) para detalles.

## 🔧 Herramientas

- **Flask** - Framework web
- **pytest** - Testing framework
- **radon** - Métricas de complejidad
- **pylint** - Linter
- **flasgger** - Swagger/OpenAPI docs

## 🌿 Workflow de Branches

```
master (main branch)
  ├── feature/TER-XXX-nombre-feature
  ├── docs/nombre-documentacion
  └── bugfix/TER-XXX-descripcion-bug
```

**Convenciones:**
- `feature/` - Nuevas funcionalidades
- `docs/` - Solo documentación
- `bugfix/` - Corrección de bugs
- Prefijo con ticket Jira cuando aplique

## 📝 Commit Messages

```
tipo(scope): descripción corta

Descripción más larga si es necesario.

Refs: TER-123
```

**Tipos:**
- `feat` - Nueva funcionalidad
- `fix` - Corrección de bug
- `refactor` - Refactorización sin cambio de funcionalidad
- `docs` - Solo documentación
- `test` - Agregar o modificar tests
- `chore` - Mantenimiento (deps, config, etc)

## 🔗 Enlaces Útiles

- [CLAUDE.md](../../CLAUDE.md) - Instrucciones para Claude Code
- [Análisis y Auditorías](../analisis/)
- [Plan de Mantenimiento](../mantenimiento/)
- [API Docs (Swagger)](http://localhost:5050/docs/) - Cuando el servidor está corriendo

---

**Última actualización:** 2026-02-06
