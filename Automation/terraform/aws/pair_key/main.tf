resource "tls_private_key" "key_public" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "aws_key_pair" "key_public" {
  key_name   = "key_public"
  public_key = tls_private_key.key_public.public_key_openssh
}

resource "local_file" "private_key" {
  content         = tls_private_key.key_public.private_key_pem
  filename        = "../key_public.pem"
  file_permission = "0600"
}
