#!/bin/bash
# Azure Deployment Script
# File: deploy-azure.sh

set -e

echo "🚀 FertiVision Azure Deployment Script"
echo "======================================"

# Configuration
RESOURCE_GROUP=${RESOURCE_GROUP:-fertivision-rg}
APP_SERVICE_PLAN=${APP_SERVICE_PLAN:-fertivision-plan}
WEB_APP_NAME=${WEB_APP_NAME:-fertivision-app-$(date +%s)}
LOCATION=${LOCATION:-eastus}
SKU=${SKU:-B1}

# Check dependencies
check_dependencies() {
    echo "📋 Checking dependencies..."
    
    if ! command -v az &> /dev/null; then
        echo "❌ Azure CLI not found. Please install: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
        exit 1
    fi
    
    echo "✅ Dependencies check passed"
}

# Azure login and setup
azure_login() {
    echo "🔐 Checking Azure login..."
    
    if ! az account show &> /dev/null; then
        echo "🔑 Please login to Azure..."
        az login
    fi
    
    # Set subscription if multiple exist
    SUBSCRIPTIONS=$(az account list --query "length([])")
    if [ "$SUBSCRIPTIONS" -gt 1 ]; then
        echo "📝 Available subscriptions:"
        az account list --output table
        read -p "Enter subscription ID: " SUBSCRIPTION_ID
        az account set --subscription $SUBSCRIPTION_ID
    fi
    
    echo "✅ Azure authentication successful"
}

# Create Azure resources
create_resources() {
    echo "🏗️ Creating Azure resources..."
    
    # Create resource group
    echo "📦 Creating resource group: $RESOURCE_GROUP"
    az group create --name $RESOURCE_GROUP --location $LOCATION
    
    # Create App Service plan
    echo "⚙️ Creating App Service plan: $APP_SERVICE_PLAN"
    az appservice plan create \
        --name $APP_SERVICE_PLAN \
        --resource-group $RESOURCE_GROUP \
        --sku $SKU \
        --is-linux
    
    # Create Web App
    echo "🌐 Creating Web App: $WEB_APP_NAME"
    az webapp create \
        --resource-group $RESOURCE_GROUP \
        --plan $APP_SERVICE_PLAN \
        --name $WEB_APP_NAME \
        --runtime "PYTHON|3.9" \
        --startup-file "app.py"
    
    echo "✅ Azure resources created successfully"
}

# Configure Web App
configure_webapp() {
    echo "⚙️ Configuring Web App..."
    
    # Set environment variables
    az webapp config appsettings set \
        --resource-group $RESOURCE_GROUP \
        --name $WEB_APP_NAME \
        --settings \
            FLASK_ENV=production \
            DATABASE_URL="sqlite:///reproductive_analysis.db" \
            SCM_DO_BUILD_DURING_DEPLOYMENT=true \
            ENABLE_ORYX_BUILD=true
    
    # Configure startup command
    az webapp config set \
        --resource-group $RESOURCE_GROUP \
        --name $WEB_APP_NAME \
        --startup-file "gunicorn --bind=0.0.0.0 --timeout 600 app:app"
    
    echo "✅ Web App configuration completed"
}

# Deploy application
deploy_application() {
    echo "🚀 Deploying application..."
    
    # Create deployment package
    echo "📦 Creating deployment package..."
    zip -r deployment.zip . -x "*.git*" "*__pycache__*" "*.pyc" "venv/*" ".venv/*"
    
    # Deploy via ZIP
    az webapp deployment source config-zip \
        --resource-group $RESOURCE_GROUP \
        --name $WEB_APP_NAME \
        --src deployment.zip
    
    # Clean up
    rm deployment.zip
    
    echo "✅ Application deployed successfully"
}

# Container deployment (alternative)
deploy_container() {
    echo "🐳 Deploying with container..."
    
    # Build and push to Azure Container Registry
    ACR_NAME="fertivisionacr$(date +%s)"
    
    # Create ACR
    az acr create \
        --resource-group $RESOURCE_GROUP \
        --name $ACR_NAME \
        --sku Basic \
        --admin-enabled true
    
    # Build and push image
    az acr build \
        --resource-group $RESOURCE_GROUP \
        --registry $ACR_NAME \
        --image fertivision:latest \
        --file Dockerfile.production .
    
    # Deploy container to Web App
    az webapp create \
        --resource-group $RESOURCE_GROUP \
        --plan $APP_SERVICE_PLAN \
        --name "$WEB_APP_NAME-container" \
        --deployment-container-image-name "$ACR_NAME.azurecr.io/fertivision:latest"
    
    echo "✅ Container deployment completed"
}

# Get deployment information
get_deployment_info() {
    echo "📊 Deployment Information:"
    echo "=========================="
    
    # Get Web App URL
    WEB_APP_URL=$(az webapp show --resource-group $RESOURCE_GROUP --name $WEB_APP_NAME --query "defaultHostName" --output tsv)
    
    echo "🌐 Application URL: https://$WEB_APP_URL"
    echo "📊 Resource Group: $RESOURCE_GROUP"
    echo "⚙️ App Service Plan: $APP_SERVICE_PLAN"
    echo "🔗 Azure Portal: https://portal.azure.com"
    
    echo ""
    echo "📈 Monitor your application:"
    echo "   - Application Insights: az monitor app-insights component show"
    echo "   - Logs: az webapp log tail --resource-group $RESOURCE_GROUP --name $WEB_APP_NAME"
    echo "   - Metrics: az monitor metrics list"
}

# Main deployment function
main() {
    echo "Choose deployment method:"
    echo "1) Web App (App Service) - Recommended"
    echo "2) Container Deployment"
    
    read -p "Enter choice (1-2): " choice
    
    case $choice in
        1)
            create_resources
            configure_webapp
            deploy_application
            ;;
        2)
            create_resources
            deploy_container
            ;;
        *)
            echo "❌ Invalid choice"
            exit 1
            ;;
    esac
    
    get_deployment_info
    
    echo ""
    echo "🎉 Azure Deployment completed successfully!"
}

# Run deployment
check_dependencies
azure_login
main
