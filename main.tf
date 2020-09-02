resource "aws_ses_email_identity" "email" {
  count = length(var.email_identitys) > 0 ? length(var.email_identitys) : 0

  email = var.email_identitys[count.index]
}



