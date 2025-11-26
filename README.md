# App Termostato - API REST

API REST Flask para gestión de un termostato. Actúa como backend proveyendo datos al frontend `webapp_termostato`.

## Descripción

Este proyecto es parte de un caso de estudio académico/didáctico que demuestra la arquitectura cliente-servidor con separación de frontend y backend.

La API gestiona:
- Temperatura ambiente actual
- Temperatura deseada configurada
- Estado del climatizador (encendido/apagado)
- Nivel de carga de la batería
- Nivel de carga del dispositivo

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

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/termostato/bateria/` | Obtiene nivel de batería |
| POST | `/termostato/bateria/` | Establece nivel de batería |

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

### Nivel de Carga

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/termostato/nivel_de_carga/` | Obtiene nivel de carga del dispositivo |
| POST | `/termostato/nivel_de_carga/` | Establece nivel de carga del dispositivo |

**GET Response:**
```json
{"nivel_de_carga": "normal"}
```

**POST Request:**
```json
{"nivel_de_carga": "bajo"}
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

# Obtener nivel de carga
curl http://localhost:5050/termostato/nivel_de_carga/

# Establecer nivel de carga
curl -X POST http://localhost:5050/termostato/nivel_de_carga/ \
  -H "Content-Type: application/json" \
  -d '{"nivel_de_carga": "bajo"}'
```

## Proyecto Relacionado

Este backend es consumido por:
- **webapp_termostato**: Frontend web que muestra los datos del termostato

## Licencia

Proyecto académico/didáctico para el curso ISSE.
