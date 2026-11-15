"""Geração de vendas sintéticas para o MiniRetail."""

import csv
import random
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path

PRODUCTS = [
    (101, "Arroz 5kg", "Alimentos", Decimal("24.90")),
    (102, "Feijao 1kg", "Alimentos", Decimal("8.50")),
    (103, "Cafe 500g", "Bebidas", Decimal("18.90")),
    (104, "Leite 1L", "Bebidas", Decimal("5.20")),
    (105, "Detergente", "Limpeza", Decimal("2.80")),
    (106, "Sabao em po", "Limpeza", Decimal("14.50")),
    (107, "Shampoo", "Higiene", Decimal("12.90")),
    (108, "Sabonete", "Higiene", Decimal("3.50")),
]

COLUMNS = [
    "id_venda",
    "data_venda",
    "id_produto",
    "produto",
    "categoria",
    "quantidade",
    "preco_unitario",
    "valor_total",
]


def generate_sales(
    total: int = 1000,
    seed: int = 42,
) -> list[dict[str, str]]:
    """Gera registros de vendas válidos e reproduzíveis."""
    if total <= 0:
        raise ValueError("total deve ser maior que zero")

    rng = random.Random(seed)

    start_date = date(2026, 1, 1)
    sales = []

    for sale_id in range(1, total + 1):
        product_id, name, category, price = rng.choice(PRODUCTS)

        quantity = rng.randint(1, 10)
        sale_date = start_date + timedelta(days=rng.randint(0, 89))

        total_value = price * quantity

        sales.append(
            {
                "id_venda": str(sale_id),
                "data_venda": sale_date.isoformat(),
                "id_produto": str(product_id),
                "produto": name,
                "categoria": category,
                "quantidade": str(quantity),
                "preco_unitario": f"{price:.2f}",
                "valor_total": f"{total_value:.2f}",
            }
        )

    return sales


def save_sales(
    sales: list[dict[str, str]],
    output_path: Path,
) -> None:
    """Salva os registros em CSV."""
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=COLUMNS,
        )

        writer.writeheader()
        writer.writerows(sales)


def main() -> None:
    """Gera o dataset padrão do projeto."""
    output_path = Path("data/vendas.csv")

    sales = generate_sales(
        total=1000,
        seed=42,
    )

    save_sales(sales, output_path)

    print(f"Arquivo criado: {output_path}")
    print(f"Total de vendas: {len(sales)}")


if __name__ == "__main__":
    main()
