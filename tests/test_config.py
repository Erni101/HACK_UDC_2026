"""Tests del módulo src.config."""

from src.config import Settings


def test_settings_defaults():
    s = Settings()
    assert s.project_name == "HACK_UDC_2026"
    assert s.env == "development"
    assert isinstance(s.random_seed, int)
