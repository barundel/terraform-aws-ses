#!/usr/bin/env bash

# Set AWS Profile & name of image as variable
export AWS_PROFILE=${1}
IMAGE_NAME=postfix

# Build container locally
docker build -t ${IMAGE_NAME} --build-arg aws_profile=${AWS_PROFILE} .

# Get login details for ECR REPO & run the login command
$(aws ecr get-login --no-include-email --region eu-west-1)

# Get the current account number
ACCOUNT_ID=`aws sts get-caller-identity --output text --query 'Account'`

# Tag the image as latest
docker tag ${IMAGE_NAME}:latest ${ACCOUNT_ID}.dkr.ecr.eu-west-1.amazonaws.com/${IMAGE_NAME}:latest

# Push the image to the repo
docker push ${ACCOUNT_ID}.dkr.ecr.eu-west-1.amazonaws.com/${IMAGE_NAME}:latest

# Force a new deployment of the service
aws ecs update-service --cluster shared-app-cluster --service postfix --force-new-deployment

