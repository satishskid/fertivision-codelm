#!/bin/bash
# Simple Google Cloud SDK Installation for macOS

echo "🚀 Installing Google Cloud SDK..."

# Install using Homebrew (easiest for macOS)
if command -v brew &> /dev/null; then
    echo "Installing via Homebrew..."
    brew install --cask google-cloud-sdk
else
    echo "Installing via curl..."
    curl https://sdk.cloud.google.com | bash
fi

echo "✅ Installation complete!"
echo ""
echo "Next steps:"
echo "1. Restart your terminal or run: source ~/.zshrc"
echo "2. Run: gcloud init"
echo "3. Follow the authentication prompts"
echo "4. Create a new project when prompted"
echo "5. Then run: ./deploy-free-cloudrun.sh"
