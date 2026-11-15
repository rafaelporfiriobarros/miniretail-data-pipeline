"""Testes das regras de transformação."""

import pytest

from miniretail.generate_data import generate_sales
from miniretail.transform import (
    transform_sale,
    transform_sales,
)


def test_transform_valid_sale() -> None:
    row = generate_sales(1)[0]

    sale = transform_sale(row)

    assert sale.id_venda == 1
    assert sale.quantidade > 0


def test_reject_negative_quantity() -> None:
    row = generate_sales(1)[0]
    row["quantidade"] = "-2"

    with pytest.raises(
        ValueError,
        match="Quantidade deve ser positiva",
    ):
        transform_sale(row)


def test_reject_inconsistent_total() -> None:
    row = generate_sales(1)[0]
    row["valor_total"] = "999.99"

    with pytest.raises(
        ValueError,
        match="Valor total inconsistente",
    ):
        transform_sale(row)


def test_reject_duplicate_id() -> None:
    row = generate_sales(1)[0]

    valid, rejected = transform_sales([row, row.copy()])

    assert len(valid) == 1
    assert len(rejected) == 1
    assert "duplicado" in rejected[0].reason


def test_reject_invalid_date() -> None:
    row = generate_sales(1)[0]
    row["data_venda"] = "data-invalida"

    with pytest.raises(
        ValueError,
        match="Campos ausentes ou tipos inválidos",
    ):
        transform_sale(row)


def test_valid_sales_are_preserved() -> None:
    rows = generate_sales(3)
    rows[1]["quantidade"] = "0"

    valid, rejected = transform_sales(rows)

    assert len(valid) == 2
    assert len(rejected) == 1
