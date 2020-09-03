# terraform-aws-ses [![Build Status](https://github.com/barundel/terraform-aws-ses/workflows/release/badge.svg)](https://github.com/barundel/terraform-aws-ses/actions)
> This is a terraform module for creating Amazon Web Services Simple Email Service resources. 

## Table of Contents

- [Maintenance](#maintenance)
- [Examples](#examples)
    - [aws_ses_email_identity](#aws_ses_email_identity)
- [License](#license)

## Maintenance

This project is maintained [Ben](https://github.com/barundel), anyone is welcome to contribute.

## Examples 

#### aws_ses_email_identity
This adds an email address identity into SES. You can call it independently or pass in a list as in this example: 

````
module "email" {
  source = "../../terraform-aws-ses/email-identity"
  email_identitys = ["your.email@gmail.com", "your.email+hello@gmail.com", "your.email+0334@gmail.com"]
}
````

<!--- BEGIN_TF_DOCS --->
## Requirements

| Name | Version |
|------|---------|
| terraform | >= 0.13.1 |
| aws | >= 3.4.0 |

## Providers

| Name | Version |
|------|---------|
| aws | >= 3.4.0 |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| email\_identitys | The email addresses to verify in SES. | `list` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| email\_identity\_arn | The ARN of the email identity created. |
| test | Testing terraform outputs possible issue with #23073 |

<!--- END_TF_DOCS --->

## License

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.