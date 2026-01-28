# Historias de Usuario - app_termostato

## Sitio del proyecto en Jira:
App_Termostato: https://vvalotto-1760995393359.atlassian.net/jira/software/projects/TER/summary


## Resumen del Backlog

| ID | Título | Tipo | Prioridad | Story Points |
|----|--------|------|-----------|--------------|
| TRM-001 | Validación de rangos de temperatura | Funcional | Alta | 2 |
| TRM-002 | Validación de rango de batería | Funcional | Alta | 1 |
| TRM-003 | Endpoint GET unificado del termostato | Funcional | Alta | 2 |
| TRM-004 | Endpoint POST unificado del termostato | Funcional | Media | 3 |
| TRM-005 | Lógica automática del climatizador | Funcional | Media | 3 |
| TRM-006 | Historial de temperaturas | Funcional | Baja | 5 |
| TRM-007 | Persistencia en archivo JSON | Funcional | Baja | 5 |
| TRM-008 | Simulación de consumo de batería | Funcional | Baja | 3 |
| TRM-009 | Sistema de logging | No Funcional | Alta | 2 |
| TRM-010 | Manejo de errores estandarizado | No Funcional | Alta | 2 |
| TRM-011 | Habilitar CORS | No Funcional | Alta | 1 |
| TRM-012 | Tests unitarios del modelo | No Funcional | Media | 3 |
| TRM-013 | Tests de integración de API | No Funcional | Media | 5 |
| TRM-014 | Documentación OpenAPI/Swagger | No Funcional | Baja | 3 |
| TRM-015 | Configuración por variables de entorno | No Funcional | Baja | 2 |
| TRM-016 | Health check mejorado | No Funcional | Baja | 1 |

---

## Historias de Usuario - Funcionales

### TRM-001: Validación de rangos de temperatura

**Tipo:** Funcional
**Prioridad:** Alta
**Story Points:** 2
**Componente:** general/termostato.py

#### Descripción
**Como** usuario del termostato
**Quiero** que el sistema valide los rangos de temperatura ingresados
**Para** evitar configuraciones inválidas que no correspondan a valores reales

#### Criterios de Aceptación
- [ ] La `temperatura_ambiente` solo acepta valores entre 0°C y 50°C
- [ ] La `temperatura_deseada` solo acepta valores entre 15°C y 30°C
- [ ] Si se ingresa un valor fuera de rango, el sistema retorna error 400 con mensaje descriptivo
- [ ] Los valores límite (0, 50, 15, 30) son aceptados correctamente
- [ ] El mensaje de error indica el rango válido esperado

#### Notas Técnicas
- Implementar validación en los setters de la clase `Termostato`
- Lanzar excepción `ValueError` con mensaje descriptivo
- Capturar excepción en `api.py` y retornar respuesta HTTP 400

---

### TRM-002: Validación de rango de batería

**Tipo:** Funcional
**Prioridad:** Alta
**Story Points:** 1
**Componente:** general/termostato.py

#### Descripción
**Como** usuario del termostato
**Quiero** que el nivel de batería esté limitado entre 0% y 100%
**Para** que los valores reflejen un porcentaje real de carga

#### Criterios de Aceptación
- [ ] La `carga_bateria` solo acepta valores entre 0.0 y 100.0
- [ ] Si se ingresa un valor fuera de rango, el sistema retorna error 400
- [ ] Los valores límite (0.0, 100.0) son aceptados correctamente
- [ ] El valor se sigue redondeando a 2 decimales

#### Notas Técnicas
- Implementar validación en el setter de `carga_bateria`
- Mantener el redondeo existente a 2 decimales

---

### TRM-003: Endpoint GET unificado del termostato

**Tipo:** Funcional
**Prioridad:** Alta
**Story Points:** 2
**Componente:** servicios/api.py

#### Descripción
**Como** desarrollador del frontend
**Quiero** obtener todo el estado del termostato en una sola llamada
**Para** reducir la cantidad de requests necesarios y simplificar la integración

#### Criterios de Aceptación
- [ ] Existe endpoint `GET /termostato/` que retorna todas las propiedades
- [ ] La respuesta incluye: temperatura_ambiente, temperatura_deseada, carga_bateria, estado_climatizador, indicador
- [ ] El formato de respuesta es JSON
- [ ] El código de respuesta es 200 OK
- [ ] Los endpoints individuales siguen funcionando

