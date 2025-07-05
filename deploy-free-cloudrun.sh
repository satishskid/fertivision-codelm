#!/bin/bash
# Quick Deploy Script for Google Cloud Run (Free Tier)

echo "🚀 FertiVision - Google Cloud Run Free Deployment"
echo "================================================"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "Installing Google Cloud SDK..."
    curl https://sdk.cloud.google.com | bash
    exec -l $SHELL
fi

# Set project (you'll need to create one)
echo "📝 Setting up Google Cloud Project..."
echo "1. Go to https://console.cloud.google.com"
echo "2. Create a new project (free)"
echo "3. Enable Cloud Run API"
echo "4. Run: gcloud auth login"
echo "5. Run: gcloud config set project YOUR_PROJECT_ID"
echo ""

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
