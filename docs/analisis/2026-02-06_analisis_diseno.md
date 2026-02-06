# Análisis de Diseño - app_termostato

**Fecha:** 2026-02-06
**Criterios aplicados:** Principios SOLID, Cohesión, Acoplamiento, Code Smells

---

## Resumen Ejecutivo

### Calificación General: **C+ (6.5/10)**

**Fortalezas:**
- ✅ Uso correcto de abstracciones (ABC) en capa de datos
- ✅ Inyección de dependencias en Termostato
- ✅ Segregación de interfaces bien aplicada
- ✅ Estructura modular del proyecto

**Debilidades Críticas:**
- ❌ Violación de SRP en clase Termostato (God Object)
- ❌ Uso de Singleton (anti-pattern) en Configurador
- ❌ Alto acoplamiento entre api.py y Configurador
- ❌ Duplicación masiva de código en endpoints

---

## 1. Análisis SOLID

### 1.1 Single Responsibility Principle (SRP) ⚠️ VIOLADO

#### 🔴 **CRÍTICO: Termostato (app/general/termostato.py)**

**Responsabilidades identificadas (debería tener 1, tiene 6):**

| # | Responsabilidad | Líneas | Evidencia |
|---|----------------|--------|-----------|
| 1 | Modelo de datos | 10-40 | Atributos de temperatura, batería, climatizador |
| 2 | Validación de datos | 46-102 | Setters con validación de rangos |
| 3 | Cálculo de indicadores | 104-115 | Property `indicador` con lógica de negocio |
| 4 | Persistencia | 117-127 | Método `_guardar_estado()` |
| 5 | Carga de estado | 129-138 | Método `cargar_estado()` |
| 6 | Gestión de historial | 140-148 | Método `_registrar_en_historial()` |

**Impacto:**
- Dificulta testing unitario (necesita mockear múltiples dependencias)
- Viola Open/Closed (cambios en persistencia requieren modificar Termostato)
- Baja cohesión
- Alta complejidad cognitiva

**Recomendación:**
```
Termostato (solo modelo)
  ↓ usa
TermostatoService (orquestación)
  ↓ usa
TermostatoValidator (validación)
TermostatoPersistidor (persistencia)
HistorialService (registro de temperaturas)
IndicadorCalculator (cálculo de indicadores)
```

#### 🟡 **MODERADO: api.py**

**Violaciones:**
- Mezcla validación de requests con lógica de endpoint (líneas 254-267)
- Configuración de Swagger embebida en mismo archivo (líneas 28-63)

**Recomendación:**
- Extraer validación a `RequestValidator`
- Mover configuración Swagger a `app/configuracion/swagger_config.py`

#### ✅ **CUMPLE:**
- `Config` - Solo configuración
- `HistorialRepositorioMemoria` - Solo almacenamiento
- `TermostatoPersistidorJSON` - Solo persistencia en JSON
- `HistorialRepositorio` (ABC) - Solo definición de contrato

---

### 1.2 Open/Closed Principle (OCP) ⚠️ PARCIALMENTE VIOLADO

#### ✅ **BIEN APLICADO:**

**Extensibilidad mediante abstracciones:**
```python
# Se pueden agregar nuevas implementaciones sin modificar código existente
HistorialRepositorio (ABC)
  ├── HistorialRepositorioMemoria ✓
  ├── HistorialRepositorioDB (futuro) ✓
  └── HistorialRepositorioRedis (futuro) ✓

TermostatoPersistidor (ABC)
  ├── TermostatoPersistidorJSON ✓
  ├── TermostatoPersistidorMySQL (futuro) ✓
  └── TermostatoPersistidorMongoDB (futuro) ✓
```

#### 🔴 **VIOLADO:**

**Lógica de indicador hardcoded (termostato.py:104-115):**
```python
@property
def indicador(self):
    if self._carga_bateria > Config.INDICADOR_UMBRAL_NORMAL:
        return "NORMAL"
    if self._carga_bateria >= Config.INDICADOR_UMBRAL_BAJO:
        return "BAJO"
    return "CRITICO"
```

**Problema:** Para cambiar estrategia de cálculo, hay que modificar la clase.

