# 🚀 FertiVision Simplified Cloud Deployment

**One-Platform Solution for Demo and Presales**

---

## 🎯 **Recommended Stack: Vercel All-in-One**

### **Why Vercel is Perfect for FertiVision Cloud:**
- ✅ **Single platform** - no multiple services to manage
- ✅ **One-click deployment** from GitHub
- ✅ **Built-in database** (Vercel Postgres)
- ✅ **Built-in authentication** integration with Clerk
- ✅ **Automatic scaling** and global CDN
- ✅ **Generous free tier** - perfect for demos
- ✅ **Easy Razorpay integration** for payments

### 💰 **Cost Breakdown**
| Component | Free Tier | Cost After Free |
|-----------|-----------|-----------------|
| **Vercel Hosting** | 100GB bandwidth | $20/month |
| **Vercel Postgres** | 60 hours compute | $20/month |
| **Clerk Auth** | 10,000 MAU | $25/month |
| **Razorpay** | Transaction fees only | 2% per transaction |
| **Total** | **$0/month** for demos | ~$65/month at scale |

---

## 🚀 **One-Click Deployment Guide**

### **Step 1: Create Next.js App (5 minutes)**

```bash
# Create the app
npx create-next-app@latest fertivision-cloud \
  --typescript \
  --tailwind \
  --eslint \
  --app \
  --src-dir \
  --import-alias "@/*"

cd fertivision-cloud
```

### **Step 2: Add Dependencies (2 minutes)**

```bash
# Install required packages
npm install @clerk/nextjs razorpay @vercel/postgres @vercel/kv
npm install @headlessui/react @heroicons/react framer-motion
npm install react-dropzone react-hot-toast recharts
```

### **Step 3: Deploy to Vercel (1 minute)**

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy (will prompt for setup)
vercel

# Follow prompts:
# 1. Link to existing project? No
# 2. Project name: fertivision-cloud
# 3. Directory: ./
# 4. Override settings? No
```

### **Step 4: Add Database (2 minutes)**

```bash
# Add Vercel Postgres
vercel postgres create

# Add Vercel KV (for caching)
vercel kv create
```

### **Step 5: Configure Environment Variables**

In Vercel Dashboard → Project → Settings → Environment Variables:

```env
# Clerk Authentication
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
CLERK_SECRET_KEY=sk_test_...

# Razorpay
NEXT_PUBLIC_RAZORPAY_KEY_ID=rzp_test_...
RAZORPAY_KEY_SECRET=...

# Database (auto-configured by Vercel)
POSTGRES_URL=...
KV_URL=...
```

---

## 🔧 **Project Structure**

```
fertivision-cloud/
├── 📄 package.json
├── 📄 next.config.js
├── 📄 tailwind.config.js
├── 📄 .env.local
├── 📁 src/
│   ├── 📁 app/
│   │   ├── 📄 layout.tsx          # Root layout with Clerk
│   │   ├── 📄 page.tsx            # Landing page
│   │   ├── 📄 globals.css         # Global styles
│   │   ├── 📁 dashboard/
│   │   │   └── 📄 page.tsx        # User dashboard
│   │   ├── 📁 analysis/
│   │   │   └── 📄 page.tsx        # Analysis interface
│   │   ├── 📁 pricing/
│   │   │   └── 📄 page.tsx        # Pricing page
│   │   └── 📁 api/
│   │       ├── 📁 analyze/
│   │       │   ├── 📄 sperm.ts    # Sperm analysis API
│   │       │   ├── 📄 embryo.ts   # Embryo analysis API
│   │       │   └── 📄 follicle.ts # Follicle analysis API
│   │       ├── 📁 subscription/
│   │       │   ├── 📄 create.ts   # Create subscription
│   │       │   └── 📄 webhook.ts  # Razorpay webhook
│   │       └── 📁 user/
│   │           └── 📄 profile.ts  # User profile API
│   ├── 📁 components/
│   │   ├── 📄 Layout.tsx          # App layout
│   │   ├── 📄 AnalysisUpload.tsx  # Upload component
│   │   ├── 📄 ResultsDisplay.tsx  # Results component
│   │   ├── 📄 PricingCard.tsx     # Pricing component
│   │   └── 📄 SubscriptionGate.tsx # Subscription check
│   ├── 📁 lib/
│   │   ├── 📄 db.ts               # Database connection
│   │   ├── 📄 auth.ts             # Clerk helpers
│   │   ├── 📄 razorpay.ts         # Payment helpers
│   │   └── 📄 analysis.ts         # Analysis engine
│   └── 📁 types/
│       └── 📄 index.ts            # TypeScript types
├── 📁 public/
│   └── 📁 images/                 # Static assets
└── 📄 vercel.json                 # Vercel configuration
```

---

## 🔐 **Authentication Setup (Clerk)**

### **1. Create Clerk Application**
1. Visit [clerk.com](https://clerk.com)
2. Create new application
3. Choose: Email + Google + GitHub
4. Copy API keys

### **2. Add Clerk to Next.js**

```typescript
// src/app/layout.tsx
import { ClerkProvider } from '@clerk/nextjs'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body>{children}</body>
      </html>
    </ClerkProvider>
  )
}
```

### **3. Protect Routes**

```typescript
// src/app/dashboard/page.tsx
import { auth } from '@clerk/nextjs'
import { redirect } from 'next/navigation'

