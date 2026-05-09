import pandas as pd
import logging
import os

# Configuração de Logging para Observabilidade (Foco em SRE)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [DATA-PIPELINE] - %(message)s'
)
logger = logging.getLogger(__name__)

def run_etl_pipeline(file_path):
    logger.info(f"Starting ingestion for file: {file_path}")
    
    if not os.path.exists(file_path):
        logger.error(f"Critical Error: File {file_path} not found!")
        return

    try:
        # 1. EXTRAÇÃO
        df = pd.read_csv(file_path)
        logger.info(f"Loaded {len(df)} records from CSV.")

        # 2. TRANSFORMAÇÃO (Onde os erros propositais serão pegos)
        # Convertendo sale_value para numérico (forçando erro se houver texto)
        df['sale_value'] = pd.to_numeric(df['sale_value'], errors='raise')
        
        # 3. CARREGAMENTO (Simulação)
        logger.info("Data transformed successfully. Ready to load into RDS.")
        # Aqui entrará a lógica de conexão com o PostgreSQL futuramente

    except ValueError as e:
        logger.error(f"Data Quality Incident Detected: Type mismatch in 'sale_value'. Details: {e}")
        # Aqui o Sentinel entraria em ação
    except Exception as e:
        logger.critical(f"Unexpected Pipeline Failure: {e}")

if __name__ == "__main__":
    DATA_PATH = "data/mock_data.csv"
    run_etl_pipeline(DATA_PATH)