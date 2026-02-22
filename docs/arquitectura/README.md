# Arquitectura — app_termostato

## Documentos

| Archivo | Descripción |
|---------|-------------|
| [ARQUITECTURA.md](./ARQUITECTURA.md) | Estructura de módulos, patrones de diseño, principios SOLID |
| [arquitectura_c4.md](./arquitectura_c4.md) | Modelo C4: contexto, contenedores, componentes, clases |

---

## Stack

| Capa | Tecnología |
|------|-----------|
| Runtime | Python 3.12 |
| Framework | Flask 3.1 + Flasgger |
| Testing | pytest + requests |
| Persistencia | JSON (archivo local) |
| Despliegue | Docker + Google Cloud Run |

---

## Patrones Aplicados

| Patrón | Dónde | Propósito |
|--------|-------|-----------|
| Application Factory | `api.py` | Inyección de dependencias, testabilidad |
| Factory Method | `factory.py` | Reemplaza Singleton |
| Facade | `termostato.py` | Interfaz pública estable |
| Strategy | `calculadores.py` | Intercambio de algoritmo de indicador (OCP) |
| Decorator | `decorators.py` | Elimina duplicación GET/POST |

---

## Guía Rápida para Contribuidores

```bash
# Setup
pip install -r requirements.txt

# Servidor de desarrollo
python run.py          # http://localhost:5050

# Tests unitarios e integración
pytest tests/ -v

# Tests de sistema (requiere servidor corriendo)
pytest tests/test_sistema.py -v -m sistema

# Quality check
python quality/scripts/calculate_metrics.py app/
```

### Workflow de branches

```
master
  ├── feature/TER-XXX-descripcion
  ├── test/descripcion
  ├── docs/descripcion
  └── bugfix/TER-XXX-descripcion
```

### Formato de commits

```
tipo(scope): descripción corta

feat | fix | refactor | test | docs | chore
```

---

**Última actualización:** 2026-02-22
