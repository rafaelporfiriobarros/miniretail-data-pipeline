
-- MiniRetail Data Pipeline
-- Etapa 2: modelagem relacional

CREATE SCHEMA IF NOT EXISTS retail;

CREATE TABLE IF NOT EXISTS retail.vendas (
    id_venda INTEGER PRIMARY KEY,

    data_venda DATE NOT NULL,

    id_produto INTEGER NOT NULL,

    produto VARCHAR(100) NOT NULL,

    categoria VARCHAR(50) NOT NULL,

    quantidade INTEGER NOT NULL,

    preco_unitario NUMERIC(10, 2) NOT NULL,

    valor_total NUMERIC(12, 2) NOT NULL,

    CONSTRAINT ck_quantidade_positiva
        CHECK (quantidade > 0),

    CONSTRAINT ck_preco_nao_negativo
        CHECK (preco_unitario >= 0),

    CONSTRAINT ck_total_consistente
        CHECK (
            valor_total = quantidade * preco_unitario
        ),

    CONSTRAINT ck_produto_nao_vazio
        CHECK (length(trim(produto)) > 0),

    CONSTRAINT ck_categoria_nao_vazia
        CHECK (length(trim(categoria)) > 0)
);

CREATE INDEX IF NOT EXISTS idx_vendas_data
    ON retail.vendas (data_venda);
