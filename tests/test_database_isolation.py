"""Testes de isolamento do banco PostgreSQL."""


def test_uses_test_database(test_db_connection):
    """Confirma a conexao ao banco de testes."""

    with test_db_connection.cursor() as cursor:
        cursor.execute("SELECT current_database()")
        database_name = cursor.fetchone()[0]

    assert database_name == "miniretail_test"


def test_sales_table_exists(test_db_connection):
    """Confirma a existencia da tabela de vendas."""

    with test_db_connection.cursor() as cursor:
        cursor.execute("SELECT to_regclass('retail.vendas')")
        table_name = cursor.fetchone()[0]

    assert table_name == "retail.vendas"


def test_analytics_view_exists(test_db_connection):
    """Confirma a existencia da view executiva."""

    with test_db_connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT to_regclass(
                'retail.vw_resumo_vendas'
            )
            """
        )
        view_name = cursor.fetchone()[0]

    assert view_name == "retail.vw_resumo_vendas"
