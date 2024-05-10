variable "terraform_user" {
  type    = string
  default = "terraform"
}


variable "cloudtrail_name" {
  type        = string
  description = "CloudTrail Name"
  default     = "optica-trail"
}

variable "project_name" {
  type        = string
  description = "Project Name"
  default     = "optica"
}

variable "account_id" {
  type        = string
  description = "AWS Account ID"
}

variable "region" {
  type        = string
  description = "AWS Region"
  default     = "us-west-2"
}

variable "cluster_name" {
  type        = string
  description = "EKS Cluster Name"
  default     = "optica"
}

variable "Environment" {
  type        = string
  description = "Environment"
  default     = "staging"
}

variable "ecr_repo_name" {
  type        = string
  description = "ECR Repository Name"
  default     = "optica-1515"
}

variable "sqs_queue_name" {
  type        = string
  description = "SQS Queue Name"
  default     = "optica-queue"
}


variable "sqs_queue_name_out" {
  type        = string
  description = "SQS Queue Name"
  default     = "optica-queue-out"
}

