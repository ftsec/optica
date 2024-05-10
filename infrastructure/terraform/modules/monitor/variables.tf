variable "cloudtrail_name" {
  description = "The name of the CloudTrail."
  type        = string
}

variable "s3_bucket_name" {
  description = "The name of the S3 bucket where CloudTrail logs are stored."
  type        = string
}

variable "is_multi_region_trail" {
  description = "Whether the trail is a multi-region trail."
  type        = bool
}

variable "kms_key_id" {
  description = "The ARN of the KMS key used for encrypting CloudTrail logs."
  type        = string
}

variable "cloud_watch_logs_role_arn" {
  description = "The ARN of the IAM role for CloudWatch logs used by CloudTrail."
  type        = string
}

variable "s3_bucket_arn" {
  description = "ARN of the S3 bucket to include in the event selector."
  type        = string
}

variable "terraform_state_bucket_arn" {
  description = "ARN of the Terraform state S3 bucket to include in the event selector."
  type        = string
}

variable "cloudtrail_log_group_name" {
  description = "The name of the CloudWatch log group for CloudTrail logs."
  type        = string
}

variable "cloudtrail_log_group_retention_in_days" {
  description = "The number of days to retain the CloudTrail log events."
  type        = number
}

variable "kms_log_group_key_arn" {
  description = "The ARN of the KMS key used for encrypting CloudWatch logs."
  type        = string
}

variable "read_write_type" {
    description = "The read/write type for the event selector."
    type        = string
}

variable "s3_key_prefix" {
    description = "The prefix for the specified S3 bucket."
    type        = string
}