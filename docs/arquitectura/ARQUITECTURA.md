# Arquitectura del Sistema

## Stack

- **Runtime:** Python 3.12
- **Framework:** Flask + Flasgger (Swagger)
- **Testing:** pytest
- **Persistencia:** JSON (archivo local)

---

## Estructura de módulos

```
app/
├── configuracion/
│   ├── config.py           # Variables de entorno centralizadas
│   ├── factory.py          # TermostatoFactory — crea instancias sin Singleton
│   └── swagger_config.py   # Configuración Flasgger extraída de api.py
├── general/
│   ├── termostato.py       # Facade — interfaz pública estable
│   ├── termostato_modelo.py# TermostatoModelo — dataclass puro
│   ├── validators.py       # TermostatoValidator — validaciones de rangos
│   └── calculadores.py     # Strategy Pattern — cálculo de indicador
├── servicios/
│   ├── api.py              # Application Factory Pattern — endpoints Flask
│   ├── decorators.py       # @endpoint_termostato — elimina duplicación
│   ├── errors.py           # error_response — respuesta de error uniforme
│   └── termostato_service.py # TermostatoService — orquestación
└── datos/
    └── ...                 # Repositorios, persistidor, mappers
```

---

## Patrones de Diseño

### Application Factory Pattern (`api.py`)

`create_app(termostato=None, ...)` permite inyectar dependencias:

```python
# Producción
app = create_app()

# Tests
app = create_app(termostato=Mock())
```

### Factory Pattern (`factory.py`)

`TermostatoFactory` reemplaza el Singleton `Configurador`. Cada llamada retorna una instancia independiente:

```python
termostato = TermostatoFactory.crear_termostato()
```

### Strategy Pattern — Indicador de Batería (`calculadores.py`)

Permite cambiar el algoritmo de cálculo del indicador sin modificar `Termostato` (cumple OCP).

**Estrategias disponibles:**

| Clase | Niveles | Descripción |
|-------|---------|-------------|
| `IndicadorCalculatorTresNiveles` | NORMAL / BAJO / CRITICO | Estrategia por defecto |
| `IndicadorCalculatorCincoNiveles` | EXCELENTE / BUENO / NORMAL / BAJO / CRITICO | Estrategia extendida |

**Uso:**

```python
# Por defecto (3 niveles)
termostato = Termostato()

# Con estrategia personalizada
from app.general.calculadores import IndicadorCalculatorCincoNiveles
termostato = Termostato(indicador_calc=IndicadorCalculatorCincoNiveles())

# Via Factory
termostato = TermostatoFactory.crear_termostato(
    indicador_calc=IndicadorCalculatorCincoNiveles()
)
```

**Cómo agregar una nueva estrategia:**

1. Crear clase en `app/general/calculadores.py` que herede de `IndicadorCalculator`
2. Implementar el método `calcular(self, carga_bateria: float) -> str`
3. Inyectar al construir `Termostato` o via `TermostatoFactory`
4. Agregar tests en `tests/test_calculadores.py`

```python
# Ejemplo: estrategia binaria
class IndicadorCalculatorBinario(IndicadorCalculator):
    def calcular(self, carga_bateria: float) -> str:
        return "OK" if carga_bateria >= 2.5 else "FALLA"
```

### Decorator Pattern (`decorators.py`)

`@endpoint_termostato` centraliza la lógica GET/POST de los endpoints, eliminando ~120 LOC de duplicación.

---

## Principios SOLID aplicados

| Principio | Aplicación |
|-----------|-----------|
| **SRP** | Termostato dividido en Modelo, Validator, Calculator, Service |
| **OCP** | Strategy Pattern en calculadores — extensible sin modificar Termostato |
| **DIP** | TermostatoService recibe dependencias por constructor |

---

*Última actualización: 2026-02-22*
