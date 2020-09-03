output "email_identity_arn" {
  value = concat(aws_ses_email_identity.email.*.arn, [""])[0]
  description = "The ARN of the email identity created."
}

// Testing terraform outputs possible issue with #23073
output "test_2" {
  value = "123"
}