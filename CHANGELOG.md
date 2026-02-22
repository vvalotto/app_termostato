# Changelog

Todos los cambios notables de este proyecto se documentan en este archivo.

El formato esta basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

## [1.3.0] - 2026-02-22

### Agregado
- **Suite de testing de sistema** (64 tests automatizados con `requests` contra servidor real)
  - Cobertura: happy path, límites, errores, flujos E2E y casos de borde
  - Marker pytest `sistema` para ejecución selectiva
  - Plan de testing documentado en `docs/testing/plan_testing_sistema.md`
- **Strategy Pattern** para cálculo de indicador de batería (HU-007)
  - `IndicadorCalculatorTresNiveles` — estrategia por defecto (NORMAL/BAJO/CRITICO)
  - `IndicadorCalculatorCincoNiveles` — estrategia extendida (EXCELENTE/BUENO/NORMAL/BAJO/CRITICO)
  - Inyectable via constructor de `Termostato` o `TermostatoFactory`

### Modificado
- **Refactoring arquitectónico completo** — épica de deuda técnica cerrada (7/8 HUs)
  - **HU-001**: God Object `Termostato` descompuesto en `TermostatoModelo`, `TermostatoValidator`, `TermostatoService` y `Termostato` (Facade)
  - **HU-002**: Singleton `Configurador` reemplazado por `TermostatoFactory` (Factory Method)
  - **HU-003**: Duplicación de endpoints eliminada mediante decorador `@endpoint_termostato`
  - **HU-004**: Validación de `estado_climatizador` extraída a `TermostatoValidator`
  - **HU-005**: Imports y estructura de módulos reorganizada (`app/configuracion/`, `app/datos/`)
  - **HU-006**: Configuración Swagger extraída a `swagger_config.py`
- **Application Factory Pattern** en `api.py` — `create_app()` con inyección de dependencias
- Quality Gates post-refactoring: CC=1.69, MI=90.15, Pylint=8.89 (Grado A)

### Corregido
- **Bug**: `GET /termostato/historial/` siempre retornaba vacío — dos instancias separadas de
  `HistorialRepositorioMemoria` entre el termostato y el endpoint; ahora comparten la misma instancia

### Descartado
- **HU-008**: DI Container — over-engineering, Application Factory Pattern es suficiente (ver ADR-002)

## [1.2.0] - 2025-12-27

### Agregado
- **TER-19**: Indicador de bateria calculado automaticamente segun nivel de carga
  - `> 3.5` = NORMAL
  - `>= 2.5 y <= 3.5` = BAJO
  - `< 2.5` = CRITICO
- Variables de entorno para configurar umbrales del indicador:
  - `INDICADOR_UMBRAL_NORMAL` (default: 3.5)
  - `INDICADOR_UMBRAL_BAJO` (default: 2.5)
- Tests unitarios para calculo dinamico del indicador (4 tests nuevos)
- Test de integracion para verificar indicador via API

### Modificado
- Endpoint `GET /termostato/indicador/` ahora devuelve valor calculado
- Property `indicador` en modelo `Termostato` ahora es solo lectura
- Mejorado score Pylint del modelo termostato (9.05/10)

### Eliminado
- Endpoint `POST /termostato/indicador/` (indicador ya no es configurable manualmente)
- Atributo `_indicador` del modelo (ahora se calcula dinamicamente)

## [1.1.0] - 2025-12-21

### Agregado
- **TER-14**: Documentacion interactiva OpenAPI/Swagger en `/docs/`
- **TER-13**: Tests de integracion de API (27 tests)
- **TER-12**: Tests unitarios del modelo Termostato (33 tests, 100% cobertura)
- **TER-16**: Health check mejorado con uptime, version y timestamp
- **TER-15**: Configuracion completa por variables de entorno
- **TER-07**: Persistencia de estado en archivo JSON
- Historial de temperaturas con endpoint `/termostato/historial/`
- Ambiente de calidad con metricas CC, MI, Pylint
- Soporte para despliegue en Google Cloud Run

### Modificado
- Refactorizacion de estructura de proyecto
- Mejora en manejo de errores con respuestas JSON estandarizadas

### Corregido
- Import circular entre modulos

## [1.0.0] - 2025-12-01

### Agregado
- Version inicial de la API REST
- Endpoints basicos del termostato:
  - `/termostato/temperatura_ambiente/`
  - `/termostato/temperatura_deseada/`
  - `/termostato/bateria/`
  - `/termostato/estado_climatizador/`
  - `/termostato/indicador/`
- Modelo de datos `Termostato` con validacion de rangos
- Health check en `/comprueba/`
- Configuracion CORS para frontend
