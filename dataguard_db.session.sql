CREATE TABLE IF NOT EXISTS public.data_quality_logs (
    id SERIAL PRIMARY KEY,
    transaction_id VARCHAR(50),
    incident_type VARCHAR(50) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    details TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);