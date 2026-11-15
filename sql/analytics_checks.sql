
-- MiniRetail Data Pipeline
-- Etapa 4: validacoes analiticas
--
-- Cada consulta deve retornar true.

-- 1. Total de vendas consistente
SELECT
    (
        SELECT total_vendas
        FROM retail.vw_resumo_vendas
    ) = (
        SELECT COUNT(*)
        FROM retail.vendas
    ) AS total_vendas_ok;


-- 2. Faturamento consistente
SELECT
    (
        SELECT faturamento_total
        FROM retail.vw_resumo_vendas
    ) = (
        SELECT COALESCE(SUM(valor_total), 0)
        FROM retail.vendas
    ) AS faturamento_ok;


-- 3. Soma mensal consistente
SELECT
    COALESCE(
        (SELECT SUM(faturamento_total)
         FROM retail.vw_vendas_mensais),
        0
    ) = (
        SELECT COALESCE(SUM(valor_total), 0)
        FROM retail.vendas
    ) AS faturamento_mensal_ok;


-- 4. Soma por categoria consistente
SELECT
    COALESCE(
        (SELECT SUM(faturamento_total)
         FROM retail.vw_categorias),
        0
    ) = (
        SELECT COALESCE(SUM(valor_total), 0)
        FROM retail.vendas
    ) AS faturamento_categoria_ok;


-- 5. Soma diaria consistente
SELECT
    COALESCE(
        (SELECT SUM(faturamento_total)
         FROM retail.vw_vendas_diarias),
        0
    ) = (
        SELECT COALESCE(SUM(valor_total), 0)
        FROM retail.vendas
    ) AS faturamento_diario_ok;


-- 6. Participacao das categorias
SELECT
    COALESCE(
        (
            SELECT ABS(
                SUM(participacao_percentual) - 100
            ) <= 0.05
            FROM retail.vw_categorias
        ),
        TRUE
    ) AS participacao_ok;
