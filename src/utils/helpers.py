"""Funciones auxiliares reutilizables en todo el proyecto."""

import logging
import time
from contextlib import contextmanager
from typing import Generator

logger = logging.getLogger(__name__)


def setup_logging(level: str = "INFO") -> None:
    """Configura el sistema de logging del proyecto.

    Parameters
    ----------
    level:
        Nivel de log (``"DEBUG"``, ``"INFO"``, ``"WARNING"``, ``"ERROR"``).
    """
    logging.basicConfig(
        format="%(asctime)s | %(levelname)-8s | %(name)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=getattr(logging, level.upper(), logging.INFO),
    )
    # basicConfig is a no-op when handlers already exist — set level explicitly
    logging.getLogger().setLevel(getattr(logging, level.upper(), logging.INFO))


@contextmanager
def timer(label: str = "Operación") -> Generator[None, None, None]:
    """Context manager que mide y muestra el tiempo de ejecución de un bloque.

    Example
    -------
    >>> with timer("Entrenamiento"):
    ...     model.fit(X_train, y_train)
    """
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        logger.info("%s completada en %.3f s", label, elapsed)


def flatten(nested: list) -> list:
    """Aplana una lista anidada de forma recursiva.

    Parameters
    ----------
    nested:
        Lista que puede contener sub-listas.

    Returns
    -------
    list
        Lista plana con todos los elementos.

    Example
    -------
    >>> flatten([[1, 2], [3, [4, 5]]])
    [1, 2, 3, 4, 5]
    """
    result: list = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result
