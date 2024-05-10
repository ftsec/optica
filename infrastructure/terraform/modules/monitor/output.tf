output "cloudtrail_arn" {
  description = "The ARN of the CloudTrail."
  value       = aws_cloudtrail.trail.arn
}

output "cloudwatch_log_group_arn" {
  description = "The ARN of the CloudWatch log group for CloudTrail."
  value       = aws_cloudwatch_log_group.log_group.arn
}


output "cloudwatch_role_arn" {
    description = "The ARN of the IAM role for CloudWatch."
    value       = aws_iam_role.cloudwatch_role.arn
}

output "cloudwatch_role" {
    description = "The ARN of the IAM role for CloudWatch."
    value       = aws_iam_role.cloudwatch_role
}
output "vpc_flow_logs_role" {
  value = aws_iam_role.vpc_flow_logs_role
}