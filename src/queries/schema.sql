-- Schema para o DataGuard Sentinel
-- Foco: Rastreabilidade e Integridade de Dados

-- 1. Tabela de Ingestão de Vendas
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

-- 2. Tabela de Logs de Incidentes (UNIFICADA)
-- Esta tabela agora suporta tanto erros de transação quanto erros genéricos de Python
CREATE TABLE IF NOT EXISTS data_quality_logs (
    id SERIAL PRIMARY KEY,
    transaction_id VARCHAR(50),             -- Referência opcional à venda
    incident_type VARCHAR(50) NOT NULL,    -- ex: 'InvalidValue', 'ParseError'
    severity VARCHAR(20) NOT NULL,         -- ex: 'HIGH', 'CRITICAL'
    details TEXT,                          -- A mensagem de erro capturada pelo Python
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices para performance
CREATE INDEX IF NOT EXISTS idx_sale_date ON raw_sales_data(sale_date);
CREATE INDEX IF NOT EXISTS idx_incident_status ON raw_sales_data(status);
CREATE INDEX IF NOT EXISTS idx_incident_type ON data_quality_logs(incident_type);