#!/bin/bash

# 🚀 FertiVision Cloud SaaS - One-Click Setup Script
# Creates a complete cloud-ready version using Vercel + Clerk + Razorpay

echo "🚀 FertiVision Cloud SaaS Setup"
echo "==============================="

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

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

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed. Please install Node.js 18+ first."
    echo "Visit: https://nodejs.org/"
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    print_error "Node.js 18+ is required. Current version: $(node --version)"
    exit 1
fi

print_status "Node.js $(node --version) detected"

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    print_error "npm is not installed. Please install npm first."
    exit 1
fi

print_status "npm $(npm --version) detected"

# Project name
PROJECT_NAME="fertivision-cloud-saas"
print_info "Creating project: $PROJECT_NAME"

# Create Next.js app
print_info "Creating Next.js application with TypeScript and Tailwind..."
npx create-next-app@latest $PROJECT_NAME \
  --typescript \
  --tailwind \
  --eslint \
  --app \
  --src-dir \
  --import-alias "@/*" \
  --use-npm

if [ $? -ne 0 ]; then
    print_error "Failed to create Next.js app"
    exit 1
fi

cd $PROJECT_NAME

print_status "Next.js app created successfully"

# Install additional dependencies
print_info "Installing FertiVision dependencies..."
npm install @clerk/nextjs razorpay @vercel/postgres @vercel/kv @vercel/analytics

# Install UI dependencies
npm install @headlessui/react @heroicons/react framer-motion
npm install react-dropzone react-hot-toast recharts date-fns

# Install development dependencies
npm install -D @types/node

print_status "Dependencies installed"

# Create environment variables template
print_info "Creating environment configuration..."
cat > .env.local << 'EOF'
# Clerk Authentication
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_your_key_here
CLERK_SECRET_KEY=sk_test_your_key_here

# Razorpay
NEXT_PUBLIC_RAZORPAY_KEY_ID=rzp_test_your_key_here
RAZORPAY_KEY_SECRET=your_secret_here

# Database (will be auto-configured by Vercel)
POSTGRES_URL=
KV_URL=

# App Configuration
NEXT_PUBLIC_APP_NAME=FertiVision
NEXT_PUBLIC_APP_URL=http://localhost:3000
EOF

print_status "Environment template created"

# Create basic project structure
print_info "Setting up project structure..."

# Create directories
mkdir -p src/components
mkdir -p src/lib
mkdir -p src/types
mkdir -p src/app/api/analyze
mkdir -p src/app/api/subscription
mkdir -p src/app/api/user
mkdir -p src/app/dashboard
mkdir -p src/app/analysis
mkdir -p src/app/pricing
mkdir -p src/app/sign-in
mkdir -p src/app/sign-up

# Create basic layout with Clerk
cat > src/app/layout.tsx << 'EOF'
import { ClerkProvider } from '@clerk/nextjs'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'FertiVision - AI-Enhanced Reproductive Medicine',
  description: 'Advanced AI analysis for reproductive medicine',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body className={inter.className}>{children}</body>
      </html>
    </ClerkProvider>
  )
}
EOF

# Create landing page
cat > src/app/page.tsx << 'EOF'
import { SignInButton, SignUpButton, UserButton, auth } from '@clerk/nextjs'
import Link from 'next/link'

export default function Home() {
  const { userId } = auth()

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <nav className="flex justify-between items-center p-6">
        <h1 className="text-2xl font-bold text-indigo-900">FertiVision</h1>
        <div className="flex items-center space-x-4">
          {userId ? (
            <>
              <Link href="/dashboard" className="text-indigo-600 hover:text-indigo-800">
                Dashboard
              </Link>
              <UserButton />
            </>
          ) : (
            <>
              <SignInButton mode="modal">
                <button className="text-indigo-600 hover:text-indigo-800">
                  Sign In
                </button>
              </SignInButton>
              <SignUpButton mode="modal">
                <button className="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700">
                  Get Started
                </button>
              </SignUpButton>
            </>
          )}
        </div>
      </nav>

      <div className="container mx-auto px-6 py-20 text-center">
        <h1 className="text-5xl font-bold text-gray-900 mb-6">
          AI-Enhanced Reproductive Medicine
        </h1>
        <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
          Advanced AI analysis for sperm, oocyte, embryo, and follicle assessment. 
          WHO 2021 and ESHRE compliant analysis with enterprise-grade accuracy.
        </p>
        
        <div className="grid md:grid-cols-3 gap-8 mt-16">
          <div className="bg-white p-6 rounded-lg shadow-lg">
            <h3 className="text-xl font-semibold mb-4">🧬 Sperm Analysis</h3>
            <p className="text-gray-600">WHO 2021 compliant semen analysis with automated parameter assessment</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-lg">
            <h3 className="text-xl font-semibold mb-4">🥚 Oocyte Assessment</h3>
            <p className="text-gray-600">ESHRE guidelines-based maturity evaluation and quality grading</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-lg">
            <h3 className="text-xl font-semibold mb-4">👶 Embryo Grading</h3>
            <p className="text-gray-600">Gardner grading system for Day 3-6 embryo development assessment</p>
          </div>
        </div>

        {!userId && (
          <div className="mt-12">
            <SignUpButton mode="modal">
              <button className="bg-indigo-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-indigo-700 transition-colors">
                Start Free Trial
              </button>
            </SignUpButton>
          </div>
        )}
      </div>
    </main>
  )
}
EOF

