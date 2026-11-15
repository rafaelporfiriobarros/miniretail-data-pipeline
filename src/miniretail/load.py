"""Carregamento de vendas no PostgreSQL."""

import os

import psycopg

from miniretail.transform import Sale


def get_connection() -> psycopg.Connection:
    """Cria conexão usando variáveis de ambiente."""
    required = [
        "DATABASE_HOST",
        "DATABASE_PORT",
        "DATABASE_NAME",
        "DATABASE_USER",
        "DATABASE_PASSWORD",
    ]

    missing = [name for name in required if not os.getenv(name)]

    if missing:
        raise ValueError("Variáveis de ambiente ausentes: " + ", ".join(missing))

    return psycopg.connect(
        host=os.environ["DATABASE_HOST"],
        port=int(os.environ["DATABASE_PORT"]),
        dbname=os.environ["DATABASE_NAME"],
        user=os.environ["DATABASE_USER"],
        password=os.environ["DATABASE_PASSWORD"],
        connect_timeout=5,
    )


def load_sales(
    sales: list[Sale],
) -> int:
    """Insere vendas novas e ignora IDs existentes."""
    if not sales:
        return 0

    query = """
        INSERT INTO retail.vendas (
            id_venda,
            data_venda,
            id_produto,
            produto,
            categoria,
            quantidade,
            preco_unitario,
            valor_total
        )
        VALUES (
            %s, %s, %s, %s,
            %s, %s, %s, %s
        )
        ON CONFLICT (id_venda) DO NOTHING
    """

    inserted = 0

    with get_connection() as connection, connection.cursor() as cursor:
        for sale in sales:
            cursor.execute(
                query,
                (
                    sale.id_venda,
                    sale.data_venda,
                    sale.id_produto,
                    sale.produto,
                    sale.categoria,
                    sale.quantidade,
                    sale.preco_unitario,
                    sale.valor_total,
                ),
            )

            inserted += cursor.rowcount

    return inserted
