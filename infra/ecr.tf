resource "aws_ecr_repository" "app" {
  name = "capstone-user-api"
  force_delete         = true
}