# Create dashboard page
cat > src/app/dashboard/page.tsx << 'EOF'
import { auth } from '@clerk/nextjs'
import { redirect } from 'next/navigation'
import Link from 'next/link'

export default function Dashboard() {
  const { userId } = auth()
  
  if (!userId) {
    redirect('/sign-in')
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm border-b">
        <div className="container mx-auto px-6 py-4">
          <h1 className="text-2xl font-bold text-indigo-900">FertiVision Dashboard</h1>
        </div>
      </nav>

      <div className="container mx-auto px-6 py-8">
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          <Link href="/analysis" className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition-shadow">
            <h3 className="text-xl font-semibold mb-2">🧬 New Analysis</h3>
            <p className="text-gray-600">Upload images for AI-powered analysis</p>
          </Link>
          
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-xl font-semibold mb-2">📊 Recent Results</h3>
            <p className="text-gray-600">View your analysis history</p>
          </div>
          
          <Link href="/pricing" className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition-shadow">
            <h3 className="text-xl font-semibold mb-2">💳 Subscription</h3>
            <p className="text-gray-600">Manage your plan and billing</p>
          </Link>
        </div>
      </div>
    </div>
  )
}
EOF

# Create analysis page
cat > src/app/analysis/page.tsx << 'EOF'
import { auth } from '@clerk/nextjs'
import { redirect } from 'next/navigation'

