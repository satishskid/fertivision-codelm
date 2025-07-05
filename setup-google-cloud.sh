#!/bin/bash
# Google Cloud SDK Setup for macOS - Step by Step
# Run this first before deploying to Cloud Run

echo "🛠️ Setting up Google Cloud SDK for FertiVision"
echo "=============================================="

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ This script is designed for macOS. Please install gcloud manually."
    exit 1
fi

# Install Google Cloud SDK using Homebrew (recommended for macOS)
if command -v brew &> /dev/null; then
    echo "📦 Installing Google Cloud SDK via Homebrew..."
    brew install --cask google-cloud-sdk
    
    # Add gcloud to PATH
    echo "🔧 Adding gcloud to PATH..."
    echo 'source "$(brew --prefix)/share/google-cloud-sdk/path.zsh.inc"' >> ~/.zshrc
    echo 'source "$(brew --prefix)/share/google-cloud-sdk/completion.zsh.inc"' >> ~/.zshrc
    
    # Reload shell configuration
    source ~/.zshrc 2>/dev/null || true
    
else
    echo "📦 Homebrew not found. Installing Google Cloud SDK manually..."
    
    # Download and install manually
    cd ~
    curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-456.0.0-darwin-x86_64.tar.gz
    tar -xf google-cloud-cli-456.0.0-darwin-x86_64.tar.gz
    ./google-cloud-sdk/install.sh --quiet --path-update=true
    
    # Add to PATH
    echo 'source "$HOME/google-cloud-sdk/path.zsh.inc"' >> ~/.zshrc
    echo 'source "$HOME/google-cloud-sdk/completion.zsh.inc"' >> ~/.zshrc
    
    # Clean up
    rm google-cloud-cli-456.0.0-darwin-x86_64.tar.gz
fi

echo ""
echo "✅ Google Cloud SDK installation complete!"
echo ""
echo "🔄 Please run the following commands to complete setup:"
echo "======================================================="
echo ""
echo "1. Reload your shell:"
echo "   source ~/.zshrc"
echo ""
echo "2. Initialize gcloud:"
echo "   gcloud init"
echo ""
echo "3. Login to Google Cloud:"
echo "   gcloud auth login"
echo ""
echo "4. Create a new project (or use existing):"
echo "   gcloud projects create YOUR-PROJECT-ID"
echo ""
echo "5. Set your project:"
echo "   gcloud config set project YOUR-PROJECT-ID"
echo ""
echo "6. Enable required APIs:"
echo "   gcloud services enable run.googleapis.com"
echo "   gcloud services enable cloudbuild.googleapis.com"
echo ""
echo "7. Deploy FertiVision:"
echo "   ./deploy-free-cloudrun.sh"
echo ""
echo "💡 Or follow the interactive setup by running: gcloud init"
