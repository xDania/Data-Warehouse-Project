# --> AirByte ---------------------------------------------------------------------------

resource "aws_security_group" "airbyte_sg" {
  name        = "airbyte-security-group"
  description = "port 8000 and 22"

  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

}

resource "aws_instance" "AirByte" {
  ami                    = "ami-080e1f13689e07408"
  instance_type          = "t2.large"
  key_name               = "key_public"
  vpc_security_group_ids = [aws_security_group.airbyte_sg.id]

  tags = {
    Name = "AirByte"
  }

  root_block_device {
    volume_size = 20
  }

}

resource "aws_ec2_instance_state" "AirByte_state" {
  instance_id = aws_instance.AirByte.id
  state       = var.state
}

# --> MetaBase ---------------------------------------------------------------------------
resource "aws_security_group" "metabase_sg" {
  name        = "metabase-security-group"
  description = "port 3000 and 22"

  ingress {
    from_port   = 3000
    to_port     = 3000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "Metabase" {
  ami                    = "ami-080e1f13689e07408"
  instance_type          = "t2.small"
  key_name               = "key_public"
  vpc_security_group_ids = [aws_security_group.metabase_sg.id]

  tags = {
    Name = "Metabase"
  }

  root_block_device {
    volume_size = 20
  }

}

resource "aws_ec2_instance_state" "Metabase_state" {
  instance_id = aws_instance.Metabase.id
  state       = var.state
}
