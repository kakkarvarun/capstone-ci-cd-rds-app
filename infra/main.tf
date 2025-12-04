terraform {
  required_version = ">= 1.5.0"

  backend "s3" {
    bucket         = "varun-capstone-tf-state-902890"
    key            = "terraform.tfstate"
    region         = "ca-central-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }

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
