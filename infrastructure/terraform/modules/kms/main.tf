

data "aws_iam_policy_document" "kms_custom_policy" {
  statement {
    sid    = "Enable IAM User Permissions"
    effect = "Allow"
    principals {
      type = "AWS"
      identifiers = [
        "arn:aws:iam::${var.account_id}:user/terraform",
        "arn:aws:iam::${var.account_id}:root"
      ]
    }
    actions   = ["kms:*"]
    resources = ["*"]
  }

  statement {
    sid    = "Allow Use of the Key"
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["cloudtrail.amazonaws.com", "logs.${var.region}.amazonaws.com"]
    }
    actions = [
      "kms:Encrypt",
      "kms:Decrypt",
      "kms:ReEncrypt*",
      "kms:GenerateDataKey*",
      "kms:DescribeKey"
    ]
    resources = ["*"]
  }
}


resource "aws_kms_key" "kms_key" {
  is_enabled          = true
  enable_key_rotation = true
  policy              = data.aws_iam_policy_document.kms_custom_policy.json
  tags = {
    Name = var.key_name
    Project = var.project_name
  }
}


