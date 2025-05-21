provider "aws" {
  profile = "serverless"
  region  = "us-east-1"
  default_tags {
    tags = {
      Environment = "Dev"
    }
  }
}