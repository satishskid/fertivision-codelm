#!/bin/bash

# FertiVision Cloud Deployment Script
# Optimized for Google Cloud Run deployment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ID="${GOOGLE_CLOUD_PROJECT:-fertivision-prod}"
SERVICE_NAME="fertivision"
REGION="${GOOGLE_CLOUD_REGION:-us-central1}"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"
DATABASE_INSTANCE="${SERVICE_NAME}-db"
STORAGE_BUCKET="${SERVICE_NAME}-uploads"

echo -e "${BLUE}🚀 FertiVision Cloud Deployment Starting...${NC}"

# Function to print status
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check prerequisites
check_prerequisites() {
    echo -e "${BLUE}🔍 Checking prerequisites...${NC}"
    
    if ! command -v gcloud &> /dev/null; then
        print_error "Google Cloud SDK not installed. Please install it first."
        exit 1
    fi
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker not installed. Please install it first."
        exit 1
    fi
    
    # Check if authenticated
    if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
        print_error "Not authenticated with Google Cloud. Run: gcloud auth login"
        exit 1
    fi
    
    print_status "Prerequisites check passed"
}

# Set up Google Cloud project
setup_project() {
    echo -e "${BLUE}🔧 Setting up Google Cloud project...${NC}"
    
    # Set project
    gcloud config set project ${PROJECT_ID}
    
    # Enable required APIs
    echo "Enabling required APIs..."
    gcloud services enable \
        cloudbuild.googleapis.com \
        run.googleapis.com \
        sql-component.googleapis.com \
        storage-api.googleapis.com \
        cloudresourcemanager.googleapis.com
    
    print_status "Google Cloud project setup completed"
}

# Build and push Docker image
build_and_push() {
    echo -e "${BLUE}🏗️  Building and pushing Docker image...${NC}"
    
    # Build using Cloud Build for better performance
    gcloud builds submit \
        --tag ${IMAGE_NAME} \
        --docker-file Dockerfile.cloud \
        --timeout=10m
    
    print_status "Docker image built and pushed successfully"
}

# Create Cloud SQL database
create_database() {
    echo -e "${BLUE}🗄️  Setting up Cloud SQL database...${NC}"
    
    # Check if instance already exists
    if gcloud sql instances describe ${DATABASE_INSTANCE} --region=${REGION} &>/dev/null; then
        print_warning "Database instance ${DATABASE_INSTANCE} already exists"
    else
        echo "Creating Cloud SQL instance..."
        gcloud sql instances create ${DATABASE_INSTANCE} \
            --database-version=POSTGRES_14 \
            --tier=db-g1-small \
            --region=${REGION} \
            --storage-type=SSD \
            --storage-size=20GB \
            --backup-start-time=03:00 \
            --enable-bin-log \
            --deletion-protection
        
        # Create database
        gcloud sql databases create fertivision --instance=${DATABASE_INSTANCE}
        
        # Create user
        gcloud sql users create fertivision-user \
            --instance=${DATABASE_INSTANCE} \
            --password=$(openssl rand -base64 32)
    fi
    
    print_status "Cloud SQL database setup completed"
}

# Create Cloud Storage bucket
create_storage() {
    echo -e "${BLUE}🪣 Setting up Cloud Storage...${NC}"
    
    # Create bucket for uploads
    if gsutil ls -b gs://${STORAGE_BUCKET} &>/dev/null; then
        print_warning "Storage bucket ${STORAGE_BUCKET} already exists"
    else
        gsutil mb -p ${PROJECT_ID} -c STANDARD -l ${REGION} gs://${STORAGE_BUCKET}
        
        # Set CORS for web uploads
        cat > cors.json << EOF
[
    {
        "origin": ["*"],
        "method": ["GET", "POST", "PUT", "DELETE"],
        "responseHeader": ["Content-Type", "Authorization"],
        "maxAgeSeconds": 3600
    }
]
EOF
        gsutil cors set cors.json gs://${STORAGE_BUCKET}
        rm cors.json
    fi
    
    print_status "Cloud Storage setup completed"
}

