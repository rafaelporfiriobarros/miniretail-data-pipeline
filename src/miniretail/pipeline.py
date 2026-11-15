"""Orquestração do pipeline MiniRetail."""

from dataclasses import dataclass
from pathlib import Path

from miniretail.extract import extract_sales
from miniretail.load import load_sales
from miniretail.transform import transform_sales


@dataclass(frozen=True)
class PipelineResult:
    extracted: int
    valid: int
    rejected: int
    inserted: int


def get_pipeline_status() -> str:
    """Mantém a verificação inicial do projeto."""
    return "MiniRetail Data Pipeline - ambiente configurado"


def run_pipeline(
    csv_path: Path,
) -> PipelineResult:
    """Executa extracao, transformacao e carga."""

    rows = extract_sales(csv_path)

    valid_sales, rejected_sales = transform_sales(rows)

    for rejected in rejected_sales:
        print(f"REJEITADO linha {rejected.row_number}: {rejected.reason}")

    inserted = load_sales(valid_sales)

    return PipelineResult(
        extracted=len(rows),
        valid=len(valid_sales),
        rejected=len(rejected_sales),
        inserted=inserted,
    )


def main() -> None:
    """Executa o pipeline usando o CSV padrão."""
    result = run_pipeline(Path("data/vendas.csv"))

    print("\nResumo do pipeline")
    print(f"Extraídos: {result.extracted}")
    print(f"Válidos: {result.valid}")
    print(f"Rejeitados: {result.rejected}")
    print(f"Inseridos: {result.inserted}")


if __name__ == "__main__":
    main()
