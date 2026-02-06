# [HU-007] Implementar Strategy Pattern para cálculo de indicador

**Epic:** Refactorización Deuda Técnica - Diseño
**Prioridad:** 🟢 Baja
**Estimación:** 5 Story Points
**Sprint:** TBD
**Jira:** TBD

---

## 📖 Historia de Usuario

**Como** desarrollador del sistema
**Quiero** implementar Strategy Pattern para el cálculo del indicador de batería
**Para** permitir diferentes estrategias de cálculo sin modificar la clase Termostato (cumplir OCP)

## 🎯 Criterios de Aceptación

- [ ] **AC1:** Interface `IndicadorCalculator` (ABC) creada
- [ ] **AC2:** `IndicadorCalculatorTresNiveles` implementa estrategia actual
- [ ] **AC3:** Se puede crear `IndicadorCalculatorCincoNiveles` sin modificar Termostato
- [ ] **AC4:** Termostato recibe calculador por inyección de dependencias
- [ ] **AC5:** Comportamiento funcional idéntico al actual (estrategia 3 niveles)
- [ ] **AC6:** Tests de cada estrategia creados
- [ ] **AC7:** Documentación de cómo agregar nuevas estrategias

## 📋 Tareas Técnicas

- [ ] **T1:** Crear interface `IndicadorCalculator` en `app/general/calculadores.py`
- [ ] **T2:** Implementar `IndicadorCalculatorTresNiveles` (estrategia actual)
- [ ] **T3:** (Opcional) Implementar `IndicadorCalculatorCincoNiveles` como ejemplo
- [ ] **T4:** Refactorizar property `indicador` en Termostato
  - Delegar cálculo al calculador inyectado
- [ ] **T5:** Actualizar Configurador/Factory para inyectar calculador
- [ ] **T6:** Crear tests unitarios de cada estrategia
- [ ] **T7:** Documentar patrón en ARQUITECTURA.md
- [ ] **T8:** Code review

## 🔗 Contexto

