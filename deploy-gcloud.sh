#!/bin/bash
# Google Cloud Run Deployment Script
# File: deploy-gcloud.sh

set -e

echo "🚀 FertiVision Google Cloud Run Deployment Script"
echo "=================================================="

# Configuration
PROJECT_ID=${PROJECT_ID:-}
SERVICE_NAME=${SERVICE_NAME:-fertivision}
REGION=${REGION:-us-central1}
MEMORY=${MEMORY:-2Gi}
CPU=${CPU:-2}
MAX_INSTANCES=${MAX_INSTANCES:-100}
MIN_INSTANCES=${MIN_INSTANCES:-0}

# Check dependencies
check_dependencies() {
    echo "📋 Checking dependencies..."
    
    if ! command -v gcloud &> /dev/null; then
        echo "❌ Google Cloud SDK not found. Please install: https://cloud.google.com/sdk/docs/install"
        exit 1
    fi
    
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker not found. Please install: https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    echo "✅ Dependencies check passed"
}

# Google Cloud authentication and setup
gcloud_setup() {
    echo "🔐 Setting up Google Cloud..."
    
    # Login if not authenticated
    if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q "."; then
        echo "🔑 Please login to Google Cloud..."
        gcloud auth login
    fi
    
    # Set or create project
    if [ -z "$PROJECT_ID" ]; then
        echo "📝 Available projects:"
        gcloud projects list
        read -p "Enter Project ID (or 'new' to create): " PROJECT_ID
        
        if [ "$PROJECT_ID" == "new" ]; then
            read -p "Enter new project ID: " PROJECT_ID
            read -p "Enter project name: " PROJECT_NAME
            gcloud projects create $PROJECT_ID --name="$PROJECT_NAME"
            echo "✅ Project created: $PROJECT_ID"
        fi
    fi
    
    # Set active project
    gcloud config set project $PROJECT_ID
    
    # Enable required APIs
    echo "⚡ Enabling required APIs..."
    gcloud services enable cloudbuild.googleapis.com
    gcloud services enable run.googleapis.com
    gcloud services enable containerregistry.googleapis.com
    
    echo "✅ Google Cloud setup completed"
}

# Build and deploy application
deploy_cloud_run() {
    echo "🏗️ Building and deploying to Cloud Run..."
    
    # Configure Docker for gcloud
    gcloud auth configure-docker
    
    # Build container image
    echo "🐳 Building container image..."
    IMAGE_URL="gcr.io/$PROJECT_ID/$SERVICE_NAME:$(date +%Y%m%d-%H%M%S)"
    
    docker build -f Dockerfile.production -t $IMAGE_URL .
    
    # Push image to Container Registry
    echo "📤 Pushing image to Container Registry..."
    docker push $IMAGE_URL
    
    # Deploy to Cloud Run
    echo "🚀 Deploying to Cloud Run..."
    gcloud run deploy $SERVICE_NAME \
        --image $IMAGE_URL \
        --platform managed \
        --region $REGION \
        --allow-unauthenticated \
        --memory $MEMORY \
        --cpu $CPU \
        --timeout 300 \
        --concurrency 100 \
        --max-instances $MAX_INSTANCES \
        --min-instances $MIN_INSTANCES \
        --set-env-vars "FLASK_ENV=production,DATABASE_URL=sqlite:///reproductive_analysis.db,PORT=8080"
    
    echo "✅ Cloud Run deployment completed"
}

# Deploy with Cloud Build (CI/CD)
deploy_with_cloudbuild() {
    echo "🔧 Setting up Cloud Build deployment..."
    
    # Submit build
    gcloud builds submit \
        --config cloudbuild.yaml \
        --substitutions _SERVICE_NAME=$SERVICE_NAME,_REGION=$REGION
    
    echo "✅ Cloud Build deployment completed"
}

