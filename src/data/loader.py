"""Funciones de carga de datos."""

from pathlib import Path
from typing import Optional

import pandas as pd


def load_dataset(path: str, encoding: str = "utf-8") -> pd.DataFrame:
    """Carga un dataset desde *path* y devuelve un DataFrame.

    Parameters
    ----------
    path:
        Ruta al archivo (CSV, JSON o Excel). Relativa a la raíz del proyecto.
    encoding:
        Codificación del archivo de texto. Por defecto ``"utf-8"``.

    Returns
    -------
    pd.DataFrame
        DataFrame con los datos cargados.

    Raises
    ------
    FileNotFoundError
        Si el archivo no existe.
    ValueError
        Si el formato del archivo no está soportado.
    """
    file = Path(path)
    if not file.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {file}")

    suffix = file.suffix.lower()
    loaders = {
        ".csv": lambda p: pd.read_csv(p, encoding=encoding),
        ".json": lambda p: pd.read_json(p, encoding=encoding),
        ".xlsx": lambda p: pd.read_excel(p),
        ".xls": lambda p: pd.read_excel(p),
        ".parquet": lambda p: pd.read_parquet(p),
    }

    if suffix not in loaders:
        raise ValueError(
            f"Formato no soportado: '{suffix}'. "
            f"Formatos válidos: {list(loaders.keys())}"
        )

    return loaders[suffix](file)


def split_dataset(
    df: pd.DataFrame,
    test_size: float = 0.2,
    random_state: Optional[int] = 42,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Divide *df* en conjuntos de entrenamiento y test.

    Parameters
    ----------
    df:
        DataFrame completo.
    test_size:
        Proporción del conjunto de test (0–1). Por defecto ``0.2``.
    random_state:
        Semilla para reproducibilidad.

    Returns
    -------
    tuple[pd.DataFrame, pd.DataFrame]
        ``(train_df, test_df)``
    """
    from sklearn.model_selection import train_test_split  # importación diferida: evita requerir sklearn cuando sólo se usa load_dataset

    train_df, test_df = train_test_split(df, test_size=test_size, random_state=random_state)
    return train_df.reset_index(drop=True), test_df.reset_index(drop=True)
