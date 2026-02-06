# [HU-002] Eliminar Singleton en Configurador

**Epic:** Refactorización Deuda Técnica - Diseño
**Prioridad:** 🔴 Alta
**Estimación:** 8 Story Points
**Sprint:** TBD
**Jira:** TBD

---

## 📖 Historia de Usuario

**Como** desarrollador del sistema
**Quiero** reemplazar el patrón Singleton del Configurador por un Factory pattern puro con inyección de dependencias
**Para** facilitar el testing unitario independiente y reducir el acoplamiento global

## 🎯 Criterios de Aceptación

- [ ] **AC1:** Configurador se convierte en Factory puro (sin variables de clase estáticas)
- [ ] **AC2:** api.py usa inyección de dependencias en lugar de singleton global
- [ ] **AC3:** Tests pueden crear instancias independientes de Termostato sin estado compartido
- [ ] **AC4:** Factory puede crear instancias con diferentes configuraciones (útil para testing)
- [ ] **AC5:** No hay estado global compartido en el módulo
- [ ] **AC6:** Todos los tests existentes pasan
- [ ] **AC7:** Tests de api.py pueden ejecutarse en paralelo sin interferencia
- [ ] **AC8:** Métricas de calidad pasan quality gates

## 📋 Tareas Técnicas

- [ ] **T1:** Crear `TermostatoFactory` en `app/configuracion/factory.py`
  - Método `crear_termostato()` que retorna nueva instancia
  - Método `crear_historial_repositorio()` configurable
  - Método `crear_persistidor()` configurable
- [ ] **T2:** Refactorizar `app/servicios/api.py`
  - Agregar función `create_app(termostato=None)` para dependency injection
  - Eliminar variable global `termostato = Configurador.termostato`
  - Usar closure o app context para acceder a instancia
- [ ] **T3:** Actualizar `run.py`
  - Usar `create_app()` con factory
- [ ] **T4:** Crear `TestFactory` para tests
  - Permite crear instancias con mocks
  - Facilita testing aislado
- [ ] **T5:** Actualizar tests existentes
  - `tests/test_api.py` - usar TestFactory
  - `tests/test_termostato.py` - crear instancias independientes
  - `tests/conftest.py` - agregar fixtures con factory
- [ ] **T6:** Deprecar `Configurador` (opcional: mantener como wrapper)
- [ ] **T7:** Code review
- [ ] **T8:** Ejecutar quality-check

## 🔗 Contexto

