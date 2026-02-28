"""Tests del módulo src.data.loader."""

from pathlib import Path

import pandas as pd
import pytest

from src.data.loader import load_dataset, split_dataset


class TestLoadDataset:
    def test_load_csv(self, tmp_path: Path, sample_df: pd.DataFrame):
        csv_file = tmp_path / "test.csv"
        sample_df.to_csv(csv_file, index=False)
        df = load_dataset(str(csv_file))
        assert isinstance(df, pd.DataFrame)
        assert df.shape == sample_df.shape

    def test_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            load_dataset("data/raw/no_existe.csv")

    def test_unsupported_format(self, tmp_path: Path):
        bad_file = tmp_path / "datos.txt"
        bad_file.write_text("hello")
        with pytest.raises(ValueError, match="Formato no soportado"):
            load_dataset(str(bad_file))


class TestSplitDataset:
    def test_split_sizes(self, sample_df: pd.DataFrame):
        train, test = split_dataset(sample_df, test_size=0.2)
        assert len(train) + len(test) == len(sample_df)
        assert len(test) == pytest.approx(len(sample_df) * 0.2, abs=1)

    def test_split_no_overlap(self, sample_df: pd.DataFrame):
        train, test = split_dataset(sample_df, test_size=0.3, random_state=0)
        train_ids = set(train["id"])
        test_ids = set(test["id"])
        assert train_ids.isdisjoint(test_ids)
