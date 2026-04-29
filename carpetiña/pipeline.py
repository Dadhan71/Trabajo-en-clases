import shutil
import logging
import pandas as pd
from datetime import datetime
from pathlib import Path
 
from ingesta import ingestar
from limpieza import limpiar
from validacion import validar
from guardado import guardar
 
# ── LOGGING ─────────────────────────────────────────────────────────────────
Path("logs").mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(f"logs/pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)
 
# ── EJECUCIÓN ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    log.info("======== INICIO DEL PIPELINE ========")
 
    df = ingestar(
        origen="data/raw/historial_ventas.csv",
        destino="data/raw/historial_ventas_backup.csv"
    )
 
    df_limpio = limpiar(df)
 
    df_validos, df_errores = validar(df_limpio)
 
    guardar(df_validos, df_errores)
 
    log.info("======== PIPELINE FINALIZADO ========")