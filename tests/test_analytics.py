"""Testes de integração da camada analítica."""

import os

import pytest

from miniretail.load import get_connection


def require_database() -> None:
    """Pula testes quando o banco não foi configurado."""
    required = (
        "DATABASE_HOST",
        "DATABASE_PORT",
        "DATABASE_NAME",
        "DATABASE_USER",
        "DATABASE_PASSWORD",
    )

    if not all(os.getenv(name) for name in required):
        pytest.skip("Variáveis de banco não configuradas")


@pytest.fixture
def connection():
    """Abre conexão com o PostgreSQL."""
    require_database()

    with get_connection() as conn:
        yield conn


def test_analytics_total_sales(connection) -> None:
    """Valida a quantidade total de vendas."""
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT total_vendas
            FROM retail.vw_resumo_vendas
            """
        )
        analytics_total = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM retail.vendas")
        source_total = cursor.fetchone()[0]

    assert analytics_total == source_total


def test_analytics_revenue(connection) -> None:
    """Valida o faturamento total."""
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT faturamento_total
            FROM retail.vw_resumo_vendas
            """
        )
        analytics_revenue = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT COALESCE(
                SUM(valor_total),
                0
            )
            FROM retail.vendas
            """
        )
        source_revenue = cursor.fetchone()[0]

    assert analytics_revenue == source_revenue


def test_monthly_revenue(connection) -> None:
    """Valida a soma do faturamento mensal."""
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT COALESCE(
                SUM(faturamento_total),
                0
            )
            FROM retail.vw_vendas_mensais
            """
        )
        monthly_revenue = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT COALESCE(
                SUM(valor_total),
                0
            )
            FROM retail.vendas
            """
        )
        source_revenue = cursor.fetchone()[0]

    assert monthly_revenue == source_revenue


def test_category_revenue(connection) -> None:
    """Valida a soma do faturamento por categoria."""
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT COALESCE(
                SUM(faturamento_total),
                0
            )
            FROM retail.vw_categorias
            """
        )
        category_revenue = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT COALESCE(
                SUM(valor_total),
                0
            )
            FROM retail.vendas
            """
        )
        source_revenue = cursor.fetchone()[0]

    assert category_revenue == source_revenue


def test_daily_revenue(connection) -> None:
    """Valida a soma do faturamento diario."""
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT COALESCE(
                SUM(faturamento_total),
                0
            )
            FROM retail.vw_vendas_diarias
            """
        )
        daily_revenue = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT COALESCE(
                SUM(valor_total),
                0
            )
            FROM retail.vendas
            """
        )
        source_revenue = cursor.fetchone()[0]

    assert daily_revenue == source_revenue
