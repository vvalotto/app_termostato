# Plan de Testing de Sistema — app_termostato

**Versión:** 1.0
**Fecha:** 2026-02-22
**Aplicación:** REST API Termostato
**Versión de la app:** 1.2.0

---

## 1. Introducción

### 1.1 Propósito

Este documento define el plan de testing de **sistema** para la API REST `app_termostato`. A diferencia de los tests unitarios e integración ya existentes, el testing de sistema valida el comportamiento del sistema completo tal como lo experimenta un cliente externo: enviando peticiones HTTP reales a un servidor levantado, verificando respuestas end-to-end y validando flujos de negocio completos.

### 1.2 Alcance

**En alcance:**
- Todos los endpoints REST bajo `/termostato/` y `/comprueba/`
- Flujos de negocio completos (multi-paso)
- Validaciones de dominio observables desde la API
- Persistencia de estado entre peticiones en la misma sesión
- Estructura y semántica de respuestas JSON
- Códigos HTTP y manejo de errores

**Fuera de alcance:**
- Tests de carga / performance (requieren herramienta dedicada tipo Locust/k6)
- Tests de seguridad (autenticación, autorización — la API no tiene autenticación)
- Tests de interfaz de usuario (no existe frontend en este repo)
- Tests de contrato con el frontend `webapp_termostato`

### 1.3 Diferencia con Tests Existentes

| Nivel | Archivo existente | Qué valida |
|-------|------------------|-----------|
| Unitario | `test_validators.py`, `test_calculadores.py` | Clases aisladas con mocks |
| Unitario | `test_termostato.py`, `test_termostato_service.py` | Dominio con dependencias inyectadas |
| Integración | `test_api.py` | Endpoints con cliente Flask de test (sin red real) |
| **Sistema** | **`test_sistema.py` (nuevo)** | **Servidor real levantado, peticiones HTTP reales** |

---

## 2. Entorno de Prueba

### 2.1 Configuración

| Parámetro | Valor |
|-----------|-------|
| Servidor | `http://localhost:5050` |
| Modo | `DEBUG=False` (para simular producción) |
| Herramienta HTTP | `requests` (o `curl` para ejecución manual) |
| Framework de test | `pytest` + `requests` |
| Estado inicial | Valores por defecto de `Config` |

### 2.2 Prerequisitos

```bash
# 1. Levantar el servidor (en terminal separada)
python run.py

# 2. Verificar que el servidor responde
curl http://localhost:5050/comprueba/

# 3. Instalar dependencias de test de sistema (si aplica)
pip install requests pytest
```

### 2.3 Variables de Entorno para Testing

```bash
PORT=5050
DEBUG=false
TEMPERATURA_AMBIENTE_INICIAL=20
TEMPERATURA_DESEADA_INICIAL=24
CARGA_BATERIA_INICIAL=5.0
```

---

## 3. Inventario de Endpoints

| ID | Método | Ruta | Campo POST | Descripción |
|----|--------|------|-----------|-------------|
| E-01 | GET | `/comprueba/` | — | Health check |
| E-02 | GET | `/termostato/` | — | Estado completo |
| E-03 | GET | `/termostato/historial/` | — | Historial de temperaturas |
| E-04 | GET | `/termostato/temperatura_ambiente/` | — | Leer temp. ambiente |
| E-05 | POST | `/termostato/temperatura_ambiente/` | `ambiente` | Actualizar temp. ambiente |
| E-06 | GET | `/termostato/temperatura_deseada/` | — | Leer temp. deseada |
| E-07 | POST | `/termostato/temperatura_deseada/` | `deseada` | Actualizar temp. deseada |
| E-08 | GET | `/termostato/bateria/` | — | Leer carga batería |
| E-09 | POST | `/termostato/bateria/` | `bateria` | Actualizar batería |
| E-10 | GET | `/termostato/estado_climatizador/` | — | Leer estado climatizador |
| E-11 | POST | `/termostato/estado_climatizador/` | `climatizador` | Actualizar climatizador |
| E-12 | GET | `/termostato/indicador/` | — | Leer indicador (solo lectura) |

---

## 4. Casos de Prueba

