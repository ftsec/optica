
data "aws_caller_identity" "current" {}
data "aws_region" "current" {}
data "aws_partition" "current" {}


module "eks_admins_iam_role" {
  source  = "terraform-aws-modules/iam/aws//modules/iam-assumable-role"
  version = "5.39.0"

  role_name         = "optica_infra_admin_role"
  create_role       = true
  role_requires_mfa = false
  custom_role_policy_arns = [
    module.allow_eks_access_iam_policy.arn,
    module.list_oidc_providers_policy.arn,
    module.optica_sqs_policy.arn
  ]
  trusted_role_arns = [
    "arn:aws:iam::${module.vpc.vpc_owner_id}:root",
    module.cluster_admin_user.iam_user_arn
  ]
}


module "cluster_admin_user" {
  source  = "terraform-aws-modules/iam/aws//modules/iam-user"
  version = "5.39.0"


  name                          = "optica_infra_admin_user"
  create_iam_access_key         = false
  create_iam_user_login_profile = false

  force_destroy = true
}

module "assume_role_policy" {
  source  = "terraform-aws-modules/iam/aws//modules/iam-policy"
  version = "5.39.0"

  name          = "cluster_admin_assume_role_policy"
  create_policy = true

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "sts:AssumeRole",
        ]
        Resource = module.eks_admins_iam_role.iam_role_arn
      },
    ]
  })
}

module "allow_eks_access_iam_policy" {
  source  = "terraform-aws-modules/iam/aws//modules/iam-policy"
  version = "5.39.0"

  name          = "allow_eks_access"
  create_policy = true

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow",
        Action   = ["eks:DescribeCluster", ],
        Resource = ["arn:aws:eks:us-west-2:${data.aws_caller_identity.current.account_id}:cluster/${var.cluster_name}"]
      }
    ]
  })
}

module "list_oidc_providers_policy" {
  source  = "terraform-aws-modules/iam/aws//modules/iam-policy"
  version = "5.39.0"

  name          = "ListOIDCProvidersPolicy"
  create_policy = true

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = "iam:ListOpenIDConnectProviders"
        Resource = "*"
      },
    ]
  })
}

module "eks_admin_iam_group" {
  source  = "terraform-aws-modules/iam/aws//modules/iam-group-with-policies"
  version = "5.39.0"

  name                              = "optica_infra_admins_group"
  create_group                      = true
  attach_iam_self_management_policy = false
  group_users                       = [module.cluster_admin_user.iam_user_name]
  custom_group_policy_arns = [
    module.assume_role_policy.arn,
    module.list_oidc_providers_policy.arn
  ]
}


locals {
  cluster_namespace    = "optica"
  service_account_name = "optica-service"
}


module "optica_sqs_policy" {
  source  = "terraform-aws-modules/iam/aws//modules/iam-policy"
  version = "5.39.0"

  name          = "optica_sqs_policy"
  create_policy = true

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = ["sqs:SendMessage",
          "sqs:ReceiveMessage",
          "sqs:ListQueues",
          "sqs:DeleteMessage",
        "sqs:GetQueueUrl",
        "sqs:PurgeQueue"]
        Resource = [
        "arn:aws:sqs:us-west-2:${data.aws_caller_identity.current.account_id}:${var.sqs_queue_name}",
        "arn:aws:sqs:us-west-2:${data.aws_caller_identity.current.account_id}:${var.sqs_queue_name_out}"]
      },
    ]
  })
}


module "iam_assumable_role_self_assume" {
  source = "terraform-aws-modules/iam/aws//modules/iam-assumable-role-with-oidc"

  create_role            = true
  allow_self_assume_role = true

  role_name = "optica-role-with-oidc-self-assume"

  tags = {
    Role        = "role-with-oidc-self-assume"
    Environment = var.Environment
  }

  provider_url  = module.eks.oidc_provider_arn
  provider_urls = [module.eks.oidc_provider_arn]

  role_policy_arns = [module.optica_sqs_policy.arn]

  oidc_fully_qualified_subjects = ["system:serviceaccount:${local.cluster_namespace}:${local.service_account_name}"]
}