export default function Dashboard() {
  const { userId } = auth()
  
  if (!userId) {
    redirect('/sign-in')
  }
  
  return <div>Protected Dashboard</div>
}
```

---

## 💳 **Payment Integration (Razorpay)**

### **1. Create Razorpay Account**
1. Visit [razorpay.com](https://razorpay.com)
2. Complete KYC verification
3. Get API keys from dashboard

### **2. Create Subscription Plans**

```typescript
// src/lib/razorpay.ts
import Razorpay from 'razorpay'

const razorpay = new Razorpay({
  key_id: process.env.NEXT_PUBLIC_RAZORPAY_KEY_ID!,
  key_secret: process.env.RAZORPAY_KEY_SECRET!,
})

export const plans = {
  free: { price: 0, analyses: 10 },
  professional: { price: 299900, analyses: 500 }, // ₹2,999
  enterprise: { price: 999900, analyses: -1 },    // ₹9,999
}

export async function createSubscription(planId: string, customerId: string) {
  return await razorpay.subscriptions.create({
    plan_id: planId,
    customer_notify: 1,
    total_count: 12, // 12 months
    notes: { customer_id: customerId }
  })
}
```

### **3. Frontend Payment Integration**

```typescript
// src/components/PricingCard.tsx
'use client'
import { useUser } from '@clerk/nextjs'

export default function PricingCard({ plan }: { plan: any }) {
  const { user } = useUser()
  
  const handleSubscribe = async () => {
    const response = await fetch('/api/subscription/create', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ planId: plan.id, userId: user?.id })
    })
    
    const { subscription } = await response.json()
    
    // Open Razorpay checkout
    const options = {
      subscription_id: subscription.id,
      name: 'FertiVision',
      description: `${plan.name} Plan`,
      handler: function (response: any) {
        // Handle successful payment
        window.location.href = '/dashboard'
      }
    }
    
    const rzp = new (window as any).Razorpay(options)
    rzp.open()
  }
  
  return (
    <div className="pricing-card">
      <h3>{plan.name}</h3>
      <p>₹{plan.price / 100}/month</p>
      <button onClick={handleSubscribe}>Subscribe</button>
    </div>
  )
}
```

---

## 🗄️ **Database Setup (Vercel Postgres)**

### **1. Database Schema**

```sql
-- Create tables in Vercel Postgres dashboard
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  clerk_user_id VARCHAR(255) UNIQUE NOT NULL,
  email VARCHAR(255) NOT NULL,
  subscription_plan VARCHAR(50) DEFAULT 'free',
  analyses_used INTEGER DEFAULT 0,
  analyses_limit INTEGER DEFAULT 10,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE analyses (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  analysis_type VARCHAR(50) NOT NULL,
  image_url VARCHAR(500),
  results JSONB NOT NULL,
  confidence DECIMAL(5,2),
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE subscriptions (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  razorpay_subscription_id VARCHAR(255),
  plan_id VARCHAR(50),
  status VARCHAR(50),
  current_period_start TIMESTAMP,
  current_period_end TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW()
);
```

### **2. Database Connection**

```typescript
// src/lib/db.ts
import { sql } from '@vercel/postgres'

export async function createUser(clerkUserId: string, email: string) {
  return await sql`
    INSERT INTO users (clerk_user_id, email)
    VALUES (${clerkUserId}, ${email})
    ON CONFLICT (clerk_user_id) DO NOTHING
    RETURNING *
  `
}

export async function getUserByClerkId(clerkUserId: string) {
  return await sql`
    SELECT * FROM users WHERE clerk_user_id = ${clerkUserId}
  `
}

export async function saveAnalysis(userId: number, analysisType: string, results: any) {
  return await sql`
    INSERT INTO analyses (user_id, analysis_type, results, confidence)
    VALUES (${userId}, ${analysisType}, ${JSON.stringify(results)}, ${results.confidence})
    RETURNING *
  `
}
```

---

## 🧬 **Analysis API Implementation**

### **Sperm Analysis Endpoint**

```typescript
// src/app/api/analyze/sperm/route.ts
import { auth } from '@clerk/nextjs'
import { NextRequest, NextResponse } from 'next/server'
import { getUserByClerkId, saveAnalysis } from '@/lib/db'
import { analyzeSpermImage } from '@/lib/analysis'

export async function POST(request: NextRequest) {
  try {
    const { userId } = auth()
    if (!userId) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }
    
    // Get user from database
    const userResult = await getUserByClerkId(userId)
    const user = userResult.rows[0]
    
    if (!user) {
      return NextResponse.json({ error: 'User not found' }, { status: 404 })
    }
    
    // Check usage limits
    if (user.analyses_used >= user.analyses_limit && user.subscription_plan === 'free') {
      return NextResponse.json({ error: 'Usage limit exceeded' }, { status: 403 })
    }
    
    // Get image from form data
    const formData = await request.formData()
    const image = formData.get('image') as File
    
    if (!image) {
      return NextResponse.json({ error: 'No image provided' }, { status: 400 })
    }
    
    // Perform analysis
    const analysisResult = await analyzeSpermImage(image)
    
    // Save to database
    await saveAnalysis(user.id, 'sperm', analysisResult)
    
    // Update usage count
    await sql`
      UPDATE users 
      SET analyses_used = analyses_used + 1 
      WHERE id = ${user.id}
    `
    
    return NextResponse.json({
      success: true,
      ...analysisResult
    })
    
  } catch (error) {
    console.error('Analysis error:', error)
    return NextResponse.json({ error: 'Analysis failed' }, { status: 500 })
  }
}
```

---

## 🚀 **Deployment Commands**

### **Initial Deployment**
```bash
# 1. Create and deploy
npx create-next-app@latest fertivision-cloud --typescript --tailwind
cd fertivision-cloud
vercel

