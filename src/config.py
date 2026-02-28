"""Configuración global del proyecto.

Lee variables de entorno desde el archivo .env (si existe).
Copia .env.example → .env y rellena los valores antes de ejecutar.
"""

from pathlib import Path
import os

from dotenv import load_dotenv

# Carga .env desde la raíz del proyecto (no falla si no existe)
load_dotenv(Path(__file__).resolve().parents[1] / ".env")


class Settings:
    """Parámetros de configuración leídos de variables de entorno."""

    project_name: str = os.getenv("PROJECT_NAME", "HACK_UDC_2026")
    env: str = os.getenv("ENV", "development")
    data_path: str = os.getenv("DATA_PATH", "data/raw/dataset.csv")
    random_seed: int = int(os.getenv("RANDOM_SEED", "42"))
    log_level: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()