### 4.1 TS-HC — Health Check

#### TS-HC-01: Health check responde correctamente

**Precondición:** Servidor levantado.
**Pasos:**
1. `GET /comprueba/`

**Resultado esperado:**
- Status: `200 OK`
- Body:
  ```json
  {
    "status": "ok",
    "version": "1.2.0",
    "uptime_seconds": <entero >= 0>,
    "timestamp": "<ISO-8601>"
  }
```
- `uptime_seconds` es un entero no negativo
- `timestamp` tiene formato ISO-8601 válido

#### TS-HC-02: Uptime crece entre llamadas

**Pasos:**
1. `GET /comprueba/` → anotar `uptime_seconds` como `t1`
2. Esperar 2 segundos
3. `GET /comprueba/` → anotar `uptime_seconds` como `t2`

**Resultado esperado:**
- `t2 > t1`

---

### 4.2 TS-EST — Estado Completo

#### TS-EST-01: GET /termostato/ retorna todos los campos

**Pasos:**
1. `GET /termostato/`

**Resultado esperado:**
- Status: `200 OK`
- Body contiene exactamente los campos:
  ```json
  {
    "temperatura_ambiente": 20,
    "temperatura_deseada": 24,
    "carga_bateria": 5.0,
    "estado_climatizador": "apagado",
    "indicador": "NORMAL"
  }
  ```

#### TS-EST-02: GET /termostato/ refleja cambios previos

**Precondición:** Servidor con estado inicial.
**Pasos:**
1. `POST /termostato/temperatura_ambiente/` con `{"ambiente": 35}`
2. `POST /termostato/temperatura_deseada/` con `{"deseada": 28}`
3. `GET /termostato/`

**Resultado esperado:**
- `temperatura_ambiente`: `35`
- `temperatura_deseada`: `28`
- Los demás campos tienen sus valores actuales

---

### 4.3 TS-TA — Temperatura Ambiente

#### TS-TA-01: GET retorna valor actual

**Pasos:**
1. `GET /termostato/temperatura_ambiente/`

**Resultado esperado:**
- Status: `200 OK`
- Body: `{"temperatura_ambiente": 20}`

#### TS-TA-02: POST actualiza valor correctamente

**Pasos:**
1. `POST /termostato/temperatura_ambiente/` con `{"ambiente": 30}`

**Resultado esperado:**
- Status: `201 Created`
- Body: `{"mensaje": "dato registrado"}`

2. `GET /termostato/temperatura_ambiente/`
- Body: `{"temperatura_ambiente": 30}`

#### TS-TA-03: POST acepta valor en límite inferior (0)

**Pasos:**
1. `POST /termostato/temperatura_ambiente/` con `{"ambiente": 0}`

**Resultado esperado:**
- Status: `201 Created`
- `GET` posterior retorna `{"temperatura_ambiente": 0}`

#### TS-TA-04: POST acepta valor en límite superior (50)

**Pasos:**
1. `POST /termostato/temperatura_ambiente/` con `{"ambiente": 50}`

**Resultado esperado:**
- Status: `201 Created`
- `GET` posterior retorna `{"temperatura_ambiente": 50}`

#### TS-TA-05: POST acepta valor como string numérico (conversión de tipo)

**Pasos:**
1. `POST /termostato/temperatura_ambiente/` con `{"ambiente": "25"}`

**Resultado esperado:**
- Status: `201 Created`
- `GET` posterior retorna `{"temperatura_ambiente": 25}` (entero)

#### TS-TA-06: POST acepta float y lo trunca a entero

**Pasos:**
1. `POST /termostato/temperatura_ambiente/` con `{"ambiente": 22.7}`

**Resultado esperado:**
- Status: `201 Created`
- `GET` posterior retorna `{"temperatura_ambiente": 22}` (int, truncado)

#### TS-TA-07: POST rechaza valor por encima del máximo (>50)

**Pasos:**
1. `POST /termostato/temperatura_ambiente/` con `{"ambiente": 51}`

**Resultado esperado:**
- Status: `400 Bad Request`
- Body contiene campo `error` con código `400`

#### TS-TA-08: POST rechaza valor por debajo del mínimo (<0)

