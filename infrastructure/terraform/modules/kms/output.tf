output "key_arn" {
  description = "The ARN of the KMS key used for encrypting log groups"
  value       = aws_kms_key.kms_key.arn
}

output "key_id" {
  description = "The ID of the KMS key used for encrypting log groups"
  value       = aws_kms_key.kms_key.key_id
}


output "kms_custom_policy" {
  value = data.aws_iam_policy_document.kms_custom_policy
}

output "kms_key_id" {
    value = aws_kms_key.kms_key.key_id
}

