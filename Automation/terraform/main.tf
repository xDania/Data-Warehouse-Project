provider "aws" {
  access_key = var.AWS_ACCESS_KEY_ID
  secret_key = var.AWS_SECRET_ACCESS_KEY
  region     = local.aws_region
}

module "snowflake" {
  source             = "./snowflake"
  snowflake_password = var.SNOWFLAKE_PASSWORD
  snowflake_account  = local.snowflake_account
  snowflake_user     = var.SNOWFLAKE_USER
}

module "aws" {
  source = "./aws"
}

module "pair_key" {
  source = "./aws/pair_key"
}

module "s3" {
  source = "./aws/s3"

}

module "ec2" {
  source = "./aws/ec2"
}
