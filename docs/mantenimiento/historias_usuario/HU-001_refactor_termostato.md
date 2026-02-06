# [HU-001] Refactorizar clase Termostato (God Object)

**Epic:** Refactorización Deuda Técnica - Diseño
**Prioridad:** 🔴 Alta
**Estimación:** 13 Story Points
**Sprint:** TBD
**Jira:** TBD

---

## 📖 Historia de Usuario

**Como** desarrollador del sistema
**Quiero** separar las responsabilidades de la clase Termostato en componentes especializados
**Para** mejorar la testabilidad, reducir el acoplamiento y cumplir el principio de responsabilidad única (SRP)

## 🎯 Criterios de Aceptación

- [ ] **AC1:** Termostato se convierte en modelo de datos puro (dataclass) con solo propiedades
- [ ] **AC2:** TermostatoValidator creado y valida todos los rangos correctamente
- [ ] **AC3:** IndicadorCalculator creado y calcula indicadores basado en batería
- [ ] **AC4:** TermostatoService orquesta persistencia e historial
- [ ] **AC5:** Todos los tests existentes pasan sin modificación funcional
- [ ] **AC6:** Cobertura de tests >= 85% en nuevos componentes
- [ ] **AC7:** Complejidad Ciclomática de Termostato <= 5
- [ ] **AC8:** Métricas de calidad pasan quality gates (CC <= 10, MI > 20, Pylint >= 8.0)

## 📋 Tareas Técnicas

- [ ] **T1:** Crear `TermostatoModelo` como dataclass en `app/general/termostato_modelo.py`
- [ ] **T2:** Crear `TermostatoValidator` en `app/general/validators.py`
  - Extraer validaciones de temperatura_ambiente
  - Extraer validaciones de temperatura_deseada
  - Extraer validaciones de carga_bateria
  - Extraer validaciones de estado_climatizador
- [ ] **T3:** Crear `IndicadorCalculator` en `app/general/calculadores.py`
  - Extraer lógica del property `indicador`
  - Implementar interface/ABC para extensibilidad futura
- [ ] **T4:** Crear `TermostatoService` en `app/servicios/termostato_service.py`
  - Orquestar validación, persistencia, historial
  - Implementar métodos de actualización
- [ ] **T5:** Refactorizar `Termostato` original usando los nuevos componentes
- [ ] **T6:** Actualizar `Configurador` para instanciar nuevos componentes
- [ ] **T7:** Actualizar tests unitarios
  - `tests/test_termostato.py`
  - `tests/test_validators.py` (nuevo)
  - `tests/test_calculadores.py` (nuevo)
  - `tests/test_termostato_service.py` (nuevo)
- [ ] **T8:** Actualizar tests de integración
- [ ] **T9:** Code review
- [ ] **T10:** Ejecutar quality-check y validar métricas

## 🔗 Contexto

