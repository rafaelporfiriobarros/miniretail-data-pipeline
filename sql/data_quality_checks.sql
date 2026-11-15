
-- MiniRetail: auditoria de qualidade de dados
-- Todas as consultas sao somente leitura.

SELECT
    'duplicate_sale_ids' AS check_name,
    COUNT(*) AS violations
FROM (
    SELECT id_venda
    FROM retail.vendas
    GROUP BY id_venda
    HAVING COUNT(*) > 1
) AS duplicates

UNION ALL

SELECT
    'invalid_quantity',
    COUNT(*)
FROM retail.vendas
WHERE quantidade <= 0

UNION ALL

SELECT
    'invalid_unit_price',
    COUNT(*)
FROM retail.vendas
WHERE preco_unitario < 0

UNION ALL

SELECT
    'inconsistent_total',
    COUNT(*)
FROM retail.vendas
WHERE valor_total <> quantidade * preco_unitario

UNION ALL

SELECT
    'empty_product',
    COUNT(*)
FROM retail.vendas
WHERE TRIM(produto) = ''

UNION ALL

SELECT
    'empty_category',
    COUNT(*)
FROM retail.vendas
WHERE TRIM(categoria) = ''

UNION ALL

SELECT
    'future_sale_date',
    COUNT(*)
FROM retail.vendas
WHERE data_venda > CURRENT_DATE

ORDER BY check_name;
