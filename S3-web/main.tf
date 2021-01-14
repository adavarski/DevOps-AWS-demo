provider "aws" {
  region = "us-east-2"
}

resource "aws_s3_bucket" "s3-static-website-demo" {
  bucket = "s3-static-website-demo"
  acl    = "public-read"

  website {
    index_document = "index.html"
}
}
