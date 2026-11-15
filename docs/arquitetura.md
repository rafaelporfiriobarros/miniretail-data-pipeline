# Arquitetura Técnica — MiniRetail Data Pipeline

## 1. Visão geral

O **MiniRetail Data Pipeline** é um projeto educacional de Engenharia de Dados que simula o processamento de vendas de uma empresa varejista fictícia.

O objetivo é demonstrar a construção de um pipeline **ETL (Extract, Transform, Load)** reproduzível, utilizando Python, PostgreSQL, SQL, Docker, testes automatizados e integração contínua.

A solução contempla geração de dados, extração, transformação, validação, armazenamento relacional e disponibilização de informações para análises de negócio.

**Todos os dados utilizados são sintéticos e não representam transações comerciais reais.**

## 2. Problema de negócio

Uma empresa varejista precisa transformar registros transacionais em informações estruturadas e confiáveis para apoiar decisões comerciais e operacionais.

O projeto busca responder às seguintes perguntas:

- Qual é o faturamento total do período?
- Como as vendas evoluem mensalmente?
- Quais produtos apresentam maior faturamento?
- Quais categorias contribuem mais para a receita?
- Qual é o volume total de unidades vendidas?
- Qual é o ticket médio das vendas?
- Os registros atendem às regras de qualidade estabelecidas?

A solução organiza os dados transacionais em uma base PostgreSQL e disponibiliza consultas SQL para acompanhar indicadores de desempenho.

## 3. Tecnologias utilizadas

| Tecnologia | Responsabilidade |
|---|---|
| Python 3.12 | Desenvolvimento e execução do pipeline ETL |
| UV | Gerenciamento de dependências e ambiente Python |
| PostgreSQL 17 | Armazenamento relacional e integridade dos dados |
| SQL | Modelagem, consultas analíticas e validações |
| Docker Compose | Provisionamento da infraestrutura local |
| Psycopg 3 | Integração entre Python e PostgreSQL |
| Pytest | Testes unitários e de integração |
| Ruff | Análise estática e formatação do código |
| Git | Controle de versão |
| GitHub | Hospedagem e versionamento do projeto |
| GitHub Actions | Integração contínua e execução automatizada dos testes |

## 4. Arquitetura e fluxo de processamento

O MiniRetail utiliza uma arquitetura ETL, na qual os dados são extraídos de um arquivo CSV, transformados e carregados em uma tabela relacional.

**Fluxo de processamento:**

```text
        GERADOR DE DADOS SINTÉTICOS
            generate_data.py
                   |
                   v
             data/vendas.csv
                   |
                   v
             EXTRAÇÃO (E)
               extract.py
                   |
                   v
            TRANSFORMAÇÃO (T)
              transform.py
                   |
                   v
               CARGA (L)
                load.py
                   |
                   v
              POSTGRESQL
             retail.vendas
                   |
                   v
            VIEWS ANALÍTICAS
            sql/analytics.sql
                   |
                   v
          INDICADORES DE NEGÓCIO
```

O módulo `pipeline.py` coordena as etapas de extração, transformação e carga.

A infraestrutura local é disponibilizada por meio do Docker Compose, enquanto o GitHub Actions automatiza a preparação de um ambiente temporário e a execução das verificações.

## 5. Camadas de processamento

### 5.1. Origem e geração dos dados

O módulo `generate_data.py` produz registros sintéticos de vendas de uma empresa varejista fictícia.

Os dados são armazenados no arquivo:

`data/vendas.csv`

O gerador utiliza uma semente fixa (`seed=42`), permitindo reproduzir o mesmo conjunto de registros.

Na configuração padrão, são geradas **1.000 vendas sintéticas**, distribuídas entre janeiro e março de 2026.

Cada registro contém informações sobre produto, categoria, data, quantidade, preço unitário e valor total.

### 5.2. Extração — Extract

O módulo `extract.py` realiza a leitura dos registros presentes no CSV.

Suas responsabilidades incluem:

- Localizar e abrir o arquivo de origem.
- Interpretar os registros CSV.
- Verificar a estrutura e a ordem esperada das colunas.
- Disponibilizar os dados para a etapa de transformação.

A extração não realiza a persistência dos dados no PostgreSQL.

### 5.3. Transformação — Transform

O módulo `transform.py` converte os registros extraídos em objetos Python tipados e aplica regras de validação.

Entre as verificações implementadas estão:

- Identificadores válidos.
- Quantidade de produtos maior que zero.
- Preço unitário não negativo.
- Produto e categoria preenchidos.
- Datas válidas.
- Valores monetários consistentes.
- Compatibilidade entre quantidade, preço unitário e valor total.
- Identificação de IDs duplicados entre os registros aceitos no processamento.

A consistência monetária segue a regra:

**Valor total = Quantidade × Preço unitário**

