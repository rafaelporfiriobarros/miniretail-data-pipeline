"""Fixtures compartilhadas para testes de integração."""

import os

import psycopg
import pytest

TEST_DATABASE_NAME = "miniretail_test"


@pytest.fixture
def test_db_connection():
    """Conecta exclusivamente ao banco de testes."""

    required = (
        "DATABASE_HOST",
        "DATABASE_PORT",
        "DATABASE_USER",
        "DATABASE_PASSWORD",
    )

    missing = [name for name in required if not os.getenv(name)]

    if missing:
        pytest.fail("Variaveis de ambiente ausentes: " + ", ".join(missing))

    with psycopg.connect(
        host=os.environ["DATABASE_HOST"],
        port=int(os.environ["DATABASE_PORT"]),
        dbname=TEST_DATABASE_NAME,
        user=os.environ["DATABASE_USER"],
        password=os.environ["DATABASE_PASSWORD"],
        connect_timeout=5,
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT current_database()")
            database_name = cursor.fetchone()[0]

        if database_name != TEST_DATABASE_NAME:
            raise RuntimeError("Conexao insegura: banco inesperado")

        yield connection