**Pasos:**
1. `POST /termostato/temperatura_ambiente/` con `{"ambiente": -1}`

**Resultado esperado:**
- Status: `400 Bad Request`

#### TS-TA-09: POST rechaza campo faltante

**Pasos:**
1. `POST /termostato/temperatura_ambiente/` con `{}`

**Resultado esperado:**
- Status: `400 Bad Request`

#### TS-TA-10: POST rechaza campo incorrecto

**Pasos:**
1. `POST /termostato/temperatura_ambiente/` con `{"temperatura": 25}` (campo equivocado)

**Resultado esperado:**
- Status: `400 Bad Request`

#### TS-TA-11: POST rechaza Content-Type no JSON

**Pasos:**
1. `POST /termostato/temperatura_ambiente/` con body `ambiente=25` y `Content-Type: application/x-www-form-urlencoded`

**Resultado esperado:**
- Status: `415 Unsupported Media Type`

---

### 4.4 TS-TD — Temperatura Deseada

#### TS-TD-01: GET retorna valor actual

**Pasos:**
1. `GET /termostato/temperatura_deseada/`

**Resultado esperado:**
- Status: `200 OK`
- Body: `{"temperatura_deseada": 24}`

#### TS-TD-02: POST actualiza valor correctamente

**Pasos:**
1. `POST /termostato/temperatura_deseada/` con `{"deseada": 20}`

**Resultado esperado:**
- Status: `201 Created`
- `GET` posterior: `{"temperatura_deseada": 20}`

#### TS-TD-03: POST acepta límite inferior (15)

**Pasos:**
1. `POST /termostato/temperatura_deseada/` con `{"deseada": 15}`

**Resultado esperado:**
- Status: `201 Created`
- `GET` posterior: `{"temperatura_deseada": 15}`

#### TS-TD-04: POST acepta límite superior (30)

**Pasos:**
1. `POST /termostato/temperatura_deseada/` con `{"deseada": 30}`

**Resultado esperado:**
- Status: `201 Created`
- `GET` posterior: `{"temperatura_deseada": 30}`

#### TS-TD-05: POST rechaza valor fuera de rango (>30)

**Pasos:**
1. `POST /termostato/temperatura_deseada/` con `{"deseada": 31}`

**Resultado esperado:**
- Status: `400 Bad Request`

#### TS-TD-06: POST rechaza valor fuera de rango (<15)

**Pasos:**
1. `POST /termostato/temperatura_deseada/` con `{"deseada": 14}`

**Resultado esperado:**
- Status: `400 Bad Request`

---

### 4.5 TS-BA — Batería

#### TS-BA-01: GET retorna valor actual

**Pasos:**
1. `GET /termostato/bateria/`

**Resultado esperado:**
- Status: `200 OK`
- Body: `{"carga_bateria": 5.0}`

#### TS-BA-02: POST actualiza valor correctamente

**Pasos:**
1. `POST /termostato/bateria/` con `{"bateria": 3.5}`

**Resultado esperado:**
- Status: `201 Created`
- `GET` posterior: `{"carga_bateria": 3.5}`

#### TS-BA-03: POST acepta límite inferior (0.0)

**Pasos:**
1. `POST /termostato/bateria/` con `{"bateria": 0.0}`

**Resultado esperado:**
- Status: `201 Created`
- `GET` posterior: `{"carga_bateria": 0.0}`

#### TS-BA-04: POST acepta límite superior (5.0)

**Pasos:**
1. `POST /termostato/bateria/` con `{"bateria": 5.0}`

**Resultado esperado:**
- Status: `201 Created`
- `GET` posterior: `{"carga_bateria": 5.0}`

#### TS-BA-05: POST redondea a 2 decimales

**Pasos:**
1. `POST /termostato/bateria/` con `{"bateria": 3.14159}`

**Resultado esperado:**
- Status: `201 Created`
- `GET` posterior: `{"carga_bateria": 3.14}` (redondeado)

#### TS-BA-06: POST acepta entero y lo convierte a float

**Pasos:**
1. `POST /termostato/bateria/` con `{"bateria": 3}`

