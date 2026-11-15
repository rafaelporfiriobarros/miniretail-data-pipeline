"""Testes automatizados de qualidade de dados."""

import pytest

from miniretail.load import get_connection

QUALITY_CHECKS = {
    "duplicate_sale_ids": """
        SELECT COUNT(*)
        FROM (
            SELECT id_venda
            FROM retail.vendas
            GROUP BY id_venda
            HAVING COUNT(*) > 1
        ) AS duplicates
    """,
    "invalid_quantity": """
        SELECT COUNT(*)
        FROM retail.vendas
        WHERE quantidade <= 0
    """,
    "invalid_unit_price": """
        SELECT COUNT(*)
        FROM retail.vendas
        WHERE preco_unitario < 0
    """,
    "inconsistent_total": """
        SELECT COUNT(*)
        FROM retail.vendas
        WHERE valor_total <> quantidade * preco_unitario
    """,
    "empty_product": """
        SELECT COUNT(*)
        FROM retail.vendas
        WHERE TRIM(produto) = ''
    """,
    "empty_category": """
        SELECT COUNT(*)
        FROM retail.vendas
        WHERE TRIM(categoria) = ''
    """,
    "future_sale_date": """
        SELECT COUNT(*)
        FROM retail.vendas
        WHERE data_venda > CURRENT_DATE
    """,
}


@pytest.mark.parametrize(
    ("check_name", "query"),
    QUALITY_CHECKS.items(),
)
def test_data_quality(check_name, query):
    """Cada regra deve apresentar zero violacoes."""

    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT current_database()")
        database_name = cursor.fetchone()[0]

        assert database_name == "miniretail", (
            f"Auditoria conectada ao banco inesperado: {database_name}"
        )

        cursor.execute("SET TRANSACTION READ ONLY")
        cursor.execute(query)
        violations = cursor.fetchone()[0]

    assert violations == 0, f"Regra {check_name}: {violations} violacoes encontradas"
