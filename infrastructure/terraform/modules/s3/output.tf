output "s3_bucket_id_logs" {
  value     = aws_s3_bucket.logs.id
  sensitive = false
}

output "logs_bucket_name" {
  description = "The name of the logs bucket."
  value       = aws_s3_bucket.logs.bucket
}

output "logs_bucket_arn" {
  description = "The ARN of the logs bucket."
  value       = aws_s3_bucket.logs.arn
}

output "sse_configuration" {
  description = "The server-side encryption configuration of the logs bucket."
  value       = aws_s3_bucket_server_side_encryption_configuration.logs_sse.rule
}

output "public_access_block_settings" {
  description = "Public access block settings for the logs bucket."
  value       = aws_s3_bucket_public_access_block.s3_public_access_block_vpc_flow_logs
}

output "terraform_state_bucket_arn" {
  value     = aws_s3_bucket.terraform_state.arn
  sensitive = false
}

output "cloudtrail_bucket_policy" {
  description = "The bucket policy for the CloudTrail bucket."
  value       = aws_s3_bucket_policy.cloudtrail_bucket_policy.policy
}

