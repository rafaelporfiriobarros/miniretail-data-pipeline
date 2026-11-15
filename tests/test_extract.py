"""Testes de extração CSV."""

import csv

import pytest

from miniretail.extract import extract_sales
from miniretail.generate_data import (
    COLUMNS,
    generate_sales,
    save_sales,
)


def test_extract_valid_csv(tmp_path) -> None:
    path = tmp_path / "vendas.csv"

    save_sales(generate_sales(5), path)

    rows = extract_sales(path)

    assert len(rows) == 5
    assert list(rows[0]) == COLUMNS


def test_extract_missing_file(tmp_path) -> None:
    path = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError):
        extract_sales(path)


def test_extract_invalid_header(tmp_path) -> None:
    path = tmp_path / "invalid.csv"
    path.write_text(
        "id,nome\n1,Produto\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="Cabeçalho CSV inválido",
    ):
        extract_sales(path)


def test_extract_invalid_column_count(tmp_path) -> None:
    path = tmp_path / "invalid.csv"

    with path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as file:
        writer = csv.writer(file)
        writer.writerow(COLUMNS)
        writer.writerow(["1", "2026-01-01"])

    with pytest.raises(
        ValueError,
        match="número incorreto de colunas",
    ):
        extract_sales(path)
