#!/bin/bash

# FertiVision Cloud Deployment Script with Performance Optimizations
# This script deploys the optimized version to various cloud platforms

set -e

echo "🚀 FertiVision Cloud Deployment with Performance Optimizations"
echo "============================================================="

# Configuration
APP_NAME="fertivision-optimized"
VERSION="v2.0.0"
DOCKER_IMAGE="$APP_NAME:$VERSION"

# Check dependencies
command -v docker >/dev/null 2>&1 || { echo "❌ Docker is required but not installed. Aborting." >&2; exit 1; }
command -v docker-compose >/dev/null 2>&1 || { echo "❌ Docker Compose is required but not installed. Aborting." >&2; exit 1; }

# Function to deploy to different platforms
deploy_to_platform() {
    local platform=$1
    
    case $platform in
        "local")
            deploy_local
            ;;
        "aws")
            deploy_aws
            ;;
        "gcp")
            deploy_gcp
            ;;
        "azure")
            deploy_azure
            ;;
        "digital-ocean")
            deploy_digital_ocean
            ;;
        *)
            echo "❌ Unsupported platform: $platform"
            exit 1
            ;;
    esac
}

# Local deployment with Docker Compose
deploy_local() {
    echo "🏠 Deploying to local environment..."
    
    # Create necessary directories
    mkdir -p uploads exports ssl
    
    # Generate self-signed SSL certificates for testing
    if [ ! -f ssl/cert.pem ]; then
        echo "🔐 Generating SSL certificates..."
        openssl req -x509 -newkey rsa:4096 -keyout ssl/key.pem -out ssl/cert.pem -days 365 -nodes \
            -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
    fi
    
    # Create environment file
    cat > .env << EOF
# Database Configuration
DB_PASSWORD=fertivision_secure_password_$(date +%s)
POSTGRES_PASSWORD=\${DB_PASSWORD}

# Redis Configuration
REDIS_HOST=redis
REDIS_PORT=6379

# Celery Configuration
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# MinIO Configuration
MINIO_ACCESS_KEY=fertivision_minio
MINIO_SECRET_KEY=fertivision_minio_secret_$(date +%s)

# Monitoring
GRAFANA_PASSWORD=admin_password_$(date +%s)

# Application Configuration
FLASK_ENV=production
ANALYSIS_MODE=DEEPSEEK
EOF
    
    # Build and deploy with Docker Compose
    echo "🔨 Building optimized Docker image..."
    docker-compose -f docker-compose.production.yml build
    
    echo "🚀 Starting services..."
    docker-compose -f docker-compose.production.yml up -d
    
    # Wait for services to be ready
    echo "⏳ Waiting for services to be ready..."
    sleep 30
    
    # Run database migrations
    echo "📊 Running database migrations..."
    docker-compose -f docker-compose.production.yml exec -T app python -c "
import os
os.system('python -c \"from performance_optimization import DatabaseOptimizer; db = DatabaseOptimizer(); db.optimize_queries()\"')
"
    
    echo "✅ Local deployment completed!"
    echo "📊 Application: http://localhost"
    echo "📊 Monitoring: http://localhost:3000 (Grafana)"
    echo "🌸 Flower (Celery): http://localhost:5555"
    echo "📈 Prometheus: http://localhost:9090"
}

# AWS ECS Deployment
deploy_aws() {
    echo "☁️ Deploying to AWS ECS..."
    
    # Check AWS CLI
    command -v aws >/dev/null 2>&1 || { echo "❌ AWS CLI is required. Please install it first." >&2; exit 1; }
    
    # Create ECS task definition
    cat > ecs-task-definition.json << EOF
{
    "family": "$APP_NAME",
    "networkMode": "awsvpc",
    "requiresCompatibilities": ["FARGATE"],
    "cpu": "1024",
    "memory": "2048",
    "executionRoleArn": "arn:aws:iam::ACCOUNT_ID:role/ecsTaskExecutionRole",
    "containerDefinitions": [
        {
            "name": "$APP_NAME",
            "image": "$DOCKER_IMAGE",
            "portMappings": [
                {
                    "containerPort": 5000,
                    "protocol": "tcp"
                }
            ],
            "environment": [
                {"name": "FLASK_ENV", "value": "production"},
                {"name": "ANALYSIS_MODE", "value": "DEEPSEEK"}
            ],
            "logConfiguration": {
                "logDriver": "awslogs",
                "options": {
                    "awslogs-group": "/ecs/$APP_NAME",
                    "awslogs-region": "us-east-1",
                    "awslogs-stream-prefix": "ecs"
                }
            }
        }
    ]
}
EOF
    
    echo "📋 ECS task definition created: ecs-task-definition.json"
    echo "⚠️  Please update ACCOUNT_ID and deploy using AWS Console or CLI"
}

# Google Cloud Run Deployment
deploy_gcp() {
    echo "☁️ Deploying to Google Cloud Run..."
    
    # Check gcloud CLI
    command -v gcloud >/dev/null 2>&1 || { echo "❌ Google Cloud CLI is required." >&2; exit 1; }
    
    # Build and push to Google Container Registry
    PROJECT_ID=$(gcloud config get-value project)
    IMAGE_URL="gcr.io/$PROJECT_ID/$APP_NAME:$VERSION"
    
    echo "🔨 Building and pushing Docker image..."
    docker build -t $IMAGE_URL .
    docker push $IMAGE_URL
    
    # Deploy to Cloud Run
    echo "🚀 Deploying to Cloud Run..."
    gcloud run deploy $APP_NAME \
        --image $IMAGE_URL \
        --platform managed \
        --region us-central1 \
        --allow-unauthenticated \
        --memory 2Gi \
        --cpu 2 \
        --concurrency 100 \
        --max-instances 10 \
        --set-env-vars "FLASK_ENV=production,ANALYSIS_MODE=DEEPSEEK"
    
    echo "✅ Google Cloud Run deployment completed!"
}

