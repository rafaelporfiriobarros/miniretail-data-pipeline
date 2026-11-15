"""Extração de vendas a partir de arquivos CSV."""

import csv
from pathlib import Path

from miniretail.generate_data import COLUMNS


def extract_sales(
    file_path: Path,
) -> list[dict[str, str]]:
    """Lê um CSV e retorna os registros."""
    if not file_path.is_file():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

    with file_path.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as file:
        reader = csv.DictReader(file)

        if reader.fieldnames != COLUMNS:
            raise ValueError(f"Cabeçalho CSV inválido. Esperado: {COLUMNS}")

        rows = list(reader)

    for row in rows:
        if None in row or any(value is None for value in row.values()):
            raise ValueError("CSV contém linhas com número incorreto de colunas")

    return rows
