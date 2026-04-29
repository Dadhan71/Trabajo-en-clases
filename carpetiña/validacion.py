import logging
import pandas as pd
from datetime import datetime
 
log = logging.getLogger(__name__)
 
METODOS_PAGO_VALIDOS = {"efectivo", "tarjeta", "transferencia", "débito", "crédito"}
 
 
def validar(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Aplica validaciones semánticas y separa registros válidos de erróneos.
 
    Validaciones semánticas:
        1. edad entre 0 y 120.
        2. monto mayor a 0.
        3. metodo_pago dentro de valores permitidos.
        4. fecha_compra no futura.
        5. nombre no es un número (campo de texto real).
 
    Retorna (df_validos, df_errores).
    """
    log.info("── Validación semántica iniciada ──")
 
    df = df.copy()
    df["_errores"] = ""
 
    # ── Validación semántica 1: edad entre 0 y 120 ───────────────────────────
    mascara_edad = ~df["edad"].between(0, 120)
    df.loc[mascara_edad, "_errores"] += "edad fuera de rango [0-120]; "
    log.info(f"Semántica 1 — edad fuera de rango: {mascara_edad.sum()} registros")
 
    # ── Validación semántica 2: monto > 0 ────────────────────────────────────
    mascara_monto = df["monto"] <= 0
    df.loc[mascara_monto, "_errores"] += "monto <= 0; "
    log.info(f"Semántica 2 — monto inválido (<= 0): {mascara_monto.sum()} registros")
 
    # ── Validación semántica 3: metodo_pago en lista permitida ───────────────
    mascara_pago = ~df["metodo_pago"].str.lower().isin(METODOS_PAGO_VALIDOS)
    df.loc[mascara_pago, "_errores"] += f"metodo_pago no reconocido; "
    log.info(f"Semántica 3 — metodo_pago no reconocido: {mascara_pago.sum()} registros")
 
    # ── Validación semántica 4: fecha_compra no futura ───────────────────────
    hoy = pd.Timestamp(datetime.now().date())
    mascara_fecha = df["fecha_compra"] > hoy
    df.loc[mascara_fecha, "_errores"] += "fecha_compra futura; "
    log.info(f"Semántica 4 — fecha futura: {mascara_fecha.sum()} registros")
 
    # ── Validación semántica 5: nombre no es numérico ────────────────────────
    mascara_nombre = df["nombre"].str.isnumeric()
    df.loc[mascara_nombre, "_errores"] += "nombre es numérico; "
    log.info(f"Semántica 5 — nombre numérico: {mascara_nombre.sum()} registros")
 
    # ── Separación ───────────────────────────────────────────────────────────
    df_errores = df[df["_errores"] != ""].copy()
    df_validos = df[df["_errores"] == ""].drop(columns=["_errores"])
    df_errores = df_errores.rename(columns={"_errores": "motivo_error"})
 
    log.info(f"Registros válidos:  {len(df_validos)}")
    log.info(f"Registros erróneos: {len(df_errores)}")
    log.info("── Validación finalizada ──")
 
    return df_validos, df_errores