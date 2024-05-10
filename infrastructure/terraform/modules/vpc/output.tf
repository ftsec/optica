output "vpc_id" {
  value       = aws_vpc.main.id
  description = "VPC ID"
  sensitive   = false
}

output "vpc_cidr_block" {
  value     = aws_vpc.main.cidr_block
  sensitive = false
}

output "vpc_flow_logs_arn" {
  value = aws_flow_log.vpc_flow_logs.arn
}

output "public_subnets_ids" {
    value = [aws_subnet.public_subnet_1.id, aws_subnet.public_subnet_2.id]
}

output "private_subnets_ids" {
    value = [aws_subnet.private_subnet_1.id, aws_subnet.private_subnet_2.id]
}

output "vpc_owner_id" {
    value = aws_vpc.main.owner_id
}