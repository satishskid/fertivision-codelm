# 🚀 FertiVision Cloud Deployment Guide

**Complete step-by-step guide for deploying FertiVision SaaS to production**

---

## 🎯 **Recommended Free Cloud Stack**

### 🏆 **Primary Stack (Recommended)**
- **Frontend**: Vercel (Free tier: Unlimited personal projects)
- **Backend**: Railway ($5/month after 500 hours free)
- **Database**: Supabase (Free tier: 50,000 MAU)
- **Auth**: Clerk (Free tier: 10,000 MAU)
- **Payments**: Razorpay (Transaction-based fees only)
- **File Storage**: Cloudinary (Free tier: 25 credits/month)

### 💰 **Total Monthly Cost**: ~$5-10 for small scale

---

## 📋 **Pre-Deployment Checklist**

### 1. **Account Setup**
- [ ] Vercel account created
- [ ] Railway account created
- [ ] Supabase project created
- [ ] Clerk application created
- [ ] Razorpay account created (with KYC completed)
- [ ] Cloudinary account created

### 2. **Domain & SSL**
- [ ] Domain purchased (optional for demo)
- [ ] DNS configured
- [ ] SSL certificates (handled by Vercel)

---

## 🔧 **Step-by-Step Deployment**

### Step 1: Database Setup (Supabase)

1. **Create Supabase Project**
   ```bash
   # Visit https://supabase.com
   # Create new project
   # Note down: Project URL, API Key, Database Password
   ```

2. **Run Database Migrations**
   ```sql
   -- Execute in Supabase SQL Editor
   
   -- Users table
   CREATE TABLE users (
       id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
       clerk_user_id VARCHAR UNIQUE NOT NULL,
       email VARCHAR NOT NULL,
       full_name VARCHAR,
       subscription_plan VARCHAR DEFAULT 'free',
       analyses_used INTEGER DEFAULT 0,
       analyses_limit INTEGER DEFAULT 10,
       created_at TIMESTAMP DEFAULT NOW(),
       updated_at TIMESTAMP DEFAULT NOW()
   );

   -- Analyses table
   CREATE TABLE analyses (
       id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
       user_id UUID REFERENCES users(id) ON DELETE CASCADE,
       analysis_type VARCHAR NOT NULL,
       image_url VARCHAR,
       image_filename VARCHAR,
       patient_id VARCHAR,
       case_id VARCHAR,
       results JSONB NOT NULL,
       confidence DECIMAL,
       processing_time INTEGER,
       created_at TIMESTAMP DEFAULT NOW()
   );

   -- Subscriptions table
   CREATE TABLE subscriptions (
       id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
       user_id UUID REFERENCES users(id) ON DELETE CASCADE,
       razorpay_subscription_id VARCHAR UNIQUE,
       plan_id VARCHAR NOT NULL,
       status VARCHAR DEFAULT 'created',
       current_period_start TIMESTAMP,
       current_period_end TIMESTAMP,
       created_at TIMESTAMP DEFAULT NOW(),
       updated_at TIMESTAMP DEFAULT NOW()
   );

   -- Usage tracking
   CREATE TABLE usage_logs (
       id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
       user_id UUID REFERENCES users(id) ON DELETE CASCADE,
       analysis_id UUID REFERENCES analyses(id) ON DELETE CASCADE,
       action VARCHAR NOT NULL,
       metadata JSONB,
       created_at TIMESTAMP DEFAULT NOW()
   );

   -- Indexes for performance
   CREATE INDEX idx_users_clerk_id ON users(clerk_user_id);
   CREATE INDEX idx_analyses_user_id ON analyses(user_id);
   CREATE INDEX idx_analyses_created_at ON analyses(created_at);
   CREATE INDEX idx_subscriptions_user_id ON subscriptions(user_id);
   ```

3. **Enable Row Level Security (RLS)**
   ```sql
   -- Enable RLS
   ALTER TABLE users ENABLE ROW LEVEL SECURITY;
   ALTER TABLE analyses ENABLE ROW LEVEL SECURITY;
   ALTER TABLE subscriptions ENABLE ROW LEVEL SECURITY;
   ALTER TABLE usage_logs ENABLE ROW LEVEL SECURITY;

   -- Create policies
   CREATE POLICY "Users can view own data" ON users
       FOR ALL USING (clerk_user_id = auth.jwt() ->> 'sub');

   CREATE POLICY "Users can view own analyses" ON analyses
       FOR ALL USING (user_id IN (
           SELECT id FROM users WHERE clerk_user_id = auth.jwt() ->> 'sub'
       ));
   ```

### Step 2: Authentication Setup (Clerk)

1. **Create Clerk Application**
   ```bash
   # Visit https://clerk.com
   # Create new application
   # Choose: Email + Password, Google, GitHub
   # Note down: Publishable Key, Secret Key
   ```

2. **Configure Clerk Settings**
   ```javascript
   // In Clerk Dashboard:
   // 1. Enable email verification
   // 2. Configure OAuth providers
   // 3. Set up webhooks for user events
   // 4. Configure session settings
   ```

3. **Webhook Configuration**
   ```javascript
   // Webhook URL: https://your-api.railway.app/webhooks/clerk
   // Events to listen: user.created, user.updated, user.deleted
   ```

### Step 3: Payment Setup (Razorpay)

1. **Create Razorpay Account**
   ```bash
   # Visit https://razorpay.com
   # Complete KYC verification
   # Create test/live API keys
   # Note down: Key ID, Key Secret
   ```

