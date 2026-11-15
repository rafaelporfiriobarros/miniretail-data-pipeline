"""Testes de integração do pipeline ETL completo."""

import pytest

from miniretail.generate_data import generate_sales, save_sales
from miniretail.pipeline import run_pipeline

TEST_IDS = (910001, 910002)


@pytest.fixture
def pipeline_test_environment(
    monkeypatch,
    tmp_path,
    test_db_connection,
):
    """Prepara dados e garante isolamento do banco."""

    connection = test_db_connection

    with connection.cursor() as cursor:
        cursor.execute("SELECT current_database()")
        database_name = cursor.fetchone()[0]

    if database_name != "miniretail_test":
        pytest.fail("Banco de testes incorreto")

    monkeypatch.setenv(
        "DATABASE_NAME",
        "miniretail_test",
    )

    def cleanup():
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM retail.vendas
                WHERE id_venda = ANY(%s)
                """,
                (list(TEST_IDS),),
            )
        connection.commit()

    # Remover somente os IDs reservados aos testes.
    cleanup()

    try:
        sales = generate_sales(total=2, seed=42)

        for sale, sale_id in zip(
            sales,
            TEST_IDS,
            strict=True,
        ):
            sale["id_venda"] = str(sale_id)

        csv_path = tmp_path / "vendas_integracao.csv"
        save_sales(sales, csv_path)

        yield {
            "connection": connection,
            "csv_path": csv_path,
            "sales": sales,
        }

    finally:
        connection.rollback()
        cleanup()


def count_test_sales(connection):
    """Conta somente as vendas reservadas aos testes."""

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM retail.vendas
            WHERE id_venda = ANY(%s)
            """,
            (list(TEST_IDS),),
        )
        return cursor.fetchone()[0]


def test_pipeline_inserts_valid_sales(
    pipeline_test_environment,
):
    """O pipeline carrega vendas validas."""

    environment = pipeline_test_environment

    result = run_pipeline(environment["csv_path"])

    assert result.extracted == 2
    assert result.valid == 2
    assert result.rejected == 0
    assert result.inserted == 2

    assert count_test_sales(environment["connection"]) == 2


def test_pipeline_is_idempotent(
    pipeline_test_environment,
):
    """Executar duas vezes nao duplica registros."""

    environment = pipeline_test_environment

    first = run_pipeline(environment["csv_path"])
    second = run_pipeline(environment["csv_path"])

    assert first.inserted == 2
    assert second.inserted == 0

    assert count_test_sales(environment["connection"]) == 2


def test_pipeline_rejects_invalid_sale(
    pipeline_test_environment,
):
    """Registros invalidos nao chegam ao banco."""

    environment = pipeline_test_environment

    sales = environment["sales"]
    sales[1]["quantidade"] = "-5"

    save_sales(sales, environment["csv_path"])

    result = run_pipeline(environment["csv_path"])

    assert result.extracted == 2
    assert result.valid == 1
    assert result.rejected == 1
    assert result.inserted == 1

    assert count_test_sales(environment["connection"]) == 1