**Solución - Strategy Pattern:**
```python
class IndicadorCalculator(ABC):
    @abstractmethod
    def calcular(self, carga_bateria: float) -> str:
        pass

class IndicadorCalculatorTresNiveles(IndicadorCalculator):
    def calcular(self, carga_bateria: float) -> str:
        # Lógica actual

class IndicadorCalculatorCincoNiveles(IndicadorCalculator):
    def calcular(self, carga_bateria: float) -> str:
        # Nueva lógica sin modificar Termostato
```

---

### 1.3 Liskov Substitution Principle (LSP) ✅ CUMPLE

**Correcto:**
- `HistorialRepositorioMemoria` es sustituible por `HistorialRepositorio`
- `TermostatoPersistidorJSON` es sustituible por `TermostatoPersistidor`
- No hay herencia entre clases concretas que pueda romper el principio

**Comentario:** El uso de ABC en lugar de herencia tradicional facilita LSP.

---

### 1.4 Interface Segregation Principle (ISP) ✅ CUMPLE

**Interfaces cohesivas y mínimas:**

| Interface | Métodos | Cohesión | ISP |
|-----------|---------|----------|-----|
| `HistorialRepositorio` | 4 (agregar, obtener, cantidad, limpiar) | Alta | ✅ |
| `TermostatoPersistidor` | 3 (guardar, cargar, existe) | Alta | ✅ |

**Ninguna clase obligada a implementar métodos que no necesita.**

---

### 1.5 Dependency Inversion Principle (DIP) ⚠️ PARCIALMENTE VIOLADO

#### ✅ **BIEN APLICADO:**

**Termostato depende de abstracciones (termostato.py:22-24):**
```python
def __init__(self, historial_repositorio=None, persistidor=None, ...):
    self._historial_repositorio = historial_repositorio  # ABC
    self._persistidor = persistidor  # ABC
```

#### 🔴 **VIOLACIONES:**

**1. Import dentro de método (termostato.py:143):**
```python
def _registrar_en_historial(self, temperatura):
    if self._historial_repositorio:
        from app.datos import RegistroTemperatura  # ❌ CODE SMELL
```

**2. Dependencia directa de singleton (api.py:66):**
```python
termostato = Configurador.termostato  # ❌ Acoplamiento fuerte
```

**3. Configurador crea implementaciones concretas (configurador.py:24-26):**
```python
historial_repositorio = HistorialRepositorioMemoria()  # ❌ No abstracción
persistidor = TermostatoPersistidorJSON()  # ❌ No abstracción
```

**Solución - Dependency Injection Container:**
```python
# app/configuracion/container.py
class DIContainer:
    def get_historial_repositorio(self) -> HistorialRepositorio:
        return HistorialRepositorioMemoria()

    def get_persistidor(self) -> TermostatoPersistidor:
        return TermostatoPersistidorJSON()

    def get_termostato(self) -> Termostato:
        return Termostato(
            historial_repositorio=self.get_historial_repositorio(),
            persistidor=self.get_persistidor()
        )
```

---

## 2. Cohesión y Acoplamiento

### 2.1 Cohesión

#### ✅ **ALTA COHESIÓN (Excelente):**

| Módulo | Cohesión | Justificación |
|--------|----------|---------------|
| `HistorialRepositorioMemoria` | ⭐⭐⭐⭐⭐ | Todos los métodos trabajan con `_registros` |
| `TermostatoPersistidorJSON` | ⭐⭐⭐⭐⭐ | Todos los métodos sobre archivo JSON |
| `Config` | ⭐⭐⭐⭐⭐ | Solo constantes de configuración |

#### 🔴 **BAJA COHESIÓN (Crítico):**

| Módulo | Cohesión | Problema |
|--------|----------|----------|
| `Termostato` | ⭐⭐ | Mezcla 6 responsabilidades diferentes |
| `Configurador` | ⭐⭐⭐ | Mezcla Factory + Singleton + Initialization |

---

### 2.2 Acoplamiento

#### 🔴 **ALTO ACOPLAMIENTO (Crítico):**