export default function Analysis() {
  const { userId } = auth()
  
  if (!userId) {
    redirect('/sign-in')
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm border-b">
        <div className="container mx-auto px-6 py-4">
          <h1 className="text-2xl font-bold text-indigo-900">AI Analysis</h1>
        </div>
      </nav>

      <div className="container mx-auto px-6 py-8">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Upload Medical Images</h2>
          <div className="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center">
            <p className="text-gray-500 mb-4">Drag and drop images here, or click to select</p>
            <button className="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700">
              Select Images
            </button>
          </div>
          
          <div className="mt-6 grid md:grid-cols-2 lg:grid-cols-4 gap-4">
            <button className="p-4 border rounded-lg hover:bg-gray-50">
              🧬 Sperm Analysis
            </button>
            <button className="p-4 border rounded-lg hover:bg-gray-50">
              🥚 Oocyte Assessment
            </button>
            <button className="p-4 border rounded-lg hover:bg-gray-50">
              👶 Embryo Grading
            </button>
            <button className="p-4 border rounded-lg hover:bg-gray-50">
              🔬 Follicle Count
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
EOF

# Create pricing page
cat > src/app/pricing/page.tsx << 'EOF'
export default function Pricing() {
  const plans = [
    {
      name: 'Free',
      price: 0,
      analyses: 10,
      features: ['10 analyses/month', 'Basic support', 'Standard processing']
    },
    {
      name: 'Professional',
      price: 2999,
      analyses: 500,
      features: ['500 analyses/month', 'Priority support', 'Fast processing', 'API access']
    },
    {
      name: 'Enterprise',
      price: 9999,
      analyses: -1,
      features: ['Unlimited analyses', '24/7 support', 'Custom integrations', 'White-label']
    }
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-6 py-16">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">Choose Your Plan</h1>
          <p className="text-xl text-gray-600">Scale your reproductive medicine practice with AI</p>
        </div>

        <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          {plans.map((plan) => (
            <div key={plan.name} className="bg-white rounded-lg shadow-lg p-8">
              <h3 className="text-2xl font-bold text-center mb-4">{plan.name}</h3>
              <div className="text-center mb-6">
                <span className="text-4xl font-bold">₹{plan.price}</span>
                <span className="text-gray-600">/month</span>
              </div>
              <ul className="space-y-3 mb-8">
                {plan.features.map((feature, index) => (
                  <li key={index} className="flex items-center">
                    <span className="text-green-500 mr-2">✓</span>
                    {feature}
                  </li>
                ))}
              </ul>
              <button className="w-full bg-indigo-600 text-white py-3 rounded-lg hover:bg-indigo-700 transition-colors">
                {plan.price === 0 ? 'Get Started' : 'Subscribe'}
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
EOF

# Create basic API endpoint
cat > src/app/api/analyze/sperm/route.ts << 'EOF'
import { auth } from '@clerk/nextjs'
import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  try {
    const { userId } = auth()
    
    if (!userId) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    // Mock analysis result for demo
    const mockResult = {
      success: true,
      analysis_id: `analysis_${Date.now()}`,
      classification: 'Normozoospermia',
      confidence: 94.2,
      parameters: {
        concentration: 45.0,
        progressive_motility: 65.0,
        normal_morphology: 8.0
      },
      technical_details: {
        'Concentration': '45.0 × 10⁶/ml (Ref: >15)',
        'Progressive Motility': '65% (Ref: >32%)',
        'Normal Morphology': '8% (Ref: >4%)'
      },
      clinical_recommendations: [
        'Excellent fertility potential',
        'Suitable for all ART procedures'
      ],
      timestamp: new Date().toISOString(),
      processing_time: 2.3
    }

    return NextResponse.json(mockResult)
    
  } catch (error) {
    console.error('Analysis error:', error)
    return NextResponse.json({ error: 'Analysis failed' }, { status: 500 })
  }
}
EOF

# Create vercel.json configuration
cat > vercel.json << 'EOF'
{
  "version": 2,
  "env": {
    "NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY": "@clerk_publishable_key",
    "CLERK_SECRET_KEY": "@clerk_secret_key",
    "NEXT_PUBLIC_RAZORPAY_KEY_ID": "@razorpay_key_id",
    "RAZORPAY_KEY_SECRET": "@razorpay_key_secret"
  },
  "build": {
    "env": {
      "NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY": "@clerk_publishable_key",
      "CLERK_SECRET_KEY": "@clerk_secret_key"
    }
  }
}
EOF

# Update package.json scripts
npm pkg set scripts.dev="next dev"
npm pkg set scripts.build="next build"
npm pkg set scripts.start="next start"
npm pkg set scripts.deploy="vercel --prod"

print_status "Project structure created"

# Create README for the cloud version
cat > README.md << 'EOF'
# 🌐 FertiVision Cloud SaaS

AI-Enhanced Reproductive Medicine Analysis Platform - Cloud Version

## 🚀 Quick Deploy to Vercel

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Deploy**
   ```bash
   vercel
   ```

3. **Add Database**
   ```bash
   vercel postgres create
   vercel kv create
   ```

4. **Configure Environment Variables**
   - Go to Vercel Dashboard → Project → Settings → Environment Variables
   - Add your Clerk and Razorpay keys

## 🔧 Local Development

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

## 🔑 Required Environment Variables

```env
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
CLERK_SECRET_KEY=sk_test_...
NEXT_PUBLIC_RAZORPAY_KEY_ID=rzp_test_...
RAZORPAY_KEY_SECRET=...
```

## 📚 Documentation

See `../simplified-cloud-deployment.md` for complete setup guide.

© 2025 FertiVision powered by AI | Made by greybrain.ai
EOF

print_status "Cloud SaaS project created successfully!"

echo ""
echo "🎉 FertiVision Cloud SaaS Setup Complete!"
echo "========================================"
echo ""
print_info "Project created in: $PROJECT_NAME"
echo ""
print_warning "Next steps:"
echo "1. cd $PROJECT_NAME"
echo "2. Configure environment variables in .env.local"
echo "3. npm run dev (for local development)"
echo "4. vercel (to deploy to cloud)"
echo ""
print_info "For complete setup guide, see: simplified-cloud-deployment.md"
echo ""
print_status "Ready for demo and presales! 🚀"
