# [HU-003] Eliminar duplicación en endpoints API

**Epic:** Refactorización Deuda Técnica - Diseño
**Prioridad:** 🔴 Alta
**Estimación:** 5 Story Points
**Sprint:** TBD
**Jira:** TBD

---

## 📖 Historia de Usuario

**Como** desarrollador del sistema
**Quiero** eliminar el código duplicado en los endpoints de la API REST
**Para** facilitar el mantenimiento, reducir bugs y cumplir el principio DRY (Don't Repeat Yourself)

## 🎯 Criterios de Aceptación

- [ ] **AC1:** Código duplicado reducido de ~200 LOC a < 50 LOC
- [ ] **AC2:** Lógica común de GET/POST extraída a decorador o función genérica
- [ ] **AC3:** Endpoints funcionan exactamente igual (no breaking changes)
- [ ] **AC4:** Tests existentes pasan sin modificación
- [ ] **AC5:** Nuevos endpoints pueden agregarse con < 10 líneas de código
- [ ] **AC6:** Documentación Swagger se mantiene intacta
- [ ] **AC7:** Validación de errores centralizada
- [ ] **AC8:** Métricas de calidad pasan quality gates

## 📋 Tareas Técnicas

- [ ] **T1:** Analizar patrón común en endpoints actuales
- [ ] **T2:** Crear decorador `@endpoint_termostato` en `app/servicios/decorators.py`
- [ ] **T3:** Refactorizar endpoint `temperatura_ambiente` usando decorador
- [ ] **T4:** Refactorizar endpoint `temperatura_deseada` usando decorador
- [ ] **T5:** Refactorizar endpoint `bateria` usando decorador
- [ ] **T6:** Refactorizar endpoint `estado_climatizador` usando decorador
- [ ] **T7:** Crear tests unitarios del decorador
- [ ] **T8:** Ejecutar tests de regresión de API
- [ ] **T9:** Code review
- [ ] **T10:** Ejecutar quality-check

## 🔗 Contexto

**Problema identificado:**
- **Análisis:** [docs/analisis/2026-02-06_analisis_diseno.md](../../analisis/2026-02-06_analisis_diseno.md#3-code-smells)
- **Code smell:** Massive Duplication
- **Principio violado:** DRY (Don't Repeat Yourself)
- **Duplicación:** ~200 líneas repetidas con 95% de similitud
- **Impacto:**
  - Bugs deben corregirse en 6 lugares
  - Cambios requieren editar múltiples funciones
  - Dificulta agregar nuevos endpoints

**Código actual (DUPLICADO 6 veces):**

```python
# Este patrón se repite en 6 endpoints con mínimas variaciones
@app_api.route("/termostato/temperatura_ambiente/", methods=["GET", "POST"])
def obtener_temperatura_ambiente():
    if request.method == 'POST':
        datos = request.get_json()
        if not datos or "ambiente" not in datos:  # ❌ Duplicado
            logger.warning("POST /termostato/temperatura_ambiente/ - Campo requerido faltante")
            return error_response(400, "Campo requerido faltante", "Se requiere campo 'ambiente'")
        try:
            termostato.temperatura_ambiente = datos["ambiente"]  # ❌ Duplicado
        except ValueError as e:
            logger.warning("POST /termostato/temperatura_ambiente/ - %s", e)
            return error_response(400, "Valor fuera de rango", str(e))
        logger.info("POST /termostato/temperatura_ambiente/ -> 201")
        return jsonify({'mensaje': 'dato registrado'}), 201
    else:
        logger.info("GET /termostato/temperatura_ambiente/ -> 200")
        return jsonify({'temperatura_ambiente': termostato.temperatura_ambiente})
```

**Solución propuesta - Decorador:**

```python
# app/servicios/decorators.py
def endpoint_termostato(campo_modelo: str, campo_request: str = None, validar: bool = True):
    """
    Decorador para endpoints GET/POST del termostato.

    Args:
        campo_modelo: Nombre del atributo en el modelo Termostato (ej: 'temperatura_ambiente')
        campo_request: Nombre del campo en el request JSON (ej: 'ambiente'). Si None, usa campo_modelo
        validar: Si True, captura ValueError y retorna 400
    """
    if campo_request is None:
        campo_request = campo_modelo

    def decorator(func):
        @wraps(func)
        def wrapper():
            route = request.path

            if request.method == 'POST':
                datos = request.get_json()

                # Validar presencia de campo
                if not datos or campo_request not in datos:
                    logger.warning(f"POST {route} - Campo requerido faltante")
                    return error_response(
                        400,
                        "Campo requerido faltante",
                        f"Se requiere campo '{campo_request}'"
                    )

                try:
                    # Actualizar valor en modelo
                    setattr(termostato, campo_modelo, datos[campo_request])
                    logger.info(f"POST {route} -> 201")
                    return jsonify({'mensaje': 'dato registrado'}), 201

                except ValueError as e:
                    if validar:
                        logger.warning(f"POST {route} - {e}")
                        return error_response(400, "Valor fuera de rango", str(e))
                    raise

            else:  # GET
                logger.info(f"GET {route} -> 200")
                valor = getattr(termostato, campo_modelo)
                return jsonify({campo_modelo: valor})

        return wrapper
    return decorator


# app/servicios/api.py (REFACTORIZADO)
@app_api.route("/termostato/temperatura_ambiente/", methods=["GET", "POST"])
@endpoint_termostato("temperatura_ambiente", "ambiente")
def obtener_temperatura_ambiente():
    """Gestiona la temperatura ambiente.
    ---
    [Documentación Swagger se mantiene]
    """
    pass  # ✅ Lógica manejada por decorador


@app_api.route("/termostato/temperatura_deseada/", methods=["GET", "POST"])
@endpoint_termostato("temperatura_deseada", "deseada")
def obtener_temperatura_deseada():
    """Gestiona la temperatura deseada.
    ---
    [Documentación Swagger se mantiene]
    """
    pass


@app_api.route("/termostato/bateria/", methods=["GET", "POST"])
@endpoint_termostato("carga_bateria", "bateria")
def obtener_carga_bateria():
    """Gestiona la carga de bateria.
    ---
    [Documentación Swagger se mantiene]
    """
    pass


@app_api.route("/termostato/estado_climatizador/", methods=["GET", "POST"])
@endpoint_termostato("estado_climatizador", "climatizador", validar=False)
def obtener_estado_climatizador():
    """Gestiona el estado del climatizador.
    ---
    [Documentación Swagger se mantiene]
    """
    pass
```

**Beneficios:**
- ✅ De ~30 líneas por endpoint a ~6 líneas
- ✅ Bugs se corrigen en 1 solo lugar
- ✅ Agregar endpoint nuevo: < 10 líneas
- ✅ Documentación Swagger se mantiene
- ✅ Testing más fácil (testear decorador una vez)

**Archivos afectados:**
- `app/servicios/decorators.py` (crear)
- `app/servicios/api.py` (refactorizar endpoints)
- `tests/test_decorators.py` (crear)
- `tests/test_api.py` (actualizar si necesario)

## 📊 Métricas

**Antes:**
- **LOC en api.py:** 429
- **Duplicación:** ~200 LOC (46%)
- **Endpoints:** 6 funciones × ~30 LOC = 180 LOC

**Después (esperado):**
- **LOC en api.py:** ~250 (-180 LOC)
- **LOC en decorators.py:** ~40 LOC (nuevo)
- **Duplicación:** ~0%
- **Endpoints:** 6 funciones × ~6 LOC = 36 LOC
- **Ahorro neto:** ~140 LOC

## 🔗 Referencias

- **Análisis de diseño:** [docs/analisis/2026-02-06_analisis_diseno.md](../../analisis/2026-02-06_analisis_diseno.md#3-massive-duplication)
- **Jira:** TBD
- **Principio:** [DRY - Don't Repeat Yourself](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself)

## 🧪 Testing

**Escenarios a validar:**

### Tests Unitarios - Decorador
- Decorador GET retorna valor correcto
- Decorador POST actualiza valor correctamente
- Decorador POST sin campo requerido retorna 400
- Decorador POST con ValueError retorna 400
- Decorador respeta parámetro validar=False
- Logging funciona correctamente

### Tests de Integración - Endpoints
- GET /termostato/temperatura_ambiente/ funciona
- POST /termostato/temperatura_ambiente/ con valor válido funciona
- POST /termostato/temperatura_ambiente/ con valor inválido retorna 400
- POST /termostato/temperatura_ambiente/ sin campo retorna 400
- Repetir para todos los endpoints refactorizados

### Tests de Regresión
- **CRÍTICO:** Comportamiento de API exactamente igual que antes
- Códigos de estado HTTP iguales
- Formato de respuestas JSON igual
- Mensajes de error iguales

## ⚠️ Riesgos

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Breaking changes en API | Baja | Alto | Tests de regresión exhaustivos |
| Documentación Swagger se pierde | Baja | Medio | Verificar que docstrings se preservan |
| Comportamiento sutil diferente | Media | Alto | Tests de comparación antes/después |
| Decorador complejo de mantener | Baja | Bajo | Documentar bien, tests unitarios |

**Mitigación general:**
- Refactorizar endpoint por endpoint
- Tests de regresión después de cada cambio
- Comparar responses HTTP antes/después

## 🚀 Despliegue

- [ ] **Requiere migración de datos:** NO
- [ ] **Breaking changes:** NO
- [ ] **Requiere actualizar frontend:** NO
- [ ] **Requiere actualizar docs:** SÍ (comentar nueva arquitectura)
- [ ] **Requiere comunicación a equipo:** SÍ (cambio interno)

## 📝 Definición de Done (DoD)

- [ ] Decorador implementado y testeado
- [ ] 6 endpoints refactorizados
- [ ] Tests unitarios del decorador creados
- [ ] Tests de regresión pasan 100%
- [ ] Reducción de >= 140 LOC
- [ ] Code review aprobado
- [ ] Quality gates pasan
- [ ] Documentación actualizada
- [ ] Branch mergeado a master

---

**Creado:** 2026-02-06
**Actualizado:** 2026-02-06
**Autor:** Equipo de Desarrollo
