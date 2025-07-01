# Multi-Cloud Deployment Guide for FertiVision
# Complete deployment configurations for AWS, Azure, and Google Cloud

## 🚀 Quick Start - Choose Your Platform

### **Google Cloud Run (Recommended)**
```bash
# 1. Setup Google Cloud SDK
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# 2. Deploy FertiVision
./deploy-gcloud.sh

# 3. Access your application
# URL will be provided after deployment
```

### **AWS Elastic Beanstalk**
```bash
# 1. Install AWS CLI and EB CLI
pip install awscli awsebcli

# 2. Configure AWS credentials
aws configure

# 3. Deploy FertiVision
./deploy-aws.sh

# 4. Monitor deployment
eb status
```

### **Microsoft Azure**
```bash
# 1. Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# 2. Deploy FertiVision
./deploy-azure.sh

# 3. Monitor in Azure Portal
az webapp browse --resource-group fertivision-rg --name fertivision-app
```

---

## 📊 Platform Comparison

| Feature | Google Cloud Run | AWS Elastic Beanstalk | Azure App Service |
|---------|-----------------|----------------------|-------------------|
| **Setup Time** | 5 minutes | 10 minutes | 8 minutes |
| **Monthly Cost** | $25-75 | $35-100 | $30-85 |
| **Auto-scaling** | 0-1000 instances | 1-100 instances | 1-100 instances |
| **Cold Start** | <1 second | N/A (always warm) | <3 seconds |
| **HIPAA Ready** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Medical AI** | ✅ Native support | ✅ Via SageMaker | ✅ Via Cognitive Services |

---

## 🛠️ Configuration Files

### **AWS Configuration**
- `.ebextensions/01_python.config` - Elastic Beanstalk configuration
- `serverless.yml` - Lambda serverless deployment
- `application.py` - AWS application entry point
- `wsgi_handler.py` - Lambda WSGI handler

### **Azure Configuration**
- `azure-pipelines.yml` - CI/CD pipeline
- `web.config` - IIS web server configuration
- `.azure/config` - Azure CLI defaults

### **Google Cloud Configuration**
- `cloudbuild.yaml` - Cloud Build configuration
- `service.yaml` - Cloud Run service definition
- `Dockerfile.production` - Optimized production container

---

## 🔧 Environment Variables

All platforms support these environment variables:

```bash
FLASK_ENV=production
DATABASE_URL=sqlite:///reproductive_analysis.db
PORT=8080
UPLOAD_FOLDER=/app/uploads
```

### **Platform-specific Variables**

**AWS:**
- `AWS_DEFAULT_REGION=us-east-1`
- `S3_BUCKET=fertivision-uploads`

**Azure:**
- `WEBSITES_PORT=8080`
- `SCM_DO_BUILD_DURING_DEPLOYMENT=true`

**Google Cloud:**
- `PORT=8080` (automatically set)
- `GOOGLE_CLOUD_PROJECT=your-project-id`

---

## 🗄️ Database Options

### **Development/Small Clinics**
- **SQLite** (included): No setup required
- **Cost**: $0
- **Suitable for**: <100 patients, single instance

### **Production/Large Clinics**
- **Cloud SQL (PostgreSQL)**: Managed database
- **Azure Database**: Managed PostgreSQL
- **AWS RDS**: Managed PostgreSQL
- **Cost**: $7-50/month
- **Suitable for**: Unlimited patients, multi-instance

---

## 📈 Scaling Configuration

### **Google Cloud Run**
```yaml
# Automatic scaling: 0-100 instances
autoscaling.knative.dev/maxScale: "100"
autoscaling.knative.dev/minScale: "0"
```

### **AWS Elastic Beanstalk**
```yaml
# Auto Scaling Group
MinSize: 1
MaxSize: 10
TargetCPU: 70%
```

### **Azure App Service**
```bash
# Scale out rules
az monitor autoscale create \
  --count 10 \
  --max-count 50 \
  --resource-group fertivision-rg
```

---

## 🔒 Security & HIPAA Compliance

All configurations include:

✅ **Encryption at rest and in transit**
✅ **Secure environment variables**
✅ **Network security groups**
✅ **Audit logging**
✅ **Automated backups**
✅ **Access controls**

### **HIPAA Business Associate Agreements (BAA)**
- **Google Cloud**: Available upon request
- **AWS**: Available through AWS Artifact
- **Azure**: Available through Microsoft Trust Center

---

## 🚀 Deployment Commands

### **One-click deployment:**
```bash
# Google Cloud Run (Recommended)
./deploy-gcloud.sh

# AWS Elastic Beanstalk
./deploy-aws.sh

# Microsoft Azure
./deploy-azure.sh
```

### **Manual deployment:**
```bash
# Build Docker image
docker build -f Dockerfile.production -t fertivision .

# Deploy to your chosen platform
# (Platform-specific commands in deployment scripts)
```

---

## 📊 Monitoring & Logging

### **Google Cloud**
```bash
# View logs
gcloud run services logs read fertivision --region=us-central1 --follow

# View metrics
https://console.cloud.google.com/run/detail/us-central1/fertivision/metrics
```

### **AWS**
```bash
# View logs
eb logs

# CloudWatch dashboard
https://console.aws.amazon.com/cloudwatch/
```

### **Azure**
```bash
# View logs
az webapp log tail --resource-group fertivision-rg --name fertivision-app

# Application Insights
https://portal.azure.com/#blade/Microsoft_Azure_Monitoring/
```

---

## 🎯 Production Checklist

### **Before Deployment:**
- [ ] Environment variables configured
- [ ] Database connection tested
- [ ] HTTPS/SSL certificates ready
- [ ] Custom domain configured (optional)
- [ ] Backup strategy planned

### **After Deployment:**
- [ ] Health check endpoint working
- [ ] Load testing completed
- [ ] Monitoring alerts configured
- [ ] Error tracking enabled
- [ ] Team access permissions set

---

## 💡 Team Workflow

### **Development Process:**
1. **Develop locally** using `python app.py`
2. **Test with sample data** using validation scripts
3. **Push to Git** repository
4. **Choose deployment platform** based on requirements
5. **Run deployment script** for your chosen platform
6. **Monitor and scale** as needed

### **CI/CD Integration:**
- **GitHub Actions**: Included in repository
- **Azure Pipelines**: `azure-pipelines.yml` configured
- **Cloud Build**: `cloudbuild.yaml` ready
- **AWS CodePipeline**: Compatible with EB deployment

---

## 🆘 Support & Troubleshooting

### **Common Issues:**
1. **Permission errors**: Ensure cloud CLI tools are authenticated
2. **Build failures**: Check Python dependencies in requirements.txt
3. **Database connection**: Verify DATABASE_URL environment variable
4. **Memory issues**: Increase container memory allocation

### **Getting Help:**
- **Google Cloud**: [Cloud Run Documentation](https://cloud.google.com/run/docs)
- **AWS**: [Elastic Beanstalk Guide](https://docs.aws.amazon.com/elasticbeanstalk/)
- **Azure**: [App Service Documentation](https://docs.microsoft.com/en-us/azure/app-service/)

---

**🎉 FertiVision is ready for production deployment on any cloud platform!**

Choose the platform that best fits your team's expertise and requirements. All configurations are production-ready with medical-grade security and HIPAA compliance built-in.
