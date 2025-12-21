# TUTORIAL: Ambiente Agéntico para Calidad de Código en Python

**Autor:** Prof. Victor Valotto - FIUNER  
**Versión:** 1.0  
**Fecha:** Diciembre 2025  
**Nivel:** Intermedio  
**Duración estimada:** 2-3 horas  

---

## 📋 Tabla de Contenidos

1. [Introducción](#1-introducción)
2. [Requisitos Previos](#2-requisitos-previos)
3. [Conceptos Fundamentales](#3-conceptos-fundamentales)
4. [Arquitectura del Ambiente Agéntico](#4-arquitectura-del-ambiente-agéntico)
5. [Paso 1: Instalación de Herramientas](#5-paso-1-instalación-de-herramientas)
6. [Paso 2: Configuración de Claude Code](#6-paso-2-configuración-de-claude-code)
7. [Paso 3: Crear el Agente de Calidad](#7-paso-3-crear-el-agente-de-calidad)
8. [Paso 4: Scripts de Medición](#8-paso-4-scripts-de-medición)
9. [Paso 5: Quality Gates Automáticos](#9-paso-5-quality-gates-automáticos)
10. [Paso 6: Prueba con Proyecto Real](#10-paso-6-prueba-con-proyecto-real)
11. [Paso 7: Reportes y Trazabilidad](#11-paso-7-reportes-y-trazabilidad)
12. [Troubleshooting](#12-troubleshooting)
13. [Extensiones Futuras](#13-extensiones-futuras)

---

## 1. Introducción

### 1.1 ¿Qué es un Ambiente Agéntico?

Un **ambiente agéntico** es un sistema donde agentes de IA (en nuestro caso, Claude Code) ejecutan tareas específicas de forma autónoma, siguiendo reglas predefinidas. En este tutorial, crearemos un agente especializado en **medir calidad de código Python**.

### 1.2 Objetivos del Tutorial

Al completar este tutorial, serás capaz de:

- ✅ Configurar un agente de Claude Code para calidad de código
- ✅ Automatizar mediciones de métricas básicas (LOC, CC, MI, Pylint)
- ✅ Implementar quality gates que bloqueen código de baja calidad
- ✅ Generar reportes automáticos de calidad
- ✅ Integrar el agente en tu flujo de desarrollo

### 1.3 ¿Por qué Métricas "Mínimas"?

Nos enfocamos en **4 métricas fundamentales** que cubren el 80% de los problemas de calidad:

| Métrica | Qué mide | Por qué es esencial |
|---------|----------|---------------------|
| **LOC/SLOC** | Tamaño del código | Detecta archivos/funciones demasiado grandes |
| **CC** | Complejidad ciclomática | Identifica código difícil de entender/testear |
| **MI** | Índice de mantenibilidad | Predice dificultad de mantenimiento futuro |
| **Pylint Score** | Calidad general | Detecta errores de estilo y problemas comunes |

Estas métricas son:
- **Rápidas de calcular** (< 5 segundos en proyectos medianos)
- **Fáciles de interpretar** (umbrales claros)
- **Accionables** (el agente puede sugerir mejoras específicas)
- **Bloqueantes** (pueden detener commits de código malo)

---

## 2. Requisitos Previos

### 2.1 Software Requerido

| Software | Versión | Propósito |
|----------|---------|-----------|
| Python | 3.8+ | Lenguaje base |
| Claude Code | Latest | Motor de agentes |
| Git | 2.x+ | Control de versiones |

### 2.2 Conocimientos Requeridos

- ✅ Python intermedio (clases, módulos, decoradores)
- ✅ Git básico (commit, branch, push)
- ✅ Terminal/bash básico
- ⚠️ NO se requiere experiencia previa con agentes IA

### 2.3 Proyecto de Prueba

Para este tutorial usaremos un proyecto real: **ISSE_Termostato**

```bash
# Clonar el proyecto de ejemplo
git clone https://github.com/vvalotto/ISSE_Termostato.git
cd ISSE_Termostato
```

**Características del proyecto:**
- ~30 archivos Python
- Clean Architecture
- Tests existentes (84% cobertura)
- Ideal para probar métricas

---

## 3. Conceptos Fundamentales

### 3.1 ¿Qué es un Agente en Claude Code?

Un **agente** (o **subagent**) en Claude Code es un archivo markdown (`.md`) que define:

1. **Nombre**: Identificador único del agente
2. **Descripción**: Cuándo debe activarse
3. **Herramientas**: Qué puede hacer (read, write, bash, etc.)
4. **Instrucciones**: Cómo debe comportarse

**Ejemplo básico:**

```markdown
---
name: mi-agente
description: Use this agent when...
tools: Read, Bash
---

You are an expert in...
```

### 3.2 ¿Cómo Funciona el Flujo?

```
┌─────────────┐
│   Usuario   │ "Analiza la calidad del código"
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│   Claude Code       │ Detecta que debe usar quality-agent
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Quality Agent      │ Lee instrucciones de .claude/agents/
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Herramientas       │ Ejecuta radon, pylint, etc.
│  (radon, pylint)    │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Quality Report     │ Genera reporte con métricas
└─────────────────────┘
```

### 3.3 Métricas Básicas - Definiciones

#### **LOC (Lines of Code)**
```
Total de líneas en el archivo, incluyendo:
- Código ejecutable
- Comentarios
- Líneas en blanco
```

**Umbrales:**
- Función: ≤ 50 LOC
- Clase: ≤ 300 LOC
- Módulo: ≤ 500 LOC

#### **CC (Cyclomatic Complexity)**
```
Número de caminos independientes en una función.
CC = aristas - nodos + 2 (en el grafo de control de flujo)
```

**Fórmula práctica:**
```
CC = 1 + número de puntos de decisión (if, while, for, and, or, except)
```

**Umbrales:**
- CC ≤ 5: Bajo riesgo (excelente)
- CC 6-10: Riesgo moderado (aceptable)
- CC > 10: Alto riesgo (refactorizar)

#### **MI (Maintainability Index)**
```
MI = 171 - 5.2×ln(V) - 0.23×CC - 16.2×ln(LOC)

Donde:
- V = Volumen de Halstead
- CC = Complejidad ciclomática
- LOC = Líneas de código
```

**Umbrales:**
- MI > 20: Mantenible
- MI 10-20: Moderadamente mantenible
- MI < 10: Difícil de mantener

#### **Pylint Score**
```
Score = 10.0 × (1 - (errores + warnings) / statements)
```

**Umbrales:**
- Pylint ≥ 9.0: Excelente
- Pylint ≥ 8.0: Aceptable
- Pylint < 8.0: Necesita mejoras

---

## 4. Arquitectura del Ambiente Agéntico

### 4.1 Estructura de Directorios

```
proyecto/
├── .claude/
│   ├── agents/
│   │   └── quality-agent.md          # Agente de calidad
│   ├── commands/
│   │   ├── quality-check.md          # Comando /quality-check
│   │   └── quality-report.md         # Comando /quality-report
│   └── settings.json                 # Hooks automáticos
│
├── scripts/
│   ├── metrics/
│   │   ├── calculate_metrics.py      # Calcula métricas
│   │   ├── validate_gates.py         # Valida quality gates
│   │   └── generate_report.py        # Genera reporte
│   └── requirements.txt              # Dependencias
│
├── reports/                          # Reportes generados
│   ├── quality_YYYYMMDD_HHMMSS.json
│   └── quality_YYYYMMDD_HHMMSS.md
│
└── src/                              # Código fuente del proyecto
    └── ...
```

### 4.2 Flujo de Trabajo

```
┌──────────────────────────────────────────────────┐
│  1. DESARROLLO                                   │
│     Developer escribe código                     │
└────────────────┬─────────────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────────────┐
│  2. ANÁLISIS AUTOMÁTICO                          │
│     Quality Agent se activa                      │
│     - Detecta archivos modificados               │
│     - Ejecuta calculate_metrics.py               │
└────────────────┬─────────────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────────────┐
│  3. VALIDACIÓN                                   │
│     validate_gates.py                            │
│     - Compara contra umbrales                    │
│     - ✅ PASS o ❌ FAIL                          │
└────────────────┬─────────────────────────────────┘
                 │
                 ▼
        ┌────────┴────────┐
        │                 │
        ▼                 ▼
  ┌──────────┐      ┌──────────┐
  │ ✅ PASS  │      │ ❌ FAIL  │
  │ Continue │      │ Block    │
  └──────────┘      └────┬─────┘
                         │
                         ▼
                   ┌──────────────────┐
                   │ 4. REPORTE       │
                   │ Sugerencias      │
                   │ de mejora        │
                   └──────────────────┘
```

---

## 5. Paso 1: Instalación de Herramientas

### 5.1 Instalar Claude Code

```bash
# Instalar Claude Code globalmente
npm install -g @anthropic-ai/claude-code

# Verificar instalación
claude --version

# Autenticar (sigue las instrucciones en pantalla)
claude auth login
```

### 5.2 Instalar Herramientas de Métricas Python

```bash
# Crear archivo de dependencias
cat > scripts/requirements.txt << 'EOF'
radon>=6.0.1
pylint>=3.0.0
pytest>=8.0.0
pytest-cov>=4.1.0
EOF

# Instalar herramientas
pip install -r scripts/requirements.txt

# Verificar instalación
radon --version
pylint --version
pytest --version
```

### 5.3 Verificar que Todo Funciona

```bash
# Test rápido de radon (métricas de complejidad)
echo 'def hello(): pass' > /tmp/test.py
radon cc /tmp/test.py
# Debe mostrar: F 1:0 hello - A (1)

# Test rápido de pylint (calidad general)
pylint /tmp/test.py --score=yes
# Debe mostrar un score cercano a 10.0

# Limpiar
rm /tmp/test.py
```

**✅ Si todos los comandos funcionan, estás listo para continuar.**

---

## 6. Paso 2: Configuración de Claude Code

### 6.1 Inicializar Proyecto

```bash
# En el directorio de tu proyecto (ej: ISSE_Termostato)
cd ISSE_Termostato

# Crear estructura de directorios para Claude
mkdir -p .claude/agents
mkdir -p .claude/commands
mkdir -p scripts/metrics
mkdir -p reports

# Crear archivo de configuración básico
touch .claude/settings.json
```

### 6.2 Configurar Settings Básicos

Crear `.claude/settings.json`:

```json
{
  "version": "1.0",
  "project_name": "ISSE_Termostato",
  "quality_gates": {
    "max_complexity": 10,
    "min_maintainability": 20,
    "min_pylint_score": 8.0,
    "max_function_lines": 50
  },
  "hooks": {
    "PostToolUse": []
  }
}
```

**Explicación:**
- `quality_gates`: Umbrales que definen código aceptable
- `hooks`: Se configurarán más adelante para automatización

---

## 7. Paso 3: Crear el Agente de Calidad

### 7.1 Crear el Archivo del Agente

Crear `.claude/agents/quality-agent.md`:

```markdown
---
name: quality-agent
description: AUTOMATICALLY analyzes Python code quality using essential metrics. Use this agent proactively when Python files are modified or when user asks for quality analysis.
tools: Read, Write, Edit, Bash, Glob, Grep
---

You are a Python code quality expert specialized in objective metrics analysis.

## Your Mission

Analyze Python code quality using 4 essential metrics:
1. **LOC/SLOC** - Code size
2. **Cyclomatic Complexity (CC)** - Structural complexity
3. **Maintainability Index (MI)** - Overall maintainability
4. **Pylint Score** - Code quality and style

## When to Activate

- When user modifies Python files (automatic)
- When user asks "check quality", "analyze code", etc.
- Before commits (if hooks are configured)
- On explicit request: "use quality-agent"

## Analysis Workflow

### Step 1: Identify Target
```bash
# If user specified a file/directory
TARGET="$1"

# If not specified, analyze modified files
if [ -z "$TARGET" ]; then
  TARGET=$(git diff --name-only --cached '*.py' | tr '\n' ' ')
fi

# If still empty, analyze entire project
if [ -z "$TARGET" ]; then
  TARGET="."
fi
```

### Step 2: Calculate Metrics

Execute the following commands:

```bash
# 1. LOC and SLOC (Lines of Code)
radon raw $TARGET -s

# 2. Cyclomatic Complexity
radon cc $TARGET -a -s --total-average

# 3. Maintainability Index
radon mi $TARGET -s

# 4. Pylint Score
pylint $TARGET --output-format=json --score=yes 2>&1 | tee /tmp/pylint_output.json
```

### Step 3: Validate Quality Gates

Compare results against thresholds from `.claude/settings.json`:

| Metric | Threshold | Action if Violated |
|--------|-----------|-------------------|
| CC | ≤ 10 | ❌ BLOCK - Function too complex |
| MI | > 20 | ❌ BLOCK - Hard to maintain |
| Pylint | ≥ 8.0 | ❌ BLOCK - Quality issues |
| Function LOC | ≤ 50 | ⚠️  WARNING - Consider refactoring |

### Step 4: Generate Report

Create a markdown report with:

#### Executive Summary
- Overall Grade: A/B/C/D/F
- Quality Gates: X/4 passed
- Blocking Issues: N

#### Detailed Metrics

**1. Size Metrics**
```
Total LOC: XXX
Source LOC: XXX
Comments: XX%
Blank Lines: XX%
```

**2. Complexity Analysis**
```
Average CC: X.X
Max CC: X (in function: XXXX)
Distribution:
  - A (1-5):   XX functions (XX%)
  - B (6-10):  XX functions (XX%)
  - C (11-20): XX functions (XX%)
  - D (21+):   XX functions (XX%)
```

**3. Maintainability**
```
Average MI: XX.X
Modules with MI < 20: X
```

**4. Pylint Analysis**
```
Score: X.X / 10.0
Errors: X
Warnings: X
Refactor suggestions: X
```

#### Quality Gates Status

```
✅ PASS: Cyclomatic Complexity (avg: 5.2 ≤ 10)
✅ PASS: Maintainability Index (avg: 45.3 > 20)
❌ FAIL: Pylint Score (7.8 < 8.0)
⚠️  WARNING: Function size (3 functions > 50 LOC)
```

#### Recommendations

List specific, actionable improvements:

1. **CRITICAL**: Function `calculate_metrics` has CC=15 (limit: 10)
   - Suggestion: Extract nested conditions into separate functions
   - Location: `scripts/metrics.py:45`

2. **HIGH**: Module `configurador.py` has MI=18 (limit: 20)
   - Suggestion: Reduce dependencies, split into smaller modules
   - Location: `configurador/configurador.py`

3. **MEDIUM**: 5 PEP8 violations in `gestor_ambiente.py`
   - Run: `autopep8 --in-place gestor_ambiente.py`

#### Next Steps

- Fix CRITICAL issues before committing
- Run: `python scripts/metrics/calculate_metrics.py src/` to re-check

### Step 5: Save Report

Save detailed report to:
- `reports/quality_YYYYMMDD_HHMMSS.md` (human-readable)
- `reports/quality_YYYYMMDD_HHMMSS.json` (machine-readable)

## Output Format

Always provide:
1. Clear PASS/FAIL status
2. Specific file:line references
3. Actionable recommendations
4. Commands to fix issues

## Error Handling

If tools fail:
- Show the actual error message
- Suggest installation commands
- Don't fail silently

## Important Notes

- Be objective - metrics don't lie
- Don't apologize for bad metrics - report them
- Prioritize blocking issues (CC, MI, Pylint)
- Be constructive with recommendations
```

### 7.2 Verificar el Agente

```bash
# Listar agentes disponibles
ls -la .claude/agents/

# Debe mostrar: quality-agent.md
```

---

## 8. Paso 4: Scripts de Medición

### 8.1 Script Principal: calculate_metrics.py

Crear `scripts/metrics/calculate_metrics.py`:

```python
#!/usr/bin/env python3
"""
Calculate essential code quality metrics for Python projects.
Outputs JSON with metrics data.
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime


class MetricsCalculator:
    """Calculates code quality metrics using radon and pylint."""
    
    def __init__(self, target_path="."):
        self.target_path = Path(target_path)
        self.metrics = {
            "timestamp": datetime.now().isoformat(),
            "target": str(self.target_path),
            "size": {},
            "complexity": {},
            "maintainability": {},
            "pylint": {},
            "summary": {}
        }
    
    def calculate_size_metrics(self):
        """Calculate LOC, SLOC using radon raw."""
        try:
            result = subprocess.run(
                ["radon", "raw", str(self.target_path), "-s", "-j"],
                capture_output=True,
                text=True,
                check=True
            )
            
            raw_data = json.loads(result.stdout)
            
            # Aggregate metrics
            total_loc = 0
            total_sloc = 0
            total_comments = 0
            total_blank = 0
            
            for file_path, data in raw_data.items():
                total_loc += data.get("loc", 0)
                total_sloc += data.get("sloc", 0)
                total_comments += data.get("comments", 0)
                total_blank += data.get("blank", 0)
            
            self.metrics["size"] = {
                "loc": total_loc,
                "sloc": total_sloc,
                "comments": total_comments,
                "blank": total_blank,
                "comment_ratio": round(total_comments / total_loc * 100, 2) if total_loc > 0 else 0
            }
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"Error calculating size metrics: {e}", file=sys.stderr)
            return False
        except json.JSONDecodeError as e:
            print(f"Error parsing radon output: {e}", file=sys.stderr)
            return False
    
    def calculate_complexity_metrics(self):
        """Calculate Cyclomatic Complexity using radon cc."""
        try:
            result = subprocess.run(
                ["radon", "cc", str(self.target_path), "-a", "-s", "-j"],
                capture_output=True,
                text=True,
                check=True
            )
            
            cc_data = json.loads(result.stdout)
            
            # Aggregate complexity
            all_complexities = []
            max_cc = 0
            max_cc_function = None
            
            # Distribution by grade
            distribution = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0}
            
            for file_path, functions in cc_data.items():
                for func in functions:
                    cc = func.get("complexity", 0)
                    all_complexities.append(cc)
                    
                    if cc > max_cc:
                        max_cc = cc
                        max_cc_function = f"{file_path}:{func.get('lineno')} {func.get('name')}"
                    
                    # Grade distribution
                    grade = func.get("rank", "F")
                    if grade in distribution:
                        distribution[grade] += 1
            
            avg_cc = sum(all_complexities) / len(all_complexities) if all_complexities else 0
            
            self.metrics["complexity"] = {
                "average": round(avg_cc, 2),
                "max": max_cc,
                "max_location": max_cc_function,
                "total_functions": len(all_complexities),
                "distribution": distribution
            }
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"Error calculating complexity: {e}", file=sys.stderr)
            return False
        except json.JSONDecodeError as e:
            print(f"Error parsing radon cc output: {e}", file=sys.stderr)
            return False
    
    def calculate_maintainability_index(self):
        """Calculate Maintainability Index using radon mi."""
        try:
            result = subprocess.run(
                ["radon", "mi", str(self.target_path), "-s", "-j"],
                capture_output=True,
                text=True,
                check=True
            )
            
            mi_data = json.loads(result.stdout)
            
            # Aggregate MI
            all_mi = []
            min_mi = 100
            min_mi_file = None
            
            for file_path, data in mi_data.items():
                mi = data.get("mi", 0)
                all_mi.append(mi)
                
                if mi < min_mi:
                    min_mi = mi
                    min_mi_file = file_path
            
            avg_mi = sum(all_mi) / len(all_mi) if all_mi else 0
            
            # Count modules below threshold
            below_threshold = sum(1 for mi in all_mi if mi < 20)
            
            self.metrics["maintainability"] = {
                "average": round(avg_mi, 2),
                "min": round(min_mi, 2),
                "min_file": min_mi_file,
                "below_threshold_count": below_threshold
            }
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"Error calculating MI: {e}", file=sys.stderr)
            return False
        except json.JSONDecodeError as e:
            print(f"Error parsing radon mi output: {e}", file=sys.stderr)
            return False
    
    def calculate_pylint_score(self):
        """Calculate Pylint score."""
        try:
            result = subprocess.run(
                ["pylint", str(self.target_path), "--output-format=json", "--score=yes"],
                capture_output=True,
                text=True
            )
            
            # Pylint returns non-zero even with warnings, so don't check=True
            
            # Parse JSON output
            messages = json.loads(result.stdout) if result.stdout else []
            
            # Extract score from stderr (Pylint writes score there)
            score_line = [line for line in result.stderr.split('\n') if 'rated at' in line.lower()]
            score = 0.0
            if score_line:
                # Extract score using regex
                import re
                match = re.search(r'(\d+\.\d+)/10', score_line[0])
                if match:
                    score = float(match.group(1))
            
            # Count message types
            errors = sum(1 for msg in messages if msg.get("type") == "error")
            warnings = sum(1 for msg in messages if msg.get("type") == "warning")
            refactor = sum(1 for msg in messages if msg.get("type") == "refactor")
            convention = sum(1 for msg in messages if msg.get("type") == "convention")
            
            self.metrics["pylint"] = {
                "score": score,
                "errors": errors,
                "warnings": warnings,
                "refactor": refactor,
                "convention": convention,
                "total_messages": len(messages)
            }
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"Error running pylint: {e}", file=sys.stderr)
            return False
        except json.JSONDecodeError as e:
            print(f"Error parsing pylint output: {e}", file=sys.stderr)
            return False
    
    def generate_summary(self):
        """Generate executive summary with pass/fail status."""
        
        # Quality gates from .claude/settings.json (hardcoded for now)
        gates = {
            "max_complexity": 10,
            "min_maintainability": 20,
            "min_pylint_score": 8.0
        }
        
        # Check each gate
        complexity_pass = self.metrics["complexity"]["average"] <= gates["max_complexity"]
        mi_pass = self.metrics["maintainability"]["average"] > gates["min_maintainability"]
        pylint_pass = self.metrics["pylint"]["score"] >= gates["min_pylint_score"]
        
        passed = sum([complexity_pass, mi_pass, pylint_pass])
        
        # Overall grade
        if passed == 3:
            grade = "A"
        elif passed == 2:
            grade = "B"
        elif passed == 1:
            grade = "C"
        else:
            grade = "F"
        
        self.metrics["summary"] = {
            "grade": grade,
            "gates_passed": passed,
            "gates_total": 3,
            "blocking_issues": 3 - passed,
            "quality_gates": {
                "complexity": {
                    "status": "PASS" if complexity_pass else "FAIL",
                    "value": self.metrics["complexity"]["average"],
                    "threshold": gates["max_complexity"]
                },
                "maintainability": {
                    "status": "PASS" if mi_pass else "FAIL",
                    "value": self.metrics["maintainability"]["average"],
                    "threshold": gates["min_maintainability"]
                },
                "pylint": {
                    "status": "PASS" if pylint_pass else "FAIL",
                    "value": self.metrics["pylint"]["score"],
                    "threshold": gates["min_pylint_score"]
                }
            }
        }
    
    def run_all(self):
        """Run all metric calculations."""
        success = True
        
        print("📊 Calculating code quality metrics...")
        print(f"Target: {self.target_path}\n")
        
        print("1/4 Calculating size metrics...", end=" ")
        if self.calculate_size_metrics():
            print("✅")
        else:
            print("❌")
            success = False
        
        print("2/4 Calculating complexity...", end=" ")
        if self.calculate_complexity_metrics():
            print("✅")
        else:
            print("❌")
            success = False
        
        print("3/4 Calculating maintainability index...", end=" ")
        if self.calculate_maintainability_index():
            print("✅")
        else:
            print("❌")
            success = False
        
        print("4/4 Running pylint analysis...", end=" ")
        if self.calculate_pylint_score():
            print("✅")
        else:
            print("❌")
            success = False
        
        if success:
            self.generate_summary()
            print("\n✅ All metrics calculated successfully!")
        else:
            print("\n⚠️  Some metrics failed to calculate")
        
        return success
    
    def save_json(self, output_path):
        """Save metrics as JSON."""
        with open(output_path, 'w') as f:
            json.dump(self.metrics, f, indent=2)
        print(f"\n💾 Metrics saved to: {output_path}")
    
    def print_summary(self):
        """Print executive summary to console."""
        summary = self.metrics["summary"]
        
        print("\n" + "="*60)
        print("📊 QUALITY METRICS SUMMARY")
        print("="*60)
        
        print(f"\n🎯 Overall Grade: {summary['grade']}")
        print(f"✅ Quality Gates: {summary['gates_passed']}/{summary['gates_total']} passed")
        print(f"🚨 Blocking Issues: {summary['blocking_issues']}")
        
        print("\n📏 Size Metrics:")
        print(f"  - Total LOC: {self.metrics['size']['loc']}")
        print(f"  - Source LOC: {self.metrics['size']['sloc']}")
        print(f"  - Comments: {self.metrics['size']['comment_ratio']}%")
        
        print("\n🔀 Complexity:")
        print(f"  - Average CC: {self.metrics['complexity']['average']}")
        print(f"  - Max CC: {self.metrics['complexity']['max']} ({self.metrics['complexity']['max_location']})")
        
        print("\n🔧 Maintainability:")
        print(f"  - Average MI: {self.metrics['maintainability']['average']}")
        print(f"  - Modules below threshold: {self.metrics['maintainability']['below_threshold_count']}")
        
        print("\n🔍 Pylint:")
        print(f"  - Score: {self.metrics['pylint']['score']}/10.0")
        print(f"  - Errors: {self.metrics['pylint']['errors']}")
        print(f"  - Warnings: {self.metrics['pylint']['warnings']}")
        
        print("\n✅❌ Quality Gates Status:")
        for gate, data in summary["quality_gates"].items():
            status_emoji = "✅" if data["status"] == "PASS" else "❌"
            print(f"  {status_emoji} {gate.title()}: {data['value']} (threshold: {data['threshold']})")
        
        print("\n" + "="*60)


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    
    calculator = MetricsCalculator(target)
    
    if calculator.run_all():
        # Save JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"reports/quality_{timestamp}.json"
        calculator.save_json(output_file)
        
        # Print summary
        calculator.print_summary()
        
        # Exit with appropriate code
        blocking = calculator.metrics["summary"]["blocking_issues"]
        sys.exit(0 if blocking == 0 else 1)
    else:
        print("\n❌ Failed to calculate metrics")
        sys.exit(2)
```

### 8.2 Script de Validación: validate_gates.py

Crear `scripts/metrics/validate_gates.py`:

```python
#!/usr/bin/env python3
"""
Validate quality gates based on calculated metrics.
Returns exit code 0 if all gates pass, 1 if any fail.
"""

import json
import sys
from pathlib import Path


def load_metrics(metrics_file):
    """Load metrics from JSON file."""
    with open(metrics_file, 'r') as f:
        return json.load(f)


def validate_gates(metrics):
    """Validate all quality gates."""
    
    summary = metrics.get("summary", {})
    gates = summary.get("quality_gates", {})
    
    print("🔍 Validating Quality Gates...")
    print("="*60)
    
    all_passed = True
    
    for gate_name, gate_data in gates.items():
        status = gate_data["status"]
        value = gate_data["value"]
        threshold = gate_data["threshold"]
        
        if status == "PASS":
            print(f"✅ {gate_name.upper()}: PASS")
            print(f"   Value: {value}, Threshold: {threshold}")
        else:
            print(f"❌ {gate_name.upper()}: FAIL")
            print(f"   Value: {value}, Threshold: {threshold}")
            all_passed = False
        
        print()
    
    print("="*60)
    
    if all_passed:
        print("✅ ALL QUALITY GATES PASSED!")
        return 0
    else:
        print("❌ SOME QUALITY GATES FAILED!")
        print("\nPlease fix the issues before committing.")
        return 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_gates.py <metrics_file.json>")
        sys.exit(2)
    
    metrics_file = sys.argv[1]
    
    if not Path(metrics_file).exists():
        print(f"Error: Metrics file not found: {metrics_file}")
        sys.exit(2)
    
    metrics = load_metrics(metrics_file)
    exit_code = validate_gates(metrics)
    sys.exit(exit_code)
```

### 8.3 Hacer Scripts Ejecutables

```bash
chmod +x scripts/metrics/calculate_metrics.py
chmod +x scripts/metrics/validate_gates.py
```

---

## 9. Paso 5: Quality Gates Automáticos

### 9.1 Configurar Hooks

Editar `.claude/settings.json` para agregar hooks automáticos:

```json
{
  "version": "1.0",
  "project_name": "ISSE_Termostato",
  "quality_gates": {
    "max_complexity": 10,
    "min_maintainability": 20,
    "min_pylint_score": 8.0,
    "max_function_lines": 50
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit:*.py|Create:*.py",
        "hooks": [
          {
            "type": "command",
            "command": "echo '🔍 Quality check triggered by Python file change...'"
          },
          {
            "type": "command",
            "command": "python scripts/metrics/calculate_metrics.py $(git diff --name-only '*.py' | head -1) > /tmp/quality_check.log 2>&1 || echo '⚠️  Quality issues detected'"
          }
        ]
      }
    ]
  }
}
```

**Qué hace esto:**
- Cada vez que Claude edita o crea un archivo `.py`
- Automáticamente ejecuta `calculate_metrics.py`
- Si fallan quality gates, muestra advertencia

### 9.2 Crear Comando Personalizado

Crear `.claude/commands/quality-check.md`:

```markdown
# Quality Check Command

Runs comprehensive quality analysis on Python code.

Usage:
```
/quality-check [path]
```

If no path specified, analyzes all Python files in the project.

**Steps:**

1. Identify target files
2. Run calculate_metrics.py
3. Show summary report
4. Suggest fixes if needed

**Example:**
```
/quality-check src/entidades/
/quality-check  # analyzes entire project
```
```

---

## 10. Paso 6: Prueba con Proyecto Real

### 10.1 Análisis Completo del Proyecto

```bash
# Ir al directorio del proyecto
cd ISSE_Termostato

# Ejecutar análisis completo
python scripts/metrics/calculate_metrics.py .
```

**Salida esperada:**

```
📊 Calculating code quality metrics...
Target: .

1/4 Calculating size metrics... ✅
2/4 Calculating complexity... ✅
3/4 Calculating maintainability index... ✅
4/4 Running pylint analysis... ✅

✅ All metrics calculated successfully!

💾 Metrics saved to: reports/quality_20251218_143022.json

============================================================
📊 QUALITY METRICS SUMMARY
============================================================

🎯 Overall Grade: B
✅ Quality Gates: 2/3 passed
🚨 Blocking Issues: 1

📏 Size Metrics:
  - Total LOC: 1245
  - Source LOC: 987
  - Comments: 12.5%

🔀 Complexity:
  - Average CC: 5.2
  - Max CC: 15 (gestor_climatizador.py:45 accionar_climatizador)

🔧 Maintainability:
  - Average MI: 45.3
  - Modules below threshold: 0

🔍 Pylint:
  - Score: 7.8/10.0
  - Errors: 0
  - Warnings: 12

✅❌ Quality Gates Status:
  ✅ Complexity: 5.2 (threshold: 10)
  ✅ Maintainability: 45.3 (threshold: 20)
  ❌ Pylint: 7.8 (threshold: 8.0)

============================================================
```

### 10.2 Análisis de Módulo Específico

```bash
# Analizar solo la capa de entidades
python scripts/metrics/calculate_metrics.py entidades/

# Analizar un archivo específico
python scripts/metrics/calculate_metrics.py entidades/ambiente.py
```

### 10.3 Probar con Claude Code

```bash
# Iniciar Claude Code en el proyecto
claude

# En el prompt de Claude:
# "Use quality-agent to analyze the code quality of this project"
```

Claude debería:
1. Detectar el agente `quality-agent`
2. Ejecutar los scripts de métricas
3. Generar un reporte detallado
4. Sugerir mejoras específicas

---

## 11. Paso 7: Reportes y Trazabilidad

### 11.1 Generar Reporte Markdown

Crear `scripts/metrics/generate_report.py`:

```python
#!/usr/bin/env python3
"""
Generate human-readable markdown report from metrics JSON.
"""

import json
import sys
from datetime import datetime
from pathlib import Path


def generate_markdown_report(metrics):
    """Generate detailed markdown report."""
    
    report = f"""# Code Quality Report

**Generated:** {metrics['timestamp']}  
**Target:** `{metrics['target']}`  
**Overall Grade:** {metrics['summary']['grade']}

---

## 📊 Executive Summary

- **Quality Gates Passed:** {metrics['summary']['gates_passed']}/{metrics['summary']['gates_total']}
- **Blocking Issues:** {metrics['summary']['blocking_issues']}
- **Grade:** {metrics['summary']['grade']}

---

## 📏 Size Metrics

| Metric | Value |
|--------|-------|
| Total LOC | {metrics['size']['loc']} |
| Source LOC | {metrics['size']['sloc']} |
| Comments | {metrics['size']['comments']} ({metrics['size']['comment_ratio']}%) |
| Blank Lines | {metrics['size']['blank']} |

---

## 🔀 Complexity Analysis

| Metric | Value |
|--------|-------|
| Average CC | {metrics['complexity']['average']} |
| Max CC | {metrics['complexity']['max']} |
| Max Location | {metrics['complexity']['max_location']} |
| Total Functions | {metrics['complexity']['total_functions']} |

### Complexity Distribution

| Grade | Range | Count | Percentage |
|-------|-------|-------|------------|
| A | 1-5 | {metrics['complexity']['distribution']['A']} | {metrics['complexity']['distribution']['A'] / metrics['complexity']['total_functions'] * 100:.1f}% |
| B | 6-10 | {metrics['complexity']['distribution']['B']} | {metrics['complexity']['distribution']['B'] / metrics['complexity']['total_functions'] * 100:.1f}% |
| C | 11-20 | {metrics['complexity']['distribution']['C']} | {metrics['complexity']['distribution']['C'] / metrics['complexity']['total_functions'] * 100:.1f}% |
| D | 21-30 | {metrics['complexity']['distribution']['D']} | {metrics['complexity']['distribution']['D'] / metrics['complexity']['total_functions'] * 100:.1f}% |
| E | 31-40 | {metrics['complexity']['distribution']['E']} | {metrics['complexity']['distribution']['E'] / metrics['complexity']['total_functions'] * 100:.1f}% |
| F | 40+ | {metrics['complexity']['distribution']['F']} | {metrics['complexity']['distribution']['F'] / metrics['complexity']['total_functions'] * 100:.1f}% |

---

## 🔧 Maintainability

| Metric | Value |
|--------|-------|
| Average MI | {metrics['maintainability']['average']} |
| Minimum MI | {metrics['maintainability']['min']} |
| Worst File | {metrics['maintainability']['min_file']} |
| Modules < 20 | {metrics['maintainability']['below_threshold_count']} |

---

## 🔍 Pylint Analysis

| Metric | Value |
|--------|-------|
| Score | {metrics['pylint']['score']}/10.0 |
| Errors | {metrics['pylint']['errors']} |
| Warnings | {metrics['pylint']['warnings']} |
| Refactor | {metrics['pylint']['refactor']} |
| Convention | {metrics['pylint']['convention']} |

---

## ✅❌ Quality Gates Status

"""
    
    for gate_name, gate_data in metrics['summary']['quality_gates'].items():
        status_emoji = "✅" if gate_data["status"] == "PASS" else "❌"
        report += f"### {status_emoji} {gate_name.upper()}\n\n"
        report += f"- **Status:** {gate_data['status']}\n"
        report += f"- **Value:** {gate_data['value']}\n"
        report += f"- **Threshold:** {gate_data['threshold']}\n\n"
    
    report += """---

## 🎯 Recommendations

"""
    
    # Generate specific recommendations based on failed gates
    blocking = metrics['summary']['blocking_issues']
    
    if blocking == 0:
        report += "✅ **No blocking issues found!** Code quality is good.\n\n"
        report += "**Suggested Improvements:**\n"
        report += "- Continue monitoring metrics in future commits\n"
        report += "- Consider increasing test coverage\n"
        report += "- Document complex algorithms\n"
    else:
        report += f"🚨 **{blocking} blocking issue(s) found!** Please fix before committing.\n\n"
        
        for gate_name, gate_data in metrics['summary']['quality_gates'].items():
            if gate_data["status"] == "FAIL":
                report += f"### Fix {gate_name.upper()}\n\n"
                
                if gate_name == "complexity":
                    report += f"**Issue:** Average complexity ({gate_data['value']}) exceeds threshold ({gate_data['threshold']})\n\n"
                    report += "**Actions:**\n"
                    report += f"1. Refactor function with CC={metrics['complexity']['max']}: `{metrics['complexity']['max_location']}`\n"
                    report += "2. Extract complex conditions into separate functions\n"
                    report += "3. Consider applying the Strategy pattern for branching logic\n\n"
                
                elif gate_name == "maintainability":
                    report += f"**Issue:** Average MI ({gate_data['value']}) below threshold ({gate_data['threshold']})\n\n"
                    report += "**Actions:**\n"
                    report += f"1. Review module: `{metrics['maintainability']['min_file']}`\n"
                    report += "2. Split large modules into smaller, cohesive units\n"
                    report += "3. Reduce dependencies between modules\n"
                    report += "4. Improve documentation and comments\n\n"
                
                elif gate_name == "pylint":
                    report += f"**Issue:** Pylint score ({gate_data['value']}) below threshold ({gate_data['threshold']})\n\n"
                    report += "**Actions:**\n"
                    report += f"1. Fix {metrics['pylint']['errors']} error(s)\n"
                    report += f"2. Address {metrics['pylint']['warnings']} warning(s)\n"
                    report += "3. Run: `pylint --list-msgs` to understand violations\n"
                    report += "4. Run: `autopep8 --in-place <file>` to auto-fix style issues\n\n"
    
    report += """---

## 📈 Tracking

- **Report File:** `{report_file}`
- **Metrics JSON:** `{json_file}`

"""
    
    return report


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_report.py <metrics.json>")
        sys.exit(1)
    
    metrics_file = sys.argv[1]
    
    with open(metrics_file, 'r') as f:
        metrics = json.load(f)
    
    # Generate report
    report = generate_markdown_report(metrics)
    
    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"reports/quality_{timestamp}.md"
    
    with open(report_file, 'w') as f:
        f.write(report)
    
    print(f"📝 Report generated: {report_file}")
    
    # Also print to console
    print("\n" + report)
```

### 11.2 Ejecutar Generación de Reporte

```bash
# Calcular métricas
python scripts/metrics/calculate_metrics.py . > /tmp/calc.log

# Generar reporte markdown
LATEST_JSON=$(ls -t reports/quality_*.json | head -1)
python scripts/metrics/generate_report.py $LATEST_JSON
```

---

## 12. Troubleshooting

### 12.1 Error: "radon: command not found"

**Problema:** Las herramientas de métricas no están instaladas.

**Solución:**
```bash
pip install radon pylint pytest pytest-cov
```

### 12.2 Error: "No module named 'radon'"

**Problema:** Python no encuentra el módulo radon.

**Solución:**
```bash
# Verificar que estás en el entorno correcto
which python
which pip

# Reinstalar
pip install --upgrade radon
```

### 12.3 Claude No Encuentra el Agente

**Problema:** Claude no activa el agente automáticamente.

**Solución:**
```bash
# Verificar estructura
ls -la .claude/agents/quality-agent.md

# Reiniciar sesión de Claude
# Exit y volver a entrar

# Invocar explícitamente
# "Use quality-agent to analyze code"
```

### 12.4 Hooks No Se Ejecutan

**Problema:** Los hooks en `.claude/settings.json` no se disparan.

**Solución:**
1. Verificar sintaxis JSON válida
2. Reiniciar Claude Code
3. Probar manualmente:
   ```bash
   python scripts/metrics/calculate_metrics.py .
   ```

### 12.5 Permisos de Ejecución

**Problema:** "Permission denied" al ejecutar scripts.

**Solución:**
```bash
chmod +x scripts/metrics/*.py
```

---

## 13. Extensiones Futuras

### 13.1 Agregar Más Métricas (Fase 2)

Una vez que domines las 4 métricas básicas, podés agregar:

- **Cohesión (LCOM)**: Mide relación entre métodos
- **Acoplamiento (CBO)**: Dependencias entre clases
- **Cobertura de tests**: % de código testeado
- **Seguridad (bandit)**: Vulnerabilidades

### 13.2 Integración con CI/CD

```yaml
# .github/workflows/quality.yml
name: Code Quality Check

on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.8'
      - name: Install dependencies
        run: |
          pip install radon pylint
      - name: Run quality checks
        run: |
          python scripts/metrics/calculate_metrics.py .
          python scripts/metrics/validate_gates.py reports/quality_*.json
```

### 13.3 Dashboard Visual

Crear un dashboard con Streamlit:

```python
# scripts/dashboard.py
import streamlit as st
import json
import plotly.express as px

st.title("Code Quality Dashboard")

# Load latest metrics
# ... visualizar métricas con gráficos
```

### 13.4 Histórico de Métricas

Guardar métricas en base de datos para tracking temporal:

```python
# scripts/track_metrics.py
import sqlite3
from datetime import datetime

# Store metrics history
# Generate trend charts
```

---

## 🎓 Conclusión

¡Felicitaciones! Has creado un **ambiente agéntico funcional** para calidad de código.

### Lo que Lograste

✅ Agente Claude Code especializado en calidad  
✅ Scripts de medición automatizados  
✅ Quality gates que bloquean código malo  
✅ Reportes detallados y accionables  
✅ Base para extensión futura  

### Próximos Pasos

1. **Practica:** Usa el agente en tus proyectos reales
2. **Refina:** Ajusta umbrales según tu contexto
3. **Extiende:** Agrega más métricas (Fase 2)
4. **Integra:** Conecta con Jira/Confluence/GitHub
5. **Escala:** Crea más agentes especializados

### Recursos Adicionales

- [Catálogo de Métricas Completo](./Catalogo_Metricas_Calidad_Diseno.pdf)
- [Documentación Radon](https://radon.readthedocs.io/)
- [Documentación Pylint](https://pylint.readthedocs.io/)
- [Claude Code Docs](https://code.claude.com/docs)

---

**Tutorial creado por:** Prof. Victor Valotto - FIUNER  
**Licencia:** Uso educativo  
**Contacto:** vvalotto@fiuner.edu.ar  

---

## Apéndice A: Referencia Rápida de Comandos

```bash
# Setup inicial
pip install radon pylint pytest pytest-cov
mkdir -p .claude/agents .claude/commands scripts/metrics reports

# Análisis completo
python scripts/metrics/calculate_metrics.py .

# Análisis específico
python scripts/metrics/calculate_metrics.py src/entidades/

# Validar quality gates
python scripts/metrics/validate_gates.py reports/quality_*.json

# Generar reporte
python scripts/metrics/generate_report.py reports/quality_*.json

# Con Claude Code
claude
# "Use quality-agent to analyze code quality"
```

## Apéndice B: Umbrales Recomendados

| Métrica | Excelente | Aceptable | Refactorizar |
|---------|-----------|-----------|--------------|
| CC | ≤ 5 | 6-10 | > 10 |
| MI | > 40 | 20-40 | < 20 |
| Pylint | ≥ 9.0 | 8.0-8.9 | < 8.0 |
| LOC/Función | < 30 | 30-50 | > 50 |
| LOC/Clase | < 200 | 200-300 | > 300 |
| LOC/Módulo | < 300 | 300-500 | > 500 |

## Apéndice C: Glosario

- **Agente:** Entidad autónoma que ejecuta tareas específicas
- **CC:** Cyclomatic Complexity - mide caminos en código
- **MI:** Maintainability Index - predice mantenibilidad
- **LOC:** Lines of Code - líneas totales
- **SLOC:** Source Lines of Code - líneas sin comentarios/blancos
- **Quality Gate:** Umbral que debe cumplirse para aprobar
- **Hook:** Acción automática disparada por eventos
- **Subagent:** Sinónimo de agente en Claude Code

---

**FIN DEL TUTORIAL**