# Deploy to Cloud Run
deploy_app() {
    echo -e "${BLUE}🚀 Deploying to Cloud Run...${NC}"
    
    # Get database connection name
    CONNECTION_NAME=$(gcloud sql instances describe ${DATABASE_INSTANCE} --region=${REGION} --format="value(connectionName)")
    
    # Generate database URL
    DB_PASSWORD=$(gcloud sql users describe fertivision-user --instance=${DATABASE_INSTANCE} --format="value(password)" || echo "defaultpassword")
    DATABASE_URL="postgresql://fertivision-user:${DB_PASSWORD}@localhost/fertivision?host=/cloudsql/${CONNECTION_NAME}"
    
    # Deploy to Cloud Run
    gcloud run deploy ${SERVICE_NAME} \
        --image ${IMAGE_NAME} \
        --platform managed \
        --region ${REGION} \
        --allow-unauthenticated \
        --memory 2Gi \
        --cpu 2 \
        --max-instances 100 \
        --min-instances 1 \
        --concurrency 100 \
        --timeout 300 \
        --add-cloudsql-instances ${CONNECTION_NAME} \
        --set-env-vars "DATABASE_URL=${DATABASE_URL}" \
        --set-env-vars "CLOUD_STORAGE_BUCKET=${STORAGE_BUCKET}" \
        --set-env-vars "GOOGLE_CLOUD_PROJECT=${PROJECT_ID}" \
        --set-env-vars "FLASK_ENV=production" \
        --set-env-vars "SECRET_KEY=$(openssl rand -base64 32)"
    
    # Get service URL
    SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} --region=${REGION} --format="value(status.url)")
    
    print_status "Application deployed successfully"
    echo -e "${GREEN}🌐 Service URL: ${SERVICE_URL}${NC}"
}

# Setup custom domain (optional)
setup_domain() {
    if [ -n "$CUSTOM_DOMAIN" ]; then
        echo -e "${BLUE}🌍 Setting up custom domain...${NC}"
        
        gcloud run domain-mappings create \
            --service ${SERVICE_NAME} \
            --domain ${CUSTOM_DOMAIN} \
            --region ${REGION}
        
        print_status "Custom domain setup completed"
        echo -e "${GREEN}Please add the following DNS records:${NC}"
        gcloud run domain-mappings describe ${CUSTOM_DOMAIN} --region=${REGION}
    fi
}

# Setup monitoring and alerting
setup_monitoring() {
    echo -e "${BLUE}📊 Setting up monitoring...${NC}"
    
    # Create notification channel (email)
    if [ -n "$NOTIFICATION_EMAIL" ]; then
        gcloud alpha monitoring channels create \
            --display-name="FertiVision Alerts" \
            --type=email \
            --channel-labels=email_address=${NOTIFICATION_EMAIL}
    fi
    
    # Create uptime check
    gcloud alpha monitoring uptime create ${SERVICE_NAME}-uptime \
        --hostname=$(echo ${SERVICE_URL} | sed 's|https://||') \
        --path=/health
    
    print_status "Monitoring setup completed"
}

# Run database migrations
run_migrations() {
    echo -e "${BLUE}🔄 Running database migrations...${NC}"
    
    # This would typically run your database migration script
    # For now, we'll just test the connection
    gcloud run jobs create migrate-job \
        --image ${IMAGE_NAME} \
        --region ${REGION} \
        --add-cloudsql-instances ${CONNECTION_NAME} \
        --set-env-vars "DATABASE_URL=${DATABASE_URL}" \
        --command "python" \
        --args "init.sql"
    
    print_status "Database migrations completed"
}

# Main deployment function
main() {
    echo -e "${BLUE}🚀 Starting FertiVision Cloud Deployment${NC}"
    echo "================================================="
    echo "Project ID: ${PROJECT_ID}"
    echo "Region: ${REGION}"
    echo "Service Name: ${SERVICE_NAME}"
    echo "================================================="
    
    check_prerequisites
    setup_project
    build_and_push
    create_database
    create_storage
    deploy_app
    setup_domain
    setup_monitoring
    
    echo ""
    echo -e "${GREEN}🎉 Deployment completed successfully!${NC}"
    echo ""
    echo -e "${BLUE}📋 Next Steps:${NC}"
    echo "1. Visit your application: ${SERVICE_URL}"
    echo "2. Test the health endpoint: ${SERVICE_URL}/health"
    echo "3. Upload a test image and run analysis"
    echo "4. Monitor performance in Google Cloud Console"
    echo ""
    echo -e "${BLUE}💰 Estimated Monthly Cost:${NC}"
    echo "- Cloud Run: $25-50 (small practice)"
    echo "- Cloud SQL: $7-15"
    echo "- Cloud Storage: $1-5"
    echo "- Total: ~$35-70/month"
    echo ""
    echo -e "${GREEN}✅ FertiVision is now running in production!${NC}"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --project-id)
            PROJECT_ID="$2"
            shift 2
            ;;
        --region)
            REGION="$2"
            shift 2
            ;;
        --domain)
            CUSTOM_DOMAIN="$2"
            shift 2
            ;;
        --email)
            NOTIFICATION_EMAIL="$2"
            shift 2
            ;;
        --help)
            echo "Usage: $0 [options]"
            echo "Options:"
            echo "  --project-id    Google Cloud Project ID"
            echo "  --region        Deployment region (default: us-central1)"
            echo "  --domain        Custom domain name (optional)"
            echo "  --email         Notification email for alerts (optional)"
            echo "  --help          Show this help message"
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Run main deployment
main
