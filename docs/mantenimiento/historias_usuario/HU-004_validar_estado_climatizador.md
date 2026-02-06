# [HU-004] Agregar validación a estado_climatizador

**Epic:** Refactorización Deuda Técnica - Diseño
**Prioridad:** 🟡 Media
**Estimación:** 2 Story Points
**Sprint:** TBD
**Jira:** TBD

---

## 📖 Historia de Usuario

**Como** sistema de control del termostato
**Quiero** validar que el estado del climatizador solo acepte valores permitidos
**Para** prevenir datos inválidos y mejorar la robustez del sistema

## 🎯 Criterios de Aceptación

- [ ] **AC1:** estado_climatizador solo acepta: "apagado", "encendido", "enfriando", "calentando"
- [ ] **AC2:** Valores inválidos lanzan ValueError con mensaje descriptivo
- [ ] **AC3:** Validación es case-insensitive ("Apagado" → "apagado")
- [ ] **AC4:** Tests cubren todos los casos válidos e inválidos
- [ ] **AC5:** API retorna 400 con mensaje claro cuando se envía estado inválido
- [ ] **AC6:** Documentación Swagger actualizada con valores permitidos

## 📋 Tareas Técnicas

- [ ] **T1:** Definir constante `ESTADOS_CLIMATIZADOR_VALIDOS` en `app/configuracion/config.py`
- [ ] **T2:** Actualizar setter de `estado_climatizador` en `termostato.py`
  - Convertir a minúsculas
  - Validar contra valores permitidos
  - Lanzar ValueError si inválido
- [ ] **T3:** Actualizar docstring de Swagger en `api.py` con valores permitidos
- [ ] **T4:** Crear tests unitarios
  - Test valores válidos (4 casos)
  - Test valores inválidos (casos comunes)
  - Test case-insensitive
- [ ] **T5:** Crear test de integración API
  - POST con valor válido → 201
  - POST con valor inválido → 400
- [ ] **T6:** Code review
- [ ] **T7:** Ejecutar quality-check

## 🔗 Contexto

**Problema identificado:**
- **Análisis:** [docs/analisis/2026-02-06_analisis_diseno.md](../../analisis/2026-02-06_analisis_diseno.md#5-missing-validation)
- **Code smell:** Missing Validation
- **Ubicación:** `app/general/termostato.py:99-102`
- **Riesgo:** Estado inválido puede causar bugs en lógica de negocio

**Código actual (SIN VALIDACIÓN):**

```python
@estado_climatizador.setter
def estado_climatizador(self, valor):
    """Establece el estado del climatizador."""
    self._estado_climatizador = str(valor)  # ❌ Acepta CUALQUIER string
    self._guardar_estado()
```

**Solución propuesta:**

```python
# app/configuracion/config.py
ESTADOS_CLIMATIZADOR_VALIDOS = {
    "apagado",
    "encendido",
    "enfriando",
    "calentando"
}


# app/general/termostato.py
@estado_climatizador.setter
def estado_climatizador(self, valor):
    """Establece el estado del climatizador.

    Args:
        valor: Estado del climatizador. Valores válidos:
               'apagado', 'encendido', 'enfriando', 'calentando'

    Raises:
        ValueError: Si el estado no es uno de los valores permitidos
    """
    valor = str(valor).lower().strip()

    if valor not in Config.ESTADOS_CLIMATIZADOR_VALIDOS:
        raise ValueError(
            f"estado_climatizador debe ser uno de: "
            f"{', '.join(sorted(Config.ESTADOS_CLIMATIZADOR_VALIDOS))}. "
            f"Recibido: '{valor}'"
        )

    self._estado_climatizador = valor
    self._guardar_estado()
```

**Archivos afectados:**
- `app/configuracion/config.py` (agregar constante)
- `app/general/termostato.py` (actualizar setter)
- `app/servicios/api.py` (actualizar docstring Swagger)
- `tests/test_termostato.py` (agregar tests de validación)
- `tests/test_api.py` (agregar test de error 400)

## 📊 Métricas

**Antes:**
- **Validación:** ❌ Ninguna
- **Valores permitidos:** ∞ (cualquier string)
- **Robustez:** Baja

**Después:**
- **Validación:** ✅ Completa
- **Valores permitidos:** 4 (whitelist)
- **Robustez:** Alta

## 🔗 Referencias

- **Análisis de diseño:** [docs/analisis/2026-02-06_analisis_diseno.md](../../analisis/2026-02-06_analisis_diseno.md)
- **Jira:** TBD

## 🧪 Testing

**Escenarios a validar:**

### Tests Unitarios - Termostato
```python
def test_estado_climatizador_valido_apagado():
    termostato.estado_climatizador = "apagado"
    assert termostato.estado_climatizador == "apagado"

def test_estado_climatizador_valido_encendido():
    termostato.estado_climatizador = "encendido"
    assert termostato.estado_climatizador == "encendido"

def test_estado_climatizador_valido_enfriando():
    termostato.estado_climatizador = "enfriando"
    assert termostato.estado_climatizador == "enfriando"

def test_estado_climatizador_valido_calentando():
    termostato.estado_climatizador = "calentando"
    assert termostato.estado_climatizador == "calentando"

def test_estado_climatizador_case_insensitive():
    termostato.estado_climatizador = "APAGADO"
    assert termostato.estado_climatizador == "apagado"

def test_estado_climatizador_invalido():
    with pytest.raises(ValueError, match="estado_climatizador debe ser uno de"):
        termostato.estado_climatizador = "desconocido"

def test_estado_climatizador_vacio():
    with pytest.raises(ValueError):
        termostato.estado_climatizador = ""

def test_estado_climatizador_con_espacios():
    termostato.estado_climatizador = "  apagado  "
    assert termostato.estado_climatizador == "apagado"
```

### Tests de Integración - API
```python
def test_post_estado_climatizador_valido(client):
    response = client.post('/termostato/estado_climatizador/',
                          json={'climatizador': 'enfriando'})
    assert response.status_code == 201

def test_post_estado_climatizador_invalido(client):
    response = client.post('/termostato/estado_climatizador/',
                          json={'climatizador': 'modo_turbo'})
    assert response.status_code == 400
    assert 'debe ser uno de' in response.json['error']['detalle']
```

## ⚠️ Riesgos

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Breaking changes si frontend usa valores inválidos | Media | Alto | Revisar logs de producción primero |
| Datos persistidos con valores inválidos | Baja | Medio | Script de migración/limpieza |

**Mitigación general:**
- Revisar logs para ver qué valores se usan actualmente
- Si hay valores no contemplados, agregarlos a la whitelist

## 🚀 Despliegue

- [ ] **Requiere migración de datos:** POSIBLE (revisar estados persistidos)
- [ ] **Breaking changes:** POSIBLE (si frontend usa valores no permitidos)
- [ ] **Requiere actualizar frontend:** POSIBLE (verificar valores usados)
- [ ] **Requiere actualizar docs:** SÍ (Swagger)

## 📝 Definición de Done (DoD)

- [ ] Constante ESTADOS_CLIMATIZADOR_VALIDOS definida
- [ ] Validación implementada en setter
- [ ] Tests unitarios creados (8+ tests)
- [ ] Tests de API creados
- [ ] Swagger actualizado
- [ ] Code review aprobado
- [ ] No hay valores inválidos en producción (verificado)
- [ ] Branch mergeado a master

---

**Creado:** 2026-02-06
**Actualizado:** 2026-02-06
**Autor:** Equipo de Desarrollo
