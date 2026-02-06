# [HU-008] Crear Dependency Injection Container

**Epic:** Refactorización Deuda Técnica - Diseño
**Prioridad:** 🟢 Baja
**Estimación:** 8 Story Points
**Sprint:** TBD
**Jira:** TBD

---

## 📖 Historia de Usuario

**Como** desarrollador del sistema
**Quiero** implementar un contenedor de inyección de dependencias centralizado
**Para** mejorar la testabilidad, configuración y mantenibilidad del sistema

## 🎯 Criterios de Aceptación

- [ ] **AC1:** DIContainer creado con métodos para cada dependencia
- [ ] **AC2:** Configurador/Factory usa DIContainer
- [ ] **AC3:** Fácil crear container de testing con mocks
- [ ] **AC4:** Dependencias se resuelven automáticamente (resolución transitiva)
- [ ] **AC5:** Container soporta singletons y factories
- [ ] **AC6:** Documentación de cómo usar DIContainer
- [ ] **AC7:** Tests pueden usar TestDIContainer con mocks

## 📋 Tareas Técnicas

- [ ] **T1:** Crear `DIContainer` en `app/configuracion/di_container.py`
  - Métodos `get_config()`, `get_termostato()`, etc.
  - Soporte para singletons (lazy initialization)
  - Soporte para factories (nueva instancia cada vez)
- [ ] **T2:** Crear `TestDIContainer` para testing
  - Permite inyectar mocks fácilmente
- [ ] **T3:** Refactorizar Configurador para usar DIContainer
- [ ] **T4:** Actualizar api.py para usar DIContainer
- [ ] **T5:** Actualizar run.py para usar DIContainer
- [ ] **T6:** Actualizar tests para usar TestDIContainer
- [ ] **T7:** Documentar en ARQUITECTURA.md
- [ ] **T8:** Code review

## 🔗 Contexto

