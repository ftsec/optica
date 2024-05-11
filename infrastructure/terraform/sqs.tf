module "sqs" {
  source              = "terraform-aws-modules/sqs/aws"
  name                = var.sqs_queue_name
  create_queue_policy = true
  queue_policy_statements = {
    sqs = {
      sid     = "SQS"
      actions = ["sqs:SendMessage", "sqs:ReceiveMessage", "sqs:DeleteMessage"]

    }
  }
  tags = {
    Environment = "dev"
    Terraform   = "true"
  }
}


module "sqs-out" {
  source              = "terraform-aws-modules/sqs/aws"
  name                = var.sqs_queue_name_out
  create_queue_policy = true

  queue_policy_statements = {
    sqs = {
      sid     = "SQS"
      actions = ["sqs:SendMessage", "sqs:ReceiveMessage", "sqs:DeleteMessage","sqs:PurgeQueue"]
    }
  }
  tags = {
    Environment = "dev"
    Terraform   = "true"
  }
}


