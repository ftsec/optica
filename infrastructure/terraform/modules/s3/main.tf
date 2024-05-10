module  "optica_tf_state_kms_key"{
  source = "../kms"
  account_id = var.account_id
  region = var.region
  key_name = "terraform_state_key"
  project_name = "optica"
}

module "log_group_kms_key" {
  source = "../kms"
  account_id = var.account_id
  region = var.region
  key_name = "log_group_key"
  project_name = "optica"
}
resource "aws_s3_bucket" "terraform_state" {
  bucket = "opticatfstate"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "terraform_state_sse" {
  bucket = aws_s3_bucket.terraform_state.id
  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = module.optica_tf_state_kms_key.key_arn
      sse_algorithm     = "aws:kms"
    }
  }
}

resource "aws_s3_bucket_versioning" "terraform_state_versioning_tf_state" {
  bucket = aws_s3_bucket.terraform_state.id
  versioning_configuration {
    status = "Enabled"
  }
}


resource "aws_s3_bucket_public_access_block" "s3_public_access_block_tf_state" {
  bucket                  = aws_s3_bucket.terraform_state.id
  block_public_acls       = true
  ignore_public_acls      = true
  block_public_policy     = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket" "logs" {
  bucket = var.account_logs_bucket_name
}

resource "aws_s3_bucket_server_side_encryption_configuration" "logs_sse" {
  bucket = aws_s3_bucket.logs.id
  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = module.log_group_kms_key.key_arn
      sse_algorithm     = "aws:kms"
    }
  }
}

resource "aws_s3_bucket_versioning" "terraform_state_versioning_logs" {
  bucket = aws_s3_bucket.logs.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_public_access_block" "s3_public_access_block_vpc_flow_logs" {
  bucket                  = aws_s3_bucket.logs.id
  block_public_acls       = true
  ignore_public_acls      = true
  block_public_policy     = true
  restrict_public_buckets = true
}


resource "aws_s3_bucket_logging" "s3_bucket_logging" {
  bucket = aws_s3_bucket.logs.id

  target_bucket = aws_s3_bucket.logs.id
  target_prefix = "log/log-delivery-logs/"
}

resource "aws_s3_bucket_logging" "s3_bucket_logging_tf_state" {
  bucket = aws_s3_bucket.terraform_state.bucket

  target_bucket = aws_s3_bucket.logs.id
  target_prefix = "log/tfstate/"
}

data "aws_iam_policy_document" "cloudtrail_s3_policy" {
  statement {
    sid    = "AWSCloudTrailWrite"
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["cloudtrail.amazonaws.com"]
    }

    actions   = ["s3:PutObject"]
    resources = ["${aws_s3_bucket.logs.arn}/cloudtrail/*"]

    condition {
      test     = "StringEquals"
      variable = "s3:x-amz-acl"
      values   = ["bucket-owner-full-control"]
    }
  }

  statement {
    sid    = "AWSCloudTrailRead"
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["cloudtrail.amazonaws.com"]
    }
    actions   = ["s3:GetBucketAcl"]
    resources = [aws_s3_bucket.logs.arn]
  }
}


resource "aws_s3_bucket_policy" "cloudtrail_bucket_policy" {
  bucket = aws_s3_bucket.logs.id
  policy = data.aws_iam_policy_document.cloudtrail_s3_policy.json
}