#### Ejemplo de Respuesta
```json
{
  "temperatura_ambiente": 20,
  "temperatura_deseada": 24,
  "carga_bateria": 85.50,
  "estado_climatizador": "apagado",
  "indicador": "NORMAL"
}
```

---

### TRM-004: Endpoint POST unificado del termostato

**Tipo:** Funcional
**Prioridad:** Media
**Story Points:** 3
**Componente:** servicios/api.py

#### Descripción
**Como** desarrollador del frontend
**Quiero** actualizar múltiples propiedades del termostato en una sola llamada
**Para** optimizar la comunicación y mantener consistencia en las actualizaciones

#### Criterios de Aceptación
- [ ] Existe endpoint `POST /termostato/` que acepta actualización parcial o total
- [ ] Solo se actualizan las propiedades enviadas en el JSON
- [ ] Las propiedades no enviadas mantienen su valor actual
- [ ] Se validan todas las propiedades antes de aplicar cambios
- [ ] Si hay error en una propiedad, no se actualiza ninguna (transaccional)
- [ ] El código de respuesta es 200 OK con el estado actualizado

#### Ejemplo de Request
```json
{
  "temperatura_deseada": 22,
  "estado_climatizador": "calentando"
}
```

---

### TRM-005: Lógica automática del climatizador

**Tipo:** Funcional
**Prioridad:** Media
**Story Points:** 3
**Componente:** general/termostato.py

#### Descripción
**Como** usuario del termostato
**Quiero** que el estado del climatizador se calcule automáticamente
**Para** que refleje el comportamiento real de un termostato inteligente

#### Criterios de Aceptación
- [ ] Si `temperatura_ambiente` < `temperatura_deseada` - 1°C, estado = "calentando"
- [ ] Si `temperatura_ambiente` > `temperatura_deseada` + 1°C, estado = "enfriando"
- [ ] Si la diferencia es <= 1°C, estado = "apagado" (histéresis)
- [ ] El estado se recalcula automáticamente al cambiar cualquier temperatura
- [ ] Existe opción para forzar el estado manualmente (override)

#### Notas Técnicas
- Implementar método `_calcular_estado_climatizador()` en clase Termostato
- Llamar al método en los setters de temperatura
- Agregar flag `modo_manual` para permitir override

---

### TRM-006: Historial de temperaturas

**Tipo:** Funcional
**Prioridad:** Baja
**Story Points:** 5
**Componente:** general/termostato.py, servicios/api.py

#### Descripción
**Como** usuario del termostato
**Quiero** consultar el historial de temperaturas registradas
**Para** analizar la evolución térmica del ambiente

#### Criterios de Aceptación
- [ ] El sistema almacena las últimas 100 lecturas de temperatura_ambiente
- [ ] Cada registro incluye: temperatura, timestamp (ISO 8601)
- [ ] Existe endpoint `GET /termostato/historial/` para consultar el historial
- [ ] Se puede limitar la cantidad de registros con parámetro `?limite=N`
- [ ] El historial se ordena del más reciente al más antiguo

#### Ejemplo de Respuesta
```json
{
  "historial": [
    {"temperatura": 22, "timestamp": "2025-01-15T10:30:00Z"},
    {"temperatura": 21, "timestamp": "2025-01-15T10:25:00Z"}
  ],
  "total": 2
}
```

---

### TRM-007: Persistencia en archivo JSON

**Tipo:** Funcional
**Prioridad:** Baja
**Story Points:** 5
**Componente:** general/termostato.py, general/configurador.py

#### Descripción
**Como** administrador del sistema
**Quiero** que el estado del termostato se guarde en disco
**Para** que sobreviva a reinicios del servidor

#### Criterios de Aceptación
- [ ] El estado se guarda automáticamente en `data/termostato_estado.json`
- [ ] Al iniciar, el sistema carga el estado desde el archivo si existe
- [ ] Si no existe archivo, se usan valores por defecto
- [ ] El guardado ocurre después de cada modificación
- [ ] El archivo JSON es legible y editable manualmente

#### Notas Técnicas
- Crear directorio `data/` si no existe
- Agregar `data/` al `.gitignore`
- Implementar métodos `guardar()` y `cargar()` en Termostato

