"""Testes iniciais do MiniRetail."""

from miniretail import __version__
from miniretail.pipeline import get_pipeline_status


def test_project_version() -> None:
    assert __version__ == "0.1.0"


def test_pipeline_status() -> None:
    result = get_pipeline_status()

    assert result == ("MiniRetail Data Pipeline - ambiente configurado")
