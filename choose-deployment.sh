#!/bin/bash

# 🚀 FertiVision Deployment Options - FREE Alternatives
# Since Google Cloud requires billing, here are your FREE deployment options

echo "🏥 FertiVision Deployment Options"
echo "=================================="
echo ""
echo "❌ Google Cloud Run requires billing enabled"
echo "✅ Here are FREE alternatives that work immediately:"
echo ""

echo "1. 🆓 RENDER.COM (Recommended - Free & Easy)"
echo "   • 750 hours/month free"
echo "   • Automatic HTTPS"
echo "   • Zero configuration"
echo "   • Command: ./deploy-render.sh"
echo ""

echo "2. 🆓 RAILWAY.APP"
echo "   • $5 credit monthly (enough for small apps)"
echo "   • Simple deployment"
echo "   • Command: ./deploy-railway.sh"
echo ""

echo "3. 🆓 VERCEL (Static + Serverless)"
echo "   • Free forever for personal projects"
echo "   • Global CDN"
echo "   • Command: ./deploy-vercel.sh"
echo ""

echo "4. 🆓 NETLIFY"
echo "   • Free tier with 100GB bandwidth"
echo "   • Built-in forms and functions"
echo "   • Command: ./deploy-to-netlify.sh"
echo ""

echo "5. 💰 GOOGLE CLOUD (Requires Billing Setup)"
echo "   • Need to enable billing first"
echo "   • $300 free credit for new accounts"
echo "   • Instructions below"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎯 RECOMMENDED: Deploy to Render.com (FREE)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Render.com offers:"
echo "✅ FREE 750 hours/month"
echo "✅ Automatic deployments from Git"
echo "✅ Built-in SSL certificates"
echo "✅ No credit card required"
echo "✅ Perfect for medical applications"
echo ""

read -p "Would you like to deploy to Render.com now? (y/n): " choice
if [[ $choice == "y" || $choice == "Y" ]]; then
    echo ""
    echo "🚀 Deploying to Render.com..."
    ./deploy-render.sh
    exit 0
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "💳 Google Cloud Billing Setup Instructions"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "To enable Google Cloud billing:"
echo ""
echo "1. Go to: https://console.cloud.google.com/billing"
echo "2. Click 'CREATE BILLING ACCOUNT'"
echo "3. Enter payment information (you get $300 free credit)"
echo "4. Link billing account to your project"
echo "5. Come back and run: ./deploy-free-cloudrun.sh"
echo ""
echo "Google Cloud offers:"
echo "✅ $300 free credit (12 months)"
echo "✅ Always free tier for Cloud Run"
echo "✅ 2 million requests/month free"
echo "✅ Enterprise-grade infrastructure"
echo ""

read -p "Would you like to open Google Cloud Billing in your browser? (y/n): " gcbilling
if [[ $gcbilling == "y" || $gcbilling == "Y" ]]; then
    echo "Opening Google Cloud Billing console..."
    open "https://console.cloud.google.com/billing"
    echo ""
    echo "After setting up billing, run:"
    echo "  ./deploy-free-cloudrun.sh"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔧 Alternative: Local Development"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "You can also run FertiVision locally:"
echo ""
echo "1. Install dependencies:"
echo "   pip install -r requirements.txt"
echo ""
echo "2. Run the application:"
echo "   python app.py"
echo ""
echo "3. Open: http://localhost:5000"
echo ""

read -p "Would you like to start local development now? (y/n): " local
if [[ $local == "y" || $local == "Y" ]]; then
    echo ""
    echo "🏃‍♂️ Starting local development..."
    echo "Installing dependencies..."
    pip install -r requirements.txt
    echo ""
    echo "🚀 Starting FertiVision..."
    python app.py
fi

echo ""
echo "🎉 FertiVision is ready to deploy!"
echo "Choose your preferred option above."
