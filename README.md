# App Termostato - API REST

API REST Flask para gestión de un termostato. Actúa como backend proveyendo datos al frontend `webapp_termostato`.

## Descripción

Este proyecto es parte de un caso de estudio académico/didáctico que demuestra la arquitectura cliente-servidor con separación de frontend y backend.

La API gestiona:
- Temperatura ambiente actual
- Temperatura deseada configurada
- Estado del climatizador (encendido/apagado)
- La carga de la batería
- Indicador de carga del dispositivo

## Arquitectura

```
┌─────────────────────┐         ┌─────────────────────┐
│  webapp_termostato  │  HTTP   │   app_termostato    │
│     (Frontend)      │ ──────► │     (Backend)       │
│     Puerto 5001     │  REST   │     Puerto 5050     │
└─────────────────────┘         └─────────────────────┘
```

## Requisitos

- Python 3.8+
- Flask

## Instalación

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd app_termostato
```

2. Crear entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install flask
```

## Configuración

La aplicación usa variables de entorno para configuración:

| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| `PORT` | Puerto del servidor | `5050` |
| `DEBUG` | Modo debug | `True` |

Ejemplo de configuración:
```bash
export PORT=5050
export DEBUG=True
```

## Ejecución

```bash
python app.py
```

El servidor estará disponible en: http://localhost:5050

## Estructura del Proyecto

```
app_termostato/
├── app.py                   # Punto de entrada
├── servicios/
│   ├── __init__.py
│   └── api.py               # Definición de endpoints REST
├── general/
│   ├── __init__.py
│   ├── termostato.py        # Modelo de datos del termostato
│   └── configurador.py      # Configuración (instancia singleton)
├── PLAN_MEJORAS.md          # Plan de mejoras del proyecto
└── README.md                # Este archivo
```

## API Endpoints

### Health Check

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/comprueba/` | Verifica que el servidor responde |

**Respuesta:**
```
OK!
```

### Temperatura Ambiente

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/termostato/temperatura_ambiente/` | Obtiene temperatura ambiente |
| POST | `/termostato/temperatura_ambiente/` | Establece temperatura ambiente |

**GET Response:**
```json
{"temperatura_ambiente": 20}
```

**POST Request:**
```json
{"ambiente": 25}
```

### Temperatura Deseada

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/termostato/temperatura_deseada/` | Obtiene temperatura deseada |
| POST | `/termostato/temperatura_deseada/` | Establece temperatura deseada |

**GET Response:**
```json
{"temperatura_deseada": 30}
```

**POST Request:**
```json
{"deseada": 22}
```

### Batería

| Método | Endpoint | Descripción                |
|--------|----------|----------------------------|
| GET | `/termostato/bateria/` | Obtiene carga de batería   |
| POST | `/termostato/bateria/` | Establece carga de batería |

**GET Response:**
```json
{"carga_bateria": 5.0}
```

**POST Request:**
```json
{"bateria": 80}
```

### Estado Climatizador

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/termostato/estado_climatizador/` | Obtiene estado del climatizador |
| POST | `/termostato/estado_climatizador/` | Establece estado del climatizador |

**GET Response:**
```json
{"estado_climatizador": "apagado"}
```

**POST Request:**
```json
{"climatizador": "calentando"}
```

### Indicador de Carga

| Método | Endpoint                 | Descripción                                  |
|--------|--------------------------|----------------------------------------------|
| GET | `/termostato/indicador/` | Obtiene indicador de carga del dispositivo   |
| POST | `/termostato/indicador/` | Establece indicador de carga del dispositivo |

**GET Response:**
```json
{"indicador": "NORMAL"}
```

**POST Request:**
```json
{"indicador": "BAJA"}
```

## Códigos de Respuesta

| Código | Descripción |
|--------|-------------|
| 200 | OK - Petición exitosa |
| 201 | Created - Dato registrado correctamente |
| 400 | Bad Request - Falta campo requerido en JSON |
| 404 | Not Found - Endpoint no encontrado |
| 500 | Internal Server Error - Error del servidor |

## Ejemplos con cURL

```bash
# Health check
curl http://localhost:5050/comprueba/

# Obtener temperatura ambiente
curl http://localhost:5050/termostato/temperatura_ambiente/

# Establecer temperatura ambiente
curl -X POST http://localhost:5050/termostato/temperatura_ambiente/ \
  -H "Content-Type: application/json" \
  -d '{"ambiente": 25}'

# Obtener estado climatizador
curl http://localhost:5050/termostato/estado_climatizador/

# Encender climatizador
curl -X POST http://localhost:5050/termostato/estado_climatizador/ \
  -H "Content-Type: application/json" \
  -d '{"climatizador": "encendido"}'

# Obtener indicador de carga
curl http://localhost:5050/termostato/indicador/

# Establecer indicador de carga
curl -X POST http://localhost:5050/termostato/indicador/ \
  -H "Content-Type: application/json" \
  -d '{"indicador": "BAJA"}'
```

## Proyecto Relacionado

Este backend es consumido por:
- **webapp_termostato**: Frontend web que muestra los datos del termostato

## Licencia

Proyecto académico/didáctico para el curso ISSE.
