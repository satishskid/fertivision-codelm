#!/bin/bash
# Pre-deployment validation script for FertiVision
# Validates all components before Google Cloud deployment

set -e

echo "🔍 FertiVision Pre-Deployment Validation"
echo "========================================"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️ $1${NC}"
}

VALIDATION_PASSED=true

# 1. Check core application files
echo "📁 Checking core application files..."
required_files=(
    "app.py"
    "requirements.txt"
    "Dockerfile"
    "cloudbuild.yaml"
    ".gcloudignore"
    ".dockerignore"
    "model_config.py"
    "model_service.py"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        print_status "Found: $file"
    else
        print_error "Missing: $file"
        VALIDATION_PASSED=false
    fi
done

# 2. Check Python syntax
echo ""
echo "🐍 Checking Python syntax..."
if command -v python3 &> /dev/null; then
    for py_file in app.py model_config.py model_service.py; do
        if python3 -m py_compile "$py_file" 2>/dev/null; then
            print_status "Syntax OK: $py_file"
        else
            print_error "Syntax error in: $py_file"
            VALIDATION_PASSED=false
        fi
    done
else
    print_warning "Python3 not found - skipping syntax check"
fi

# 3. Check Docker configuration
echo ""
echo "🐳 Checking Docker configuration..."

# Check Dockerfile
if grep -q "ENV PORT=8080" Dockerfile; then
    print_status "PORT environment variable configured"
else
    print_error "PORT environment variable not configured in Dockerfile"
    VALIDATION_PASSED=false
fi

if grep -q "gunicorn --bind 0.0.0.0:\$PORT" Dockerfile; then
    print_status "Dynamic port binding configured"
else
    print_error "Dynamic port binding not configured"
    VALIDATION_PASSED=false
fi

# 4. Check Cloud Build configuration
echo ""
echo "☁️ Checking Cloud Build configuration..."

if grep -q "gcr.io/\$PROJECT_ID/fertivision" cloudbuild.yaml; then
    print_status "Container image configuration OK"
else
    print_error "Container image configuration missing"
    VALIDATION_PASSED=false
fi

if grep -q "/health" cloudbuild.yaml; then
    print_status "Health check endpoint configured"
else
    print_warning "Health check endpoint not found in build config"
fi

# 5. Check optimization files
echo ""
echo "⚡ Checking optimization files..."

if [ -f ".gcloudignore" ]; then
    lines=$(wc -l < .gcloudignore)
    if [ "$lines" -gt 10 ]; then
        print_status ".gcloudignore configured with $lines exclusions"
    else
        print_warning ".gcloudignore seems minimal"
    fi
else
    print_error ".gcloudignore missing"
    VALIDATION_PASSED=false
fi

if [ -f ".dockerignore" ]; then
    lines=$(wc -l < .dockerignore)
    if [ "$lines" -gt 10 ]; then
        print_status ".dockerignore configured with $lines exclusions"
    else
        print_warning ".dockerignore seems minimal"
    fi
else
    print_error ".dockerignore missing"
    VALIDATION_PASSED=false
fi

# 6. Check deployment scripts
echo ""
echo "🚀 Checking deployment scripts..."

deployment_scripts=(
    "deploy-gcloud.sh"
    "deploy-cloud-optimized.sh"
    "deploy-free-cloudrun.sh"
)

for script in "${deployment_scripts[@]}"; do
    if [ -f "$script" ]; then
        if [ -x "$script" ]; then
            print_status "Executable: $script"
        else
            print_warning "Not executable: $script (run: chmod +x $script)"
        fi
    else
        print_warning "Missing: $script"
    fi
done

# 7. Check environment configuration
echo ""
echo "🔧 Checking environment configuration..."

if grep -q "FLASK_ENV=production" cloudbuild.yaml; then
    print_status "Production environment configured"
else
    print_warning "Production environment not explicitly set"
fi

if grep -q "DEBUG_MODE=true" cloudbuild.yaml; then
    print_status "Debug mode enabled for initial deployment"
else
    print_warning "Debug mode not enabled"
fi

# 8. Check application structure
echo ""
echo "📂 Checking application structure..."

required_dirs=(
    "static"
    "templates"
)

for dir in "${required_dirs[@]}"; do
    if [ -d "$dir" ]; then
        files_count=$(find "$dir" -type f | wc -l)
        print_status "Directory $dir exists with $files_count files"
    else
        print_warning "Directory $dir missing"
    fi
done

# 9. Check health endpoints
echo ""
echo "🏥 Checking health endpoint implementation..."

if grep -q "@app.route('/health')" app.py; then
    print_status "Health endpoint implemented"
else
    print_error "Health endpoint missing"
    VALIDATION_PASSED=false
fi

if grep -q "@app.route('/ready')" app.py; then
    print_status "Readiness endpoint implemented"
else
    print_warning "Readiness endpoint missing"
fi

# 10. Final validation summary
echo ""
echo "📊 Validation Summary"
echo "===================="

if [ "$VALIDATION_PASSED" = true ]; then
    print_status "All critical validations passed!"
    print_info "🚀 Ready for Google Cloud deployment"
    echo ""
    echo "Next steps:"
    echo "1. Run: ./deploy-free-cloudrun.sh (for quick deployment)"
    echo "2. Or: ./deploy-gcloud.sh (for full deployment)"
    echo "3. Or: Follow DEPLOY-GITHUB-TO-CLOUDRUN.md for GitHub integration"
    exit 0
else
    print_error "Some validations failed - please fix before deployment"
    exit 1
fi
