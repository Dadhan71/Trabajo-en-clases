import shutil
import logging
import pandas as pd
from pathlib import Path
 
log = logging.getLogger(__name__)
 
COLUMNAS_ESPERADAS = ["id", "nombre", "edad", "monto", "ciudad", "fecha_compra", "metodo_pago"]
 
 
def ingestar(origen: str, destino: str) -> pd.DataFrame:
    """
    Copia el archivo original como respaldo y lo carga en un DataFrame.
    Realiza validaciones estructurales básicas antes de continuar.
    """
    log.info(f"Ingesta iniciada — origen: {origen}")
 
    # ── Creación de carpetas necesarias ──────────────────────────────────────
    Path(origen).parent.mkdir(parents=True, exist_ok=True)
    log.info(f"✓ Carpeta asegurada: {Path(origen).parent}")
 
    # ── Validación estructural 1: el archivo existe ──────────────────────────
    if not Path(origen).exists():
        log.error(f"Archivo no encontrado: {origen}")
        raise FileNotFoundError(f"No se encontró el archivo: {origen}")
    log.info("✓ Validación 1: archivo existe")
 
    # Respaldo
    Path(destino).parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(origen, destino)
    log.info(f"Respaldo guardado en: {destino}")
 
    # Carga
    df = pd.read_csv(origen, encoding="utf-8-sig", sep=",")
    log.info(f"Filas cargadas: {len(df)} | Columnas: {list(df.columns)}")
 
    # ── Validación estructural 2: columnas esperadas presentes ───────────────
    faltantes = [c for c in COLUMNAS_ESPERADAS if c not in df.columns]
    if faltantes:
        log.error(f"Columnas faltantes: {faltantes}")
        raise ValueError(f"El archivo no tiene las columnas esperadas: {faltantes}")
    log.info("✓ Validación 2: todas las columnas esperadas presentes")
 
    # ── Validación estructural 3: el DataFrame no está vacío ────────────────
    if df.empty:
        log.error("El archivo está vacío")
        raise ValueError("El archivo CSV no contiene datos")
    log.info("✓ Validación 3: el DataFrame no está vacío")
 
    log.info(f"Nulos por columna:\n{df.isnull().sum().to_string()}")
    log.info(f"Filas duplicadas: {df.duplicated().sum()}")
 
    return df