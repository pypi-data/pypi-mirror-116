provider "aws" {
  region = var.region_id
}

data "aws_caller_identity" "current" {}
data "aws_region" "current" {}



