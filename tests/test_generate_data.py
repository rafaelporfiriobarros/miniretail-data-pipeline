"""Testes do gerador de dados sintéticos."""

import csv
from decimal import Decimal

import pytest

from miniretail.generate_data import (
    COLUMNS,
    generate_sales,
    save_sales,
)


def test_generate_exactly_1000_sales() -> None:
    sales = generate_sales(total=1000)

    assert len(sales) == 1000


def test_sale_ids_are_unique() -> None:
    sales = generate_sales(total=1000)

    ids = [sale["id_venda"] for sale in sales]

    assert len(ids) == len(set(ids))


def test_sales_are_reproducible() -> None:
    first = generate_sales(total=100, seed=42)
    second = generate_sales(total=100, seed=42)

    assert first == second


def test_sales_have_valid_values() -> None:
    sales = generate_sales(total=1000)

    for sale in sales:
        quantity = int(sale["quantidade"])
        price = Decimal(sale["preco_unitario"])
        total = Decimal(sale["valor_total"])

        assert quantity > 0
        assert price >= 0
        assert total == price * quantity


def test_invalid_total_raises_error() -> None:
    with pytest.raises(
        ValueError,
        match="total deve ser maior que zero",
    ):
        generate_sales(total=0)


def test_csv_is_created(tmp_path) -> None:
    output = tmp_path / "vendas.csv"

    sales = generate_sales(total=10)

    save_sales(sales, output)

    assert output.exists()

    with output.open(
        encoding="utf-8",
        newline="",
    ) as file:
        reader = csv.DictReader(file)
        rows = list(reader)

        assert reader.fieldnames == COLUMNS
        assert len(rows) == 10
