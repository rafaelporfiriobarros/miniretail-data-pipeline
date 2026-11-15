"""Testes de integração com transações PostgreSQL."""

import pytest
from psycopg.errors import CheckViolation

INSERT_SALE_SQL = """
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
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (id_venda) DO NOTHING
"""


def make_sale(sale_id, quantity=2, total="20.00"):
    """Cria uma venda sintética para testes."""

    return (
        sale_id,
        "2026-01-15",
        101,
        "Produto Teste",
        "Alimentos",
        quantity,
        "10.00",
        total,
    )


def count_sale(connection, sale_id):
    """Conta registros por identificador."""

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM retail.vendas
            WHERE id_venda = %s
            """,
            (sale_id,),
        )
        return cursor.fetchone()[0]


def test_insert_sale_and_rollback(test_db_connection):
    """Insere uma venda e desfaz a transacao."""

    connection = test_db_connection
    sale_id = 900001

    try:
        assert count_sale(connection, sale_id) == 0

        with connection.cursor() as cursor:
            cursor.execute(
                INSERT_SALE_SQL,
                make_sale(sale_id),
            )

        assert count_sale(connection, sale_id) == 1

    finally:
        connection.rollback()

    assert count_sale(connection, sale_id) == 0
    connection.rollback()


def test_insert_is_idempotent(test_db_connection):
    """Reexecutar a insercao nao duplica a venda."""

    connection = test_db_connection
    sale_id = 900002

    try:
        assert count_sale(connection, sale_id) == 0

        with connection.cursor() as cursor:
            cursor.execute(
                INSERT_SALE_SQL,
                make_sale(sale_id),
            )
            first_insert = cursor.rowcount

            cursor.execute(
                INSERT_SALE_SQL,
                make_sale(sale_id),
            )
            second_insert = cursor.rowcount

        assert first_insert == 1
        assert second_insert == 0
        assert count_sale(connection, sale_id) == 1

    finally:
        connection.rollback()


def test_invalid_sale_rolls_back(test_db_connection):
    """Uma venda invalida impede a carga parcial."""

    connection = test_db_connection
    valid_id = 900003
    invalid_id = 900004

    try:
        assert count_sale(connection, valid_id) == 0
        assert count_sale(connection, invalid_id) == 0

        with pytest.raises(CheckViolation), connection.cursor() as cursor:
            cursor.execute(
                INSERT_SALE_SQL,
                make_sale(valid_id),
            )

            cursor.execute(
                INSERT_SALE_SQL,
                make_sale(
                    invalid_id,
                    quantity=-2,
                    total="-20.00",
                ),
            )

    finally:
        connection.rollback()

    assert count_sale(connection, valid_id) == 0
    assert count_sale(connection, invalid_id) == 0
    connection.rollback()
