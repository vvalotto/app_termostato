# Plan de Implementación: HU-002 - Eliminar Singleton en Configurador

**Patrón:** Flask REST (Layered + Application Factory)
**Producto:** app_termostato
**Estimación HU:** 8 SP
**Estimación Total:** 1h 45min
**BDD:** No aplica (refactorización de arquitectura interna)

---

## Análisis del código actual

`Configurador` tiene 4 variables de clase estáticas que actúan como Singleton implícito:
- `historial_repositorio` — instancia única global
- `historial_mapper` — instancia única global
- `persistidor` — instancia única global
- `termostato` — instancia única global (el más problemático)

`api.py` consume `Configurador.termostato` al nivel de módulo, lo que hace imposible
inyectar mocks en tests sin parchear el módulo completo.

## Estrategia de implementación

**Application Factory Pattern** (estándar Flask):
- `TermostatoFactory` crea instancias bajo demanda
- `create_app(termostato=None)` permite inyectar dependencias
- `Configurador` se mantiene como wrapper deprecated para no romper imports externos
- Tests usan `create_app(termostato=Mock())` directamente

---

## Tareas

### T1 - Crear `app/configuracion/factory.py` (20 min)
- [x] Clase `TermostatoFactory` con métodos estáticos:
  - `crear_termostato(historial_repositorio, persistidor, config)` → Termostato
  - `crear_historial_repositorio()` → HistorialRepositorioMemoria
  - `crear_historial_mapper()` → HistorialMapper
  - `crear_persistidor(ruta)` → TermostatoPersistidorJSON

### T2 - Refactorizar `app/servicios/api.py` (25 min)
- [ ] Agregar función `create_app(termostato=None) -> Flask`
  - Mueve toda la configuración Flask dentro de la función
  - `termostato` se inyecta o se crea via `TermostatoFactory`
  - Todos los endpoints pasan a ser closures sobre `termostato`
  - `app_api` pasa a ser creado por `create_app()` para compatibilidad con `run.py`
- [ ] Eliminar `termostato = Configurador.termostato` global

### T3 - Actualizar `run.py` (5 min)
- [ ] Importar `create_app` en lugar de `app_api` directamente
- [ ] Usar `app = create_app()` antes de `app.run()`

### T4 - Actualizar `tests/conftest.py` (15 min)
- [ ] Crear `conftest.py` si no existe
- [ ] Fixture `app` que usa `create_app(termostato=mock)`
- [ ] Fixture `client` basada en la fixture `app`

### T5 - Actualizar `tests/test_api.py` (15 min)
- [ ] Reemplazar fixture local `client` por la de `conftest.py`
- [ ] Verificar que todos los tests siguen pasando

### T6 - Actualizar `tests/test_decorators.py` (10 min)
- [ ] Reemplazar fixture local `client` por la de `conftest.py`

### T7 - Deprecar `Configurador` (5 min)
- [ ] Agregar docstring `@deprecated` en `configurador.py`
- [ ] Mantener funcionando para no romper imports

### T8 - Tests unitarios de TermostatoFactory (15 min)
- [ ] `tests/test_factory.py` (crear)
  - Factory crea termostato con config por defecto
  - Factory acepta dependencias customizadas
  - Dos llamadas retornan instancias independientes (no singleton)

### T9 - Quality check (10 min)
- [ ] Ejecutar `/quality-check app/`
  - Pylint ≥ 8.0, CC ≤ 10, MI > 20

---

## Archivos afectados

| Archivo | Acción |
|---------|--------|
| `app/configuracion/factory.py` | Crear |
| `app/configuracion/configurador.py` | Deprecar (mantener) |
| `app/servicios/api.py` | Refactorizar (add create_app) |
| `run.py` | Actualizar |
| `tests/conftest.py` | Crear |
| `tests/test_api.py` | Actualizar fixtures |
| `tests/test_decorators.py` | Actualizar fixtures |
| `tests/test_factory.py` | Crear |

---

**Estado:** ✅ COMPLETADO
**Creado:** 2026-02-22
**Completado:** 2026-02-22

## Lecciones Aprendidas

- ✅ Application Factory Pattern resuelve el Singleton limpiamente — `create_app()` es el estándar Flask
- ✅ Mantener `app_api = create_app()` al final del módulo preserva compatibilidad sin romper nada
- 💡 Los tests de "dos instancias no comparten estado" son el mejor indicador de que el Singleton fue eliminado
- ⚠️ El `DeprecationWarning` en `configurador.py` puede generar ruido en tests — considerar suprimir en conftest
