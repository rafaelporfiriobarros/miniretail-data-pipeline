
# Requisitos — MiniRetail Data Pipeline

## Problema de negócio

Uma pequena loja precisa consolidar vendas
registradas em arquivos CSV.

## Objetivo

Construir um pipeline ETL simples que
transforme dados brutos em informações
confiáveis para análise comercial.

## Requisitos funcionais

- RF01: Ler arquivos CSV de vendas.
- RF02: Validar campos obrigatórios.
- RF03: Identificar vendas duplicadas.
- RF04: Carregar vendas válidas no PostgreSQL.
- RF05: Gerar indicadores comerciais.

## Requisitos não funcionais

- RNF01: Código Python modular.
- RNF02: Testes automatizados.
- RNF03: Carga idempotente.
- RNF04: Configurações sensíveis fora do Git.
- RNF05: Execução reproduzível.

## Regras de negócio

- Cada venda possui um ID único.
- Quantidade deve ser maior que zero.
- Preço unitário não pode ser negativo.
- Valor total = quantidade * preço unitário.
- Registros inválidos não entram na base válida.
- Vendas duplicadas não são contabilizadas duas vezes.

## Fora do escopo

- Interface web.
- Machine Learning.
- Processamento em tempo real.
- Cloud.
- Orquestração com Airflow.

## Critérios de aceite finais

- Pipeline processa dados sintéticos.
- Dados inválidos são identificados.
- Reexecuções não duplicam vendas.
- Indicadores SQL produzem resultados corretos.
- Testes automatizados passam.
- README permite reproduzir o projeto.