**Diagrama de dependencias problemáticas:**
```
api.py ━━━━━━━━━━━━━━┓
                      ↓ (dependencia directa)
                 Configurador (singleton global)
                      ↓
                 Termostato
                   ↙    ↘
         Config (static)  RegistroTemperatura
```

**Problemas:**
1. **api.py → Configurador:** Acoplamiento singleton (dificulta testing)
2. **Termostato → Config:** Acoplamiento a clase estática (líneas 50, 68, 85, 111)
3. **Termostato → RegistroTemperatura:** Import dentro de método (línea 143)
4. **Configurador → implementaciones concretas:** No usa abstracciones

**Impacto:**
- Imposible testear api.py sin Configurador
- Imposible testear Termostato sin Config
- Dificulta cambiar implementaciones

#### ✅ **BAJO ACOPLAMIENTO (Bien):**

```
TermostatoPersistidorJSON → TermostatoPersistidor (ABC)
HistorialRepositorioMemoria → HistorialRepositorio (ABC)
```

---

## 3. Code Smells Detectados

### 🔴 Nivel Crítico

#### 1. **Singleton Anti-Pattern (configurador.py:14-34)**

**Ubicación:** `app/configuracion/configurador.py`

**Código:**
```python
class Configurador:
    historial_repositorio = HistorialRepositorioMemoria()  # Variables de clase
    termostato = Termostato(...)  # ❌ Singleton implícito
```

**Problemas:**
- Estado global compartido
- Dificulta testing (no se puede resetear entre tests)
- Acoplamiento fuerte desde api.py
- Viola SRP (mezcla Factory + Singleton)

**Impacto:** 🔴 CRÍTICO
**Esfuerzo corrección:** 🟡 MEDIO

**Solución:**
```python
# Factory puro sin singleton
class TermostatoFactory:
    @staticmethod
    def crear() -> Termostato:
        historial_repo = HistorialRepositorioMemoria()
        persistidor = TermostatoPersistidorJSON()
        return Termostato(historial_repositorio=historial_repo, ...)

# En api.py - inyectar dependencia
def create_app(termostato: Termostato = None):
    if termostato is None:
        termostato = TermostatoFactory.crear()
    # ...
```

---

#### 2. **God Object - Termostato (termostato.py:10-149)**

**Métricas:**
- **Líneas:** 149 (debería ser < 100)
- **Responsabilidades:** 6 (debería ser 1)
- **Complejidad Ciclomática:** ~15 (debería ser < 10)

**Problema:** Clase hace demasiado.

**Impacto:** 🔴 CRÍTICO
**Esfuerzo corrección:** 🔴 ALTO

**Refactorización propuesta:**

```python
# 1. Modelo puro (solo datos)
@dataclass
class TermostatoModelo:
    temperatura_ambiente: int
    temperatura_deseada: int
    carga_bateria: float
    estado_climatizador: str

# 2. Validador
class TermostatoValidator:
    def validar_temperatura_ambiente(self, valor: int) -> None:
        if not (Config.TEMPERATURA_AMBIENTE_MIN <= valor <= Config.TEMPERATURA_AMBIENTE_MAX):
            raise ValueError(...)

# 3. Servicio de persistencia
class TermostatoService:
    def __init__(self, persistidor: TermostatoPersistidor):
        self._persistidor = persistidor

    def guardar(self, modelo: TermostatoModelo) -> None:
        self._persistidor.guardar(asdict(modelo))

# 4. Calculador de indicador
class IndicadorCalculator:
    def calcular(self, carga_bateria: float) -> str:
        # Lógica actual
```

---

#### 3. **Massive Duplication - api.py (líneas 204-428)**

**Problema:** 6 endpoints con 95% de código duplicado.

**Ejemplo de patrón repetido:**
```python
# Se repite 6 veces con mínimas variaciones
if request.method == 'POST':
    datos = request.get_json()
    if not datos or "campo" not in datos:  # ❌ Duplicado
        return error_response(400, "Campo requerido faltante", ...)
    try:
        termostato.campo = datos["campo"]  # ❌ Duplicado
    except ValueError as e:
        return error_response(400, "Valor fuera de rango", str(e))
    return jsonify({'mensaje': 'dato registrado'}), 201
else:
    return jsonify({'campo': termostato.campo})
```

