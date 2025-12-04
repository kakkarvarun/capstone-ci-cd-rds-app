resource "aws_db_subnet_group" "rds_subnets" {
  name       = "capstone-rds-subnets"
  subnet_ids = data.aws_subnets.default.ids
}

resource "aws_db_instance" "userdb" {
  identifier              = "capstone-userdb"
  allocated_storage       = 20
  engine                  = "postgres"
  engine_version          = "16"
  instance_class          = "db.t3.micro"
  db_name                 = "userdb"
  username                = "appuser"
  password                = "CapstoneRDS123!"
  db_subnet_group_name    = aws_db_subnet_group.rds_subnets.name
  vpc_security_group_ids  = [aws_security_group.rds_sg.id]
  publicly_accessible     = false
  skip_final_snapshot     = true
  deletion_protection     = false
}
