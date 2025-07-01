#!/bin/bash
# AWS Deployment Script
# File: deploy-aws.sh

set -e

echo "🚀 FertiVision AWS Deployment Script"
echo "====================================="

# Configuration
AWS_REGION=${AWS_REGION:-us-east-1}
EB_APPLICATION_NAME=${EB_APPLICATION_NAME:-fertivision}
EB_ENVIRONMENT_NAME=${EB_ENVIRONMENT_NAME:-fertivision-prod}
S3_BUCKET=${S3_BUCKET:-fertivision-deployments}

# Check dependencies
check_dependencies() {
    echo "📋 Checking dependencies..."
    
    if ! command -v aws &> /dev/null; then
        echo "❌ AWS CLI not found. Please install: https://aws.amazon.com/cli/"
        exit 1
    fi
    
    if ! command -v eb &> /dev/null; then
        echo "❌ EB CLI not found. Please install: pip install awsebcli"
        exit 1
    fi
    
    echo "✅ Dependencies check passed"
}

# AWS Elastic Beanstalk Deployment
deploy_elastic_beanstalk() {
    echo "🎯 Deploying to AWS Elastic Beanstalk..."
    
    # Initialize EB application if not exists
    if [ ! -f .elasticbeanstalk/config.yml ]; then
        echo "📦 Initializing Elastic Beanstalk application..."
        eb init $EB_APPLICATION_NAME --region $AWS_REGION --platform "Python 3.9 running on 64bit Amazon Linux 2"
    fi
    
    # Create environment if not exists
    if ! eb status $EB_ENVIRONMENT_NAME &> /dev/null; then
        echo "🌍 Creating Elastic Beanstalk environment..."
        eb create $EB_ENVIRONMENT_NAME --instance-type t3.medium --min-instances 1 --max-instances 10
    fi
    
    # Deploy application
    echo "🚀 Deploying application..."
    eb deploy $EB_ENVIRONMENT_NAME
    
    # Get application URL
    APP_URL=$(eb status $EB_ENVIRONMENT_NAME | grep "CNAME" | awk '{print $2}')
    echo "✅ Application deployed successfully!"
    echo "🌐 URL: http://$APP_URL"
}

# AWS Lambda Deployment (Serverless)
deploy_lambda() {
    echo "⚡ Deploying to AWS Lambda (Serverless)..."
    
    # Check if serverless is installed
    if ! command -v serverless &> /dev/null; then
        echo "📦 Installing Serverless Framework..."
        npm install -g serverless
        npm install -g serverless-python-requirements
        npm install -g serverless-wsgi
    fi
    
    # Install serverless plugins
    if [ ! -f package.json ]; then
        npm init -y
    fi
    npm install serverless-python-requirements serverless-wsgi --save-dev
    
    # Deploy with serverless
    echo "🚀 Deploying serverless application..."
    serverless deploy --stage prod --region $AWS_REGION
    
    echo "✅ Lambda deployment completed!"
}

# Main deployment function
main() {
    echo "Choose deployment method:"
    echo "1) Elastic Beanstalk (Recommended for production)"
    echo "2) Lambda + API Gateway (Serverless)"
    
    read -p "Enter choice (1-2): " choice
    
    case $choice in
        1)
            check_dependencies
            deploy_elastic_beanstalk
            ;;
        2)
            check_dependencies
            deploy_lambda
            ;;
        *)
            echo "❌ Invalid choice"
            exit 1
            ;;
    esac
    
    echo ""
    echo "🎉 AWS Deployment completed successfully!"
    echo "📊 Monitor your application:"
    echo "   - AWS Console: https://console.aws.amazon.com/"
    echo "   - CloudWatch Logs: https://console.aws.amazon.com/cloudwatch/"
    echo "   - Application Health: eb health"
}

# Environment validation
validate_environment() {
    echo "🔍 Validating AWS environment..."
    
    # Check AWS credentials
    if ! aws sts get-caller-identity &> /dev/null; then
        echo "❌ AWS credentials not configured"
        echo "   Run: aws configure"
        exit 1
    fi
    
    echo "✅ AWS credentials validated"
}

# Run deployment
validate_environment
main
