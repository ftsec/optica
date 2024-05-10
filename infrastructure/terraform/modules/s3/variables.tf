variable "account_logs_bucket_name" {
  type        = string
  description = "centralized logs Bucket Name"
  default     = "optica-account-logs"
}


variable "region" {
  type        = string
  description = "AWS Region"
}

variable "account_id" {
  type        = string
  description = "AWS Account ID"
}