"""Testes da carga PostgreSQL."""

from miniretail import load
from miniretail.generate_data import generate_sales
from miniretail.transform import transform_sale


def test_load_empty_sales() -> None:
    assert load.load_sales([]) == 0


def test_load_counts_inserted_rows(monkeypatch) -> None:
    class FakeCursor:
        rowcount = 1

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def execute(self, query, params):
            assert "ON CONFLICT" in query
            assert len(params) == 8

    class FakeConnection:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def cursor(self):
            return FakeCursor()

    monkeypatch.setattr(
        load,
        "get_connection",
        lambda: FakeConnection(),
    )

    sales = [transform_sale(row) for row in generate_sales(3)]

    assert load.load_sales(sales) == 3
