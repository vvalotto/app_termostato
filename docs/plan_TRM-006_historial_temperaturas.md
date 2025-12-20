# Plan de Implementacion TRM-006: Historial de Temperaturas

**Historia:** TRM-006
**Branch:** TER-006 (ya creado)
**Fecha:** 2025-12-20

---

## Arquitectura

```
app/
├── general/           # Capa de dominio/negocio
│   ├── termostato.py  # [MODIFICAR] Inyectar repositorio
│   └── configurador.py # [MODIFICAR] Instanciar repositorio
├── datos/             # Capa de gestion de datos [NUEVA]
│   ├── __init__.py
│   ├── registro.py
│   ├── repositorio.py
│   ├── mapper.py
│   └── memoria.py
├── servicios/
│   └── api.py         # [MODIFICAR] Nuevo endpoint
```

---

## Tareas Secuenciales

### Fase 1: Crear capa de datos

#### Tarea 1.1: Crear estructura de carpeta
- [ ] Crear directorio `app/datos/`
- [ ] Crear archivo `app/datos/__init__.py`

#### Tarea 1.2: Implementar modelo de dominio (`registro.py`)
- [ ] Crear dataclass `RegistroTemperatura`
- [ ] Atributos: `temperatura: int`, `timestamp: datetime`
- [ ] Metodo `__post_init__` para validar tipos si es necesario

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class RegistroTemperatura:
    temperatura: int
    timestamp: datetime
```

#### Tarea 1.3: Implementar interface abstracta (`repositorio.py`)
- [ ] Crear ABC `HistorialRepositorio`
- [ ] Metodo abstracto `agregar(registro: RegistroTemperatura) -> None`
- [ ] Metodo abstracto `obtener(limite: int = None) -> List[RegistroTemperatura]`
- [ ] Metodo abstracto `cantidad() -> int`
- [ ] Metodo abstracto `limpiar() -> None`

```python
from abc import ABC, abstractmethod
from typing import List, Optional
from app.datos.registro import RegistroTemperatura

class HistorialRepositorio(ABC):
    @abstractmethod
    def agregar(self, registro: RegistroTemperatura) -> None:
        pass

    @abstractmethod
    def obtener(self, limite: Optional[int] = None) -> List[RegistroTemperatura]:
        pass

    @abstractmethod
    def cantidad(self) -> int:
        pass

    @abstractmethod
    def limpiar(self) -> None:
        pass
```

#### Tarea 1.4: Implementar mapper (`mapper.py`)
- [ ] Crear clase `HistorialMapper`
- [ ] Metodo `a_dict(registro) -> dict` (para respuesta JSON)
- [ ] Metodo `desde_dict(datos) -> RegistroTemperatura` (para futuras cargas)

```python
from datetime import datetime
from app.datos.registro import RegistroTemperatura

class HistorialMapper:
    def a_dict(self, registro: RegistroTemperatura) -> dict:
        return {
            'temperatura': registro.temperatura,
            'timestamp': registro.timestamp.isoformat()
        }

    def desde_dict(self, datos: dict) -> RegistroTemperatura:
        return RegistroTemperatura(
            temperatura=datos['temperatura'],
            timestamp=datetime.fromisoformat(datos['timestamp'])
        )
```

#### Tarea 1.5: Implementar repositorio en memoria (`memoria.py`)
- [ ] Crear clase `HistorialRepositorioMemoria` que hereda de `HistorialRepositorio`
- [ ] Atributo privado `_registros: List[RegistroTemperatura]`
- [ ] Constante `MAX_REGISTROS = 100`
- [ ] Implementar `agregar()`: insertar al inicio, truncar si excede limite
- [ ] Implementar `obtener()`: retornar lista (ya ordenada por mas reciente)
- [ ] Implementar `cantidad()`: retornar len de lista
- [ ] Implementar `limpiar()`: vaciar lista

```python
from typing import List, Optional
from app.datos.registro import RegistroTemperatura
from app.datos.repositorio import HistorialRepositorio

class HistorialRepositorioMemoria(HistorialRepositorio):
    MAX_REGISTROS = 100

    def __init__(self):
        self._registros: List[RegistroTemperatura] = []

    def agregar(self, registro: RegistroTemperatura) -> None:
        self._registros.insert(0, registro)
        if len(self._registros) > self.MAX_REGISTROS:
            self._registros = self._registros[:self.MAX_REGISTROS]

    def obtener(self, limite: Optional[int] = None) -> List[RegistroTemperatura]:
        if limite is None:
            return self._registros.copy()
        return self._registros[:limite]

    def cantidad(self) -> int:
        return len(self._registros)

    def limpiar(self) -> None:
        self._registros = []
