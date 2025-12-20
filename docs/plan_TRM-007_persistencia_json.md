# Plan de Implementacion TRM-007: Persistencia en archivo JSON

**Historia:** TRM-007
**Branch:** TRM-007 (a crear o ya creado)
**Fecha:** 2025-12-20

---

## Arquitectura

```
app/
├── datos/
│   ├── __init__.py           # [MODIFICAR] Exportar nuevas clases
│   ├── registro.py
│   ├── repositorio.py
│   ├── mapper.py
│   ├── memoria.py
│   ├── persistidor.py        # [NUEVO] Interface abstracta
│   └── persistidor_json.py   # [NUEVO] Implementacion JSON
├── general/
│   ├── termostato.py         # [MODIFICAR] Agregar persistencia
│   └── configurador.py       # [MODIFICAR] Inyectar persistidor
data/
└── termostato_estado.json    # [AUTO-GENERADO en runtime]
.gitignore                    # [MODIFICAR] Agregar data/
```

---

## Tareas Secuenciales

### Fase 1: Crear componentes de persistencia

#### Tarea 1.1: Implementar interface abstracta (`persistidor.py`)
- [ ] Crear ABC `TermostatoPersistidor`
- [ ] Metodo abstracto `guardar(datos: dict) -> None`
- [ ] Metodo abstracto `cargar() -> Optional[dict]`
- [ ] Metodo abstracto `existe() -> bool`

```python
"""
Interface abstracta para persistencia del estado del termostato.
"""
from abc import ABC, abstractmethod
from typing import Optional


class TermostatoPersistidor(ABC):
    """Interface para persistir el estado del termostato."""

    @abstractmethod
    def guardar(self, datos: dict) -> None:
        """Guarda el estado del termostato."""
        pass

    @abstractmethod
    def cargar(self) -> Optional[dict]:
        """Carga el estado del termostato. Retorna None si no existe."""
        pass

    @abstractmethod
    def existe(self) -> bool:
        """Verifica si existe un estado guardado."""
        pass
```

#### Tarea 1.2: Implementar persistidor JSON (`persistidor_json.py`)
- [ ] Crear clase `TermostatoPersistidorJSON` que hereda de `TermostatoPersistidor`
- [ ] Atributo `_ruta` con path al archivo (default: `data/termostato_estado.json`)
- [ ] Implementar `guardar()`: crear directorio si no existe, escribir JSON con indentacion
- [ ] Implementar `cargar()`: leer JSON si existe, retornar None si no
- [ ] Implementar `existe()`: verificar existencia del archivo

```python
"""
Implementacion de persistencia en archivo JSON.
"""
import json
import os
from typing import Optional

from app.datos.persistidor import TermostatoPersistidor


class TermostatoPersistidorJSON(TermostatoPersistidor):
    """Persistidor que guarda el estado en un archivo JSON."""

    def __init__(self, ruta: str = "data/termostato_estado.json"):
        self._ruta = ruta

    def guardar(self, datos: dict) -> None:
        """Guarda el estado en archivo JSON."""
        directorio = os.path.dirname(self._ruta)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio)
        with open(self._ruta, 'w', encoding='utf-8') as archivo:
            json.dump(datos, archivo, indent=2, ensure_ascii=False)

    def cargar(self) -> Optional[dict]:
        """Carga el estado desde archivo JSON."""
        if not self.existe():
            return None
        with open(self._ruta, 'r', encoding='utf-8') as archivo:
            return json.load(archivo)

    def existe(self) -> bool:
        """Verifica si existe el archivo de estado."""
        return os.path.exists(self._ruta)
```

#### Tarea 1.3: Actualizar `__init__.py` de datos
- [ ] Importar y exportar `TermostatoPersistidor`
- [ ] Importar y exportar `TermostatoPersistidorJSON`

```python
# Agregar a los imports existentes:
from app.datos.persistidor import TermostatoPersistidor
from app.datos.persistidor_json import TermostatoPersistidorJSON

# Agregar a __all__:
__all__ = [
    # ... existentes ...
    'TermostatoPersistidor',
    'TermostatoPersistidorJSON',
]
```

---

### Fase 2: Integrar con capa de dominio

#### Tarea 2.1: Modificar Termostato (`termostato.py`)
- [ ] Agregar parametro `persistidor` en `__init__` (opcional, default=None)
- [ ] Guardar referencia al persistidor
- [ ] Agregar metodo privado `_guardar_estado()` que serializa y persiste
- [ ] Agregar metodo publico `cargar_estado()` para inicializacion
- [ ] Llamar `_guardar_estado()` en cada setter que modifica estado

