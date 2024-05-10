resource "aws_dynamodb_table" "statelock" {
  name                        = "terraform-state-lock"
  billing_mode                = "PAY_PER_REQUEST"
  hash_key                    = "LockID"
  deletion_protection_enabled = false
  point_in_time_recovery {
    enabled = true
  }

  server_side_encryption {
    enabled     = true
    kms_key_arn = var.kms_key_arn
  }

  attribute {
    name = "LockID"
    type = "S"
  }
}


