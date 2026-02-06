# ADR-001: Factory Pattern vs Singleton para Configurador

**Estado:** ✅ Aceptado
**Fecha:** 2026-02-06
**Autores:** Equipo de Desarrollo
**Contexto:** Refactorización HU-002 - Eliminar Singleton

---

## Contexto y Problema

El `Configurador` actual implementa un patrón Singleton implícito usando variables de clase estáticas:

```python
class Configurador:
    historial_repositorio = HistorialRepositorioMemoria()  # Variable de clase
    termostato = Termostato(...)  # Singleton implícito
```

### Problemas identificados:

1. **Testing difícil:**
   - Estado global compartido entre tests
   - Imposible ejecutar tests en paralelo
   - Dificulta crear instancias con mocks

2. **Acoplamiento fuerte:**
   - api.py depende directamente de `Configurador.termostato`
   - Violación de DIP (Dependency Inversion Principle)

3. **Falta de flexibilidad:**
   - No se puede crear múltiples instancias con diferentes configuraciones
   - Dificulta desarrollo y debugging

4. **Anti-pattern reconocido:**
   - Singleton es considerado anti-pattern en testing
   - Dificulta inyección de dependencias

### Origen:
- [Análisis de diseño 2026-02-06](../../analisis/2026-02-06_analisis_diseno.md#1-singleton-anti-pattern)
- [HU-002: Eliminar Singleton](../historias_usuario/HU-002_eliminar_singleton.md)

---

## Decisión

**Reemplazar el patrón Singleton por Factory Pattern puro con Dependency Injection.**

### Implementación:

```python
# app/configuracion/factory.py (NUEVO)
class TermostatoFactory:
    """Factory puro para crear instancias de Termostato."""

    @staticmethod
    def crear_termostato(
        historial_repositorio = None,
        persistidor = None,
        config = None
    ) -> Termostato:
        """Crea una nueva instancia de Termostato."""
        config = config or Config
        historial_repo = historial_repositorio or HistorialRepositorioMemoria()
        persist = persistidor or TermostatoPersistidorJSON()

        termostato = Termostato(
            historial_repositorio=historial_repo,
            persistidor=persist,
            temperatura_ambiente_inicial=config.TEMPERATURA_AMBIENTE_INICIAL,
            temperatura_deseada_inicial=config.TEMPERATURA_DESEADA_INICIAL,
            carga_bateria_inicial=config.CARGA_BATERIA_INICIAL
        )
        termostato.cargar_estado()
        return termostato


# app/servicios/api.py (REFACTORIZADO)
def create_app(termostato: Termostato = None) -> Flask:
    """Crea aplicación Flask con dependency injection."""
    app = Flask(__name__)
    CORS(app)

    # Inyectar dependencia
    if termostato is None:
        termostato = TermostatoFactory.crear_termostato()

    # Endpoints usan termostato inyectado via closure
    @app.route("/termostato/", methods=["GET"])
    def obtener_termostato():
        return jsonify({...})

    return app


# run.py
if __name__ == "__main__":
    app = create_app()  # Factory crea termostato
    app.run(...)


# tests/conftest.py
@pytest.fixture
def app():
    mock_termostato = Mock()
    app = create_app(termostato=mock_termostato)  # Inyectar mock
    yield app
```

---

## Alternativas Consideradas

### Alternativa 1: Mantener Singleton (Status Quo)

**Pros:**
- No requiere cambios
- Código actual funciona

**Contras:**
- ❌ Dificulta testing
- ❌ Estado global compartido
- ❌ Acoplamiento fuerte
- ❌ Anti-pattern

**Decisión:** ❌ Rechazado

---

### Alternativa 2: Singleton mejorado (con reset)

Agregar método `Configurador.reset()` para resetear estado entre tests.

```python
class Configurador:
    _termostato = None

    @classmethod
    def get_termostato(cls):
        if cls._termostato is None:
            cls._termostato = Termostato(...)
        return cls._termostato

    @classmethod
    def reset(cls):
        cls._termostato = None
```

**Pros:**
- Cambios mínimos
- Permite resetear en tests

**Contras:**
- ❌ Sigue siendo singleton (anti-pattern)
- ❌ Estado global persiste
- ❌ No resuelve acoplamiento
- ❌ Tests deben recordar llamar reset()

**Decisión:** ❌ Rechazado (no resuelve problemas fundamentales)

---

### Alternativa 3: Factory Pattern ✅ (SELECCIONADO)

**Pros:**
- ✅ Elimina estado global
- ✅ Facilita testing (inyección de mocks)
- ✅ Flexible (múltiples configuraciones)
- ✅ Cumple DIP (Dependency Inversion)
- ✅ Patrón reconocido y bien documentado
- ✅ Tests pueden ejecutarse en paralelo

**Contras:**
- Requiere refactorizar api.py (agregar create_app)
- Cambio en forma de uso (de `Configurador.termostato` a `factory.crear_termostato()`)

**Decisión:** ✅ **ACEPTADO**

---

### Alternativa 4: DI Container (futuro)

Implementar contenedor completo de inyección de dependencias.

```python
container = DIContainer()
container.register('termostato', lambda: Termostato(...))
app = create_app(container)
```

**Pros:**
- ✅ Máxima flexibilidad
- ✅ Centraliza toda la configuración
- ✅ Resolución automática de dependencias

**Contras:**
- ⚠️ Over-engineering para proyecto actual
- ⚠️ Mayor complejidad
- ⚠️ Curva de aprendizaje

**Decisión:** ⏸️ **POSPUESTO** (evaluar en HU-008 si realmente se necesita)

---

## Consecuencias

### Positivas ✅

1. **Testing mejorado:**
   - Fácil crear instancias con mocks
   - Tests pueden ejecutarse en paralelo
   - No hay estado compartido entre tests

2. **Desacoplamiento:**
   - api.py ya no depende de Configurador singleton
   - Dependency Injection explícita

3. **Flexibilidad:**
   - Fácil crear múltiples instancias
   - Configuraciones diferentes para dev/test/prod

4. **Principios SOLID:**
   - Cumple DIP (Dependency Inversion)
   - Cumple SRP (Factory solo crea objetos)

### Negativas ⚠️

1. **Cambio en API interna:**
   - `Configurador.termostato` → `factory.crear_termostato()`
   - Requiere actualizar imports y uso

2. **Refactorización necesaria:**
   - api.py requiere función `create_app()`
   - Tests requieren actualizar fixtures

3. **Complejidad inicial:**
   - Desarrolladores deben entender DI pattern
   - Documentación necesaria

### Mitigación de negativas:

- ✅ Documentar patrón en ARQUITECTURA.md
- ✅ Ejemplos claros en tests
- ✅ Mantener Configurador como wrapper temporal (deprecated) para transición suave

---

## Implementación

### Fase 1: Crear Factory (Sprint 1)
- [ ] Implementar `TermostatoFactory`
- [ ] Tests unitarios de factory
- [ ] Documentar uso

### Fase 2: Refactorizar API (Sprint 1)
- [ ] Agregar `create_app()` con DI
- [ ] Actualizar run.py
- [ ] Tests de integración

### Fase 3: Actualizar Tests (Sprint 1)
- [ ] Actualizar fixtures en conftest.py
- [ ] Actualizar tests existentes
- [ ] Verificar tests paralelos funcionan

### Fase 4: Deprecar Configurador (Sprint 2)
- [ ] Marcar Configurador como deprecated
- [ ] Agregar warnings
- [ ] Eventual remoción (post Sprint 2)

---

## Notas

### Referencias

- [Refactoring Guru: Factory Pattern](https://refactoring.guru/design-patterns/factory-method)
- [Martin Fowler: Dependency Injection](https://martinfowler.com/articles/injection.html)
- [Why Singleton is an Anti-Pattern](https://testing.googleblog.com/2008/08/by-miko-hevery-so-you-join-new-project.html)

### Lecciones Aprendidas

- Singleton dificulta testing → usar DI desde el inicio
- Estado global es problemático → preferir inyección explícita
- Factory pattern es suficiente para casos simples → no necesitar DI Container aún

### Decisiones Relacionadas

- **ADR-002 (futuro):** DI Container (si se requiere mayor complejidad)
- **HU-002:** Implementación de esta decisión
- **HU-008:** Evaluación de DI Container

---

## Validación

### Criterios de Éxito

- [ ] Tests pueden ejecutarse en paralelo con `pytest -n 4`
- [ ] api.py puede crearse con termostato mockeado
- [ ] No hay estado global compartido
- [ ] Configurador deprecated pero funcional (transición)

### Métricas

**Antes:**
- Tests en paralelo: ❌ No
- Acoplamiento api.py ↔ Configurador: 🔴 Alto
- Flexibilidad configuración: 🔴 Baja

**Después (esperado):**
- Tests en paralelo: ✅ Sí
- Acoplamiento: 🟢 Bajo (DI)
- Flexibilidad: 🟢 Alta

---

**Última actualización:** 2026-02-06
**Estado:** ✅ Aceptado, pendiente de implementación en HU-002
