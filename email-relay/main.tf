resource "aws_ecr_repository" "postfix" {
  name = "postfix"
}

resource "aws_cloudwatch_log_group" "postfix" {
  name = "/cdl/services/postfix"
}

resource "aws_lb_listener" "postfix_25" {
  "default_action" {
    target_group_arn = "${module.postfix_service.lb_target_group_arn}"
    type             = "forward"
  }
  load_balancer_arn = "${var.lb_arn}"
  protocol          = "TCP"
  port              = 25
}

resource "aws_lb_listener" "postfix_443" {
  "default_action" {
    target_group_arn = "${module.postfix_service.lb_target_group_arn}"
    type             = "forward"
  }
  load_balancer_arn = "${var.lb_arn}"
  protocol          = "TCP"
  port              = 443
}

resource "aws_ecs_task_definition" "postfix_server" {
  family                = "postfixServer"
  container_definitions = "${data.template_file.task_def.rendered}"
  cpu                   = "256"
  memory                = "256"
}


module "postfix_service" {
  source                       = "git::https://git-codecommit.eu-west-1.amazonaws.com/v1/repos/cloudteam.terraform.module.ecs-service"
  ecs_service_name             = "postfix"
  ecs_task_definition_arn      = "${aws_ecs_task_definition.postfix_server.arn}"
  ecs_cluster_name             = "shared-app-cluster"

  ecs_container_name           = "postfix"
  ecs_container_port           = "25"
  ecs_desired_count            = "2"

  ecs_placement_strategy_type  = "spread"
  ecs_placement_strategy_field = "attribute:ecs.availability-zone"

  lb_listener_arn              = "${aws_lb_listener.postfix_25.arn}"
  lb_vpc                       = "${var.vpc_id}"

  lb_target_group_health_check = {
    protocol            = "TCP"
    healthy_threshold   = 2
    unhealthy_threshold = 2
    interval            = 10
  }
}

resource "aws_route53_record" "ses_r53_record" {
  provider = "aws.net"
  name     = "ses-relay"
  type     = "A"
  zone_id  = "${var.r53_zone_id}"
  alias {
    evaluate_target_health = false
    name                   = "${var.lb_dns_name}"
    zone_id                = "${var.lb_dns_zone_id}"
  }
}

resource "aws_security_group_rule" "allow_25_into_container_instances_sg_for_postfix_relay" {
  security_group_id = "${var.container_instance_sg_id}"
  protocol          = "TCP"
  from_port         = 25
  to_port           = 25
  type              = "ingress"
  cidr_blocks       = ["10.0.0.0/8"]
}

resource "aws_security_group_rule" "allow_443_into_container_instances_sg_for_postfix_relay" {
  security_group_id = "${var.container_instance_sg_id}"
  protocol          = "TCP"
  from_port         = 443
  to_port           = 443
  type              = "ingress"
  cidr_blocks       = ["10.0.0.0/8"]
}