**Resultado esperado:**
- Status: `201 Created`
- `GET` posterior: `{"carga_bateria": 3.0}` (float)

#### TS-BA-07: POST rechaza valor fuera de rango (>5.0)

**Pasos:**
1. `POST /termostato/bateria/` con `{"bateria": 5.1}`

**Resultado esperado:**
- Status: `400 Bad Request`

#### TS-BA-08: POST rechaza valor fuera de rango (<0.0)

**Pasos:**
1. `POST /termostato/bateria/` con `{"bateria": -0.1}`

**Resultado esperado:**
- Status: `400 Bad Request`

---

### 4.6 TS-CL — Estado Climatizador

#### TS-CL-01: GET retorna valor actual

**Pasos:**
1. `GET /termostato/estado_climatizador/`

**Resultado esperado:**
- Status: `200 OK`
- Body: `{"estado_climatizador": "apagado"}`

#### TS-CL-02: POST acepta estado "encendido"

**Pasos:**
1. `POST /termostato/estado_climatizador/` con `{"climatizador": "encendido"}`

**Resultado esperado:**
- Status: `201 Created`
- `GET` posterior: `{"estado_climatizador": "encendido"}`

#### TS-CL-03: POST acepta estado "enfriando"

**Pasos:**
1. `POST /termostato/estado_climatizador/` con `{"climatizador": "enfriando"}`

**Resultado esperado:**
- Status: `201 Created`
- `GET` posterior: `{"estado_climatizador": "enfriando"}`

#### TS-CL-04: POST acepta estado "calentando"

**Pasos:**
1. `POST /termostato/estado_climatizador/` con `{"climatizador": "calentando"}`

**Resultado esperado:**
- Status: `201 Created`
- `GET` posterior: `{"estado_climatizador": "calentando"}`

#### TS-CL-05: POST normaliza a minúsculas

**Pasos:**
1. `POST /termostato/estado_climatizador/` con `{"climatizador": "ENCENDIDO"}`

**Resultado esperado:**
- Status: `201 Created`
- `GET` posterior: `{"estado_climatizador": "encendido"}`

#### TS-CL-06: POST normaliza eliminando espacios

**Pasos:**
1. `POST /termostato/estado_climatizador/` con `{"climatizador": "  apagado  "}`

**Resultado esperado:**
- Status: `201 Created`
- `GET` posterior: `{"estado_climatizador": "apagado"}`

#### TS-CL-07: POST rechaza estado inválido

**Pasos:**
1. `POST /termostato/estado_climatizador/` con `{"climatizador": "ventilando"}`

**Resultado esperado:**
- Status: `400 Bad Request`

#### TS-CL-08: POST rechaza estado vacío

**Pasos:**
1. `POST /termostato/estado_climatizador/` con `{"climatizador": ""}`

**Resultado esperado:**
- Status: `400 Bad Request`

---

### 4.7 TS-IN — Indicador de Batería

#### TS-IN-01: GET retorna indicador calculado (estado inicial NORMAL)

**Precondición:** Batería en 5.0 (valor inicial).
**Pasos:**
1. `GET /termostato/indicador/`

**Resultado esperado:**
- Status: `200 OK`
- Body: `{"indicador": "NORMAL"}`

#### TS-IN-02: Indicador cambia a BAJO al bajar batería

**Pasos:**
1. `POST /termostato/bateria/` con `{"bateria": 3.0}` (entre 2.5 y 3.5)
2. `GET /termostato/indicador/`

**Resultado esperado:**
- Body: `{"indicador": "BAJO"}`

#### TS-IN-03: Indicador cambia a CRITICO al bajar batería

**Pasos:**
1. `POST /termostato/bateria/` con `{"bateria": 1.0}` (menor que 2.5)
2. `GET /termostato/indicador/`

**Resultado esperado:**
- Body: `{"indicador": "CRITICO"}`

#### TS-IN-04: Indicador es NORMAL en umbral superior (>3.5)

**Pasos:**
1. `POST /termostato/bateria/` con `{"bateria": 3.6}`
2. `GET /termostato/indicador/`

**Resultado esperado:**
- Body: `{"indicador": "NORMAL"}`

#### TS-IN-05: Indicador es BAJO en umbral inferior (=2.5)

