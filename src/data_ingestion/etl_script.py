import pandas as pd
import logging
import os
import psycopg  # Versão 3
from datetime import datetime

from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env automaticamente
load_dotenv()

# Configuração de Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [DATA-PIPELINE] - %(message)s'
)
logger = logging.getLogger(__name__)

def log_to_sentinel(incident_type, severity, details, transaction_id=None):
    """Grava o incidente no RDS usando Psycopg 3."""
    # Montando a string de conexão (Connection String)
    # O Psycopg 3 aceita o formato 'postgresql://user:pass@host:port/dbname'
    conn_str = (
        f"host={os.getenv('DB_HOST')} "
        f"dbname={os.getenv('DB_NAME')} "
        f"user={os.getenv('DB_USER')} "
        f"password={os.getenv('DB_PASS')} "
        f"port={os.getenv('DB_PORT', 5432)}"
    )

    try:
        # No Psycopg 3, o contexto 'with' gerencia commit/rollback e fecha a conexão automaticamente
        with psycopg.connect(conn_str) as conn:
            with conn.cursor() as cur:
                sql = """
                INSERT INTO data_quality_logs (transaction_id, incident_type, severity, details)
                VALUES (%s, %s, %s, %s)
                """
                cur.execute(sql, (transaction_id, incident_type, severity, details))
                # O commit é automático ao sair do bloco 'with conn' se não houver erro
        
        logger.info("Sentinel: Incidente registrado com sucesso no RDS (via Psycopg 3).")
    except Exception as e:
        logger.error(f"Falha ao conectar com o Sentinel no RDS: {e}")

def run_etl_pipeline(file_path):
    logger.info(f"Iniciando ingestão: {file_path}")
    
    if not os.path.exists(file_path):
        logger.error(f"Erro Crítico: Arquivo {file_path} não encontrado!")
        return

    try:
        # EXTRAÇÃO
        df = pd.read_csv(file_path)
        logger.info(f"Carregados {len(df)} registros.")

        # TRANSFORMAÇÃO & VALIDAÇÃO POR LINHA
        for index, row in df.iterrows():
            try:
                # Tenta a conversão numérica
                pd.to_numeric(row['sale_value'], errors='raise')
                
            except ValueError as e:
                t_id = str(row.get('transaction_id', 'Unknown'))
                val_errado = row['sale_value']
                
                # Criando os detalhes do incidente
                error_details = f"Falha de conversão: O valor '{val_errado}' não é um número válido."
                
                logger.warning(f"Incidente de Qualidade detectado na Transação: {t_id}")
                
                # Enviando para a AWS
                log_to_sentinel(
                    incident_type='InvalidValue', 
                    severity='HIGH', 
                    details=error_details, 
                    transaction_id=t_id
                )

        logger.info("Processamento finalizado.")

    except Exception as e:
        logger.critical(f"Falha inesperada no Pipeline: {e}")
        log_to_sentinel('PipelineCrash', 'CRITICAL', str(e))

if __name__ == "__main__":
    # Certifique-se de que o PowerShell já tem as variáveis: $env:DB_HOST, etc.
    DATA_PATH = "data/mock_data.csv"
    run_etl_pipeline(DATA_PATH)