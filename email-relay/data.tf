data "template_file" "task_def" {
  template = "${file("${path.module}/lib/postfix.tpl.json")}"
  vars {
    image_url = "${aws_ecr_repository.postfix.repository_url}:latest"
    cw_logs_group = "${aws_cloudwatch_log_group.postfix.name}"
  }
}
