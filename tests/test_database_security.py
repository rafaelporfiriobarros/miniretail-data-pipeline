"""Testes automatizados de seguranca PostgreSQL."""

import pytest

ROLES = (
    "miniretail_loader",
    "miniretail_reader",
)


@pytest.mark.parametrize("role_name", ROLES)
def test_role_has_no_administrative_privileges(
    test_db_connection,
    role_name,
):
    """Roles da aplicacao nao devem ser administradoras."""

    with test_db_connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                rolcanlogin,
                rolsuper,
                rolcreatedb,
                rolcreaterole
            FROM pg_roles
            WHERE rolname = %s
            """,
            (role_name,),
        )
        result = cursor.fetchone()

    assert result is not None
    assert result == (False, False, False, False)


@pytest.mark.parametrize(
    ("role_name", "object_name", "privilege", "expected"),
    [
        (
            "miniretail_loader",
            "retail.vendas",
            "INSERT",
            True,
        ),
        (
            "miniretail_loader",
            "retail.vendas",
            "SELECT",
            True,
        ),
        (
            "miniretail_loader",
            "retail.vendas",
            "DELETE",
            False,
        ),
        (
            "miniretail_reader",
            "retail.vw_resumo_vendas",
            "SELECT",
            True,
        ),
        (
            "miniretail_reader",
            "retail.vendas",
            "INSERT",
            False,
        ),
    ],
    ids=[
        "loader-can-insert",
        "loader-can-select",
        "loader-cannot-delete",
        "reader-can-select-view",
        "reader-cannot-insert",
    ],
)
def test_table_privileges(
    test_db_connection,
    role_name,
    object_name,
    privilege,
    expected,
):
    """Confirma as permissoes esperadas para cada role."""

    with test_db_connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT has_table_privilege(
                %s, %s, %s
            )
            """,
            (role_name, object_name, privilege),
        )
        actual = cursor.fetchone()[0]

    assert actual is expected
