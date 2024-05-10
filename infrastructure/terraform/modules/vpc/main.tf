
module "cloudtrail_kms_key" {
  source = "../kms"
  account_id = var.account_id
  region = var.region
  key_name = "cloudtrail_key"
  project_name = "optica"
}

module "log_group_kms_key" {
  source = "../kms"
  account_id = var.account_id
  region = var.region
  key_name = "log_group_key"
  project_name = "optica"
}


module "s3" {
  source     = "../s3"
  account_id = var.account_id
  region     = var.region
}
module "monitor" {
  source                       = "../monitor"
  cloudtrail_name              = var.cloudtrail_name
  s3_bucket_name               = module.s3.logs_bucket_name
  is_multi_region_trail        = true
  kms_key_id                   = module.cloudtrail_kms_key.key_arn
  cloud_watch_logs_role_arn    = module.monitor.cloudwatch_role_arn
  s3_bucket_arn                = module.s3.logs_bucket_arn
  terraform_state_bucket_arn   = module.s3.terraform_state_bucket_arn
  cloudtrail_log_group_name    = "/aws/cloudtrail/${var.cloudtrail_name}"
  cloudtrail_log_group_retention_in_days = 90
  kms_log_group_key_arn        = module.log_group_kms_key.key_arn
  read_write_type = "All"
  s3_key_prefix = "cloudtrail/"
}




resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr_block
  enable_dns_support   = var.vpc_enable_dns_support
  enable_dns_hostnames = var.vpc_enable_dns_hostnames
  instance_tenancy     = var.vpc_instance_tenancy
  tags = {
    Name = var.vpc_name
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  tags = {
    Name = var.igw_name
  }
}

resource "aws_flow_log" "vpc_flow_logs" {
  iam_role_arn    = module.monitor.vpc_flow_logs_role.arn
  log_destination = module.monitor.cloudwatch_log_group_arn
  traffic_type    = var.flow_log_traffic_type
  vpc_id          = aws_vpc.main.id


  log_format = var.log_format
  tags = {
    Name = "vpc_flow_logs"
  }
}





