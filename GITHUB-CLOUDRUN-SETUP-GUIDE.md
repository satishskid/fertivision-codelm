# 🔗 FertiVision GitHub + Cloud Build Setup Guide

## 📋 **Current Status**
✅ Google Cloud Console opened  
✅ Deployment files verified (`cloudbuild.yaml`, GitHub Actions)  
✅ Repository structure validated  

---

## 🚀 **Complete Setup Process**

### **Phase 1: Google Cloud Setup** (5 minutes)

#### **1.1 Create/Select Project**
- In the open Google Cloud Console, create or select project
- **Recommended name:** `fertivision-production`
- **Note your PROJECT_ID** (usually similar to project name)

#### **1.2 Enable APIs**
Navigate to **APIs & Services > Library** and enable:

1. **Cloud Run API**
   - Direct link: `https://console.cloud.google.com/apis/library/run.googleapis.com`
   - Click "Enable"

2. **Cloud Build API** 
   - Direct link: `https://console.cloud.google.com/apis/library/cloudbuild.googleapis.com`
   - Click "Enable"

3. **Container Registry API**
   - Direct link: `https://console.cloud.google.com/apis/library/containerregistry.googleapis.com`
   - Click "Enable"

---

### **Phase 2: Cloud Build Integration** (5 minutes)

#### **2.1 Connect GitHub Repository**
1. Go to **Cloud Build > Triggers** in Google Cloud Console
2. Click **"Connect Repository"**
3. Select **GitHub** and authorize Google Cloud access
4. Choose repository: **`satishskid/fertivision-codelm`**
5. Select branch: **`stable-deployment`** (or `main` if preferred)

#### **2.2 Create Build Trigger**
1. Click **"Create Trigger"**
2. **Name:** `fertivision-deploy`
3. **Event:** Push to branch
4. **Branch:** `stable-deployment` (or your chosen branch)
5. **Configuration:** Cloud Build configuration file (cloudbuild.yaml)
6. **Location:** `/cloudbuild.yaml` (already exists in repo!)
7. Click **"Create"**

---

### **Phase 3: GitHub Actions Setup** (Alternative/Backup)

#### **3.1 Add GitHub Secrets**
Go to your GitHub repository settings:
1. Navigate to **Settings > Secrets and variables > Actions**
2. Click **"New repository secret"**
3. Add these secrets:

**Secret 1:**
- **Name:** `GCP_PROJECT_ID`
- **Value:** Your Google Cloud Project ID

**Secret 2:**
- **Name:** `GCP_SA_KEY`
- **Value:** Service Account JSON key (see instructions below)

#### **3.2 Create Service Account (for GitHub Actions)**
In Google Cloud Console:
1. Go to **IAM & Admin > Service Accounts**
2. Click **"Create Service Account"**
3. **Name:** `fertivision-deployer`
4. **Role:** Cloud Run Admin, Cloud Build Editor, Storage Admin
5. Create key (JSON format)
6. Copy the JSON content to `GCP_SA_KEY` secret

---

### **Phase 4: First Deployment** (2 minutes)

#### **4.1 Trigger First Build**
**Method A: Via Cloud Build**
- Push any small change to `stable-deployment` branch
- Monitor progress in Cloud Build console

**Method B: Via GitHub Actions**
- Push to `stable-deployment` branch
- Monitor in GitHub Actions tab

#### **4.2 Verify Deployment**
1. Check Cloud Build/GitHub Actions logs
2. Visit Cloud Run console to see service
3. Test the deployed URL

---

## 🎯 **Configuration Files Ready**

### **✅ cloudbuild.yaml**
- Automated build and deployment
- Configured for `us-central1` region
- 512Mi memory, 1 CPU
- Health checks included

### **✅ GitHub Actions Workflow**
- Triggered on push to `stable-deployment`
- Manual dispatch available
- Comprehensive deployment steps

### **✅ Docker Configuration**
- Production-optimized Dockerfile
- Dynamic port binding (PORT environment variable)
- Health check endpoints

---

## 🔍 **Monitoring & Debugging**

### **Build Logs**
- **Cloud Build:** Console > Cloud Build > History
- **GitHub Actions:** Repository > Actions tab

### **Application Logs** 
- **Cloud Run:** Console > Cloud Run > fertivision > Logs
- **Real-time:** `gcloud logging tail "resource.type=cloud_run_revision"`

### **Service Management**
- **Scale:** Cloud Run console > fertivision > Edit & Deploy
- **Traffic:** Manage traffic splitting between revisions
- **Environment:** Update environment variables

---

## 🚀 **Deployment Flow**

```
Code Change → Git Push → Cloud Build/GitHub Actions → Container Build → Cloud Run Deploy → Live Application
```

**Automatic deployments on every push to `stable-deployment` branch!**

---

## 📞 **Next Steps**

1. **Complete Google Cloud setup** (APIs and Project)
2. **Connect GitHub repository** to Cloud Build
3. **Create build trigger** 
4. **Push a test change** to trigger first deployment
5. **Monitor deployment** in Cloud Build console
6. **Test deployed application** at provided URL

**Total setup time: ~15 minutes**  
**Future deployments: Automatic on git push!**

---

## 💡 **Pro Tips**

- Use `stable-deployment` branch for production
- Monitor Cloud Build quota (free tier: 120 minutes/day)
- Set up branch protection rules in GitHub
- Configure notification webhooks for deployment status
- Use Cloud Run revisions for blue-green deployments

**Ready to proceed with setup!** 🚀
