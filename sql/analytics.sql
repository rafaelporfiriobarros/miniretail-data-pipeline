
-- MiniRetail Data Pipeline
-- Etapa 4: camada analitica
--
-- Fonte: retail.vendas
-- Granularidade: uma linha por venda/produto
--
-- Views comuns nao armazenam os resultados.
-- Os indicadores sao calculados sobre os dados atuais.


-- 1. Resumo executivo
CREATE OR REPLACE VIEW retail.vw_resumo_vendas AS
SELECT
    COUNT(*) AS total_vendas,
    COALESCE(
        SUM(valor_total),
        0
    )::NUMERIC(14, 2) AS faturamento_total,
    COALESCE(
        ROUND(AVG(valor_total), 2),
        0
    ) AS ticket_medio,
    COALESCE(
        SUM(quantidade),
        0
    ) AS unidades_vendidas
FROM retail.vendas;


-- 2. Faturamento mensal
CREATE OR REPLACE VIEW retail.vw_vendas_mensais AS
SELECT
    DATE_TRUNC(
        'month',
        data_venda
    )::DATE AS mes,
    COUNT(*) AS total_vendas,
    SUM(quantidade) AS unidades_vendidas,
    SUM(valor_total) AS faturamento_total,
    ROUND(
        AVG(valor_total),
        2
    ) AS ticket_medio
FROM retail.vendas
GROUP BY
    DATE_TRUNC('month', data_venda);


-- 3. Ranking de produtos
CREATE OR REPLACE VIEW retail.vw_ranking_produtos AS
SELECT
    id_produto,
    produto,
    categoria,
    COUNT(*) AS total_vendas,
    SUM(quantidade) AS unidades_vendidas,
    SUM(valor_total) AS faturamento_total,
    ROUND(
        AVG(valor_total),
        2
    ) AS valor_medio_por_venda
FROM retail.vendas
GROUP BY
    id_produto,
    produto,
    categoria;


-- 4. Participacao por categoria
CREATE OR REPLACE VIEW retail.vw_categorias AS
WITH faturamento_categoria AS (
    SELECT
        categoria,
        COUNT(*) AS total_vendas,
        SUM(quantidade) AS unidades_vendidas,
        SUM(valor_total) AS faturamento_total
    FROM retail.vendas
    GROUP BY categoria
)
SELECT
    categoria,
    total_vendas,
    unidades_vendidas,
    faturamento_total,
    ROUND(
        100.0 * faturamento_total
        / NULLIF(
            SUM(faturamento_total) OVER (),
            0
        ),
        2
    ) AS participacao_percentual
FROM faturamento_categoria;


-- 5. Faturamento diario
CREATE OR REPLACE VIEW retail.vw_vendas_diarias AS
SELECT
    data_venda,
    COUNT(*) AS total_vendas,
    SUM(quantidade) AS unidades_vendidas,
    SUM(valor_total) AS faturamento_total,
    ROUND(
        AVG(valor_total),
        2
    ) AS ticket_medio
FROM retail.vendas
GROUP BY data_venda;


-- 6. Resumo por produto e mes
CREATE OR REPLACE VIEW retail.vw_produtos_mensais AS
SELECT
    DATE_TRUNC(
        'month',
        data_venda
    )::DATE AS mes,
    id_produto,
    produto,
    categoria,
    COUNT(*) AS total_vendas,
    SUM(quantidade) AS unidades_vendidas,
    SUM(valor_total) AS faturamento_total
FROM retail.vendas
GROUP BY
    DATE_TRUNC('month', data_venda),
    id_produto,
    produto,
    categoria;