**Pasos:**
1. `POST /termostato/bateria/` con `{"bateria": 2.5}`
2. `GET /termostato/indicador/`

**Resultado esperado:**
- Body: `{"indicador": "BAJO"}`

#### TS-IN-06: POST en /indicador/ retorna Method Not Allowed

**Pasos:**
1. `POST /termostato/indicador/` con `{"indicador": "NORMAL"}`

**Resultado esperado:**
- Status: `405 Method Not Allowed`

---

### 4.8 TS-HI — Historial de Temperaturas

#### TS-HI-01: GET historial retorna estructura correcta

**Pasos:**
1. `GET /termostato/historial/`

**Resultado esperado:**
- Status: `200 OK`
- Body:
  ```json
  {
    "historial": [...],
    "total": <entero>
  }
  ```
- `historial` es una lista
- `total` es un entero no negativo

#### TS-HI-02: Cada registro del historial tiene la estructura correcta

**Pasos:**
1. `POST /termostato/temperatura_ambiente/` con `{"ambiente": 25}`
2. `GET /termostato/historial/`

**Resultado esperado:**
- Cada elemento de `historial` contiene:
  ```json
  {
    "temperatura": 25,
    "timestamp": "<ISO-8601>"
  }
  ```
- `timestamp` es un string con formato ISO-8601

#### TS-HI-03: Cambios de temperatura ambiente se registran en historial

**Pasos:**
1. Anotar `total` inicial = `GET /termostato/historial/` → `total`
2. `POST /termostato/temperatura_ambiente/` con `{"ambiente": 22}`
3. `POST /termostato/temperatura_ambiente/` con `{"ambiente": 28}`
4. `GET /termostato/historial/`

**Resultado esperado:**
- `total` es `total_inicial + 2`
- Los dos últimos registros tienen temperaturas `22` y `28` respectivamente

#### TS-HI-04: Otros cambios NO generan entrada en historial

**Pasos:**
1. Anotar `total` inicial = `GET /termostato/historial/` → `total`
2. `POST /termostato/temperatura_deseada/` con `{"deseada": 20}`
3. `POST /termostato/bateria/` con `{"bateria": 3.0}`
4. `POST /termostato/estado_climatizador/` con `{"climatizador": "encendido"}`
5. `GET /termostato/historial/`

**Resultado esperado:**
- `total` sigue siendo `total_inicial` (sin cambios)

#### TS-HI-05: Parámetro límite restringe registros retornados

**Precondición:** Al menos 5 registros en historial.
**Pasos:**
1. Registrar 5+ temperaturas distintas con POST
2. `GET /termostato/historial/?limite=3`

**Resultado esperado:**
- `historial` contiene exactamente 3 elementos
- `total` refleja el total real (no el limitado)

#### TS-HI-06: Historial sin parámetro límite retorna todos los registros

**Pasos:**
1. `GET /termostato/historial/`

**Resultado esperado:**
- `len(historial) == total`

---

### 4.9 TS-ERR — Manejo de Errores

#### TS-ERR-01: Ruta inexistente retorna 404

**Pasos:**
1. `GET /termostato/inexistente/`

**Resultado esperado:**
- Status: `404 Not Found`

#### TS-ERR-02: Formato de error es consistente

**Pasos:**
1. `POST /termostato/temperatura_ambiente/` con `{"ambiente": 99}` (fuera de rango)

**Resultado esperado:**
- Status: `400 Bad Request`
- Body:
  ```json
  {
    "error": {
      "codigo": 400,
      "mensaje": "<string no vacío>",
      "detalle": "<string no vacío>"
    }
  }
  ```

#### TS-ERR-03: POST sin body JSON retorna error apropiado

**Pasos:**
1. `POST /termostato/temperatura_ambiente/` sin body

**Resultado esperado:**
- Status: `400` o `415`

---

## 5. Flujos de Negocio End-to-End

Estos escenarios validan secuencias completas que simulan uso real del sistema.

### TS-F01 — Ciclo completo de actualización y lectura

**Objetivo:** Verificar que el estado persiste correctamente entre múltiples actualizaciones.

