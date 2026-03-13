#!/bin/bash
set -e

AWS_REGION=${AWS_REGION:-us-east-1}
ECR_REPO="random-fullstack"

echo "Building Docker image..."
docker build -t $ECR_REPO:latest .

echo "Logging into ECR..."
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $(aws ecr describe-repositories --repository-names $ECR_REPO --region $AWS_REGION 2>/dev/null | jq -r '.repositories[0].repositoryUri' || echo "")

REPO_URI=$(aws ecr create-repository --repository-name $ECR_REPO --region $AWS_REGION --output json | jq -r '.repository.repositoryUri')

echo "Tagging and pushing image..."
docker tag $ECR_REPO:latest $REPO_URI:latest
docker push $REPO_URI:latest

echo "Image pushed to: $REPO_URI:latest"

if [ -d "terraform" ]; then
    echo "Deploying with Terraform..."
    cd terraform
    terraform init
    terraform apply -var "aws_region=$AWS_REGION" -auto-approve
    
    LB_DNS=$(terraform output -raw load_balancer_dns)
    echo ""
    echo "Deployed! Access at: http://$LB_DNS"
fi