**Problema identificado:**
- **Análisis:** [docs/analisis/2026-02-06_analisis_diseno.md](../../analisis/2026-02-06_analisis_diseno.md#15-dependency-inversion-principle)
- **Principio violado:** DIP (parcialmente)
- **Problema:** Dependencias se crean manualmente en múltiples lugares
- **Impacto:** Dificulta testing y configuración

**Situación actual:**

```python
# Dependencias creadas en Configurador
historial_repositorio = HistorialRepositorioMemoria()
persistidor = TermostatoPersistidorJSON()
termostato = Termostato(historial_repositorio, persistidor)

# En tests: duplicar lógica de creación
mock_historial = Mock()
mock_persistidor = Mock()
termostato = Termostato(mock_historial, mock_persistidor)
```

**Solución propuesta - DI Container:**

```python
# app/configuracion/di_container.py (NUEVO)
"""Contenedor de inyección de dependencias."""

from app.configuracion.config import Config
from app.general.termostato import Termostato
from app.datos import (
    HistorialRepositorioMemoria,
    HistorialMapper,
    TermostatoPersistidorJSON
)
from app.general.calculadores import IndicadorCalculatorTresNiveles


class DIContainer:
    """Contenedor de inyección de dependencias."""

    def __init__(self):
        self._singletons = {}

    def get_config(self) -> Config:
        """Retorna instancia de Config."""
        return Config

    def get_historial_repositorio(self):
        """Retorna repositorio de historial (singleton)."""
        if 'historial_repositorio' not in self._singletons:
            self._singletons['historial_repositorio'] = HistorialRepositorioMemoria()
        return self._singletons['historial_repositorio']

    def get_historial_mapper(self):
        """Retorna mapper de historial (singleton)."""
        if 'historial_mapper' not in self._singletons:
            self._singletons['historial_mapper'] = HistorialMapper()
        return self._singletons['historial_mapper']

    def get_persistidor(self):
        """Retorna persistidor (singleton)."""
        if 'persistidor' not in self._singletons:
            self._singletons['persistidor'] = TermostatoPersistidorJSON()
        return self._singletons['persistidor']

    def get_indicador_calculator(self):
        """Retorna calculador de indicador (singleton)."""
        if 'indicador_calculator' not in self._singletons:
            self._singletons['indicador_calculator'] = IndicadorCalculatorTresNiveles()
        return self._singletons['indicador_calculator']

    def get_termostato(self) -> Termostato:
        """Retorna instancia de Termostato con dependencias inyectadas (singleton)."""
        if 'termostato' not in self._singletons:
            config = self.get_config()
            termostato = Termostato(
                historial_repositorio=self.get_historial_repositorio(),
                persistidor=self.get_persistidor(),
                indicador_calculator=self.get_indicador_calculator(),
                temperatura_ambiente_inicial=config.TEMPERATURA_AMBIENTE_INICIAL,
                temperatura_deseada_inicial=config.TEMPERATURA_DESEADA_INICIAL,
                carga_bateria_inicial=config.CARGA_BATERIA_INICIAL
            )
            termostato.cargar_estado()
            self._singletons['termostato'] = termostato
        return self._singletons['termostato']

    def reset(self):
        """Resetea todos los singletons (útil para testing)."""
        self._singletons = {}


# Instancia global del container (para producción)
container = DIContainer()


# tests/conftest.py - Container de testing
from unittest.mock import Mock

class TestDIContainer(DIContainer):
    """Container para testing con mocks."""

    def __init__(self):
        super().__init__()
        self._mocks = {}

    def set_mock(self, dependency_name: str, mock_instance):
        """Inyecta un mock para una dependencia."""
        self._mocks[dependency_name] = mock_instance

    def get_historial_repositorio(self):
        if 'historial_repositorio' in self._mocks:
            return self._mocks['historial_repositorio']
        return super().get_historial_repositorio()

    def get_persistidor(self):
        if 'persistidor' in self._mocks:
            return self._mocks['persistidor']
        return super().get_persistidor()

    # ... mismo patrón para otras dependencias


@pytest.fixture
def test_container():
    """Fixture que provee container de testing."""
    container = TestDIContainer()
    # Configurar mocks por defecto
    container.set_mock('historial_repositorio', Mock())
    container.set_mock('persistidor', Mock())
    yield container
    container.reset()


# app/servicios/api.py (REFACTORIZADO)
from app.configuracion.di_container import container

def create_app(di_container=None):
    """Crea app Flask con DI."""
    container = di_container or container
    termostato = container.get_termostato()
    # ...


# run.py (REFACTORIZADO)
from app.configuracion.di_container import container
from app.servicios.api import create_app

if __name__ == "__main__":
    app = create_app(container)
    app.run(...)


# tests/test_api.py (EJEMPLO DE USO)
def test_endpoint_con_mock(test_container):
    # Configurar comportamiento del mock
    test_container._mocks['persistidor'].guardar = Mock()

    # Crear app con container de testing
    app = create_app(test_container)
    client = app.test_client()

    # Test endpoint
    response = client.post('/termostato/temperatura_ambiente/',
                          json={'ambiente': 25})

    # Verificar que se llamó al mock
    assert test_container._mocks['persistidor'].guardar.called
```

**Beneficios:**
- ✅ Centraliza creación de dependencias
- ✅ Facilita testing con mocks
- ✅ Configuración flexible
- ✅ Resolución transitiva de dependencias
- ✅ Soporta singletons y factories

**Archivos afectados:**
- `app/configuracion/di_container.py` (crear)
- `app/configuracion/configurador.py` (refactorizar o deprecar)
- `app/servicios/api.py` (usar container)
- `run.py` (usar container)
- `tests/conftest.py` (TestDIContainer)
- `tests/test_*.py` (usar test_container fixture)
- `docs/desarrollo/ARQUITECTURA.md` (documentar)

## 📊 Métricas

**Antes:**
- **Centralización:** ❌ Dependencias creadas en múltiples lugares
- **Testabilidad:** Media (requiere duplicar lógica de creación)
- **Configuración:** Rígida (hardcoded en Configurador)

**Después:**
- **Centralización:** ✅ Todo en DIContainer
- **Testabilidad:** Alta (TestDIContainer con mocks)
- **Configuración:** Flexible (fácil cambiar implementaciones)

## 🔗 Referencias

- **Análisis de diseño:** [docs/analisis/2026-02-06_analisis_diseno.md](../../analisis/2026-02-06_analisis_diseno.md)
- **Jira:** TBD
- **Patrón:** [Dependency Injection](https://en.wikipedia.org/wiki/Dependency_injection)
- **Principio:** [DIP - Dependency Inversion Principle](https://en.wikipedia.org/wiki/Dependency_inversion_principle)

## 🧪 Testing

**Escenarios a validar:**

### Tests Unitarios - DIContainer
```python
def test_container_retorna_config():
    container = DIContainer()
    config = container.get_config()
    assert config is not None

def test_container_singleton_historial_repositorio():
    container = DIContainer()
    repo1 = container.get_historial_repositorio()
    repo2 = container.get_historial_repositorio()
    assert repo1 is repo2  # Mismo objeto

def test_container_termostato_con_dependencias():
    container = DIContainer()
    termostato = container.get_termostato()
    assert termostato._historial_repositorio is not None
    assert termostato._persistidor is not None

def test_container_reset():
    container = DIContainer()
    term1 = container.get_termostato()
    container.reset()
    term2 = container.get_termostato()
    assert term1 is not term2  # Diferentes objetos
```

### Tests - TestDIContainer
```python
def test_container_permite_inyectar_mocks():
    container = TestDIContainer()
    mock_persistidor = Mock()
    container.set_mock('persistidor', mock_persistidor)

    termostato = container.get_termostato()
    assert termostato._persistidor is mock_persistidor
```

### Tests de Integración
- API funciona con DIContainer en producción
- Tests usan TestDIContainer exitosamente
- Todas las dependencias se resuelven correctamente

## ⚠️ Riesgos

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Over-engineering para proyecto pequeño | Alta | Bajo | Evaluar si realmente se necesita |
| Complejidad aumenta | Media | Medio | Documentar bien el patrón |
| Curva de aprendizaje | Media | Bajo | Ejemplos claros en docs |

**Nota:** DI Container puede ser over-engineering para un proyecto pequeño. Evaluar si los beneficios justifican la complejidad adicional.

## 🚀 Despliegue

- [ ] **Requiere migración de datos:** NO
- [ ] **Breaking changes:** NO
- [ ] **Requiere actualizar frontend:** NO
- [ ] **Requiere actualizar docs:** SÍ (ARQUITECTURA.md, TESTING.md)

## 📝 Definición de Done (DoD)

- [ ] DIContainer implementado
- [ ] TestDIContainer implementado
- [ ] Configurador refactorizado para usar container
- [ ] api.py y run.py usan container
- [ ] Tests usan TestDIContainer
- [ ] Tests unitarios de container creados
- [ ] Documentación completa (ARQUITECTURA.md)
- [ ] Code review aprobado
- [ ] Branch mergeado a master

---

**Creado:** 2026-02-06
**Actualizado:** 2026-02-06
**Autor:** Equipo de Desarrollo