**Pasos:**
1. `POST /termostato/temperatura_ambiente/` → `{"ambiente": 18}`
2. `POST /termostato/temperatura_deseada/` → `{"deseada": 22}`
3. `POST /termostato/bateria/` → `{"bateria": 4.2}`
4. `POST /termostato/estado_climatizador/` → `{"climatizador": "calentando"}`
5. `GET /termostato/`

**Resultado esperado:**
```json
{
  "temperatura_ambiente": 18,
  "temperatura_deseada": 22,
  "carga_bateria": 4.2,
  "estado_climatizador": "calentando",
  "indicador": "NORMAL"
}
```

### TS-F02 — Degradación de batería y cambio de indicador

**Objetivo:** Verificar que el indicador refleja la degradación progresiva de batería.

**Pasos:**
1. `POST /termostato/bateria/` → `{"bateria": 5.0}`
2. `GET /termostato/indicador/` → esperar `"NORMAL"`
3. `POST /termostato/bateria/` → `{"bateria": 3.0}`
4. `GET /termostato/indicador/` → esperar `"BAJO"`
5. `POST /termostato/bateria/` → `{"bateria": 1.5}`
6. `GET /termostato/indicador/` → esperar `"CRITICO"`
7. `POST /termostato/bateria/` → `{"bateria": 4.0}`
8. `GET /termostato/indicador/` → esperar `"NORMAL"` (recuperación)

**Resultado esperado:** Indicador cambia en cada paso según los umbrales.

### TS-F03 — Historial refleja múltiples cambios de temperatura

**Objetivo:** Verificar integridad del historial ante múltiples cambios.

**Pasos:**
1. `GET /termostato/historial/` → anotar `total` inicial
2. Registrar 5 temperaturas: 15, 20, 25, 30, 35
3. `GET /termostato/historial/`

**Resultado esperado:**
- `total == total_inicial + 5`
- Las últimas 5 entradas tienen temperaturas `[15, 20, 25, 30, 35]` en ese orden
- Cada entrada tiene un `timestamp` válido en orden cronológico

### TS-F04 — Temperatura al límite del rango no modifica historial ante rechazo

**Objetivo:** Verificar que los rechazos no dejan rastros en el sistema.

**Pasos:**
1. `GET /termostato/temperatura_ambiente/` → anotar `valor_actual`
2. `GET /termostato/historial/` → anotar `total` inicial
3. `POST /termostato/temperatura_ambiente/` → `{"ambiente": 99}` (inválido)
4. `GET /termostato/temperatura_ambiente/`
5. `GET /termostato/historial/`

**Resultado esperado:**
- Paso 4: temperatura sigue siendo `valor_actual`
- Paso 5: `total` no cambia respecto al paso 2

### TS-F05 — Ciclo de encendido del climatizador

**Objetivo:** Simular transiciones de estado del climatizador.

**Pasos:**
1. `POST /termostato/estado_climatizador/` → `{"climatizador": "apagado"}`
2. `GET /termostato/estado_climatizador/` → esperar `"apagado"`
3. `POST /termostato/estado_climatizador/` → `{"climatizador": "encendido"}`
4. `GET /termostato/estado_climatizador/` → esperar `"encendido"`
5. `POST /termostato/estado_climatizador/` → `{"climatizador": "calentando"}`
6. `GET /termostato/estado_climatizador/` → esperar `"calentando"`
7. `POST /termostato/estado_climatizador/` → `{"climatizador": "apagado"}`
8. `GET /termostato/estado_climatizador/` → esperar `"apagado"`

**Resultado esperado:** Cada transición es aceptada y reflejada.

---

## 6. Casos de Borde

### TS-BE-01: Valores exactamente en los umbrales del indicador

| Batería | Indicador esperado | Descripción |
|---------|-------------------|-------------|
| 3.5 | BAJO o NORMAL | En el umbral exacto (verificar comportamiento) |
| 2.5 | BAJO o CRITICO | En el umbral exacto (verificar comportamiento) |
| 3.51 | NORMAL | Por encima del umbral NORMAL |
| 2.49 | CRITICO | Por debajo del umbral BAJO |