**Problema identificado:**
- **Análisis:** [docs/analisis/2026-02-06_analisis_diseno.md](../../analisis/2026-02-06_analisis_diseno.md#1-análisis-solid)
- **Code smell:** God Object
- **Principio violado:** SRP (Single Responsibility Principle)
- **Responsabilidades actuales:** 6 (debería ser 1)
  1. Modelo de datos
  2. Validación de datos
  3. Cálculo de indicadores
  4. Persistencia
  5. Carga de estado
  6. Gestión de historial

**Solución propuesta:**

```python
# 1. Modelo puro (solo datos)
@dataclass
class TermostatoModelo:
    temperatura_ambiente: int
    temperatura_deseada: int
    carga_bateria: float
    estado_climatizador: str

# 2. Validador
class TermostatoValidator:
    def validar_temperatura_ambiente(self, valor: int) -> None:
        if not (Config.TEMPERATURA_AMBIENTE_MIN <= valor <= Config.TEMPERATURA_AMBIENTE_MAX):
            raise ValueError(...)

    def validar_temperatura_deseada(self, valor: int) -> None:
        # ...

    def validar_carga_bateria(self, valor: float) -> None:
        # ...

    def validar_estado_climatizador(self, valor: str) -> None:
        # ...

# 3. Calculador de indicador
class IndicadorCalculator(ABC):
    @abstractmethod
    def calcular(self, carga_bateria: float) -> str:
        pass

class IndicadorCalculatorTresNiveles(IndicadorCalculator):
    def calcular(self, carga_bateria: float) -> str:
        if carga_bateria > Config.INDICADOR_UMBRAL_NORMAL:
            return "NORMAL"
        if carga_bateria >= Config.INDICADOR_UMBRAL_BAJO:
            return "BAJO"
        return "CRITICO"

# 4. Servicio de orquestación
class TermostatoService:
    def __init__(self,
                 modelo: TermostatoModelo,
                 validator: TermostatoValidator,
                 persistidor: TermostatoPersistidor,
                 historial_repo: HistorialRepositorio,
                 indicador_calc: IndicadorCalculator):
        self._modelo = modelo
        self._validator = validator
        self._persistidor = persistidor
        self._historial_repo = historial_repo
        self._indicador_calc = indicador_calc

    def actualizar_temperatura_ambiente(self, valor: int) -> None:
        self._validator.validar_temperatura_ambiente(valor)
        self._modelo.temperatura_ambiente = valor
        self._persistidor.guardar(asdict(self._modelo))
        self._registrar_historial(valor)

    def obtener_indicador(self) -> str:
        return self._indicador_calc.calcular(self._modelo.carga_bateria)

    # ...
```

**Archivos afectados:**
- `app/general/termostato.py` (refactorizar)
- `app/general/termostato_modelo.py` (crear)
- `app/general/validators.py` (crear)
- `app/general/calculadores.py` (crear)
- `app/servicios/termostato_service.py` (crear)
- `app/configuracion/configurador.py` (actualizar)
- `tests/test_termostato.py` (actualizar)
- `tests/test_validators.py` (crear)
- `tests/test_calculadores.py` (crear)
- `tests/test_termostato_service.py` (crear)

## 📊 Métricas

**Antes:**
- **Líneas:** 149
- **CC:** ~15
- **Responsabilidades:** 6
- **Cohesión:** ⭐⭐ (Baja)
- **Acoplamiento:** 🔴 Alto
- **Nota:** D

**Después (esperado):**
- **TermostatoModelo:**
  - CC: 1
  - LOC: ~30
  - Responsabilidades: 1
- **TermostatoValidator:**
  - CC: <= 5
  - LOC: ~60
  - Responsabilidades: 1
- **IndicadorCalculator:**
  - CC: <= 3
  - LOC: ~20
  - Responsabilidades: 1
- **TermostatoService:**
  - CC: <= 8
  - LOC: ~80
  - Responsabilidades: 1
- **Nota general:** B+

## 🔗 Referencias

- **Análisis de diseño:** [docs/analisis/2026-02-06_analisis_diseno.md](../../analisis/2026-02-06_analisis_diseno.md)
- **ADR relacionado:** N/A
- **Jira:** TBD (completar al crear en Jira)
- **Principio SOLID:** [SRP - Single Responsibility Principle](https://en.wikipedia.org/wiki/Single-responsibility_principle)

## 🧪 Testing

**Escenarios a validar:**

### Tests Unitarios - TermostatoModelo
- Crear modelo con valores válidos
- Acceder a propiedades

### Tests Unitarios - TermostatoValidator
- Validar temperatura_ambiente en rango válido (OK)
- Validar temperatura_ambiente fuera de rango (ValueError)
- Validar temperatura_deseada en rango válido (OK)
- Validar temperatura_deseada fuera de rango (ValueError)
- Validar carga_bateria en rango válido (OK)
- Validar carga_bateria fuera de rango (ValueError)
- Validar estado_climatizador con valores válidos (OK)
- Validar estado_climatizador con valores inválidos (ValueError)

### Tests Unitarios - IndicadorCalculator
- Calcular indicador con batería > 3.5 → "NORMAL"
- Calcular indicador con batería entre 2.5 y 3.5 → "BAJO"
- Calcular indicador con batería < 2.5 → "CRITICO"
- Calcular indicador en valores límite

### Tests Unitarios - TermostatoService
- Actualizar temperatura_ambiente válida (persistencia + historial)
- Actualizar temperatura_ambiente inválida (ValueError)
- Actualizar temperatura_deseada válida (persistencia)
- Actualizar carga_bateria válida (persistencia)
- Obtener indicador correctamente

### Tests de Integración
- API endpoints siguen funcionando igual (no breaking changes)
- Persistencia funciona correctamente
- Historial se registra correctamente
- Carga de estado desde persistidor funciona

### Tests de Regresión
- **CRÍTICO:** Toda la suite de tests existente debe pasar sin cambios funcionales

## ⚠️ Riesgos

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Breaking changes en API pública | Media | Alto | Tests de regresión exhaustivos antes de merge |
| Bugs introducidos al separar lógica | Media | Alto | Code review riguroso + cobertura >= 85% |
| Performance degradation | Baja | Medio | Benchmarks antes/después |
| Complejidad de refactoring mayor a estimada | Alta | Medio | Refactorizar incrementalmente, commit frecuentes |

**Mitigación general:**
- Crear branch de desarrollo dedicado
- Commits atómicos por cada componente nuevo
- Tests antes de refactorizar (lock behavior)
- Code review obligatorio antes de merge

## 🚀 Despliegue

- [ ] **Requiere migración de datos:** NO
- [ ] **Breaking changes:** NO (API endpoints sin cambios)
- [ ] **Requiere actualizar frontend:** NO
- [ ] **Requiere actualizar docs:** SÍ (ARQUITECTURA.md)
- [ ] **Requiere comunicación a equipo:** SÍ (cambios internos significativos)

## 📝 Definición de Done (DoD)

- [ ] Código implementado según AC
- [ ] Tests unitarios creados (>= 85% cobertura)
- [ ] Tests de integración actualizados
- [ ] Tests de regresión pasan 100%
- [ ] Quality gates pasan (CC, MI, Pylint)
- [ ] Code review aprobado
- [ ] Documentación actualizada (ARQUITECTURA.md)
- [ ] Sin warnings de linter
- [ ] Branch mergeado a master

---

**Creado:** 2026-02-06
**Actualizado:** 2026-02-06
**Autor:** Equipo de Desarrollo
