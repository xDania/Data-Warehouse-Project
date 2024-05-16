# Create a Snowflake database
resource "snowflake_database" "TPCDS" {
  name = "TPCDS"
}

# Create a Snowflake schema
resource "snowflake_schema" "RAW" {
  name     = "RAW"
  database = snowflake_database.TPCDS.name
}

# Create a Snowflake table
resource "snowflake_table" "inventory" {
  name     = "inventory"
  database = "TPCDS"
  schema   = "RAW"
  depends_on = [
    snowflake_schema.RAW
  ]

  column {
    name     = "INV_DATE_SK"
    type     = "int"
    nullable = false

  }

  column {
    name     = "INV_ITEM_SK"
    type     = "int"
    nullable = false
  }

  column {
    name = "INV_QUANTITY_ON_HAND"
    type = "int"
  }

  column {
    name     = "INV_WAREHOUSE_SK"
    type     = "int"
    nullable = false
  }

}

# Create a Snowflake file format
resource "snowflake_file_format" "COMMA_CSV" {
  name            = "COMMA_CSV"
  database        = snowflake_database.TPCDS.name
  schema          = snowflake_schema.RAW.name
  format_type     = "CSV"
  field_delimiter = ","
  skip_header     = 1
}

# Create a Snowflake stage
resource "snowflake_stage" "INV_STAGE" {
  name     = "INV_STAGE"
  database = snowflake_database.TPCDS.name
  schema   = snowflake_schema.RAW.name
}
