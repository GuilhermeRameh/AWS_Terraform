variable "aws_region" {
  type        = string
  default     = "us-east-1"
  description = "A região da AWS"
}

variable "vpc_cidr_block" {
  type        = string
  default     =  "10.0.0.0/16"
}

variable "instances" {
  description = "Instância a ser criada"
  type = map(object({
    image_id = string
    instance_type = string
    sec_group = string
  }))
}

variable "sec_groups"{
  description = "Informações dos grupos de segurança"
  type = map(object({
    name = string
    ingress = list(map(object({
      description = string
      from_port = number
      ipv6_cidr_blocks = list(string)
      prefix_list_ids = list(string)
      to_port = number
      protocol = string
      security_groups = list(string)
      self = bool
      cidr_blocks = list(string)
    })))
  }))
}

variable "users"{
  type        = map(object({
    username = string
  }))
}