"""Punto de entrada principal del proyecto."""

from src.config import settings
from src.data.loader import load_dataset
from src.utils.helpers import timer


def main() -> None:
    """Ejecuta el pipeline completo."""
    print(f"Proyecto: {settings.project_name}")
    print(f"Entorno:  {settings.env}")

    with timer("Carga de datos"):
        df = load_dataset(settings.data_path)

    print(f"Dataset cargado: {df.shape[0]} filas × {df.shape[1]} columnas")
    # TODO: añadir preprocesado, modelo y evaluación


if __name__ == "__main__":
    main()
