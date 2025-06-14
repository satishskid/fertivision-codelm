#!/bin/bash

# FertiVision Cloud Platform Deployment Script

echo "🚀 Starting FertiVision Cloud Platform Deployment..."

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: package.json not found. Please run this script from the project root."
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Add missing dependencies if needed
echo "🔧 Adding missing UI components..."
npm install lucide-react @radix-ui/react-slot

# Build the project
echo "🏗️  Building project..."
npm run build

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
else
    echo "❌ Build failed. Please check the errors above."
    exit 1
fi

# Commit changes
echo "📝 Committing changes to git..."
git add .
git commit -m "Production build ready for deployment"

# Push to GitHub
echo "🌐 Pushing to GitHub..."
git push origin main

if [ $? -eq 0 ]; then
    echo "✅ Successfully pushed to GitHub!"
else
    echo "⚠️  Push failed. You may need to set up git credentials."
fi

echo ""
echo "🎉 Deployment preparation complete!"
echo ""
echo "📋 Next Steps:"
echo "1. Go to https://netlify.com"
echo "2. Connect your GitHub repository"
echo "3. Set environment variables:"
echo "   - NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_b3V0Z29pbmctdW5pY29ybi01Ny5jbGVyay5hY2NvdW50cy5kZXYk"
echo "   - CLERK_SECRET_KEY=sk_test_BXcNNRJ7j08ewxtk7kQEelXx9rgrjEb0OAPQuzSgPe"
echo "4. Deploy!"
echo ""
echo "🌟 Your FertiVision Cloud Platform will be live!"