# 2. Add database
vercel postgres create
vercel kv create

# 3. Set environment variables in Vercel dashboard

# 4. Deploy updates
vercel --prod
```

### **Continuous Deployment**
```bash
# Connect to GitHub for auto-deployment
vercel --prod
# Choose: Link to existing project
# Choose: Connect to GitHub repository
# Every push to main branch will auto-deploy
```

---

## 📊 **Monitoring and Analytics**

### **Built-in Vercel Analytics**
- ✅ **Performance monitoring** - automatic
- ✅ **Error tracking** - built-in
- ✅ **Usage analytics** - real-time
- ✅ **Speed insights** - Core Web Vitals

### **Custom Analytics**
```typescript
// src/lib/analytics.ts
import { track } from '@vercel/analytics'

export function trackAnalysis(type: string, success: boolean) {
  track('analysis_performed', {
    type,
    success: success.toString(),
    timestamp: new Date().toISOString()
  })
}

export function trackSubscription(plan: string) {
  track('subscription_created', {
    plan,
    timestamp: new Date().toISOString()
  })
}
```

---

## 🎯 **Perfect for Demo and Presales**

### **Demo Features**
- ✅ **Live authentication** with Google/GitHub login
- ✅ **Real payment flow** with Razorpay test mode
- ✅ **Usage limits** and subscription gates
- ✅ **Professional UI** with Tailwind CSS
- ✅ **Real-time analysis** with progress indicators
- ✅ **Responsive design** for all devices

### **Presales Benefits**
- ✅ **Instant deployment** - show customers in minutes
- ✅ **Custom domains** - use your own branding
- ✅ **SSL certificates** - automatic and secure
- ✅ **Global CDN** - fast worldwide access
- ✅ **Scalability demo** - show enterprise readiness

---

## 💰 **Cost Optimization**

### **Free Tier Maximization**
- **Vercel**: 100GB bandwidth, unlimited projects
- **Vercel Postgres**: 60 hours compute time
- **Clerk**: 10,000 monthly active users
- **Razorpay**: No monthly fees, only transaction costs

### **Scaling Strategy**
- **0-100 users**: Stay on free tier ($0/month)
- **100-1000 users**: Upgrade Vercel Pro ($20/month)
- **1000+ users**: Add Vercel Postgres Pro ($20/month)
- **Enterprise**: Custom pricing with dedicated support

---

## 🎉 **Summary: Why This Stack Wins**

### ✅ **Simplicity**
- **One platform** (Vercel) handles everything
- **One-click deployment** from GitHub
- **Automatic scaling** and SSL
- **Built-in monitoring** and analytics

### ✅ **Cost-Effective**
- **Free tier** perfect for demos
- **Predictable pricing** as you scale
- **No hidden costs** or complex billing

### ✅ **Developer Experience**
- **Modern stack** (Next.js, TypeScript, Tailwind)
- **Great documentation** and community
- **Easy debugging** and monitoring
- **Fast iteration** and deployment

### ✅ **Enterprise Ready**
- **Automatic scaling** to millions of users
- **Global CDN** for worldwide performance
- **Security best practices** built-in
- **Compliance** features available

---

**🚀 Your FertiVision Cloud SaaS can be live in under 30 minutes with this simplified approach!**

© 2025 FertiVision powered by AI | Made by greybrain.ai