> **Nota:** Documentar el comportamiento exacto en los umbrales (inclusive vs exclusivo) como parte de la ejecución.

### TS-BE-02: Caracteres especiales en estado climatizador

**Pasos:**
1. `POST /termostato/estado_climatizador/` → `{"climatizador": "apagado\n"}`
2. `POST /termostato/estado_climatizador/` → `{"climatizador": "apagado\t"}`

**Resultado esperado:** `201` o `400` — documentar comportamiento.

### TS-BE-03: Batería con muchos decimales

**Pasos:**
1. `POST /termostato/bateria/` → `{"bateria": 3.999999}`

**Resultado esperado:**
- `GET` posterior: `{"carga_bateria": 4.0}` (redondeado)

### TS-BE-04: Temperatura como valor booleano (JSON)

**Pasos:**
1. `POST /termostato/temperatura_ambiente/` → `{"ambiente": true}`

**Resultado esperado:**
- `400 Bad Request` o `201` con conversión a `1` — documentar comportamiento.

### TS-BE-05: Valores negativos en batería

**Pasos:**
1. `POST /termostato/bateria/` → `{"bateria": -0.01}`

**Resultado esperado:**
- Status: `400 Bad Request`

---

## 7. Matriz de Cobertura

| Área | Casos | Happy Path | Límites | Errores | Flujos |
|------|-------|-----------|---------|---------|--------|
| Health Check | TS-HC-01/02 | ✓ | — | — | — |
| Estado completo | TS-EST-01/02 | ✓ | — | — | ✓ |
| Temperatura ambiente | TS-TA-01 a 11 | ✓ | ✓ | ✓ | ✓ |
| Temperatura deseada | TS-TD-01 a 06 | ✓ | ✓ | ✓ | — |
| Batería | TS-BA-01 a 08 | ✓ | ✓ | ✓ | ✓ |
| Climatizador | TS-CL-01 a 08 | ✓ | — | ✓ | ✓ |
| Indicador | TS-IN-01 a 06 | ✓ | ✓ | ✓ | ✓ |
| Historial | TS-HI-01 a 06 | ✓ | ✓ | — | ✓ |
| Errores generales | TS-ERR-01 a 03 | — | — | ✓ | — |
| Flujos E2E | TS-F01 a 05 | — | — | — | ✓ |
| Casos de borde | TS-BE-01 a 05 | — | ✓ | ✓ | — |

**Total de casos: 54**

---

## 8. Criterios de Aceptación del Plan

El sistema se considera **aprobado** si:

| Criterio | Umbral |
|----------|--------|
| Casos TS-HC pasados | 100% (2/2) |
| Casos Happy Path pasados | 100% |
| Casos de validación de errores pasados | >= 90% |
| Flujos E2E pasados | 100% (5/5) |
| Casos de borde documentados | 100% (aunque fallen, documentar comportamiento) |
| Ningún endpoint retorna 500 en uso normal | Obligatorio |

---

## 9. Ejecución Manual con curl

Para referencia rápida durante ejecución manual:

```bash
BASE=http://localhost:5050

# Health check
curl -s $BASE/comprueba/ | python -m json.tool

# Estado completo
curl -s $BASE/termostato/ | python -m json.tool

# POST temperatura ambiente
curl -s -X POST $BASE/termostato/temperatura_ambiente/ \
  -H "Content-Type: application/json" \
  -d '{"ambiente": 25}' | python -m json.tool

# POST batería
curl -s -X POST $BASE/termostato/bateria/ \
  -H "Content-Type: application/json" \
  -d '{"bateria": 2.0}' | python -m json.tool

# GET indicador (después de bajar batería)
curl -s $BASE/termostato/indicador/ | python -m json.tool

# GET historial con límite
curl -s "$BASE/termostato/historial/?limite=5" | python -m json.tool
```

---

## 10. Referencias

- Endpoints: `app/servicios/api.py`
- Reglas de validación: `app/general/validators.py`
- Lógica de indicador: `app/general/calculadores.py`
- Rangos configurables: `app/configuracion/config.py`
- Tests de integración existentes: `tests/test_api.py`
- Análisis de diseño: `docs/analisis/2026-02-06_analisis_diseno.md`
