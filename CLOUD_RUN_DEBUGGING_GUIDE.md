# 🔍 Google Cloud Run Debugging Guide for FertiVision

## 🚀 **Quick Deployment**
```bash
./deploy-free-cloudrun.sh
```

## 🔧 **Post-Deployment Debugging Methods**

### 1. **📊 Real-Time Log Monitoring**
```bash
# Stream live logs
gcloud logging tail "resource.type=cloud_run_revision AND resource.labels.service_name=fertivision"

# View recent logs (last 50 entries)
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=fertivision" --limit=50 --format="table(timestamp,textPayload)"

# Filter error logs only
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=fertivision AND severity>=ERROR" --limit=20
```

### 2. **🌐 Web-Based Debugging (Google Cloud Console)**
```
1. Go to: https://console.cloud.google.com/run
2. Click on "fertivision" service
3. Navigate to "LOGS" tab for real-time monitoring
4. Use "METRICS" tab for performance insights
5. Check "REVISIONS" for deployment history
```

### 3. **🏥 Health Check Debugging**
```bash
# Test your deployed app
curl [YOUR_CLOUD_RUN_URL]/health

# Expected response:
{
  "status": "healthy",
  "service": "FertiVision",
  "timestamp": "2025-07-05T10:30:45.123456"
}
```

### 4. **📈 Performance Monitoring**
```bash
# Service information and status
gcloud run services describe fertivision --region=us-central1

# Current traffic allocation
gcloud run services describe fertivision --region=us-central1 --format="value(status.traffic)"

# List all revisions
gcloud run revisions list --service=fertivision --region=us-central1
```

### 5. **🐛 Application-Level Debugging**

#### A. **Enable Debug Logs in Flask App**
Add to your `app.py`:
```python
import logging
import sys

# Configure logging for Cloud Run
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

# Add debug prints that will show in logs
@app.before_request
def log_request_info():
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())
```

#### B. **Test Specific Endpoints**
```bash
# Test document upload
curl -X POST [YOUR_URL]/upload_document \
  -F "document=@test_document.pdf" \
  -H "Content-Type: multipart/form-data"

# Test image analysis
curl -X POST [YOUR_URL]/analyze_image \
  -F "image=@test_image.jpg" \
  -H "Content-Type: multipart/form-data"
```

### 6. **🔄 Quick Redeploy for Fixes**
```bash
# After making code changes locally
gcloud run deploy fertivision --source . --region=us-central1

# Deploy specific revision (rollback)
gcloud run services update-traffic fertivision --to-revisions=REVISION_NAME=100 --region=us-central1
```

### 7. **📱 Environment Variables Debugging**
```bash
# Check current environment variables
gcloud run services describe fertivision --region=us-central1 --format="value(spec.template.spec.template.spec.containers[0].env[].name,spec.template.spec.template.spec.containers[0].env[].value)"

# Update environment variables
gcloud run services update fertivision \
  --set-env-vars "DEBUG_MODE=true,LOG_LEVEL=DEBUG" \
  --region=us-central1
```

### 8. **🚨 Common Issues & Solutions**

#### **Issue: Cold Start Timeouts**
```bash
# Increase memory allocation
gcloud run services update fertivision --memory=1Gi --region=us-central1
```

#### **Issue: Request Timeouts**
```bash
# Increase timeout
gcloud run services update fertivision --timeout=300 --region=us-central1
```

#### **Issue: File Upload Errors**
```bash
# Check container size limits
gcloud run services update fertivision --memory=2Gi --region=us-central1

# Enable request size limits
gcloud run services update fertivision --set-env-vars "MAX_CONTENT_LENGTH=16777216" --region=us-central1
```

### 9. **📊 Advanced Monitoring Setup**
```bash
# Enable Cloud Monitoring (free tier)
gcloud services enable monitoring.googleapis.com

# Create uptime check
gcloud alpha monitoring uptime create-http-uptime-check \
  --hostname=[YOUR_DOMAIN] \
  --path=/health \
  --display-name="FertiVision Health Check"
```

### 10. **🔍 Local Testing Before Deployment**
```bash
# Test with production settings locally
export FLASK_ENV=production
export DEBUG_MODE=true
python app.py

# Build and test Docker container locally
docker build -t fertivision-test .
docker run -p 8080:8080 fertivision-test
```

## 🎯 **Debugging Workflow**

1. **Deploy**: `./deploy-free-cloudrun.sh`
2. **Test**: Visit the provided URL
3. **Monitor**: `gcloud logging tail` for real-time logs
4. **Debug**: Check logs for errors
5. **Fix**: Update code locally
6. **Redeploy**: `gcloud run deploy fertivision --source .`
7. **Verify**: Test again

## 📞 **Emergency Commands**
```bash
# Quick status check
gcloud run services list --filter="fertivision"

# Force new deployment
gcloud run deploy fertivision --source . --region=us-central1 --no-traffic

# Rollback to previous version
gcloud run services update-traffic fertivision --to-latest=false --region=us-central1
```

## 💡 **Pro Tips**
- Always test `/health` endpoint first
- Monitor logs during high traffic
- Use Cloud Console for visual debugging
- Set up alerts for error rates
- Keep deployment logs for troubleshooting

---
**Happy Debugging! 🎉**