**Impacto:** 🔴 CRÍTICO
**Esfuerzo corrección:** 🟢 BAJO (refactor simple)

**Solución - Decorador genérico:**
```python
def endpoint_termostato(campo: str, campo_request: str):
    def decorator(func):
        @wraps(func)
        def wrapper():
            if request.method == 'POST':
                datos = request.get_json()
                if not datos or campo_request not in datos:
                    return error_response(400, "Campo requerido faltante")
                try:
                    setattr(termostato, campo, datos[campo_request])
                    return jsonify({'mensaje': 'dato registrado'}), 201
                except ValueError as e:
                    return error_response(400, "Valor fuera de rango", str(e))
            else:
                return jsonify({campo: getattr(termostato, campo)})
        return wrapper
    return decorator

@app_api.route("/termostato/temperatura_ambiente/", methods=["GET", "POST"])
@endpoint_termostato("temperatura_ambiente", "ambiente")
def obtener_temperatura_ambiente():
    """Documentación Swagger..."""
    pass
```

---

### 🟡 Nivel Moderado

#### 4. **Import Inside Method (termostato.py:143)**

**Código:**
```python
def _registrar_en_historial(self, temperatura):
    if self._historial_repositorio:
        from app.datos import RegistroTemperatura  # ❌
```

**Problema:**
- Indica posible dependencia circular
- Impacto en performance (import en cada llamada)
- Code smell clásico

**Solución:**
```python
# Mover import al inicio del archivo
from app.datos.registro import RegistroTemperatura
```

---

#### 5. **Missing Validation - estado_climatizador (termostato.py:99-102)**

**Código:**
```python
@estado_climatizador.setter
def estado_climatizador(self, valor):
    self._estado_climatizador = str(valor)  # ❌ Acepta cualquier string
```

**Problema:** No valida contra valores permitidos.

**Solución:**
```python
ESTADOS_VALIDOS = {"apagado", "encendido", "enfriando", "calentando"}

@estado_climatizador.setter
def estado_climatizador(self, valor):
    valor = str(valor).lower()
    if valor not in ESTADOS_VALIDOS:
        raise ValueError(f"Estado debe ser uno de: {ESTADOS_VALIDOS}")
    self._estado_climatizador = valor
```

---

#### 6. **Global Variable (api.py:69)**

**Código:**
```python
_inicio_servidor = datetime.now()  # ❌ Variable global mutable
```

**Problema:** Estado mutable en nivel de módulo.

**Solución:**
```python
class AppState:
    def __init__(self):
        self.inicio_servidor = datetime.now()

app_state = AppState()
```

---

### 🟢 Nivel Bajo

#### 7. **Hardcoded Logic en Property (termostato.py:104-115)**

Ya cubierto en OCP.

#### 8. **Magic Configuration (config.py)**

**No es realmente un smell** - uso correcto de variables de entorno.

---

## 4. Métricas de Calidad

| Archivo | LOC | CC Promedio | Responsabilidades | Cohesión | Acoplamiento | Nota |
|---------|-----|-------------|-------------------|----------|--------------|------|
| `termostato.py` | 149 | 15 | 6 | ⭐⭐ | 🔴 Alto | D |
| `api.py` | 429 | 8 | 3 | ⭐⭐⭐ | 🔴 Alto | C |
| `configurador.py` | 35 | 2 | 3 | ⭐⭐⭐ | 🔴 Alto | C |
| `config.py` | 36 | 1 | 1 | ⭐⭐⭐⭐⭐ | 🟢 Bajo | A |
| `memoria.py` | 37 | 3 | 1 | ⭐⭐⭐⭐⭐ | 🟢 Bajo | A |
| `persistidor_json.py` | 35 | 3 | 1 | ⭐⭐⭐⭐⭐ | 🟢 Bajo | A |

---

## 5. Recomendaciones Priorizadas

### 🔴 Prioridad ALTA (próximo sprint)

