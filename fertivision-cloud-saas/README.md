# 🌐 FertiVision Cloud SaaS Edition

**AI-Enhanced Reproductive Medicine Analysis Platform - Cloud Production Version**

This is the **cloud-hosted SaaS version** of FertiVision, designed for:
- 🏥 **Multi-tenant clinic deployments**
- 💼 **Enterprise customers**
- 🚀 **Scalable production use**
- 💰 **Subscription-based business model**

---

## 🎯 **What's Included**

### 🌐 **Frontend (Next.js + Vercel)**
- Modern React-based UI with SSR
- Clerk authentication integration
- Subscription management dashboard
- Multi-tenant architecture

### 🔌 **Backend API (Railway/Render)**
- Scalable FastAPI server
- PostgreSQL database
- Redis caching
- Background job processing

### 💳 **Payment & Auth Integration**
- **Clerk**: User authentication and management
- **Razorpay**: Subscription billing and payments
- **Stripe**: Alternative payment processor
- **JWT**: Secure API authentication

---

## 🚀 **Recommended Free Cloud Stack**

### 🎯 **Best Free Deployment Options**

| Service | Purpose | Free Tier | Why Recommended |
|---------|---------|-----------|-----------------|
| **Vercel** | Frontend Hosting | Unlimited personal projects | ✅ Perfect for Next.js, global CDN |
| **Railway** | Backend API | $5/month (500 hours free) | ✅ Easy deployment, PostgreSQL included |
| **Supabase** | Database + Auth | 50,000 monthly active users | ✅ PostgreSQL + real-time features |
| **Clerk** | Authentication | 10,000 monthly active users | ✅ Complete auth solution |
| **Razorpay** | Payments | No monthly fees | ✅ Popular in India, low transaction fees |

### 🏆 **Alternative Stack (All Free)**

| Service | Purpose | Free Tier | Notes |
|---------|---------|-----------|-------|
| **Netlify** | Frontend | 100GB bandwidth | ✅ Great for static sites |
| **Render** | Backend | 750 hours/month | ✅ Free PostgreSQL included |
| **PlanetScale** | Database | 1 database, 1GB storage | ✅ Serverless MySQL |
| **Clerk** | Authentication | 10,000 MAU | ✅ Same as above |
| **Razorpay** | Payments | Transaction-based | ✅ Same as above |

---

## 🏗️ **Architecture Overview**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   Database      │
│   (Vercel)      │◄──►│   (Railway)     │◄──►│   (PostgreSQL)  │
│   Next.js       │    │   FastAPI       │    │   Supabase      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Auth          │    │   Payments      │    │   File Storage  │
│   (Clerk)       │    │   (Razorpay)    │    │   (Cloudinary)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

## 💰 **Subscription Plans**

### 🆓 **Free Tier**
- 10 analyses per month
- Basic support
- Standard processing time
- Community access

### 💼 **Professional - ₹2,999/month**
- 500 analyses per month
- Priority support
- Faster processing
- API access
- Custom integrations

### 🏥 **Enterprise - ₹9,999/month**
- Unlimited analyses
- 24/7 support
- Dedicated infrastructure
- White-label options
- Custom AI models

### 🏢 **Custom Enterprise**
- Volume pricing
- On-premise deployment
- Custom features
- SLA guarantees
- Dedicated account manager

---

## 🔧 **Deployment Guide**

### 1. **Frontend Deployment (Vercel)**

```bash
# Clone repository
git clone https://github.com/your-username/fertivision-cloud-saas.git
cd fertivision-cloud-saas/frontend

# Install dependencies
npm install

# Configure environment variables
cp .env.example .env.local
# Edit .env.local with your keys

# Deploy to Vercel
npx vercel --prod
```

**Environment Variables:**
```env
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
CLERK_SECRET_KEY=sk_test_...
NEXT_PUBLIC_API_URL=https://your-api.railway.app
NEXT_PUBLIC_RAZORPAY_KEY_ID=rzp_test_...
```

### 2. **Backend Deployment (Railway)**

```bash
# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your configuration

# Deploy to Railway
railway login
railway link
railway up
```

