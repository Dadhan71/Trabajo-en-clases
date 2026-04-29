import logging
import pandas as pd
from pathlib import Path
 
log = logging.getLogger(__name__)
 
 
def guardar(df_validos: pd.DataFrame, df_errores: pd.DataFrame) -> None:
    """
    Exporta los registros válidos y erróneos a archivos CSV separados.
    """
    log.info("── Guardado iniciado ──")
 
    Path("data/processed").mkdir(parents=True, exist_ok=True)
    Path("data/errors").mkdir(parents=True, exist_ok=True)
 
    ruta_validos = "data/processed/historial_ventas_limpio.csv"
    ruta_errores = "data/errors/historial_ventas_errores.csv"
 
    df_validos.to_csv(ruta_validos, index=False, encoding="utf-8-sig")
    log.info(f"✓ Válidos guardados en:  {ruta_validos} ({len(df_validos)} filas)")
 
    df_errores.to_csv(ruta_errores, index=False, encoding="utf-8-sig")
    log.info(f"✓ Erróneos guardados en: {ruta_errores} ({len(df_errores)} filas)")
 
    log.info("── Guardado finalizado ──")