1. **Refactorizar Termostato (God Object)**
   - Extraer validación a `TermostatoValidator`
   - Extraer cálculo de indicador a `IndicadorCalculator`
   - Convertir a modelo de datos puro
   - **Esfuerzo:** 8 horas
   - **Impacto:** Mejora testabilidad, reduce acoplamiento, cumple SRP

2. **Eliminar Singleton en Configurador**
   - Implementar Factory pattern puro
   - Usar Dependency Injection en api.py
   - **Esfuerzo:** 4 horas
   - **Impacto:** Facilita testing, reduce acoplamiento global

3. **Eliminar duplicación en endpoints (api.py)**
   - Crear decorador genérico o clase base
   - **Esfuerzo:** 3 horas
   - **Impacto:** Reduce 200+ líneas, facilita mantenimiento

### 🟡 Prioridad MEDIA (backlog)

4. **Agregar validación a estado_climatizador**
   - **Esfuerzo:** 0.5 horas
   - **Impacto:** Previene bugs, mejora robustez

5. **Mover import de RegistroTemperatura al top**
   - **Esfuerzo:** 0.1 horas
   - **Impacto:** Mejora claridad, evita dependencias circulares

6. **Extraer configuración de Swagger**
   - Mover a `app/configuracion/swagger_config.py`
   - **Esfuerzo:** 1 hora
   - **Impacto:** Mejora organización

### 🟢 Prioridad BAJA (mejoras futuras)

7. **Implementar Strategy Pattern para indicador**
   - **Esfuerzo:** 2 horas
   - **Impacto:** Cumple OCP, permite extensión sin modificación

8. **Crear Dependency Injection Container**
   - **Esfuerzo:** 4 horas
   - **Impacto:** Centraliza creación de objetos, mejora testabilidad

---

## 6. Plan de Refactorización Sugerido

### Fase 1: Quick Wins (1 día)
- [ ] Mover import RegistroTemperatura al top
- [ ] Agregar validación estado_climatizador
- [ ] Eliminar variable global _inicio_servidor

### Fase 2: Reducir Duplicación (1 día)
- [ ] Crear decorador genérico para endpoints
- [ ] Refactorizar los 6 endpoints a usar decorador
- [ ] Tests de regresión

### Fase 3: Desacoplar (2 días)
- [ ] Crear TermostatoFactory (sin singleton)
- [ ] Modificar api.py para usar factory
- [ ] Actualizar tests

### Fase 4: Separar Responsabilidades (3 días)
- [ ] Crear TermostatoValidator
- [ ] Crear IndicadorCalculator
- [ ] Refactorizar Termostato a modelo puro
- [ ] Crear TermostatoService para orquestación
- [ ] Actualizar tests

### Fase 5: Aplicar Patrones Avanzados (2 días)
- [ ] Implementar Strategy para indicador
- [ ] Crear DI Container (opcional)

**Total estimado:** 9 días de desarrollo

---

## 7. Conclusiones

### Puntos Fuertes
- ✅ Buena separación en capas (servicios, datos, configuración)
- ✅ Uso correcto de ABC para abstracciones
- ✅ Inyección de dependencias en Termostato
- ✅ Módulos de datos con alta cohesión

### Puntos Críticos a Resolver
- ❌ Clase Termostato viola SRP (God Object)
- ❌ Singleton anti-pattern en Configurador
- ❌ Duplicación masiva en endpoints (DRY violado)
- ❌ Alto acoplamiento entre capas

### Impacto del Deuda Técnica Actual
- **Testabilidad:** Difícil mockear dependencias por singleton
- **Mantenibilidad:** Cambios requieren tocar múltiples responsabilidades
- **Extensibilidad:** Agregar features requiere modificar clases existentes (OCP)
- **Bugs potenciales:** Falta de validación en estado_climatizador

### Próximos Pasos
1. Priorizar Quick Wins (Fase 1)
2. Aplicar refactoring incremental (Fases 2-3)
3. Evaluar ROI de Fases 4-5 según roadmap del proyecto

---

**Preparado por:** Claude Sonnet 4.5
**Herramientas:** Análisis estático de código, Principios SOLID, Métricas de cohesión/acoplamiento
