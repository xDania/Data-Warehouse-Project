locals {
  variables = yamldecode(file("../config.yaml"))
  aws       = local.variables.aws
  snowflake = local.variables.snowflake

  aws_region        = local.aws.region
  snowflake_account = local.snowflake.account_url

}
variable "AWS_ACCESS_KEY_ID" {}
variable "AWS_SECRET_ACCESS_KEY" {}

variable "SNOWFLAKE_USER" {}
variable "SNOWFLAKE_PASSWORD" {}