---

### TRM-008: Simulación de consumo de batería

**Tipo:** Funcional
**Prioridad:** Baja
**Story Points:** 3
**Componente:** general/termostato.py

#### Descripción
**Como** usuario del termostato
**Quiero** que la batería disminuya cuando el climatizador está activo
**Para** simular un comportamiento más realista del dispositivo

#### Criterios de Aceptación
- [ ] La batería disminuye 0.1% por cada consulta cuando climatizador != "apagado"
- [ ] La batería no baja de 0%
- [ ] Cuando batería < 10%, el indicador cambia a "BATERIA_BAJA"
- [ ] Cuando batería < 5%, el climatizador se apaga automáticamente
- [ ] Existe endpoint para "cargar" la batería (simular recarga)

---

## Historias de Usuario - No Funcionales

### TRM-009: Sistema de logging

**Tipo:** No Funcional
**Prioridad:** Alta
**Story Points:** 2
**Componente:** servicios/api.py, general/termostato.py

#### Descripción
**Como** desarrollador
**Quiero** que el sistema registre logs de las operaciones
**Para** facilitar el debugging y monitoreo de la aplicación

#### Criterios de Aceptación
- [ ] Se utiliza el módulo `logging` de Python
- [ ] Logs nivel INFO para operaciones exitosas (GET, POST)
- [ ] Logs nivel WARNING para validaciones fallidas
- [ ] Logs nivel ERROR para excepciones no controladas
- [ ] El formato incluye: timestamp, nivel, mensaje
- [ ] Los logs se muestran en consola (stdout)

#### Ejemplo de Log
```
2025-01-15 10:30:00 INFO - GET /termostato/temperatura_ambiente/ -> 200
2025-01-15 10:30:05 WARNING - POST /termostato/bateria/ - Valor fuera de rango: 150
2025-01-15 10:30:10 ERROR - Error interno: [detalle]
```

---

### TRM-010: Manejo de errores estandarizado

**Tipo:** No Funcional
**Prioridad:** Alta
**Story Points:** 2
**Componente:** servicios/api.py

#### Descripción
**Como** desarrollador del frontend
**Quiero** respuestas de error consistentes y descriptivas
**Para** manejar errores de forma uniforme en el cliente

#### Criterios de Aceptación
- [ ] Todas las respuestas de error siguen el mismo formato JSON
- [ ] El formato incluye: codigo, mensaje, detalle (opcional)
- [ ] Error 400: incluye qué campo falló y por qué
- [ ] Error 404: incluye la ruta solicitada
- [ ] Error 500: incluye mensaje genérico (sin exponer detalles internos)

#### Formato de Error Estándar
```json
{
  "error": {
    "codigo": 400,
    "mensaje": "Valor fuera de rango",
    "detalle": "temperatura_deseada debe estar entre 15 y 30"
  }
}
```

---

### TRM-011: Habilitar CORS

**Tipo:** No Funcional
**Prioridad:** Alta
**Story Points:** 1
**Componente:** servicios/api.py

#### Descripción
**Como** desarrollador del frontend
**Quiero** que la API permita requests desde otros orígenes
**Para** poder consumir la API desde webapp_termostato en otro puerto

#### Criterios de Aceptación
- [ ] Se instala y configura `flask-cors`
- [ ] Se permiten requests desde cualquier origen (desarrollo)
- [ ] Los métodos GET, POST, OPTIONS están habilitados
- [ ] Las cabeceras Content-Type y Accept están permitidas

#### Notas Técnicas
- Agregar `flask-cors` a requirements.txt
- Configurar con `CORS(app_api)`

---

### TRM-012: Tests unitarios del modelo

**Tipo:** No Funcional
**Prioridad:** Media
**Story Points:** 3
**Componente:** tests/

#### Descripción
**Como** desarrollador
**Quiero** tests unitarios para la clase Termostato
**Para** asegurar que la lógica de negocio funciona correctamente

#### Criterios de Aceptación
- [ ] Existe directorio `tests/` con archivo `test_termostato.py`
- [ ] Se utiliza pytest como framework de testing
- [ ] Cobertura mínima de la clase Termostato: 80%
- [ ] Tests para cada property (get y set)
- [ ] Tests para valores límite
- [ ] Tests para valores inválidos (esperan excepción)

