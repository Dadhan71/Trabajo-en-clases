# Trabajo-en-clases

Pipeline modular en Python para ingestar, limpiar, validar y guardar datos de ventas con registros sucios.

---

## Estructura del proyecto

```
carpetiña/
├── pipeline.py          # Orquestador principal
├── ingesta.py           # Carga y validación estructural
├── limpieza.py          # Limpieza y normalización de datos
├── validacion.py        # Validaciones semánticas
├── guardado.py          # Exportación de resultados
├── data/
│   ├── raw/
│   │   ├── historial_ventas.csv         # Archivo de entrada
│   │   └── historial_ventas_backup.csv  # Respaldo automático
│   ├── processed/
│   │   └── historial_ventas_limpio.csv  # Registros válidos
│   └── errors/
│       └── historial_ventas_errores.csv # Registros rechazados
└── logs/
    └── pipeline_YYYYMMDD_HHMMSS.log     # Log de cada ejecución
```

---

## Cómo ejecutar

1. Coloca el archivo CSV en `data/raw/historial_ventas.csv`
2. Desde la carpeta del proyecto, ejecuta:

```bash
python pipeline.py
```

Los resultados quedan en `data/processed/` y `data/errors/`.

---

## Etapas del pipeline

### 1. Ingesta (`ingesta.py`)
- Crea la carpeta `data/raw/` si no existe
- Verifica que el archivo de origen exista
- Genera un respaldo automático del CSV original
- Valida que las columnas esperadas estén presentes
- Valida que el DataFrame no esté vacío

**Columnas esperadas:** `id`, `nombre`, `edad`, `monto`, `ciudad`, `fecha_compra`, `metodo_pago`

### 2. Limpieza (`limpieza.py`)
| Campo | Tratamiento |
|---|---|
| `id` | Elimina filas sin id |
| `edad` | Convierte a numérico, elimina no convertibles |
| `nombre` | Elimina filas vacías o en blanco |
| `monto` | Convierte a numérico, imputa faltantes con la **mediana** |
| `ciudad` | Elimina filas vacías o en blanco |
| `fecha_compra` | Convierte a datetime, elimina fechas no parseables |
| `metodo_pago` | Elimina filas vacías o en blanco |
| duplicados | Elimina duplicados por `id` |

### 3. Validación semántica (`validacion.py`)
Los registros que pasen limpieza se validan con estas reglas:

| # | Campo | Regla |
|---|---|---|
| 1 | `edad` | Entre 0 y 120 |
| 2 | `monto` | Mayor a 0 |
| 3 | `metodo_pago` | Uno de: `efectivo`, `tarjeta`, `transferencia`, `débito`, `crédito` |
| 4 | `fecha_compra` | No puede ser fecha futura |
| 5 | `nombre` | No puede ser un valor numérico |

Los registros que fallen alguna regla se separan con una columna `motivo_error` que describe el problema.

### 4. Guardado (`guardado.py`)
- `data/processed/historial_ventas_limpio.csv` → registros que pasaron todas las validaciones
- `data/errors/historial_ventas_errores.csv` → registros rechazados con motivo

---

## Ejemplo con `ventas_sucias.csv`

| Fila | Problema detectado | Etapa |
|---|---|---|
| Pedro Gomez (x2) | Duplicado por id | Limpieza |
| fila sin nombre | Nombre vacío | Limpieza |
| edad = 150 | Fuera de rango [0-120] | Validación |
| metodo_pago = "debito" | No reconocido | Validación |

**Resultado:** 10 filas → 3 válidas / 2 con error semántico

---

## Requisitos

```
pandas
```

> `numpy` y `missingno` ya no son necesarios tras la refactorización de `limpieza.py`.

---

## Logs

Cada ejecución genera un archivo de log en `logs/` con timestamp. Para evitar errores de encoding en Windows, ejecuta con:

```bash
set PYTHONIOENCODING=utf-8 && python pipeline.py
```
