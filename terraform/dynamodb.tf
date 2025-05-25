resource "aws_dynamodb_table" "movies" {
  name         = var.dynamodb_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"

  attribute {
    name = "id"
    type = "S"
  }

  attribute {
    name = "year"
    type = "N"
  }

  global_secondary_index {
    name            = var.dynamodb_gsi_name
    hash_key        = "year"
    projection_type = "ALL"
  }

  tags = {
    Environment = var.environment
    Project     = "movie-app"
  }
}
