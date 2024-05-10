module "sqs" {
  source              = "terraform-aws-modules/sqs/aws"
  name                = var.sqs_queue_name
  create_queue_policy = true
  queue_policy_statements = {
    sqs = {
      sid     = "SQS"
      actions = ["sqs:SendMessage", "sqs:ReceiveMessage", "sqs:DeleteMessage"]

      principals = [
        {
          type        = "Federated"
          identifiers = [module.eks.oidc_provider_arn]
          }, {
          type        = "AWS"
          identifiers = [module.iam_assumable_role_self_assume.iam_role_arn, module.eks_admins_iam_role.iam_role_arn]
        }
      ]
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

      principals = [
        {
          type        = "Federated"
          identifiers = [module.eks.oidc_provider_arn]
          }, {
          type        = "AWS"
          identifiers = [module.iam_assumable_role_self_assume.iam_role_arn, module.eks_admins_iam_role.iam_role_arn]
        }
      ]
    }
  }
  tags = {
    Environment = "dev"
    Terraform   = "true"
  }
}


