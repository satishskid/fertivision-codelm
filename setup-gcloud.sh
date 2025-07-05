#!/bin/bash
# Google Cloud SDK Setup and FertiVision Deployment

echo "🛠️ Google Cloud SDK Setup for FertiVision"
echo "=========================================="

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "This script is designed for macOS. For other systems, visit: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Install Google Cloud SDK
echo "📦 Installing Google Cloud SDK..."
if ! command -v gcloud &> /dev/null; then
    echo "Downloading and installing Google Cloud SDK..."
    
    # Download and install
    curl https://sdk.cloud.google.com | bash
    
    # Source the path
    source ~/google-cloud-sdk/path.bash.inc
    source ~/google-cloud-sdk/completion.bash.inc
    
    echo "✅ Google Cloud SDK installed!"
else
    echo "✅ Google Cloud SDK already installed"
fi

# Update gcloud components
echo "🔄 Updating gcloud components..."
gcloud components update --quiet

# Check if user is authenticated
echo "🔐 Checking authentication..."
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "Please authenticate with Google Cloud:"
    gcloud auth login
else
    echo "✅ Already authenticated"
fi

# Check/set project
echo "📝 Setting up project..."
CURRENT_PROJECT=$(gcloud config get-value project 2>/dev/null)

if [ -z "$CURRENT_PROJECT" ] || [ "$CURRENT_PROJECT" = "(unset)" ]; then
    echo ""
    echo "You need to create or select a Google Cloud project:"
    echo "1. Go to: https://console.cloud.google.com/projectcreate"
    echo "2. Create a new project (it's free!)"
    echo "3. Note your project ID"
    echo ""
    read -p "Enter your Google Cloud Project ID: " PROJECT_ID
    
    if [ -n "$PROJECT_ID" ]; then
        gcloud config set project "$PROJECT_ID"
        echo "✅ Project set to: $PROJECT_ID"
    else
        echo "❌ Project ID required. Please run this script again."
        exit 1
    fi
else
    echo "✅ Using project: $CURRENT_PROJECT"
    PROJECT_ID="$CURRENT_PROJECT"
fi

# Enable required APIs
echo "🔌 Enabling required APIs..."
gcloud services enable cloudbuild.googleapis.com --quiet
gcloud services enable run.googleapis.com --quiet
echo "✅ APIs enabled"

# Set default region
echo "🌍 Setting default region..."
gcloud config set run/region us-central1
echo "✅ Default region set to us-central1"

echo ""
echo "🎉 Setup complete! Now you can deploy FertiVision:"
echo ""
echo "Run: ./deploy-free-cloudrun.sh"
echo ""
echo "Or deploy manually with:"
echo "gcloud run deploy fertivision --source . --platform managed --region us-central1 --allow-unauthenticated"
