module "secrets_manager" {
  source = "terraform-aws-modules/secrets-manager/aws"

  # Secret
  name            = "thousandeyesbearertoken"
  description             = "thousandeyesbearertoken"
  recovery_window_in_days = 30

  create_policy       = true
  block_public_policy = true
  policy_statements = {
    read = {
      sid = "AllowAccountRead"
      principals = [{
        type        = "AWS"
        identifiers = [module.iam_assumable_role_self_assume.iam_role_arn,module.eks_admins_iam_role.iam_role_arn]
      }]
      actions   = ["secretsmanager:GetSecretValue"]
      resources = ["*"]
    }
  }

  secret_string = "9e4f98c8-23b6-40ec-bb3f-39e9e7e204b9"

  tags = {
    Environment = var.Environment
    Project     = "optica"
  }
}