Os registros válidos são encaminhados à carga. Os registros rejeitados são separados e acompanhados de informações sobre o motivo da rejeição.

### 5.4. Carga — Load

O módulo `load.py` utiliza Psycopg 3 para realizar a comunicação com o PostgreSQL.

Os registros válidos são inseridos na tabela:

`retail.vendas`

A instrução SQL utiliza a cláusula:

`ON CONFLICT (id_venda) DO NOTHING`

Esse mecanismo impede a inserção de uma nova linha quando já existe um registro com o mesmo identificador de venda.

**Idempotência:** reprocessar o mesmo arquivo não deve criar vendas duplicadas na tabela.

Entretanto, a implementação atual não compara nem atualiza automaticamente os valores de vendas previamente cadastradas.

Portanto, a idempotência implementada está relacionada à prevenção de novas inserções para identificadores existentes, e não à sincronização de alterações nos registros.

### 5.5. Camada analítica — Analytics

O arquivo `sql/analytics.sql` define seis views analíticas no PostgreSQL:

| View | Finalidade |
|---|---|
| `retail.vw_resumo_vendas` | Indicadores consolidados das vendas |
| `retail.vw_vendas_mensais` | Evolução mensal das vendas |
| `retail.vw_ranking_produtos` | Ranking de desempenho dos produtos |
| `retail.vw_categorias` | Indicadores agrupados por categoria |
| `retail.vw_vendas_diarias` | Evolução diária das vendas |
| `retail.vw_produtos_mensais` | Desempenho mensal dos produtos |

Essas views permitem consultar indicadores sem repetir toda a lógica de agregação em cada análise.

## 6. Modelo de dados

O projeto utiliza uma tabela transacional principal:

`retail.vendas`

### 6.1. Estrutura da tabela

| Coluna | Tipo PostgreSQL | Descrição |
|---|---|---|
| `id_venda` | INTEGER | Identificador único da venda |
| `data_venda` | DATE | Data da transação |
| `id_produto` | INTEGER | Identificador do produto |
| `produto` | VARCHAR(100) | Nome do produto |
| `categoria` | VARCHAR(50) | Categoria comercial |
| `quantidade` | INTEGER | Quantidade de unidades vendidas |
| `preco_unitario` | NUMERIC(10,2) | Preço unitário |
| `valor_total` | NUMERIC(12,2) | Valor total da venda |

### 6.2. Integridade dos dados

A tabela possui chave primária na coluna `id_venda`.

Também utiliza restrições SQL para garantir:

- Quantidade positiva.
- Preço unitário não negativo.
- Consistência entre quantidade, preço e valor total.
- Produto não vazio.
- Categoria não vazia.

Existe ainda um índice sobre `data_venda`, destinado a apoiar consultas que utilizam a data como critério de filtragem.

Essas restrições complementam as validações realizadas na camada Python.

## 7. Indicadores de negócio

O conjunto sintético utilizado nas validações anteriores apresentou os seguintes resultados:

| Indicador | Resultado |
|---|---:|
| Total de vendas | 1.000 |
| Faturamento simulado | R$ 62.604,50 |
| Unidades vendidas | 5.588 |
| Ticket médio aproximado | R$ 62,60 |
| Período | Janeiro a março de 2026 |

Esses resultados são derivados dos dados sintéticos e servem para demonstrar a utilização das consultas analíticas.

Não devem ser interpretados como desempenho de uma empresa real.

## 8. Qualidade de dados e testes automatizados

O projeto utiliza Pytest para validar diferentes componentes da solução.

As verificações abrangem:

- Geração reproduzível de dados sintéticos.
- Estrutura e leitura do CSV.
- Regras de transformação.
- Rejeição de registros inválidos.
- Inserção de registros no PostgreSQL.
- Idempotência da carga.
- Integração entre os componentes do pipeline.
- Transações e rollback.
- Isolamento do banco de testes.
- Consistência dos indicadores analíticos.
- Qualidade dos dados armazenados.
- Permissões de segurança.

Na validação da Etapa 5, a suíte apresentou:

**48 testes automatizados aprovados.**

O projeto também utiliza Ruff para verificar a qualidade e a formatação do código Python.

### 8.1. Verificações de qualidade de dados

O arquivo `sql/data_quality_checks.sql` contempla verificações de:

- Identificadores de vendas duplicados.
- Quantidades inválidas.
- Preços unitários negativos.
- Totais inconsistentes.
- Produtos sem identificação textual.
- Categorias vazias.
- Datas de vendas posteriores à data atual.

Essas verificações complementam as restrições da tabela e as regras de transformação.

### 8.2. Isolamento dos ambientes

O projeto utiliza dois bancos PostgreSQL:

**`miniretail`**

Armazena os dados sintéticos e fornece as informações utilizadas nas análises.

