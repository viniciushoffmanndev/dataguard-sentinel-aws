-- Schema para o DataGuard Sentinel
-- Foco: Rastreabilidade e Integridade de Dados

-- Tabela de Ingestão de Vendas (Exemplo de cenário)
CREATE TABLE IF NOT EXISTS raw_sales_data (
    id SERIAL PRIMARY KEY,
    transaction_id VARCHAR(50) UNIQUE NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    sale_value DECIMAL(10, 2) NOT NULL,
    sale_date TIMESTAMP NOT NULL,
    
    -- Campos de Auditoria (Essenciais para DataOps/SRE)
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source_file VARCHAR(255),
    status VARCHAR(20) DEFAULT 'pending' -- pending, processed, error
);

-- Tabela de Logs de Incidentes (Para a nossa Lambda Sentinel monitorar)
CREATE TABLE IF NOT EXISTS data_quality_logs (
    log_id SERIAL PRIMARY KEY,
    transaction_id VARCHAR(50),
    error_message TEXT,
    severity_level VARCHAR(10), -- INFO, WARNING, CRITICAL
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índice para busca rápida em auditorias
CREATE INDEX idx_sale_date ON raw_sales_data(sale_date);
CREATE INDEX idx_incident_status ON raw_sales_data(status);