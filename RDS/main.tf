provider "aws" {
  region = "us-east-2"
}

resource "aws_db_instance" "db" {
  identifier             = "demodb-postgres"
  allocated_storage      = 5
  engine                 = "postgres"
  instance_class         = "db.t2.micro"
  engine_version         = "11.4"
  password               = "${var.database_password}"
  name                   = "demodb"
  username               = "postgres"
  storage_encrypted      = false
  final_snapshot_identifier = "ci-postgres-backup"
  skip_final_snapshot       = true
}

resource "aws_ssm_parameter" "database_url" {
  name  = "/demodb/demo/DATABASE_URL"
  type  = "SecureString"
  value = "postgres://${aws_db_instance.db.username}:${var.database_password}@${aws_db_instance.db.endpoint}/${aws_db_instance.db.name}"
}