**`miniretail_test`**

É utilizado nos testes de integração, transações e segurança.

Essa separação reduz o risco de modificações indevidas nos dados analíticos durante os testes.

Os testes analíticos e de qualidade consultam o banco principal, enquanto os testes de integração que realizam operações de escrita utilizam o banco de testes.

## 9. Segurança

O projeto implementa mecanismos básicos de segurança e demonstra a aplicação do princípio do menor privilégio.

### 9.1. Gerenciamento de credenciais

A conexão com o PostgreSQL utiliza variáveis de ambiente:

- `DATABASE_HOST`
- `DATABASE_PORT`
- `DATABASE_NAME`
- `DATABASE_USER`
- `DATABASE_PASSWORD`

O arquivo `.env` contém configurações locais e deve permanecer fora do controle de versão.

Credenciais reais não devem ser incluídas no código-fonte nem na documentação pública.

### 9.2. Roles de laboratório

O arquivo `sql/002_security_roles.sql` define duas roles:

**`miniretail_loader`**

Possui permissões de leitura e inserção na tabela `retail.vendas`, sem permissão de exclusão.

**`miniretail_reader`**

Possui permissão de leitura sobre as tabelas e views existentes no schema `retail` do banco `miniretail_test`.

Ambas são configuradas como `NOLOGIN`, sem privilégios administrativos.

Essas roles demonstram a separação de responsabilidades, mas ainda não substituem a conta administrativa utilizada pela aplicação.

A migração para contas de conexão restritas permanece como melhoria futura.

## 10. Integração contínua — GitHub Actions

O projeto utiliza o workflow:

`.github/workflows/ci.yml`

A automação é acionada em eventos de push e pull request direcionados à branch `main`, além de permitir execução manual.

O processo realiza:

1. Preparação do ambiente Ubuntu.
2. Configuração do Python 3.12 e UV.
3. Inicialização de um PostgreSQL 17 temporário.
4. Criação dos bancos `miniretail` e `miniretail_test`.
5. Aplicação do schema SQL.
6. Criação das views analíticas.
7. Configuração das roles de segurança.
8. Geração das vendas sintéticas.
9. Execução do pipeline ETL.
10. Verificação da carga de 1.000 vendas.
11. Validação do código com Ruff.
12. Execução dos testes automatizados com Pytest.

A primeira execução do GitHub Actions foi concluída com sucesso no commit `5fdb524`.

**Resultado observado:**

- Status: Success.
- Duração total: 22 segundos.
- Job: Ruff + Pytest + PostgreSQL.

A integração contínua permite verificar o projeto em um ambiente temporário e reproduzível, independente do banco local utilizado durante o desenvolvimento.

## 11. Limitações conhecidas

O MiniRetail é um projeto educacional e apresenta limitações que devem ser consideradas:

- Utiliza uma única tabela transacional principal.
- Trabalha exclusivamente com dados sintéticos.
- Não possui modelagem dimensional completa.
- Não utiliza um orquestrador externo.
- Não implementa processamento em tempo real ou streaming.
- Não possui mecanismo automático de atualização de vendas existentes.
- Não mantém histórico persistente de execuções do pipeline.
- Não implementa observabilidade centralizada.
- As roles restritas ainda não são utilizadas como identidades de conexão da aplicação.
- Não possui processo de implantação em produção.

Essas limitações delimitam o escopo atual e ajudam a orientar futuras evoluções.

## 12. Possíveis evoluções

As próximas versões poderão incorporar:

- **Modelagem dimensional:** criação de tabelas fato e dimensão.
- **Observabilidade:** logs estruturados, métricas e monitoramento de falhas.
- **Auditoria:** histórico de execuções, registros aceitos e rejeitados.
- **Qualidade de dados:** relatórios automatizados e acompanhamento histórico.
- **Carga incremental:** processamento de novos registros e tratamento de atualizações.
- **Orquestração:** agendamento e gerenciamento de dependências entre tarefas.
- **Business Intelligence:** integração com Power BI.
- **Segurança:** utilização de contas PostgreSQL com privilégios mínimos.
- **CI/CD:** ampliação das verificações automatizadas e implantação controlada.

## 13. Conclusão

O MiniRetail Data Pipeline demonstra a implementação de uma solução de Engenharia de Dados que conecta geração de dados sintéticos, processamento ETL, armazenamento relacional, validações de qualidade, consultas analíticas e testes automatizados.

O projeto foi desenvolvido com foco em fundamentos de Engenharia de Software e Engenharia de Dados, incluindo modularização, integridade, idempotência de inserção, isolamento de testes, versionamento e integração contínua.

Mais do que gerar indicadores, a solução demonstra a importância de construir processos de dados **reproduzíveis, testáveis, documentados e preparados para evolução**.