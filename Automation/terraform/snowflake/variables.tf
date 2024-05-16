# Configure the Snowflake provider
terraform {
  required_providers {
    snowflake = {
      source  = "Snowflake-Labs/snowflake"
      version = "0.87.3-pre"
    }
  }
}

provider "snowflake" {
  account  = var.snowflake_account
  user     = var.snowflake_user
  password = var.snowflake_password
  role     = "ACCOUNTADMIN"
}

variable "snowflake_account" {}

variable "snowflake_user" {}

variable "snowflake_password" {}