**Environment Variables:**
```env
DATABASE_URL=postgresql://...
CLERK_SECRET_KEY=sk_test_...
RAZORPAY_KEY_ID=rzp_test_...
RAZORPAY_KEY_SECRET=...
REDIS_URL=redis://...
```

### 3. **Database Setup (Supabase)**

```sql
-- Create tables
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    clerk_user_id VARCHAR UNIQUE NOT NULL,
    email VARCHAR NOT NULL,
    subscription_plan VARCHAR DEFAULT 'free',
    analyses_used INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE analyses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    analysis_type VARCHAR NOT NULL,
    image_url VARCHAR,
    results JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    razorpay_subscription_id VARCHAR,
    plan_id VARCHAR,
    status VARCHAR,
    current_period_start TIMESTAMP,
    current_period_end TIMESTAMP
);
```

---

## 🔐 **Authentication Flow (Clerk)**

### Frontend Integration
```javascript
import { ClerkProvider, SignIn, SignUp, UserButton } from '@clerk/nextjs'

export default function App({ Component, pageProps }) {
  return (
    <ClerkProvider>
      <Component {...pageProps} />
    </ClerkProvider>
  )
}

// Protected route
import { withClerkMiddleware, requireAuth } from '@clerk/nextjs/api'

export default requireAuth((req, res) => {
  // Protected API route
  res.json({ message: 'Hello authenticated user!' })
})
```

### Backend Verification
```python
from clerk_backend_api import Clerk

clerk = Clerk(bearer_auth="sk_test_...")

def verify_user(token: str):
    try:
        session = clerk.sessions.verify_session(token)
        return session.user_id
    except Exception:
        raise HTTPException(401, "Invalid token")
```

---

## 💳 **Payment Integration (Razorpay)**

### Subscription Creation
```javascript
import Razorpay from 'razorpay'

const razorpay = new Razorpay({
  key_id: process.env.RAZORPAY_KEY_ID,
  key_secret: process.env.RAZORPAY_KEY_SECRET
})

// Create subscription
const subscription = await razorpay.subscriptions.create({
  plan_id: 'plan_professional',
  customer_notify: 1,
  total_count: 12, // 12 months
  notes: {
    user_id: user.id
  }
})
```

### Payment Verification
```python
import razorpay
from razorpay.errors import SignatureVerificationError

client = razorpay.Client(auth=(key_id, key_secret))

def verify_payment(payload, signature):
    try:
        client.utility.verify_webhook_signature(
            payload, signature, webhook_secret
        )
        return True
    except SignatureVerificationError:
        return False
```

---

## 📊 **Monitoring & Analytics**

### Performance Monitoring
- **Vercel Analytics**: Frontend performance
- **Railway Metrics**: Backend monitoring
- **Supabase Dashboard**: Database metrics
- **Clerk Dashboard**: User analytics

### Business Metrics
- Monthly Recurring Revenue (MRR)
- Customer Acquisition Cost (CAC)
- Churn rate
- Usage analytics per plan

---

## 🚀 **Scaling Strategy**

### Phase 1: MVP (0-100 users)
- Free tier deployment
- Basic features
- Manual support

### Phase 2: Growth (100-1000 users)
- Paid plans activation
- Automated billing
- Enhanced features

### Phase 3: Scale (1000+ users)
- Enterprise features
- Custom deployments
- Advanced analytics

---

## 🔗 **Related Projects**

- **Local Development Version**: [fertivision-local-dev](https://github.com/your-username/fertivision-local-dev)
- **Documentation**: [fertivision-docs](https://github.com/your-username/fertivision-docs)
- **Mobile App**: [fertivision-mobile](https://github.com/your-username/fertivision-mobile)

---

## 📞 **Support & Sales**

- **Demo**: [demo.fertivision.com](https://demo.fertivision.com)
- **Sales**: sales@greybrain.ai
- **Support**: support@greybrain.ai
- **Documentation**: [docs.fertivision.com](https://docs.fertivision.com)

---

**© 2025 FertiVision powered by AI | Made by greybrain.ai**

*Advancing reproductive medicine through artificial intelligence*
