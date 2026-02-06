# [HU-005] Refactorizar imports y eliminar code smells menores

**Epic:** Refactorización Deuda Técnica - Diseño
**Prioridad:** 🟡 Media
**Estimación:** 1 Story Point
**Sprint:** TBD
**Jira:** TBD

---

## 📖 Historia de Usuario

**Como** desarrollador del sistema
**Quiero** eliminar code smells menores (imports dentro de métodos, variables globales)
**Para** mejorar la calidad y claridad del código

## 🎯 Criterios de Aceptación

- [ ] **AC1:** Import de `RegistroTemperatura` movido al top del archivo
- [ ] **AC2:** Variable global `_inicio_servidor` reemplazada por clase de estado
- [ ] **AC3:** No hay imports dentro de funciones/métodos
- [ ] **AC4:** Todos los tests pasan
- [ ] **AC5:** No hay warnings de linter sobre imports

## 📋 Tareas Técnicas

- [ ] **T1:** Mover import de `RegistroTemperatura` al top de `termostato.py`
  - Verificar que no causa import circular
  - Si causa circular, refactorizar dependencias
- [ ] **T2:** Crear clase `AppState` en `api.py`
  - Encapsular `inicio_servidor`
  - Usar como singleton simple o app context
- [ ] **T3:** Actualizar función `comprueba()` para usar `AppState`
- [ ] **T4:** Ejecutar linter y verificar sin warnings
- [ ] **T5:** Ejecutar tests
- [ ] **T6:** Code review

## 🔗 Contexto

**Problema identificado:**
- **Análisis:** [docs/analisis/2026-02-06_analisis_diseno.md](../../analisis/2026-02-06_analisis_diseno.md#4-import-inside-method)
- **Code smells:**
  1. Import Inside Method (termostato.py:143)
  2. Global Variable (api.py:69)

### Problema 1: Import dentro de método

**Código actual:**
```python
# app/general/termostato.py:143
def _registrar_en_historial(self, temperatura):
    if self._historial_repositorio:
        from app.datos import RegistroTemperatura  # ❌ Import dentro de método
        registro = RegistroTemperatura(...)
```

**Solución:**
```python
# app/general/termostato.py (top del archivo)
from datetime import datetime
from app.configuracion.config import Config
from app.datos.registro import RegistroTemperatura  # ✅ Import al top

class Termostato:
    # ...

    def _registrar_en_historial(self, temperatura):
        if self._historial_repositorio:
            registro = RegistroTemperatura(
                temperatura=temperatura,
                timestamp=datetime.now()
            )
            self._historial_repositorio.agregar(registro)
```

### Problema 2: Variable global

**Código actual:**
```python
# app/servicios/api.py:69
_inicio_servidor = datetime.now()  # ❌ Variable global mutable

@app_api.route("/comprueba/", methods=["GET"])
def comprueba():
    ahora = datetime.now()
    uptime = (ahora - _inicio_servidor).total_seconds()
```

**Solución:**
```python
# app/servicios/api.py
class AppState:
    """Estado de la aplicación Flask."""
    def __init__(self):
        self.inicio_servidor = datetime.now()

app_state = AppState()

@app_api.route("/comprueba/", methods=["GET"])
def comprueba():
    ahora = datetime.now()
    uptime = (ahora - app_state.inicio_servidor).total_seconds()
```

**Archivos afectados:**
- `app/general/termostato.py` (mover import)
- `app/servicios/api.py` (AppState)
- `tests/test_termostato.py` (verificar sin cambios)
- `tests/test_api.py` (verificar sin cambios)

## 📊 Métricas

**Antes:**
- **Imports dentro de métodos:** 1
- **Variables globales:** 1
- **Linter warnings:** 2

**Después:**
- **Imports dentro de métodos:** 0
- **Variables globales:** 0 (AppState es encapsulación)
- **Linter warnings:** 0

## 🔗 Referencias

- **Análisis de diseño:** [docs/analisis/2026-02-06_analisis_diseno.md](../../analisis/2026-02-06_analisis_diseno.md)
- **Jira:** TBD

## 🧪 Testing

**Escenarios a validar:**

### Tests de Regresión
- Todos los tests existentes pasan
- Comportamiento funcional sin cambios
- Endpoint /comprueba/ sigue retornando uptime correctamente

### Tests de Import
- No hay import circular
- Termostato se importa correctamente desde otros módulos

## ⚠️ Riesgos

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Import circular | Media | Medio | Si ocurre, refactorizar dependencias |
| Breaking de uptime calculation | Muy Baja | Bajo | Test de regresión |

## 🚀 Despliegue

- [ ] **Requiere migración de datos:** NO
- [ ] **Breaking changes:** NO
- [ ] **Requiere actualizar frontend:** NO
- [ ] **Requiere actualizar docs:** NO

## 📝 Definición de Done (DoD)

- [ ] Import movido al top
- [ ] AppState implementado
- [ ] Tests pasan
- [ ] Linter sin warnings
- [ ] Code review aprobado
- [ ] Branch mergeado a master

---

**Creado:** 2026-02-06
**Actualizado:** 2026-02-06
**Autor:** Equipo de Desarrollo
