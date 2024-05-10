resource "aws_cloudwatch_log_group" "log_group" {
  name              = var.cloudtrail_log_group_name
  retention_in_days = var.cloudtrail_log_group_retention_in_days
  kms_key_id        = var.kms_log_group_key_arn
}


resource "aws_cloudtrail" "trail" {
  name                          = var.cloudtrail_name
  s3_bucket_name                = var.s3_bucket_name
  s3_key_prefix                 = var.s3_key_prefix
  include_global_service_events = true
  is_multi_region_trail         = var.is_multi_region_trail
  enable_log_file_validation    = true
  kms_key_id                    = var.kms_key_id
  cloud_watch_logs_group_arn    = "${aws_cloudwatch_log_group.log_group.arn}:*"
  cloud_watch_logs_role_arn     = var.cloud_watch_logs_role_arn
  event_selector {
    read_write_type           = var.read_write_type
    include_management_events = true
    data_resource {
      type   = "AWS::S3::Object"
      values = ["${var.s3_bucket_arn}/cloudtrail/*"]
    }
  }
}



data "aws_caller_identity" "current" {}
data "aws_region" "current" {}
data "aws_partition" "current" {}
data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["vpc-flow-logs.amazonaws.com", "logs.${data.aws_region.current.name}.amazonaws.com", "cloudtrail.amazonaws.com"]
    }
    actions = ["sts:AssumeRole"]
  }
}

data "aws_iam_policy_document" "cloudwatch_policy" {
  statement {
    effect = "Allow"

    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents",
      "logs:DescribeLogStreams"
    ]
    resources = [
      "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:${aws_cloudwatch_log_group.log_group.name}",
      "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:${aws_cloudwatch_log_group.log_group.name}:log-stream:*"
    ]
  }
}


resource "aws_iam_role" "cloudwatch_role" {
  name               = "cloudwatch_role"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

resource "aws_iam_role_policy" "cloudwatch_role_policy" {
  name   = "cloudwatch_role_policy"
  role   = aws_iam_role.cloudwatch_role.id
  policy = data.aws_iam_policy_document.cloudwatch_policy.json
}


data "aws_iam_policy_document" "vpc_flow_logs_policy" {
  statement {
    effect = "Allow"
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
      "logs:DescribeLogGroups",
      "logs:DescribeLogStreams",
    ]
    resources = [
      "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:${aws_cloudwatch_log_group.log_group.name}",
      "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:${aws_cloudwatch_log_group.log_group.name}:log-stream:*"
    ]
    condition {
      test     = "StringLike"
      variable = "aws:ResourceTag/LogStreamName"
      values   = ["${data.aws_caller_identity.current.account_id}_CloudTrail_${data.aws_region.current.name}_*"]
    }
  }
}
resource "aws_iam_role" "vpc_flow_logs_role" {
  name               = "vpc_flow_logs_role"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}
resource "aws_iam_role_policy" "vpc_flow_logs_policy" {
  name   = "vpc_flow_logs_policy"
  role   = aws_iam_role.vpc_flow_logs_role.id
  policy = data.aws_iam_policy_document.vpc_flow_logs_policy.json
}


