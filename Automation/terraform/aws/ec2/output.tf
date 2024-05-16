locals {
  airbyte_host  = aws_instance.AirByte.public_dns
  metabase_host = aws_instance.Metabase.public_dns
}

output "hosts" {
  value = jsonencode({
    airbyte_host  = local.airbyte_host,
    metabase_host = local.metabase_host
  })
}