```python
# En __init__:
def __init__(self, historial_repositorio=None, persistidor=None):
    self._historial_repositorio = historial_repositorio
    self._persistidor = persistidor
    # ... inicializacion de atributos ...

# Nuevo metodo privado:
def _guardar_estado(self):
    """Persiste el estado actual si hay persistidor configurado."""
    if self._persistidor:
        datos = {
            'temperatura_ambiente': self._temperatura_ambiente,
            'temperatura_deseada': self._temperatura_deseada,
            'carga_bateria': self._carga_bateria,
            'estado_climatizador': self._estado_climatizador,
            'indicador': self._indicador
        }
        self._persistidor.guardar(datos)

# Nuevo metodo publico:
def cargar_estado(self):
    """Carga el estado desde el persistidor si existe."""
    if self._persistidor and self._persistidor.existe():
        datos = self._persistidor.cargar()
        if datos:
            self._temperatura_ambiente = datos.get('temperatura_ambiente', 20)
            self._temperatura_deseada = datos.get('temperatura_deseada', 24)
            self._carga_bateria = datos.get('carga_bateria', 5.0)
            self._estado_climatizador = datos.get('estado_climatizador', 'apagado')
            self._indicador = datos.get('indicador', 'NORMAL')

# Modificar cada setter para llamar _guardar_estado():
@temperatura_ambiente.setter
def temperatura_ambiente(self, valor):
    # ... validacion existente ...
    self._temperatura_ambiente = valor
    self._registrar_en_historial(valor)
    self._guardar_estado()  # <-- AGREGAR
```

#### Tarea 2.2: Modificar Configurador (`configurador.py`)
- [ ] Importar `TermostatoPersistidorJSON`
- [ ] Crear instancia del persistidor
- [ ] Pasar persistidor al crear Termostato
- [ ] Llamar `cargar_estado()` despues de crear Termostato

```python
from app.datos import (
    HistorialRepositorioMemoria,
    HistorialMapper,
    TermostatoPersistidorJSON
)

class Configurador:
    historial_repositorio = HistorialRepositorioMemoria()
    historial_mapper = HistorialMapper()
    persistidor = TermostatoPersistidorJSON()
    termostato = Termostato(
        historial_repositorio=historial_repositorio,
        persistidor=persistidor
    )
    # Cargar estado guardado si existe
    termostato.cargar_estado()
```

---

### Fase 3: Configuracion del proyecto

#### Tarea 3.1: Actualizar `.gitignore`
- [ ] Agregar linea `data/` para ignorar archivos de estado

```
# Agregar al .gitignore:
data/
```

#### Tarea 3.2: Crear directorio data/ con .gitkeep (opcional)
- [ ] Si se desea trackear el directorio vacio, crear `data/.gitkeep`
- [ ] Alternativa: el directorio se crea automaticamente al guardar

---

### Fase 4: Verificacion y cierre

#### Tarea 4.1: Verificar imports
- [ ] Ejecutar `python -c "from app.servicios.api import app_api"` sin errores

#### Tarea 4.2: Probar manualmente
- [ ] Iniciar servidor con `python run.py`
- [ ] POST temperatura ambiente (ej: 25)
- [ ] Verificar que se crea `data/termostato_estado.json`
- [ ] Verificar contenido del JSON (legible, con indentacion)
- [ ] Reiniciar servidor
- [ ] GET /termostato/ y verificar que mantiene el valor 25
- [ ] Probar editar manualmente el JSON y reiniciar

#### Tarea 4.3: Ejecutar quality check
- [ ] Ejecutar `/quality-check app/`
- [ ] Verificar que todos los quality gates pasen

#### Tarea 4.4: Commit
- [ ] `git add .`
- [ ] `git commit -m "TRM-007: Implementar persistencia en archivo JSON"`

---

## Criterios de Aceptacion (Checklist Final)

- [ ] El estado se guarda automaticamente en `data/termostato_estado.json`
- [ ] Al iniciar, el sistema carga el estado desde el archivo si existe
- [ ] Si no existe archivo, se usan valores por defecto
- [ ] El guardado ocurre despues de cada modificacion
- [ ] El archivo JSON es legible y editable manualmente

---

## Ejemplo de archivo JSON generado

```json
{
  "temperatura_ambiente": 22,
  "temperatura_deseada": 24,
  "carga_bateria": 4.5,
  "estado_climatizador": "calentando",
  "indicador": "NORMAL"
}
```

---

## Notas

- El persistidor JSON es intercambiable por otras implementaciones (SQLite, Redis, etc.)
- El patron es consistente con TRM-006 (HistorialRepositorio)
- La carga inicial ocurre una sola vez al importar Configurador
- Si el archivo JSON se corrompe, el sistema usa valores por defecto
