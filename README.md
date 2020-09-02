# terraform-aws-ses
> This is a terraform module for creating Amazon Web Services Simple Email Service resources. 


#### aws_ses_email_identity
This adds an email address identity into SES. You can call it independently or pass in a list as in this example: 

````
module "email" {
  source = "../../terraform-aws-ses/email-identity"
  email_identitys = ["your.email@gmail.com", "your.email+hello@gmail.com", "your.email+0334@gmail.com"]
}
````

<!--- BEGIN_TF_DOCS --->

<!--- END_TF_DOCS --->