**Problema identificado:**
- **Análisis:** [docs/analisis/2026-02-06_analisis_diseno.md](../../analisis/2026-02-06_analisis_diseno.md#12-open-closed-principle)
- **Principio violado:** OCP (Open/Closed Principle)
- **Ubicación:** `app/general/termostato.py:104-115`
- **Impacto:** Para cambiar lógica de indicador, hay que modificar Termostato

**Código actual (hardcoded):**

```python
# app/general/termostato.py:104-115
@property
def indicador(self):
    """Calcula el indicador de carga basado en el nivel de bateria."""
    if self._carga_bateria > Config.INDICADOR_UMBRAL_NORMAL:
        return "NORMAL"
    if self._carga_bateria >= Config.INDICADOR_UMBRAL_BAJO:
        return "BAJO"
    return "CRITICO"
```

**Problema:** Agregar estrategia de 5 niveles requiere modificar Termostato (viola OCP).

**Solución propuesta - Strategy Pattern:**

```python
# app/general/calculadores.py (NUEVO)
from abc import ABC, abstractmethod
from app.configuracion.config import Config


class IndicadorCalculator(ABC):
    """Interface para estrategias de cálculo de indicador de batería."""

    @abstractmethod
    def calcular(self, carga_bateria: float) -> str:
        """Calcula el indicador basado en la carga de batería.

        Args:
            carga_bateria: Carga actual de la batería (0.0 - 5.0)

        Returns:
            str: Indicador calculado (ej: "NORMAL", "BAJO", "CRITICO")
        """
        pass


class IndicadorCalculatorTresNiveles(IndicadorCalculator):
    """Estrategia de cálculo con 3 niveles: NORMAL, BAJO, CRITICO."""

    def calcular(self, carga_bateria: float) -> str:
        """Implementa estrategia de 3 niveles."""
        if carga_bateria > Config.INDICADOR_UMBRAL_NORMAL:
            return "NORMAL"
        if carga_bateria >= Config.INDICADOR_UMBRAL_BAJO:
            return "BAJO"
        return "CRITICO"


class IndicadorCalculatorCincoNiveles(IndicadorCalculator):
    """Estrategia de cálculo con 5 niveles: EXCELENTE, BUENO, NORMAL, BAJO, CRITICO."""

    def calcular(self, carga_bateria: float) -> str:
        """Implementa estrategia de 5 niveles."""
        if carga_bateria > 4.5:
            return "EXCELENTE"
        if carga_bateria > 3.5:
            return "BUENO"
        if carga_bateria > 2.5:
            return "NORMAL"
        if carga_bateria > 1.5:
            return "BAJO"
        return "CRITICO"


# app/general/termostato.py (REFACTORIZADO)
class Termostato:
    def __init__(self,
                 historial_repositorio=None,
                 persistidor=None,
                 indicador_calculator=None,  # ✅ Inyección de dependencia
                 ...):
        self._historial_repositorio = historial_repositorio
        self._persistidor = persistidor
        self._indicador_calculator = indicador_calculator or IndicadorCalculatorTresNiveles()
        # ...

    @property
    def indicador(self):
        """Calcula el indicador de carga usando la estrategia configurada."""
        return self._indicador_calculator.calcular(self._carga_bateria)


# app/configuracion/configurador.py (ACTUALIZADO)
from app.general.calculadores import IndicadorCalculatorTresNiveles

class Configurador:
    indicador_calc = IndicadorCalculatorTresNiveles()
    termostato = Termostato(
        historial_repositorio=...,
        persistidor=...,
        indicador_calculator=indicador_calc  # ✅ Inyectar estrategia
    )


# EJEMPLO: Usar estrategia de 5 niveles (SIN modificar Termostato)
calculador_5_niveles = IndicadorCalculatorCincoNiveles()
termostato = Termostato(
    indicador_calculator=calculador_5_niveles
)
```

**Beneficios:**
- ✅ Cumple OCP (abierto a extensión, cerrado a modificación)
- ✅ Fácil agregar nuevas estrategias sin tocar Termostato
- ✅ Fácil testear cada estrategia independientemente
- ✅ Configuración flexible por inyección de dependencias

**Archivos afectados:**
- `app/general/calculadores.py` (crear)
- `app/general/termostato.py` (refactorizar property indicador)
- `app/configuracion/configurador.py` (inyectar calculador)
- `tests/test_calculadores.py` (crear)
- `tests/test_termostato.py` (actualizar)
- `docs/desarrollo/ARQUITECTURA.md` (documentar patrón)

## 📊 Métricas

**Antes:**
- **Estrategias posibles:** 1 (hardcoded)
- **OCP:** ❌ Violado
- **Extensibilidad:** Baja (requiere modificar Termostato)

**Después:**
- **Estrategias posibles:** N (extensible)
- **OCP:** ✅ Cumplido
- **Extensibilidad:** Alta (agregar estrategia = nueva clase)

## 🔗 Referencias

- **Análisis de diseño:** [docs/analisis/2026-02-06_analisis_diseno.md](../../analisis/2026-02-06_analisis_diseno.md#12-open-closed-principle)
- **Jira:** TBD
- **Patrón:** [Strategy Pattern](https://refactoring.guru/design-patterns/strategy)
- **Principio:** [OCP - Open/Closed Principle](https://en.wikipedia.org/wiki/Open%E2%80%93closed_principle)

## 🧪 Testing

**Escenarios a validar:**

### Tests Unitarios - IndicadorCalculatorTresNiveles
```python
def test_tres_niveles_normal():
    calc = IndicadorCalculatorTresNiveles()
    assert calc.calcular(4.0) == "NORMAL"

def test_tres_niveles_bajo():
    calc = IndicadorCalculatorTresNiveles()
    assert calc.calcular(3.0) == "BAJO"

def test_tres_niveles_critico():
    calc = IndicadorCalculatorTresNiveles()
    assert calc.calcular(2.0) == "CRITICO"

def test_tres_niveles_bordes():
    calc = IndicadorCalculatorTresNiveles()
    assert calc.calcular(3.5) == "BAJO"  # Justo en el umbral
    assert calc.calcular(2.5) == "BAJO"  # Justo en el umbral
```

### Tests Unitarios - IndicadorCalculatorCincoNiveles
```python
def test_cinco_niveles_excelente():
    calc = IndicadorCalculatorCincoNiveles()
    assert calc.calcular(4.8) == "EXCELENTE"

def test_cinco_niveles_todos_los_niveles():
    calc = IndicadorCalculatorCincoNiveles()
    assert calc.calcular(5.0) == "EXCELENTE"
    assert calc.calcular(4.0) == "BUENO"
    assert calc.calcular(3.0) == "NORMAL"
    assert calc.calcular(2.0) == "BAJO"
    assert calc.calcular(1.0) == "CRITICO"
```

### Tests de Integración - Termostato
```python
def test_termostato_usa_estrategia_tres_niveles():
    termostato = Termostato(
        indicador_calculator=IndicadorCalculatorTresNiveles()
    )
    termostato.carga_bateria = 4.0
    assert termostato.indicador == "NORMAL"

def test_termostato_usa_estrategia_cinco_niveles():
    termostato = Termostato(
        indicador_calculator=IndicadorCalculatorCincoNiveles()
    )
    termostato.carga_bateria = 4.8
    assert termostato.indicador == "EXCELENTE"

def test_termostato_default_usa_tres_niveles():
    termostato = Termostato()  # Sin inyectar calculador
    termostato.carga_bateria = 4.0
    assert termostato.indicador == "NORMAL"
```

### Tests de Regresión
- Comportamiento actual (3 niveles) sin cambios
- API retorna indicador correctamente

## ⚠️ Riesgos

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Breaking changes en API | Muy Baja | Alto | Usar estrategia 3 niveles por defecto |
| Over-engineering para caso simple | Media | Bajo | Pattern solo si se requieren múltiples estrategias |
| Complejidad innecesaria | Media | Bajo | Documentar bien cuándo agregar estrategias |

**Nota:** Este patrón es útil si realmente se prevén múltiples estrategias. Si solo hay 1 estrategia, puede ser over-engineering.

## 🚀 Despliegue

- [ ] **Requiere migración de datos:** NO
- [ ] **Breaking changes:** NO (usa estrategia 3 niveles por defecto)
- [ ] **Requiere actualizar frontend:** NO
- [ ] **Requiere actualizar docs:** SÍ (ARQUITECTURA.md)

## 📝 Definición de Done (DoD)

- [ ] IndicadorCalculator (ABC) creado
- [ ] IndicadorCalculatorTresNiveles implementado
- [ ] IndicadorCalculatorCincoNiveles implementado (opcional, como ejemplo)
- [ ] Termostato refactorizado con DI
- [ ] Tests de cada estrategia creados
- [ ] Comportamiento funcional sin cambios
- [ ] Patrón documentado en ARQUITECTURA.md
- [ ] Code review aprobado
- [ ] Branch mergeado a master

---

**Creado:** 2026-02-06
**Actualizado:** 2026-02-06
**Autor:** Equipo de Desarrollo
