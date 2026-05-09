# Configuração do Provedor AWS
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# 1. Bucket S3 (Data Lake / Landing Zone)
# Onde os arquivos CSV (como o nosso mock_data) serão depositados
resource "aws_s3_bucket" "dataguard_storage" {
  bucket = "dataguard-sentinel-storage-${var.environment}"

  tags = {
    Name        = "DataGuard Storage"
    Environment = var.environment
    Project     = "DataGuardSentinel"
  }
}

# 2. Instância RDS PostgreSQL (A camada de persistência)
resource "aws_db_instance" "dataguard_db" {
  allocated_storage    = 20
  db_name              = "dataguard_db"
  engine               = "postgres"
  engine_version       = "15"
  instance_class       = "db.t3.micro" # Econômico para o projeto
  username             = var.db_username
  password             = var.db_password
  parameter_group_name = "default.postgres15"
  skip_final_snapshot  = true
  publicly_accessible  = true # Para facilitar seu teste local

  tags = {
    Name        = "DataGuard-RDS"
    Environment = var.environment
  }
}