**Problema identificado:**
- **Análisis:** [docs/analisis/2026-02-06_analisis_diseno.md](../../analisis/2026-02-06_analisis_diseno.md#1-code-smells)
- **Anti-pattern:** Singleton
- **Principios violados:**
  - DIP (Dependency Inversion): api.py depende de implementación concreta
  - SRP: Configurador mezcla Factory + Singleton + Initialization
- **Impacto:**
  - Dificulta testing (estado global compartido)
  - Tests no pueden ejecutarse en paralelo
  - Imposible mockear dependencias fácilmente

**Solución propuesta:**

### Antes (Singleton):
```python
# app/configuracion/configurador.py
class Configurador:
    historial_repositorio = HistorialRepositorioMemoria()  # ❌ Variable de clase
    termostato = Termostato(...)  # ❌ Singleton implícito

# app/servicios/api.py
termostato = Configurador.termostato  # ❌ Acoplamiento fuerte
```

### Después (Factory + DI):
```python
# app/configuracion/factory.py
class TermostatoFactory:
    """Factory puro para crear instancias de Termostato."""

    @staticmethod
    def crear_termostato(
        historial_repositorio: HistorialRepositorio = None,
        persistidor: TermostatoPersistidor = None,
        config: Config = None
    ) -> Termostato:
        """Crea una nueva instancia de Termostato con dependencias configuradas."""
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

    @staticmethod
    def crear_historial_repositorio() -> HistorialRepositorio:
        """Crea repositorio de historial."""
        return HistorialRepositorioMemoria()

    @staticmethod
    def crear_persistidor(ruta: str = None) -> TermostatoPersistidor:
        """Crea persistidor JSON."""
        return TermostatoPersistidorJSON(ruta) if ruta else TermostatoPersistidorJSON()


# app/servicios/api.py
def create_app(termostato: Termostato = None) -> Flask:
    """Crea la aplicación Flask con dependency injection."""
    app = Flask(__name__)
    CORS(app)

    # Inyectar dependencia
    if termostato is None:
        termostato = TermostatoFactory.crear_termostato()

    # Usar closure para acceder a termostato en endpoints
    @app.route("/termostato/", methods=["GET"])
    def obtener_termostato():
        return jsonify({
            'temperatura_ambiente': termostato.temperatura_ambiente,
            # ...
        })

    return app


# run.py
if __name__ == "__main__":
    app = create_app()  # ✅ Dependency injection
    app.run(host='0.0.0.0', port=Config.PORT, debug=Config.DEBUG)


# tests/conftest.py
@pytest.fixture
def app():
    """Fixture que crea app con Termostato mockeado."""
    mock_termostato = Mock()
    app = create_app(termostato=mock_termostato)  # ✅ Inyectar mock
    yield app
```

**Archivos afectados:**
- `app/configuracion/factory.py` (crear)
- `app/configuracion/configurador.py` (deprecar o refactorizar)
- `app/servicios/api.py` (refactorizar - agregar create_app)
- `run.py` (actualizar)
- `tests/conftest.py` (agregar fixtures)
- `tests/test_api.py` (actualizar)
- `tests/test_termostato.py` (actualizar)

## 📊 Métricas

**Antes:**
- **Acoplamiento:** Alto (api.py → Configurador → Termostato)
- **Testabilidad:** Baja (estado global)
- **Paralelización tests:** Imposible

**Después (esperado):**
- **Acoplamiento:** Bajo (DI pattern)
- **Testabilidad:** Alta (mocks fáciles)
- **Paralelización tests:** Posible

## 🔗 Referencias

- **Análisis de diseño:** [docs/analisis/2026-02-06_analisis_diseno.md](../../analisis/2026-02-06_analisis_diseno.md)
- **ADR relacionado:** [ADR-001: Factory vs Singleton](../decisiones_arquitectura/ADR-001_factory_vs_singleton.md)
- **Jira:** TBD
- **Patrón:** [Factory Pattern](https://refactoring.guru/design-patterns/factory-method)

## 🧪 Testing

**Escenarios a validar:**

### Tests Unitarios - TermostatoFactory
- Crear termostato con configuración por defecto
- Crear termostato con repositorio customizado
- Crear termostato con persistidor customizado
- Crear termostato con config customizada
- Verificar que carga_estado() se llama automáticamente

### Tests de Integración - API con DI
- Crear app con termostato real (funciona normal)
- Crear app con termostato mockeado (para testing)
- Múltiples instancias de app no comparten estado
- Endpoints funcionan correctamente con DI

### Tests de Regresión
- Toda la suite existente debe pasar
- API endpoints responden igual que antes
- Comportamiento funcional sin cambios

### Tests de Paralelización
- Ejecutar tests de API en paralelo (pytest -n 4)
- Verificar que no hay interferencia entre tests

## ⚠️ Riesgos

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Breaking changes en imports | Media | Medio | Mantener Configurador como wrapper temporal |
| Tests fallan por cambio de arquitectura | Media | Alto | Actualizar fixtures en conftest.py |
| Flask app context issues | Baja | Alto | Usar application factory pattern estándar |
| Performance overhead por DI | Muy Baja | Bajo | DI no tiene overhead significativo |

**Mitigación general:**
- Implementar gradualmente (primero factory, luego DI)
- Tests de regresión antes de cada cambio
- Mantener Configurador como wrapper deprecated temporalmente

## 🚀 Despliegue

- [ ] **Requiere migración de datos:** NO
- [ ] **Breaking changes:** NO (API pública sin cambios)
- [ ] **Requiere actualizar frontend:** NO
- [ ] **Requiere actualizar docs:** SÍ (ARQUITECTURA.md, TESTING.md)
- [ ] **Requiere actualizar tests:** SÍ (actualizar fixtures)

## 📝 Definición de Done (DoD)

- [ ] TermostatoFactory implementado
- [ ] create_app() con DI implementado
- [ ] Configurador deprecado o refactorizado
- [ ] Tests unitarios de factory creados
- [ ] Tests existentes actualizados y pasan
- [ ] Tests pueden ejecutarse en paralelo
- [ ] Code review aprobado
- [ ] Quality gates pasan
- [ ] Documentación actualizada
- [ ] Branch mergeado a master

---

**Creado:** 2026-02-06
**Actualizado:** 2026-02-06
**Autor:** Equipo de Desarrollo