# Setup Cloud SQL (optional)
setup_cloud_sql() {
    echo "🗄️ Setting up Cloud SQL (PostgreSQL)..."
    
    read -p "Setup Cloud SQL database? (y/n): " setup_sql
    
    if [ "$setup_sql" == "y" ]; then
        INSTANCE_NAME="$SERVICE_NAME-db"
        DB_NAME="fertivision"
        
        # Create Cloud SQL instance
        gcloud sql instances create $INSTANCE_NAME \
            --database-version=POSTGRES_13 \
            --tier=db-f1-micro \
            --region=$REGION \
            --root-password=$(openssl rand -base64 32)
        
        # Create database
        gcloud sql databases create $DB_NAME --instance=$INSTANCE_NAME
        
        # Get connection name
        CONNECTION_NAME=$(gcloud sql instances describe $INSTANCE_NAME --format="value(connectionName)")
        
        echo "✅ Cloud SQL setup completed"
        echo "📊 Connection name: $CONNECTION_NAME"
        echo "🔑 Update your Cloud Run service with:"
        echo "   --add-cloudsql-instances $CONNECTION_NAME"
        echo "   --set-env-vars DATABASE_URL=postgresql://user:pass@/fertivision?host=/cloudsql/$CONNECTION_NAME"
    fi
}

# Setup custom domain (optional)
setup_custom_domain() {
    echo "🌐 Setting up custom domain..."
    
    read -p "Setup custom domain? (y/n): " setup_domain
    
    if [ "$setup_domain" == "y" ]; then
        read -p "Enter your domain (e.g., api.fertivision.com): " DOMAIN
        
        # Map domain to Cloud Run service
        gcloud run domain-mappings create \
            --service $SERVICE_NAME \
            --domain $DOMAIN \
            --region $REGION
        
        echo "✅ Custom domain mapping created"
        echo "📋 DNS Configuration required:"
        echo "   Add CNAME record: $DOMAIN -> ghs.googlehosted.com"
    fi
}

# Get deployment information
get_deployment_info() {
    echo "📊 Deployment Information:"
    echo "=========================="
    
    # Get service URL
    SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)")
    
    echo "🌐 Service URL: $SERVICE_URL"
    echo "📊 Project ID: $PROJECT_ID"
    echo "🌍 Region: $REGION"
    echo "🔗 Google Cloud Console: https://console.cloud.google.com/run/detail/$REGION/$SERVICE_NAME/metrics?project=$PROJECT_ID"
    
    echo ""
    echo "📈 Monitor your application:"
    echo "   - Logs: gcloud run services logs read $SERVICE_NAME --region=$REGION"
    echo "   - Metrics: gcloud run services describe $SERVICE_NAME --region=$REGION"
    echo "   - Traffic: https://console.cloud.google.com/run/detail/$REGION/$SERVICE_NAME/traffic?project=$PROJECT_ID"
}

# Setup monitoring and alerting
setup_monitoring() {
    echo "📊 Setting up monitoring..."
    
    # Enable Cloud Monitoring API
    gcloud services enable monitoring.googleapis.com
    
    echo "✅ Monitoring enabled"
    echo "📊 View metrics at: https://console.cloud.google.com/monitoring"
}

# Main deployment function
main() {
    echo "Choose deployment method:"
    echo "1) Direct Cloud Run deployment (Recommended)"
    echo "2) Cloud Build CI/CD deployment"
    
    read -p "Enter choice (1-2): " choice
    
    case $choice in
        1)
            deploy_cloud_run
            ;;
        2)
            deploy_with_cloudbuild
            ;;
        *)
            echo "❌ Invalid choice"
            exit 1
            ;;
    esac
    
    # Optional setups
    setup_cloud_sql
    setup_custom_domain
    setup_monitoring
    
    get_deployment_info
    
    echo ""
    echo "🎉 Google Cloud Run Deployment completed successfully!"
    echo ""
    echo "🚀 Quick commands for your team:"
    echo "   - Update service: gcloud run deploy $SERVICE_NAME --source ."
    echo "   - View logs: gcloud run services logs read $SERVICE_NAME --region=$REGION --follow"
    echo "   - Scale: gcloud run services update $SERVICE_NAME --max-instances=200 --region=$REGION"
}

# Health check endpoint
add_health_check() {
    echo "🏥 Adding health check endpoint..."
    
    cat >> app.py << 'EOF'

@app.route('/health')
def health():
    """Health check endpoint for Cloud Run"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.datetime.now().isoformat(),
        'version': '1.0.0'
    })
EOF
    
    echo "✅ Health check endpoint added"
}

# Run deployment
check_dependencies
gcloud_setup
add_health_check
main
