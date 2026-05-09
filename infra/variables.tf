variable "aws_region" {
  description = "Região da AWS"
  default     = "us-east-1"
}

variable "environment" {
  description = "Ambiente do projeto"
  default     = "dev"
}

variable "db_username" {
  description = "Usuário do banco de dados"
  sensitive   = true
  # Removido o default para forçar o uso da variável de ambiente
}

variable "db_password" {
  description = "Senha do banco de dados"
  sensitive   = true
  # Removido o default para forçar o uso da variável de ambiente
}
