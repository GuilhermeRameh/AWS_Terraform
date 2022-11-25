terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = var.aws_region
  # access_key = AWS_ACCESS_KEY_ID
  # secret_key = AWS_SECRET_ACCESS_KEY
}

resource "aws_instance" "main" {
  for_each = var.instances
  ami           =  each.value.image_id  
  instance_type =  each.value.instance_type
  subnet_id = aws_subnet.main.id
  vpc_security_group_ids = [aws_security_group.allow[each.value.sec_group].id]

  tags = {
    Name = "${each.key}"
  }
}

resource "aws_vpc" "main" {
  cidr_block       =    var.vpc_cidr_block        #"172.16.0.0/16"
  instance_tenancy = "default"

  tags = {
    name = "VPC-${var.aws_region}"
  }
}

resource "aws_subnet" "main" {
  vpc_id     = aws_vpc.main.id
  cidr_block = cidrsubnet(aws_vpc.main.cidr_block, 8, 1)  # Pega o cidr do block da vpc e divide em 2
  map_public_ip_on_launch = true

  tags = {
    Name = "new_subnet"
  }
}

resource "aws_security_group" "allow" {
  for_each = var.sec_groups
  name        = each.value.name
  vpc_id      = aws_vpc.main.id

  ingress = [for rule in each.value.ingress : rule.ingress]

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = {
    Name = each.value.name
  }
}