2. **Create Subscription Plans**
   ```javascript
   // Use Razorpay Dashboard or API
   const plans = [
     {
       id: 'plan_free',
       period: 'monthly',
       interval: 1,
       amount: 0,
       currency: 'INR'
     },
     {
       id: 'plan_professional',
       period: 'monthly', 
       interval: 1,
       amount: 299900, // ₹2,999
       currency: 'INR'
     },
     {
       id: 'plan_enterprise',
       period: 'monthly',
       interval: 1, 
       amount: 999900, // ₹9,999
       currency: 'INR'
     }
   ];
   ```

### Step 4: Backend Deployment (Railway)

1. **Prepare Backend Code**
   ```bash
   # Create requirements.txt
   fastapi==0.104.1
   uvicorn==0.24.0
   sqlalchemy==2.0.23
   psycopg2-binary==2.9.9
   alembic==1.12.1
   python-multipart==0.0.6
   python-jose==3.3.0
   passlib==1.7.4
   razorpay==1.3.0
   supabase==2.0.2
   cloudinary==1.36.0
   redis==5.0.1
   celery==5.3.4
   ```

2. **Create Railway Configuration**
   ```toml
   # railway.toml
   [build]
   builder = "NIXPACKS"

   [deploy]
   startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT"
   restartPolicyType = "ON_FAILURE"
   restartPolicyMaxRetries = 10
   ```

3. **Environment Variables for Railway**
   ```env
   # Database
   DATABASE_URL=postgresql://postgres:[password]@[host]:[port]/[database]
   
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
   
   # Redis (for caching)
   REDIS_URL=redis://...
   
   # App Settings
   ENVIRONMENT=production
   SECRET_KEY=your-secret-key
   ALLOWED_ORIGINS=https://your-frontend.vercel.app
   ```

4. **Deploy to Railway**
   ```bash
   # Install Railway CLI
   npm install -g @railway/cli
   
   # Login and deploy
   railway login
   railway link
   railway up
   ```

### Step 5: Frontend Deployment (Vercel)

1. **Prepare Frontend Code**
   ```json
   {
     "name": "fertivision-frontend",
     "version": "1.0.0",
     "scripts": {
       "dev": "next dev",
       "build": "next build",
       "start": "next start"
     },
     "dependencies": {
       "next": "14.0.0",
       "react": "18.2.0",
       "@clerk/nextjs": "4.27.0",
       "razorpay": "2.9.2",
       "axios": "1.6.0",
       "tailwindcss": "3.3.0"
     }
   }
   ```

2. **Environment Variables for Vercel**
   ```env
   # Clerk
   NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
   CLERK_SECRET_KEY=sk_test_...
   
   # API
   NEXT_PUBLIC_API_URL=https://your-api.railway.app
   
   # Razorpay
   NEXT_PUBLIC_RAZORPAY_KEY_ID=rzp_test_...
   RAZORPAY_KEY_SECRET=...
   
   # App
   NEXT_PUBLIC_APP_URL=https://your-app.vercel.app
   ```

3. **Deploy to Vercel**
   ```bash
   # Install Vercel CLI
   npm install -g vercel
   
   # Deploy
   vercel --prod
   ```

### Step 6: File Storage Setup (Cloudinary)

1. **Configure Cloudinary**
   ```javascript
   // Backend configuration
   import { v2 as cloudinary } from 'cloudinary';
   
   cloudinary.config({
     cloud_name: process.env.CLOUDINARY_CLOUD_NAME,
     api_key: process.env.CLOUDINARY_API_KEY,
     api_secret: process.env.CLOUDINARY_API_SECRET
   });
   ```

2. **Upload Preset Configuration**
   ```javascript
   // In Cloudinary Dashboard:
   // 1. Create upload preset
   // 2. Set folder: "fertivision/analyses"
   // 3. Enable auto-optimization
   // 4. Set max file size: 10MB
   ```

---

## 🔍 **Testing Deployment**

### 1. **Health Checks**
```bash
# Backend health
curl https://your-api.railway.app/health

# Frontend
curl https://your-app.vercel.app/api/health
```

### 2. **Authentication Test**
```bash
# Test Clerk integration
curl -H "Authorization: Bearer [clerk-token]" \
     https://your-api.railway.app/api/user/profile
```

### 3. **Payment Test**
```bash
# Test Razorpay webhook
curl -X POST https://your-api.railway.app/webhooks/razorpay \
     -H "Content-Type: application/json" \
     -d '{"event": "subscription.charged"}'
```

---

## 📊 **Monitoring Setup**

### 1. **Application Monitoring**
- Railway: Built-in metrics
- Vercel: Analytics dashboard
- Supabase: Database monitoring

### 2. **Error Tracking**
```bash
# Add Sentry for error tracking
pip install sentry-sdk
npm install @sentry/nextjs
```

### 3. **Uptime Monitoring**
- UptimeRobot (free)
- Pingdom (free tier)

---

## 🚀 **Go Live Checklist**

- [ ] All services deployed and healthy
- [ ] Domain configured with SSL
- [ ] Authentication working
- [ ] Payment processing tested
- [ ] Database migrations completed
- [ ] Monitoring setup
- [ ] Error tracking configured
- [ ] Backup strategy implemented
- [ ] Documentation updated
- [ ] Team access configured

---

## 💰 **Cost Optimization**

### Free Tier Limits
- **Vercel**: 100GB bandwidth/month
- **Railway**: 500 hours/month free, then $5/month
- **Supabase**: 50,000 MAU, 500MB database
- **Clerk**: 10,000 MAU
- **Cloudinary**: 25 credits/month

### Scaling Costs
- **100 users**: ~$10-20/month
- **1,000 users**: ~$50-100/month
- **10,000 users**: ~$200-500/month

---

**🎉 Your FertiVision SaaS is now ready for production!**
