variable "vpc_cidr_block" {
  description = "CIDR block for the VPC"
  type        = string
}

variable "vpc_name" {
  description = "Name for the VPC"
  type        = string
  default     = "Optica"
}


variable "cloudwatch_log_group_name" {
  description = "name of the CloudWatch Log Group for VPC Flow Logs"
  type        = string
}

variable "log_format" {
    description = "Log format for VPC Flow Logs"
    type        = string
    default     = "$${version} $${vpc-id} $${subnet-id} $${instance-id} $${interface-id} $${account-id} $${type} $${srcaddr} $${dstaddr} $${srcport} $${dstport} $${protocol} $${packets} $${bytes} $${start} $${end} $${action} $${tcp-flags}"
}

variable "flow_log_traffic_type" {
    description = "Traffic type for VPC Flow Logs"
    type        = string
    default     = "ALL"
}

variable "igw_name" {
    description = "Name for the Internet Gateway"
    type        = string
}

variable "vpc_instance_tenancy" {
    description = "Tenancy of the instances in the VPC"
    type        = string
    default     = "default"
}

variable "vpc_enable_dns_hostnames" {
    description = "Enable DNS hostname support in the VPC"
    type        = bool
}

variable "vpc_enable_dns_support" {
    description = "Enable DNS support in the VPC"
    type        = bool
}

variable "eks_cluster_name" {
  type        = string
  description = "EKS Cluster Name"
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

variable "cloudtrail_name" {
    type        = string
    description = "Name of the CloudTrail"
}

