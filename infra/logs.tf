resource "aws_cloudwatch_log_group" "ecs_app" {
  name              = "/ecs/capstone-user-api"
  retention_in_days = 7
}
