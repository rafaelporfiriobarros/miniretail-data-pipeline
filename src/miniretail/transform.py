"""Validação e transformação de vendas."""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation


@dataclass(frozen=True)
class Sale:
    id_venda: int
    data_venda: date
    id_produto: int
    produto: str
    categoria: str
    quantidade: int
    preco_unitario: Decimal
    valor_total: Decimal


@dataclass(frozen=True)
class RejectedSale:
    row_number: int
    reason: str


def transform_sale(
    row: dict[str, str],
) -> Sale:
    """Converte e valida um registro de venda."""
    try:
        sale_id = int(row["id_venda"])
        sale_date = date.fromisoformat(row["data_venda"])
        product_id = int(row["id_produto"])
        product = row["produto"].strip()
        category = row["categoria"].strip()
        quantity = int(row["quantidade"])
        price = Decimal(row["preco_unitario"])
        total = Decimal(row["valor_total"])

    except (
        KeyError,
        TypeError,
        ValueError,
        InvalidOperation,
    ) as exc:
        raise ValueError("Campos ausentes ou tipos inválidos") from exc

    if sale_id <= 0 or product_id <= 0:
        raise ValueError("Identificadores devem ser positivos")

    if not product or not category:
        raise ValueError("Produto e categoria são obrigatórios")

    if len(product) > 100 or len(category) > 50:
        raise ValueError("Produto ou categoria excede o limite")

    if quantity <= 0:
        raise ValueError("Quantidade deve ser positiva")

    if not price.is_finite() or not total.is_finite():
        raise ValueError("Valores monetários devem ser finitos")

    if price < 0:
        raise ValueError("Preço não pode ser negativo")

    if price.as_tuple().exponent < -2:
        raise ValueError("Preço deve ter no máximo 2 casas decimais")

    if total.as_tuple().exponent < -2:
        raise ValueError("Total deve ter no máximo 2 casas decimais")

    if price >= Decimal(100000000):
        raise ValueError("Preço excede o limite do banco")

    if total >= Decimal(10000000000):
        raise ValueError("Total excede o limite do banco")

    if total != price * quantity:
        raise ValueError("Valor total inconsistente")

    return Sale(
        id_venda=sale_id,
        data_venda=sale_date,
        id_produto=product_id,
        produto=product,
        categoria=category,
        quantidade=quantity,
        preco_unitario=price,
        valor_total=total,
    )


def transform_sales(
    rows: list[dict[str, str]],
) -> tuple[list[Sale], list[RejectedSale]]:
    """Valida registros e separa rejeições."""
    valid_sales = []
    rejected_sales = []
    seen_ids = set()

    for row_number, row in enumerate(
        rows,
        start=2,
    ):
        try:
            sale = transform_sale(row)

            if sale.id_venda in seen_ids:
                raise ValueError("ID de venda duplicado no CSV")

            seen_ids.add(sale.id_venda)
            valid_sales.append(sale)

        except ValueError as exc:
            rejected_sales.append(
                RejectedSale(
                    row_number=row_number,
                    reason=str(exc),
                )
            )

    return valid_sales, rejected_sales
