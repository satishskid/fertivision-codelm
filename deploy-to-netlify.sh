#!/bin/bash

# FertiVision Netlify Deployment Script
# This script creates a clean static deployment

echo "🚀 Preparing FertiVision for Netlify deployment..."

# Create a temporary deployment directory
DEPLOY_DIR="netlify-deploy"
rm -rf $DEPLOY_DIR
mkdir $DEPLOY_DIR

echo "📁 Copying static files..."

# Copy only the files needed for static deployment
cp index.html $DEPLOY_DIR/
cp netlify.toml $DEPLOY_DIR/
cp package.json $DEPLOY_DIR/
cp .nvmrc $DEPLOY_DIR/
cp _redirects $DEPLOY_DIR/

# Copy static directory
cp -r static/ $DEPLOY_DIR/

# Copy documentation
cp README.md $DEPLOY_DIR/
cp NETLIFY_DEPLOYMENT.md $DEPLOY_DIR/

echo "✅ Static files copied to $DEPLOY_DIR/"

echo "📦 Files ready for deployment:"
ls -la $DEPLOY_DIR/

echo ""
echo "🌐 Manual Deployment Options:"
echo ""
echo "Option 1: Drag & Drop to Netlify"
echo "  1. Zip the $DEPLOY_DIR folder"
echo "  2. Go to https://app.netlify.com/drop"
echo "  3. Drag and drop the zip file"
echo ""
echo "Option 2: Netlify CLI"
echo "  1. Install: npm install -g netlify-cli"
echo "  2. Login: netlify login"
echo "  3. Deploy: netlify deploy --dir=$DEPLOY_DIR --prod"
echo ""
echo "Option 3: Git Repository"
echo "  1. Create a new repository with only these files"
echo "  2. Connect to Netlify"
echo "  3. Deploy from the clean repository"

# Create a zip file for easy deployment
if command -v zip &> /dev/null; then
    echo "📦 Creating deployment zip..."
    cd $DEPLOY_DIR
    zip -r ../fertivision-static-deploy.zip .
    cd ..
    echo "✅ Created fertivision-static-deploy.zip"
    echo "   You can upload this directly to Netlify!"
fi

echo ""
echo "🎉 Deployment package ready!"
echo "   Directory: $DEPLOY_DIR/"
echo "   Zip file: fertivision-static-deploy.zip"
