# Plan de Implementacion TRM-015: Configuracion por variables de entorno

**Historia:** TRM-015
**Branch:** TRM-015 (a crear o ya creado)
**Fecha:** 2025-12-20

---

## Arquitectura

```
app/
├── configuracion/             # [NUEVA CARPETA]
│   ├── __init__.py
│   ├── config.py              # [NUEVO] Variables de entorno
│   └── configurador.py        # [MOVIDO desde general/]
├── general/
│   └── termostato.py          # [MODIFICAR] Usar Config para validacion
├── datos/
│   └── ...
├── servicios/
│   └── api.py                 # [MODIFICAR] Actualizar imports
run.py                         # [MODIFICAR] Cargar dotenv
requirements.txt               # [MODIFICAR] Agregar python-dotenv
.env.example                   # [NUEVO] Plantilla de variables
```

---

## Tareas Secuenciales

### Fase 1: Preparar dependencias

#### Tarea 1.1: Agregar python-dotenv a requirements.txt
- [ ] Agregar `python-dotenv` al archivo requirements.txt

```
python-dotenv==1.0.0
```

#### Tarea 1.2: Crear archivo .env.example
- [ ] Crear plantilla con todas las variables disponibles
- [ ] Documentar cada seccion con comentarios

```env
# ===========================================
# Configuracion del Servidor
# ===========================================
PORT=5050
DEBUG=true

# ===========================================
# Valores Iniciales del Termostato
# ===========================================
# Estos valores se usan solo si no hay estado persistido
TEMP_AMBIENTE_INICIAL=20
TEMP_DESEADA_INICIAL=24
BATERIA_INICIAL=5.0

# ===========================================
# Rangos de Validacion
# ===========================================
# Temperatura ambiente (grados Celsius)
TEMP_AMBIENTE_MIN=0
TEMP_AMBIENTE_MAX=50

# Temperatura deseada (grados Celsius)
TEMP_DESEADA_MIN=15
TEMP_DESEADA_MAX=30

# Carga de bateria
BATERIA_MIN=0.0
BATERIA_MAX=5.0
```

---

### Fase 2: Crear carpeta configuracion

#### Tarea 2.1: Crear estructura de carpeta
- [ ] Crear directorio `app/configuracion/`
- [ ] Crear archivo `app/configuracion/__init__.py`

#### Tarea 2.2: Implementar config.py
- [ ] Crear clase `Config` con todas las variables de entorno
- [ ] Usar `os.getenv()` con valores por defecto

```python
"""
Configuracion centralizada del sistema.
Carga valores desde variables de entorno.
"""
import os


class Config:
    """Configuracion del sistema cargada desde variables de entorno."""

    # Servidor
    PORT = int(os.getenv('PORT', 5050))
    DEBUG = os.getenv('DEBUG', 'true').lower() == 'true'

    # Valores iniciales del termostato
    TEMP_AMBIENTE_INICIAL = int(os.getenv('TEMP_AMBIENTE_INICIAL', 20))
    TEMP_DESEADA_INICIAL = int(os.getenv('TEMP_DESEADA_INICIAL', 24))
    BATERIA_INICIAL = float(os.getenv('BATERIA_INICIAL', 5.0))

    # Rangos de validacion - Temperatura ambiente
    TEMP_AMBIENTE_MIN = int(os.getenv('TEMP_AMBIENTE_MIN', 0))
    TEMP_AMBIENTE_MAX = int(os.getenv('TEMP_AMBIENTE_MAX', 50))

    # Rangos de validacion - Temperatura deseada
    TEMP_DESEADA_MIN = int(os.getenv('TEMP_DESEADA_MIN', 15))
    TEMP_DESEADA_MAX = int(os.getenv('TEMP_DESEADA_MAX', 30))

    # Rangos de validacion - Bateria
    BATERIA_MIN = float(os.getenv('BATERIA_MIN', 0.0))
    BATERIA_MAX = float(os.getenv('BATERIA_MAX', 5.0))
```

#### Tarea 2.3: Mover configurador.py a configuracion/
- [ ] Mover `app/general/configurador.py` a `app/configuracion/configurador.py`
- [ ] Actualizar imports internos del archivo
- [ ] Usar Config para valores iniciales

```python
"""
Configuración global de la aplicación.
Provee una instancia compartida del termostato (patrón Singleton).
"""
from app.general.termostato import Termostato
from app.datos import (
    HistorialRepositorioMemoria,
    HistorialMapper,
    TermostatoPersistidorJSON
)
from app.configuracion.config import Config


class Configurador:
    """
    Clase de configuración que mantiene la instancia global del termostato.
    """
    historial_repositorio = HistorialRepositorioMemoria()
    historial_mapper = HistorialMapper()
    persistidor = TermostatoPersistidorJSON()
    termostato = Termostato(
        historial_repositorio=historial_repositorio,
        persistidor=persistidor,
        temp_ambiente_inicial=Config.TEMP_AMBIENTE_INICIAL,
        temp_deseada_inicial=Config.TEMP_DESEADA_INICIAL,
        bateria_inicial=Config.BATERIA_INICIAL
    )
    termostato.cargar_estado()
```

