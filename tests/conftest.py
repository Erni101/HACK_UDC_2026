"""Fixtures compartidas por todos los tests."""

import pandas as pd
import pytest


@pytest.fixture
def sample_df() -> pd.DataFrame:
    """DataFrame de muestra para usar en los tests."""
    return pd.DataFrame(
        {
            "id": range(1, 11),
            "valor": [10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0],
            "categoria": ["a", "b", "a", "b", "a", "b", "a", "b", "a", "b"],
        }
    )
