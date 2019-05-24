variable "vpc_id" {}
variable "lb_arn" {}
variable "r53_zone_id" {}
variable "lb_dns_name" {}
variable "lb_dns_zone_id" {}

variable "container_instance_sg_id" {
  description = "ID of security group attached to ECS container instances."
}