#### Tarea 2.4: Actualizar __init__.py de configuracion
- [ ] Exportar Config y Configurador

```python
"""
Modulo de configuracion del sistema.
"""
from app.configuracion.config import Config
from app.configuracion.configurador import Configurador

__all__ = ['Config', 'Configurador']
```

---

### Fase 3: Modificar termostato.py

#### Tarea 3.1: Agregar parametros iniciales al constructor
- [ ] Agregar parametros `temp_ambiente_inicial`, `temp_deseada_inicial`, `bateria_inicial`
- [ ] Usar estos valores en lugar de hardcoded

```python
def __init__(self, historial_repositorio=None, persistidor=None,
             temp_ambiente_inicial=20, temp_deseada_inicial=24, bateria_inicial=5.0):
    self._historial_repositorio = historial_repositorio
    self._persistidor = persistidor
    self._temperatura_ambiente = temp_ambiente_inicial
    self._temperatura_deseada = temp_deseada_inicial
    self._carga_bateria = bateria_inicial
    # ...
```

#### Tarea 3.2: Usar Config para rangos de validacion
- [ ] Importar Config
- [ ] Reemplazar valores hardcoded en setters por Config.*

```python
from app.configuracion.config import Config

@temperatura_ambiente.setter
def temperatura_ambiente(self, valor):
    valor = int(valor)
    if not (Config.TEMP_AMBIENTE_MIN <= valor <= Config.TEMP_AMBIENTE_MAX):
        raise ValueError(
            f"temperatura_ambiente debe estar entre {Config.TEMP_AMBIENTE_MIN} y {Config.TEMP_AMBIENTE_MAX}"
        )
    self._temperatura_ambiente = valor
    # ...
```

---

### Fase 4: Actualizar imports

#### Tarea 4.1: Modificar api.py
- [ ] Cambiar import de `app.general.configurador` a `app.configuracion`

```python
# Antes:
from app.general.configurador import Configurador

# Despues:
from app.configuracion import Configurador
```

#### Tarea 4.2: Modificar run.py
- [ ] Agregar carga de dotenv al inicio
- [ ] Usar Config para PORT y DEBUG

```python
from dotenv import load_dotenv
load_dotenv()

from app.configuracion import Config
from app.servicios.api import app_api

if __name__ == "__main__":
    app_api.run(port=Config.PORT, debug=Config.DEBUG)
```

#### Tarea 4.3: Eliminar configurador.py de general/
- [ ] Eliminar archivo `app/general/configurador.py` (ya movido)

---

### Fase 5: Verificacion y cierre

#### Tarea 5.1: Verificar imports
- [ ] Ejecutar `python -c "from app.servicios.api import app_api"` sin errores

#### Tarea 5.2: Probar manualmente
- [ ] Iniciar servidor sin .env (usa valores por defecto)
- [ ] Crear .env con valores personalizados
- [ ] Reiniciar servidor y verificar que usa valores de .env
- [ ] Probar validacion con rangos personalizados

#### Tarea 5.3: Ejecutar quality check
- [ ] Ejecutar `/quality-check app/`
- [ ] Verificar que todos los quality gates pasen

#### Tarea 5.4: Commit
- [ ] `git add .`
- [ ] `git commit -m "TRM-015: Implementar configuracion por variables de entorno"`

---

## Criterios de Aceptacion (Checklist Final)

- [ ] Se crea archivo `.env.example` con variables disponibles
- [ ] Variables soportadas: TEMP_AMBIENTE_INICIAL, TEMP_DESEADA_INICIAL, BATERIA_INICIAL
- [ ] Variables de rangos: TEMP_*_MIN, TEMP_*_MAX, BATERIA_MIN, BATERIA_MAX
- [ ] Si no se definen, se usan valores por defecto actuales
- [ ] Se utiliza `python-dotenv` para cargar variables
- [ ] Configuracion centralizada en `app/configuracion/config.py`

---

## Ejemplo de uso

```bash
# Copiar plantilla
cp .env.example .env

# Editar valores
nano .env

# Iniciar servidor (cargara automaticamente .env)
python run.py
```

---

## Notas

- Los valores de .env solo se usan si no hay estado persistido (TRM-007)
- El archivo `.env` debe estar en `.gitignore` (ya esta: linea 41)
- La clase Config se importa antes que Configurador para evitar dependencias circulares
