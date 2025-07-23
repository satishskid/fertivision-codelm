#!/bin/bash
# Quick Deploy Script for Google Cloud Run (Free Tier)

echo "🚀 FertiVision - Google Cloud Run Free Deployment"
echo "================================================"

# Check if gcloud is installed and configured
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud not found. Run: ./setup-gcloud-simple.sh"
    exit 1
fi

# Check if authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | head -n1 &> /dev/null; then
    echo "❌ Not authenticated. Run: gcloud auth login --no-launch-browser"
    exit 1
fi

# Check if project is set
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
if [ -z "$PROJECT_ID" ]; then
    echo "❌ No project set. Run: gcloud config set project YOUR_PROJECT_ID"
    exit 1
fi

echo "✅ Using project: $PROJECT_ID"
echo "✅ Authenticated as: $(gcloud config get-value account)"
echo ""

# Enable required APIs
echo "🔌 Enabling required APIs..."
gcloud services enable run.googleapis.com cloudbuild.googleapis.com --quiet

# Build and deploy with debugging enabled
echo "🔨 Building and deploying to Cloud Run..."
gcloud run deploy fertivision \
    --source . \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 512Mi \
    --cpu 1 \
    --max-instances 10 \
    --concurrency 100 \
    --port 8080 \
    --set-env-vars "FLASK_ENV=production,DEBUG_MODE=true" \
    --labels "app=fertivision,env=production"

echo ""
echo "✅ Deployment complete!"
echo "🌐 Your app will be available at the provided URL"
echo "💰 Cost: FREE (within 2M requests/month)"
echo "⚡ Performance: Sub-second cold starts"
echo ""
echo "🔍 DEBUGGING COMMANDS:"
echo "====================="
echo "📊 View logs:           gcloud logging read 'resource.type=cloud_run_revision AND resource.labels.service_name=fertivision' --limit=50 --format='table(timestamp,textPayload)'"
echo "🚀 Service info:        gcloud run services describe fertivision --region=us-central1"
echo "📈 Live logs:           gcloud logging tail 'resource.type=cloud_run_revision AND resource.labels.service_name=fertivision'"
echo "🔄 Redeploy:            gcloud run deploy fertivision --source . --region=us-central1"
echo "📱 Health check:        curl [YOUR_URL]/health"
echo ""
echo "🌐 Google Cloud Console: https://console.cloud.google.com/run"
