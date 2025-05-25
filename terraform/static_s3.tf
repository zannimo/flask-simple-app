resource "aws_s3_bucket" "static_site" {
  bucket = var.bucket_name

  tags = {
    Environment = var.environment
    Project     = "movie-app"
  }
}

resource "aws_s3_bucket_website_configuration" "static_site_website" {
  bucket = aws_s3_bucket.static_site.id

  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "error.html"
  }
}

resource "aws_s3_bucket_public_access_block" "public_access" {
  bucket = aws_s3_bucket.static_site.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_policy" "allow_public_read" {
  bucket = aws_s3_bucket.static_site.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.static_site.arn}/*"
      }
    ]
  })
  depends_on = [
    aws_s3_bucket_public_access_block.public_access
  ]
}


resource "aws_s3_object" "index" {
  bucket       = aws_s3_bucket.static_site.bucket
  key          = "index.html"
  source       = "../frontend/templates/index.html"
  content_type = "text/html"
}

resource "aws_s3_object" "error" {
  bucket       = aws_s3_bucket.static_site.bucket
  key          = "error.html"
  source       = "../frontend/templates/error.html"
  content_type = "text/html"
}