#### Casos de Test Requeridos
- test_temperatura_ambiente_default
- test_temperatura_ambiente_set_valido
- test_temperatura_ambiente_set_invalido
- test_temperatura_deseada_rango
- test_carga_bateria_redondeo
- test_estado_climatizador_valores

---

### TRM-013: Tests de integración de API

**Tipo:** No Funcional
**Prioridad:** Media
**Story Points:** 5
**Componente:** tests/

#### Descripción
**Como** desarrollador
**Quiero** tests de integración para los endpoints de la API
**Para** verificar que la comunicación HTTP funciona correctamente

#### Criterios de Aceptación
- [ ] Existe archivo `tests/test_api.py`
- [ ] Se utiliza el cliente de pruebas de Flask
- [ ] Tests para cada endpoint (GET y POST)
- [ ] Tests de respuestas exitosas (200, 201)
- [ ] Tests de respuestas de error (400, 404)
- [ ] Tests de formato JSON correcto

#### Casos de Test Requeridos
- test_comprueba_endpoint
- test_get_temperatura_ambiente
- test_post_temperatura_ambiente_valido
- test_post_temperatura_ambiente_sin_json
- test_endpoint_no_existente_404

---

### TRM-014: Documentación OpenAPI/Swagger

**Tipo:** No Funcional
**Prioridad:** Baja
**Story Points:** 3
**Componente:** servicios/api.py

#### Descripción
**Como** desarrollador del frontend
**Quiero** documentación interactiva de la API
**Para** entender y probar los endpoints disponibles

#### Criterios de Aceptación
- [ ] Se instala `flask-swagger-ui` o `flasgger`
- [ ] Existe endpoint `/docs/` con interfaz Swagger UI
- [ ] Cada endpoint está documentado con descripción, parámetros y respuestas
- [ ] Se pueden probar los endpoints desde la interfaz
- [ ] La especificación OpenAPI está disponible en `/swagger.json`

---

### TRM-015: Configuración por variables de entorno

**Tipo:** No Funcional
**Prioridad:** Baja
**Story Points:** 2
**Componente:** general/configurador.py, app.py

#### Descripción
**Como** administrador del sistema
**Quiero** configurar valores iniciales mediante variables de entorno
**Para** personalizar el comportamiento sin modificar código

#### Criterios de Aceptación
- [ ] Se crea archivo `.env.example` con variables disponibles
- [ ] Variables soportadas: TEMP_AMBIENTE_INICIAL, TEMP_DESEADA_INICIAL, BATERIA_INICIAL
- [ ] Si no se definen, se usan valores por defecto actuales
- [ ] Se utiliza `python-dotenv` para cargar variables
- [ ] El README documenta las variables disponibles

#### Variables de Entorno
```
PORT=5050
DEBUG=true
TEMP_AMBIENTE_INICIAL=20
TEMP_DESEADA_INICIAL=24
BATERIA_INICIAL=100
```

---

### TRM-016: Health check mejorado

**Tipo:** No Funcional
**Prioridad:** Baja
**Story Points:** 1
**Componente:** servicios/api.py

#### Descripción
**Como** administrador del sistema
**Quiero** un health check más completo
**Para** monitorear el estado de la aplicación

#### Criterios de Aceptación
- [ ] El endpoint `/comprueba/` retorna información ampliada
- [ ] Incluye: version, status, uptime, timestamp
- [ ] El uptime se calcula desde el inicio del servidor
- [ ] El timestamp está en formato ISO 8601

#### Ejemplo de Respuesta
```json
{
  "status": "ok",
  "version": "1.0.0",
  "uptime_seconds": 3600,
  "timestamp": "2025-01-15T10:30:00Z"
}
```

---

## Definición de Prioridades

- **Alta:** Mejoras esenciales para una aplicación funcional y mantenible
- **Media:** Mejoras importantes que agregan valor significativo
- **Baja:** Mejoras deseables pero no críticas

## Story Points (Escala Fibonacci)

- **1:** Tarea trivial (< 1 hora)
- **2:** Tarea simple (1-2 horas)
- **3:** Tarea moderada (2-4 horas)
- **5:** Tarea compleja (4-8 horas)