```

#### Tarea 1.6: Actualizar `__init__.py` de datos
- [ ] Exportar clases principales para facilitar imports

```python
from app.datos.registro import RegistroTemperatura
from app.datos.repositorio import HistorialRepositorio
from app.datos.mapper import HistorialMapper
from app.datos.memoria import HistorialRepositorioMemoria
```

---

### Fase 2: Integrar con capa de dominio

#### Tarea 2.1: Modificar Configurador (`configurador.py`)
- [ ] Importar `HistorialRepositorioMemoria` y `HistorialMapper`
- [ ] Crear instancia singleton de repositorio
- [ ] Crear instancia singleton de mapper
- [ ] Pasar repositorio al crear Termostato

```python
from app.datos.memoria import HistorialRepositorioMemoria
from app.datos.mapper import HistorialMapper

class Configurador:
    historial_repositorio = HistorialRepositorioMemoria()
    historial_mapper = HistorialMapper()
    termostato = Termostato(historial_repositorio=historial_repositorio)
```

#### Tarea 2.2: Modificar Termostato (`termostato.py`)
- [ ] Agregar parametro `historial_repositorio` en `__init__` (opcional, default=None)
- [ ] Guardar referencia al repositorio
- [ ] Importar `RegistroTemperatura` y `datetime`
- [ ] Modificar setter `temperatura_ambiente`: si hay repositorio, agregar registro

```python
# En __init__:
def __init__(self, historial_repositorio=None):
    self._historial_repositorio = historial_repositorio
    # ... resto de inicializacion

# En setter de temperatura_ambiente:
@temperatura_ambiente.setter
def temperatura_ambiente(self, valor):
    valor = int(valor)
    if not (0 <= valor <= 50):
        raise ValueError("temperatura_ambiente debe estar entre 0 y 50")
    self._temperatura_ambiente = valor
    if self._historial_repositorio:
        from datetime import datetime
        from app.datos.registro import RegistroTemperatura
        registro = RegistroTemperatura(temperatura=valor, timestamp=datetime.now())
        self._historial_repositorio.agregar(registro)
```

---

### Fase 3: Crear endpoint API

#### Tarea 3.1: Agregar endpoint en api.py
- [ ] Importar `Configurador.historial_repositorio` y `Configurador.historial_mapper`
- [ ] Crear ruta `GET /termostato/historial/`
- [ ] Leer parametro query `limite` con `request.args.get('limite', type=int)`
- [ ] Obtener registros del repositorio
- [ ] Mapear a dict usando mapper
- [ ] Retornar JSON con formato especificado

```python
@app_api.route("/termostato/historial/", methods=["GET"])
def obtener_historial():
    """GET: Obtiene el historial de temperaturas ambiente."""
    limite = request.args.get('limite', type=int)
    repositorio = Configurador.historial_repositorio
    mapper = Configurador.historial_mapper

    registros = repositorio.obtener(limite)
    historial = [mapper.a_dict(r) for r in registros]

    logger.info("GET /termostato/historial/ -> 200 (%d registros)", len(historial))
    return jsonify({
        'historial': historial,
        'total': repositorio.cantidad()
    })
```

---

### Fase 4: Verificacion y cierre

#### Tarea 4.1: Verificar imports
- [ ] Ejecutar `python -c "from app.servicios.api import app_api"` sin errores

#### Tarea 4.2: Probar manualmente
- [ ] Iniciar servidor con `python run.py`
- [ ] POST varias temperaturas ambiente
- [ ] GET /termostato/historial/ y verificar respuesta
- [ ] GET /termostato/historial/?limite=5 y verificar limite

#### Tarea 4.3: Ejecutar quality check
- [ ] Ejecutar `/quality-check app/`
- [ ] Verificar que todos los quality gates pasen

#### Tarea 4.4: Commit
- [ ] `git add .`
- [ ] `git commit -m "TRM-006: Implementar historial de temperaturas con patron repositorio"`

---

## Criterios de Aceptacion (Checklist Final)

- [ ] El sistema almacena las ultimas 100 lecturas de temperatura_ambiente
- [ ] Cada registro incluye: temperatura, timestamp (ISO 8601)
- [ ] Existe endpoint `GET /termostato/historial/`
- [ ] Se puede limitar registros con parametro `?limite=N`
- [ ] El historial se ordena del mas reciente al mas antiguo

---

## Notas

- El historial es **en memoria** (se pierde al reiniciar)
- La persistencia se implementara en TRM-007 agregando `HistorialRepositorioJSON`
- El patron repositorio permite cambiar la implementacion sin modificar dominio ni API
