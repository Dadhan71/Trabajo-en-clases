import logging
import pandas as pd
 
log = logging.getLogger(__name__)
 
 
def limpiar(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia el DataFrame recibido desde la ingesta.
    - Elimina filas sin id, nombre, ciudad, fecha_compra o metodo_pago.
    - Convierte edad y monto a numérico; imputa monto faltante con la mediana.
    - Elimina duplicados por id.
    """
    log.info("── Limpieza iniciada ──")
    df = df.copy()
 
    log.info(f"Shape inicial: {df.shape}")
    log.info(f"Nulos por columna:\n{df.isnull().sum().to_string()}")
    log.info(f"Filas duplicadas: {df.duplicated().sum()}")
 
    # id
    antes = len(df)
    df.dropna(subset=['id'], inplace=True)
    log.info(f"id — eliminadas {antes - len(df)} filas sin id")
 
    # edad
    df['edad'] = df['edad'].astype(str).str.strip().replace('', pd.NA)
    df['edad'] = pd.to_numeric(df['edad'], errors='coerce')
    antes = len(df)
    df.dropna(subset=['edad'], inplace=True)
    log.info(f"edad — eliminadas {antes - len(df)} filas con edad inválida")
 
    # nombre
    df['nombre'] = df['nombre'].astype(str).str.strip().replace('', pd.NA)
    antes = len(df)
    df.dropna(subset=['nombre'], inplace=True)
    log.info(f"nombre — eliminadas {antes - len(df)} filas con nombre inválido")
 
    # monto
    df['monto'] = df['monto'].astype(str).str.strip().replace('', pd.NA)
    df['monto'] = pd.to_numeric(df['monto'], errors='coerce')
    nulos_monto = df['monto'].isnull().sum()
    df['monto'] = df['monto'].fillna(df['monto'].median())
    log.info(f"monto — imputadas {nulos_monto} filas con la mediana")
 
    # ciudad
    df['ciudad'] = df['ciudad'].astype(str).str.strip().replace('', pd.NA)
    antes = len(df)
    df.dropna(subset=['ciudad'], inplace=True)
    log.info(f"ciudad — eliminadas {antes - len(df)} filas con ciudad inválida")
 
    # fecha_compra
    df['fecha_compra'] = pd.to_datetime(df['fecha_compra'], errors='coerce')
    antes = len(df)
    df.dropna(subset=['fecha_compra'], inplace=True)
    log.info(f"fecha_compra — eliminadas {antes - len(df)} filas con fecha inválida")
 
    # metodo_pago
    df['metodo_pago'] = df['metodo_pago'].astype(str).str.strip().replace('', pd.NA)
    antes = len(df)
    df.dropna(subset=['metodo_pago'], inplace=True)
    log.info(f"metodo_pago — eliminadas {antes - len(df)} filas con método inválido")
 
    # duplicados
    antes = len(df)
    df.drop_duplicates(subset=['id'], inplace=True)
    log.info(f"duplicados — eliminadas {antes - len(df)} filas duplicadas por id")
 
    df.reset_index(drop=True, inplace=True)
    log.info(f"Shape final: {df.shape}")
    log.info("── Limpieza finalizada ──")
 
    return df