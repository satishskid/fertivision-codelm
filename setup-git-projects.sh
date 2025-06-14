#!/bin/bash

# 🚀 FertiVision Git Projects Setup Script
# Creates separate git repositories for Local Development and Cloud SaaS versions

echo "🔬 Setting up FertiVision Git Projects"
echo "======================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if git is installed
if ! command -v git &> /dev/null; then
    print_error "Git is not installed. Please install git first."
    exit 1
fi

print_info "Git is installed. Proceeding with setup..."

# Create base directory
BASE_DIR="fertivision-projects"
mkdir -p "$BASE_DIR"
cd "$BASE_DIR"

print_status "Created base directory: $BASE_DIR"

# =============================================================================
# LOCAL DEVELOPMENT VERSION
# =============================================================================

print_info "Setting up Local Development Version..."

# Create local development repository
LOCAL_DIR="fertivision-local-dev"
mkdir -p "$LOCAL_DIR"
cd "$LOCAL_DIR"

# Initialize git repository
git init
print_status "Initialized git repository for Local Development"

# Create .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/
api_audit.log

# Uploads
uploads/
api_uploads/
temp/

# Environment variables
.env
.env.local
.env.production

# Database
*.db
*.sqlite
*.sqlite3

# Cache
.cache/
.pytest_cache/

# Coverage
htmlcov/
.coverage
.coverage.*
coverage.xml

# Local development
local_config.py
test_images/
EOF

# Create requirements.txt
cat > requirements.txt << 'EOF'
# Core dependencies
Flask==3.0.0
Werkzeug==3.0.1
Pillow==10.1.0
numpy==1.24.3
opencv-python==4.8.1.78
scikit-image==0.22.0
requests==2.31.0

# Database
SQLAlchemy==2.0.23
sqlite3

# Image processing
imageio==2.31.5
matplotlib==3.8.2

# API and web
python-multipart==0.0.6
python-jose==3.3.0
passlib==1.7.4

# Development
pytest==7.4.3
pytest-cov==4.1.0
black==23.11.0
flake8==6.1.0

# Optional AI providers
groq==0.4.1
openai==1.3.7
EOF

# Create LICENSE
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2025 FertiVision powered by AI | Made by greybrain.ai

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

# Copy files from current directory (assuming we're in the workspace)
print_info "Copying files to Local Development repository..."

