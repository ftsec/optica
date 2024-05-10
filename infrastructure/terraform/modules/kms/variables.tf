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
}

variable "key_name" {
    type        = string
    description = "Key Pair Name"
}
