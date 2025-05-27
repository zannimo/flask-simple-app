resource "aws_s3_bucket" "movie_posters" {
  bucket = var.movie_posters_bucket_name

  tags = {
    Environment = var.environment
    Project     = "movie-app"
  }
}

resource "aws_s3_bucket_public_access_block" "movie_posters" {
  bucket = aws_s3_bucket.movie_posters.id

  block_public_acls   = false
  block_public_policy = false
  ignore_public_acls  = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_cors_configuration" "movie_posters_cors" {
  bucket = aws_s3_bucket.movie_posters.id

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET"]
    allowed_origins = ["*"] # You can restrict this later if you want. Check if via tf variable or via another way in terraform
    max_age_seconds = 3000
  }
}

resource "aws_s3_bucket_policy" "allow_public_read" {
  bucket = aws_s3_bucket.movie_posters.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Sid       = "PublicReadGetObject",
        Effect    = "Allow",
        Principal = "*",
        Action    = "s3:GetObject",
        Resource  = "${aws_s3_bucket.movie_posters.arn}/images/*"
      }
    ]
  })
}