# Copy main files
cp ../../netlify-deploy-fixed/* . 2>/dev/null || true
cp ../../api_server.py . 2>/dev/null || true
cp ../../fertivision_sdk.py . 2>/dev/null || true
cp ../../API_DOCUMENTATION.md . 2>/dev/null || true
cp ../../enhanced_reproductive_system.py . 2>/dev/null || true
cp ../../config.py . 2>/dev/null || true

# Copy examples directory
mkdir -p examples
cp ../../examples/* examples/ 2>/dev/null || true

# Create initial commit
git add .
git commit -m "🎉 Initial commit: FertiVision Local Development Edition

Features:
- Complete standalone application
- Flask API server with EMR integration
- Python SDK for easy integration
- Frontend web interface
- Demo mode with no external dependencies
- Comprehensive documentation

© 2025 FertiVision powered by AI | Made by greybrain.ai"

print_status "Local Development repository created and committed"

# Go back to base directory
cd ..

# =============================================================================
# CLOUD SAAS VERSION
# =============================================================================

print_info "Setting up Cloud SaaS Version..."

# Create cloud SaaS repository
CLOUD_DIR="fertivision-cloud-saas"
mkdir -p "$CLOUD_DIR"
cd "$CLOUD_DIR"

# Initialize git repository
git init
print_status "Initialized git repository for Cloud SaaS"

# Create .gitignore
cat > .gitignore << 'EOF'
# Dependencies
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environment
venv/
env/
ENV/

# Next.js
.next/
out/

# Production
/build

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local
.env.example

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# Coverage directory used by tools like istanbul
coverage/
.nyc_output

# Dependency directories
jspm_packages/

# Optional npm cache directory
.npm

# Optional eslint cache
.eslintcache

# Microbundle cache
.rpt2_cache/
.rts2_cache_cjs/
.rts2_cache_es/
.rts2_cache_umd/

# Optional REPL history
.node_repl_history

# Output of 'npm pack'
*.tgz

# Yarn Integrity file
.yarn-integrity

# parcel-bundler cache (https://parceljs.org/)
.cache
.parcel-cache

# Stores VSCode versions used for testing VSCode extensions
.vscode-test

# Temporary folders
tmp/
temp/

# Database
*.db
*.sqlite
*.sqlite3

# Uploads
uploads/
api_uploads/

# Cache
.cache/
.pytest_cache/

# Vercel
.vercel

# Railway
.railway/
EOF

# Create package.json for frontend
mkdir -p frontend
cd frontend

cat > package.json << 'EOF'
{
  "name": "fertivision-frontend",
  "version": "1.0.0",
  "description": "FertiVision Cloud SaaS Frontend",
  "main": "pages/index.js",
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "type-check": "tsc --noEmit"
  },
  "dependencies": {
    "next": "14.0.4",
    "react": "18.2.0",
    "react-dom": "18.2.0",
    "@clerk/nextjs": "4.29.1",
    "razorpay": "2.9.2",
    "axios": "1.6.2",
    "@tailwindcss/forms": "0.5.7",
    "@headlessui/react": "1.7.17",
    "@heroicons/react": "2.0.18",
    "framer-motion": "10.16.16",
    "react-hot-toast": "2.4.1",
    "react-dropzone": "14.2.3",
    "recharts": "2.8.0",
    "date-fns": "2.30.0"
  },
  "devDependencies": {
    "@types/node": "20.10.4",
    "@types/react": "18.2.45",
    "@types/react-dom": "18.2.18",
    "autoprefixer": "10.4.16",
    "eslint": "8.56.0",
    "eslint-config-next": "14.0.4",
    "postcss": "8.4.32",
    "tailwindcss": "3.3.6",
    "typescript": "5.3.3"
  },
  "keywords": [
    "fertivision",
    "ivf",
    "ai",
    "medical",
    "saas"
  ],
  "author": "greybrain.ai",
  "license": "MIT"
}
EOF

# Create .env.example
cat > .env.example << 'EOF'
# Clerk Authentication
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
CLERK_SECRET_KEY=sk_test_...

# API Configuration
NEXT_PUBLIC_API_URL=https://your-api.railway.app
NEXT_PUBLIC_APP_URL=https://your-app.vercel.app

# Razorpay
NEXT_PUBLIC_RAZORPAY_KEY_ID=rzp_test_...
RAZORPAY_KEY_SECRET=...

# App Configuration
NEXT_PUBLIC_APP_NAME=FertiVision
NEXT_PUBLIC_APP_DESCRIPTION=AI-Enhanced Reproductive Medicine Analysis
EOF

cd .. # Back to cloud directory

# Create backend requirements.txt
mkdir -p backend
cd backend

cat > requirements.txt << 'EOF'
# Core Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0

# Database
sqlalchemy==2.0.23
alembic==1.13.1
psycopg2-binary==2.9.9
asyncpg==0.29.0

# Authentication & Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6

# HTTP Client
httpx==0.25.2
requests==2.31.0

# Image Processing
Pillow==10.1.0
opencv-python==4.8.1.78
numpy==1.24.3
scikit-image==0.22.0

# File Storage
cloudinary==1.36.0

# Payment Processing
razorpay==1.3.0

# Background Tasks
celery==5.3.4
redis==5.0.1

# Monitoring & Logging
sentry-sdk[fastapi]==1.38.0

# Development
pytest==7.4.3
pytest-asyncio==0.21.1
black==23.11.0
isort==5.12.0
flake8==6.1.0

# Production
gunicorn==21.2.0
EOF

# Create .env.example
cat > .env.example << 'EOF'
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/fertivision

# Authentication
CLERK_SECRET_KEY=sk_test_...
CLERK_WEBHOOK_SECRET=whsec_...

# Payments
RAZORPAY_KEY_ID=rzp_test_...
RAZORPAY_KEY_SECRET=...
RAZORPAY_WEBHOOK_SECRET=...

# File Storage
CLOUDINARY_CLOUD_NAME=...
CLOUDINARY_API_KEY=...
CLOUDINARY_API_SECRET=...

# Redis
REDIS_URL=redis://localhost:6379

# App Settings
SECRET_KEY=your-secret-key-here
ENVIRONMENT=development
DEBUG=True
ALLOWED_ORIGINS=http://localhost:3000,https://your-app.vercel.app

# Monitoring
SENTRY_DSN=...
EOF

cd .. # Back to cloud directory

# Create railway.toml
cat > railway.toml << 'EOF'
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT"
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10

[environments.production]
variables = { ENVIRONMENT = "production" }
EOF

# Create vercel.json
cat > vercel.json << 'EOF'
{
  "version": 2,
  "builds": [
    {
      "src": "frontend/package.json",
      "use": "@vercel/next"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "frontend/$1"
    }
  ],
  "env": {
    "NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY": "@clerk_publishable_key",
    "CLERK_SECRET_KEY": "@clerk_secret_key",
    "NEXT_PUBLIC_API_URL": "@api_url",
    "NEXT_PUBLIC_RAZORPAY_KEY_ID": "@razorpay_key_id"
  }
}
EOF

# Create initial commit
git add .
git commit -m "🚀 Initial commit: FertiVision Cloud SaaS Edition

Features:
- Next.js frontend with Clerk authentication
- FastAPI backend with PostgreSQL
- Razorpay subscription billing
- Multi-tenant SaaS architecture
- Cloud deployment ready (Vercel + Railway)
- Enterprise-grade scalability

© 2025 FertiVision powered by AI | Made by greybrain.ai"

print_status "Cloud SaaS repository created and committed"

# Go back to base directory
cd ..

# =============================================================================
# SUMMARY
# =============================================================================

echo ""
echo "🎉 Git Projects Setup Complete!"
echo "==============================="
echo ""
print_status "Created two separate repositories:"
echo ""
print_info "1. 🏠 Local Development Version:"
echo "   📁 Directory: $BASE_DIR/$LOCAL_DIR"
echo "   🎯 Purpose: Local clinic deployments, R&D, education"
echo "   🔧 Tech: Flask API + Static Frontend"
echo "   💰 Cost: Free"
echo ""
print_info "2. ☁️  Cloud SaaS Version:"
echo "   📁 Directory: $BASE_DIR/$CLOUD_DIR"
echo "   🎯 Purpose: Multi-tenant SaaS, enterprise customers"
echo "   🔧 Tech: Next.js + FastAPI + PostgreSQL"
echo "   💰 Cost: Subscription-based"
echo ""
print_warning "Next Steps:"
echo "1. Push repositories to GitHub"
echo "2. Set up cloud deployment (see deployment-guide.md)"
echo "3. Configure Clerk authentication"
echo "4. Set up Razorpay payments"
echo "5. Deploy to production"
echo ""
print_info "Commands to push to GitHub:"
echo ""
echo "# For Local Development:"
echo "cd $BASE_DIR/$LOCAL_DIR"
echo "git remote add origin https://github.com/your-username/fertivision-local-dev.git"
echo "git push -u origin main"
echo ""
echo "# For Cloud SaaS:"
echo "cd $BASE_DIR/$CLOUD_DIR"
echo "git remote add origin https://github.com/your-username/fertivision-cloud-saas.git"
echo "git push -u origin main"
echo ""
print_status "Setup complete! 🚀"
EOF
