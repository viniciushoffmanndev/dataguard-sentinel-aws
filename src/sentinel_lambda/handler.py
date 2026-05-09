import json
import logging

# Configuração de logging para o CloudWatch da AWS
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    Sentinel Lambda: Monitora falhas no pipeline de dados
    e registra incidentes para auditoria e resposta rápida.
    """
    logger.info("Sentinel active. Analyzing incoming incident report...")

    try:
        # 1. Captura os detalhes do incidente enviados pelo script ETL
        incident_details = event.get('details', 'No details provided')
        error_type = event.get('error_type', 'UnknownError')
        severity = event.get('severity', 'INFO')
        
        # 2. Lógica de Triagem (SRE)
        # Se o erro for crítico, poderíamos disparar um alerta (ex: SNS/Slack)
        if severity == 'CRITICAL':
            logger.error(f"!!! CRITICAL INCIDENT !!!: {incident_details}")
        else:
            logger.warning(f"Data Quality Alert: {incident_details}")

        # 3. Preparação para o Banco de Dados (RDS)
        # Futuramente, aqui faremos o INSERT na tabela data_quality_logs
        response_message = f"Incident {error_type} logged successfully."
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'status': 'Sentinel Notified',
                'message': response_message
            })
        }

    except Exception as e:
        logger.error(f"Sentinel Failure: Could not process incident report. Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps('Internal Sentinel Error')
        }