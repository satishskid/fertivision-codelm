#!/bin/bash
# FertiVision Quick Deployment Guide
# Helps users deploy to Google Cloud Run

set -e

echo "🚀 FertiVision Quick Deployment Guide"
echo "====================================="
echo ""

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_step() {
    echo -e "${BLUE}$1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_step "Step 1: Choose your deployment method"
echo ""
echo "1) 🚀 Quick CLI Deployment (5 minutes) - Recommended for testing"
echo "2) 🏗️ Production Deployment (10 minutes) - Recommended for production"
echo "3) 🔗 GitHub Integration (15 minutes) - Recommended for CI/CD"
echo "4) ℹ️ Show deployment status and requirements"
echo ""

read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        print_step "Quick CLI Deployment Selected"
        echo ""
        print_warning "Prerequisites:"
        echo "• Google Cloud SDK installed (gcloud)"
        echo "• Authenticated with Google Cloud"
        echo "• Google Cloud project created"
        echo ""
        
        # Check if gcloud is available
        if command -v gcloud &> /dev/null; then
            print_success "Google Cloud SDK found"
            
            # Check if authenticated
            if gcloud auth list --filter=status:ACTIVE --format="value(account)" | head -n1 &> /dev/null; then
                print_success "Authenticated with Google Cloud"
                
                # Check if project is set
                PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
                if [ -n "$PROJECT_ID" ]; then
                    print_success "Using project: $PROJECT_ID"
                    echo ""
                    print_step "Starting deployment..."
                    ./deploy-free-cloudrun.sh
                else
                    print_error "No project set. Run: gcloud config set project YOUR_PROJECT_ID"
                fi
            else
                print_error "Not authenticated. Run: gcloud auth login"
            fi
        else
            print_error "Google Cloud SDK not found. Please install it first:"
            echo "https://cloud.google.com/sdk/docs/install"
        fi
        ;;
        
    2)
        print_step "Production Deployment Selected"
        echo ""
        print_warning "This will deploy with full optimizations and monitoring"
        echo ""
        
        if command -v gcloud &> /dev/null; then
            print_success "Google Cloud SDK found"
            
            read -p "Enter your Google Cloud Project ID: " PROJECT_ID
            if [ -n "$PROJECT_ID" ]; then
                read -p "Enter region (default: us-central1): " REGION
                REGION=${REGION:-us-central1}
                
                print_step "Starting production deployment..."
                ./deploy-cloud-optimized.sh --project-id "$PROJECT_ID" --region "$REGION"
            else
                print_error "Project ID is required"
            fi
        else
            print_error "Google Cloud SDK not found. Please install it first:"
            echo "https://cloud.google.com/sdk/docs/install"
        fi
        ;;
        
    3)
        print_step "GitHub Integration Selected"
        echo ""
        print_step "Follow these steps for GitHub integration:"
        echo ""
        echo "1. Open DEPLOY-GITHUB-TO-CLOUDRUN.md"
        echo "2. Create Google Cloud Project"
        echo "3. Enable APIs (Cloud Run, Cloud Build)" 
        echo "4. Connect GitHub repository"
        echo "5. Create build trigger"
        echo ""
        print_warning "This method enables automatic deployments on git push"
        echo ""
        
        read -p "Open the GitHub deployment guide? (y/n): " open_guide
        if [ "$open_guide" = "y" ] || [ "$open_guide" = "Y" ]; then
            if command -v open &> /dev/null; then
                open DEPLOY-GITHUB-TO-CLOUDRUN.md
            else
                echo "Please open: DEPLOY-GITHUB-TO-CLOUDRUN.md"
            fi
        fi
        ;;
        
    4)
        print_step "Deployment Status & Requirements"
        echo ""
        cat PRE-RELEASE-FIXES-COMPLETE.md
        ;;
        
    *)
        print_error "Invalid choice"
        exit 1
        ;;
esac