# Azure Container Instances Deployment
deploy_azure() {
    echo "☁️ Deploying to Azure Container Instances..."
    
    # Check Azure CLI
    command -v az >/dev/null 2>&1 || { echo "❌ Azure CLI is required." >&2; exit 1; }
    
    # Create resource group
    RESOURCE_GROUP="fertivision-rg"
    LOCATION="eastus"
    
    echo "📦 Creating resource group..."
    az group create --name $RESOURCE_GROUP --location $LOCATION
    
    # Create container instance
    echo "🚀 Creating container instance..."
    az container create \
        --resource-group $RESOURCE_GROUP \
        --name $APP_NAME \
        --image $DOCKER_IMAGE \
        --cpu 2 \
        --memory 4 \
        --ports 5000 \
        --environment-variables "FLASK_ENV=production" "ANALYSIS_MODE=DEEPSEEK"
    
    echo "✅ Azure deployment completed!"
}

# Digital Ocean App Platform Deployment
deploy_digital_ocean() {
    echo "🌊 Deploying to Digital Ocean App Platform..."
    
    # Create app spec
    cat > .do/app.yaml << EOF
name: $APP_NAME
services:
- name: web
  source_dir: /
  github:
    repo: your-username/fertivision-codelm
    branch: main
  run_command: gunicorn --bind 0.0.0.0:8080 app_optimized:app
  environment_slug: python
  instance_count: 2
  instance_size_slug: professional-xs
  http_port: 8080
  health_check:
    http_path: /health
  env:
  - key: FLASK_ENV
    value: production
  - key: ANALYSIS_MODE
    value: DEEPSEEK
databases:
- name: postgres-db
  engine: PG
  version: "13"
  production: true
  cluster_name: fertivision-cluster
EOF
    
    echo "📋 Digital Ocean app spec created: .do/app.yaml"
    echo "⚠️  Please deploy using Digital Ocean Console or doctl CLI"
}

# Performance testing
performance_test() {
    echo "🔬 Running performance tests..."
    
    # Check if application is running
    if ! curl -s http://localhost/health > /dev/null; then
        echo "❌ Application is not running. Please deploy first."
        exit 1
    fi
    
    # Install dependencies for testing
    pip install locust requests
    
    # Create locust test file
    cat > locustfile.py << 'EOF'
from locust import HttpUser, task, between
import json
import random

class FertiVisionUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        # Login or get auth token
        pass
    
    @task(3)
    def health_check(self):
        self.client.get("/health")
    
    @task(2)
    def list_patients(self):
        self.client.get("/api/patients")
    
    @task(1)
    def create_patient(self):
        patient_data = {
            "name": f"Test Patient {random.randint(1000, 9999)}",
            "age": random.randint(18, 45),
            "gender": random.choice(["Female", "Male"])
        }
        self.client.post("/api/patients", json=patient_data)
EOF
    
    echo "🏃 Starting load test..."
    locust -f locustfile.py --host=http://localhost --users=10 --spawn-rate=2 --run-time=60s --headless
    
    echo "✅ Performance test completed!"
}

# Monitoring setup
setup_monitoring() {
    echo "📊 Setting up monitoring..."
    
    # Create Grafana dashboards
    mkdir -p grafana/dashboards
    
    cat > grafana/dashboards/fertivision-dashboard.json << 'EOF'
{
  "dashboard": {
    "title": "FertiVision Performance Dashboard",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])"
          }
        ]
      },
      {
        "title": "Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "http_request_duration_seconds"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "singlestat",
        "targets": [
          {
            "expr": "rate(http_requests_total{status=~\"5..\"}[5m])"
          }
        ]
      }
    ]
  }
}
EOF
    
    echo "✅ Monitoring setup completed!"
}

# Cleanup function
cleanup() {
    echo "🧹 Cleaning up..."
    docker-compose -f docker-compose.production.yml down -v
    docker system prune -f
    echo "✅ Cleanup completed!"
}

# Main execution
main() {
    case ${1:-""} in
        "local")
            deploy_to_platform "local"
            ;;
        "aws")
            deploy_to_platform "aws"
            ;;
        "gcp")
            deploy_to_platform "gcp"
            ;;
        "azure")
            deploy_to_platform "azure"
            ;;
        "digital-ocean")
            deploy_to_platform "digital-ocean"
            ;;
        "test")
            performance_test
            ;;
        "monitor")
            setup_monitoring
            ;;
        "cleanup")
            cleanup
            ;;
        *)
            echo "Usage: $0 {local|aws|gcp|azure|digital-ocean|test|monitor|cleanup}"
            echo ""
            echo "Commands:"
            echo "  local          - Deploy to local Docker environment"
            echo "  aws            - Generate AWS ECS deployment files"
            echo "  gcp            - Deploy to Google Cloud Run"
            echo "  azure          - Deploy to Azure Container Instances"
            echo "  digital-ocean  - Generate Digital Ocean App Platform spec"
            echo "  test          - Run performance tests"
            echo "  monitor       - Setup monitoring dashboards"
            echo "  cleanup       - Clean up local deployment"
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
