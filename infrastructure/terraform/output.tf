output "sqs_policy_arn" {
  description = "The ARN of the SQS policy created."
  value       = module.optica_sqs_policy.arn
}

