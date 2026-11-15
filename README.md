
# MiniRetail Data Pipeline

Projeto de Engenharia de Dados
com fundamentos de Engenharia de Software.

## Objetivo

Desenvolver um pipeline ETL para processar
vendas de uma pequena loja fictícia.

## Tecnologias

- Python 3.12
- UV
- PostgreSQL
- Docker
- SQL
- Pytest
- Ruff
- Git e GitHub

## Arquitetura planejada

CSV -> Python -> PostgreSQL -> SQL Analytics

## Estrutura

- `src/miniretail/`: código Python
- `tests/`: testes automatizados
- `sql/`: scripts SQL
- `docs/`: documentação
- `data/`: arquivos de entrada

## Configuração

Requisitos: Python 3.12 e UV.

```powershell
uv sync
```

## Executar testes

```powershell
uv run pytest -v
```

## Verificar qualidade

```powershell
uv run ruff check .
uv run ruff format --check .
```

## Estado do projeto

Etapa 1: configuração e fundamentos.

O pipeline ETL ainda não foi implementado.

## Próximas etapas

1. Modelagem e dados sintéticos
2. Implementação do ETL
3. SQL e indicadores
4. Testes e qualidade
5. Publicação e documentação final

## Dados

Todos os dados de negócio serão sintéticos.
