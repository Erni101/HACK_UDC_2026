"""Tests del módulo src.utils.helpers."""

import logging
import time

import pytest

from src.utils.helpers import flatten, setup_logging, timer


class TestFlatten:
    def test_already_flat(self):
        assert flatten([1, 2, 3]) == [1, 2, 3]

    def test_one_level_nested(self):
        assert flatten([[1, 2], [3, 4]]) == [1, 2, 3, 4]

    def test_deep_nested(self):
        assert flatten([[1, [2, [3]]]]) == [1, 2, 3]

    def test_empty(self):
        assert flatten([]) == []

    def test_mixed_types(self):
        assert flatten([[1, "a"], [True]]) == [1, "a", True]


class TestTimer:
    def test_timer_logs_elapsed(self, caplog):
        setup_logging("DEBUG")
        with caplog.at_level(logging.INFO, logger="src.utils.helpers"):
            with timer("test"):
                time.sleep(0.01)
        assert any("test" in record.message for record in caplog.records)

    def test_timer_reraises_exception(self):
        with pytest.raises(ValueError, match="boom"):
            with timer("operación con error"):
                raise ValueError("boom")


class TestSetupLogging:
    def test_invalid_level_defaults_to_info(self):
        # No debe lanzar excepción con nivel inválido
        setup_logging("INVALID_LEVEL")
        root = logging.getLogger()
        assert root.level == logging.INFO
