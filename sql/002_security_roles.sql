
-- MiniRetail: roles de seguranca
-- Executar inicialmente apenas no banco miniretail_test.
-- Roles sao objetos globais da instancia PostgreSQL.

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_roles
        WHERE rolname = 'miniretail_loader'
    ) THEN
        CREATE ROLE miniretail_loader
            NOLOGIN
            NOSUPERUSER
            NOCREATEDB
            NOCREATEROLE
            NOREPLICATION;
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_roles
        WHERE rolname = 'miniretail_reader'
    ) THEN
        CREATE ROLE miniretail_reader
            NOLOGIN
            NOSUPERUSER
            NOCREATEDB
            NOCREATEROLE
            NOREPLICATION;
    END IF;
END
$$;

-- Remove possiveis privilegios herdados de PUBLIC.
REVOKE ALL ON DATABASE miniretail_test FROM PUBLIC;
REVOKE ALL ON SCHEMA retail FROM PUBLIC;

-- Permissoes de conexao.
GRANT CONNECT ON DATABASE miniretail_test
    TO miniretail_loader, miniretail_reader;

-- Acesso ao schema.
GRANT USAGE ON SCHEMA retail
    TO miniretail_loader, miniretail_reader;

-- O pipeline pode consultar e inserir vendas.
GRANT SELECT, INSERT ON retail.vendas
    TO miniretail_loader;

-- O leitor pode consultar as views analiticas.
GRANT SELECT ON ALL TABLES IN SCHEMA retail
    TO miniretail_reader;
