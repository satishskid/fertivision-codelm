#!/bin/bash
# Simple Google Cloud Setup (No Browser Required)

echo "🚀 Quick Google Cloud Setup for FertiVision"
echo "==========================================="

# Check if gcloud is available
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud not found. Installing..."
    # Install using Homebrew (faster on macOS)
    if command -v brew &> /dev/null; then
        echo "📦 Installing via Homebrew..."
        brew install --cask google-cloud-sdk
    else
        echo "📦 Installing via curl..."
        curl https://sdk.cloud.google.com | bash
        source ~/google-cloud-sdk/path.bash.inc
    fi
fi

echo "✅ Google Cloud SDK is ready!"
echo ""

# Manual setup instructions
echo "🔧 MANUAL SETUP REQUIRED:"
echo "========================"
echo ""
echo "1. 🌐 Create a Google Cloud Project:"
echo "   • Go to: https://console.cloud.google.com/projectcreate"
echo "   • Create a new project (choose any name like 'fertivision-app')"
echo "   • Note down your PROJECT_ID"
echo ""
echo "2. 🔑 Authenticate (copy-paste this command):"
echo "   gcloud auth login --no-launch-browser"
echo ""
echo "3. 📋 Set your project (replace YOUR_PROJECT_ID):"
echo "   gcloud config set project YOUR_PROJECT_ID"
echo ""
echo "4. 🔌 Enable required APIs:"
echo "   gcloud services enable run.googleapis.com"
echo "   gcloud services enable cloudbuild.googleapis.com"
echo ""
echo "5. 🚀 Deploy FertiVision:"
echo "   ./deploy-free-cloudrun.sh"
echo ""
echo "💡 TIP: Copy each command one by one and run them manually!"
echo ""

# Test if already configured
echo "🔍 Checking current configuration..."
if gcloud config get-value project &> /dev/null; then
    PROJECT_ID=$(gcloud config get-value project)
    echo "✅ Already configured with project: $PROJECT_ID"
    echo "🚀 You can run: ./deploy-free-cloudrun.sh"
else
    echo "⚠️ Not configured yet. Follow the steps above."
fi
