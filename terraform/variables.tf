variable "bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
}
variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "Dev"
}
variable "dynamodb_table_name" {
  description = "Name of the DynamoDB table"
  type        = string
  default     = "Movies"
}
variable "dynamodb_gsi_name" {
  description = "Name of the Global Secondary Index on year"
  type        = string
  default     = "year-index"
}
variable "movie_posters_bucket_name" {
  description = "S3 bucket name for movie posters"
  type        = string
}