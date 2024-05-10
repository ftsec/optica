terraform {
  #     backend "s3" {
  #       bucket         = "opticatfstate"
  #       dynamodb_table = "terraform-state-lock"
  #       key            = "global/optica/terraform.tfstate"
  #       region         = "us-west-2"
  #       encrypt        = true
  #       profile        = "terraform"
  #     }
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region  = "us-west-2"
  profile = "terraform"
}
