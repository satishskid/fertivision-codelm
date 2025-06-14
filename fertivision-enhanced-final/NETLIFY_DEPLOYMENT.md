# 🚀 FertiVision Netlify Deployment Guide

This guide provides step-by-step instructions for deploying FertiVision to Netlify as a production-ready static web application.

## 📋 Prerequisites

- Git repository with FertiVision code
- Netlify account (free tier available)
- API keys for AI services (optional, demo mode works without keys)

## 🌐 Quick Deployment

### Option 1: Deploy from Git Repository

1. **Connect Repository to Netlify**
   ```bash
   # Ensure you're on the netlify-deployment branch
   git checkout netlify-deployment
   git push origin netlify-deployment
   ```

2. **Netlify Dashboard Setup**
   - Go to [netlify.com](https://netlify.com) and sign in
   - Click "New site from Git"
   - Choose your Git provider (GitHub, GitLab, Bitbucket)
   - Select the `fertivision-codelm` repository
   - Choose the `netlify-deployment` branch

3. **Build Settings**
   ```
   Branch to deploy: netlify-deployment
   Build command: (leave empty - static site)
   Publish directory: .
   ```

4. **Deploy**
   - Click "Deploy site"
   - Your site will be available at a random Netlify URL
   - You can customize the domain later

### Option 2: Manual Deploy

1. **Prepare Files**
   ```bash
   # Create a deployment package
   zip -r fertivision-netlify.zip . -x "*.git*" "node_modules/*" "*.md" "api_server.py" "*.db"
   ```

2. **Manual Upload**
   - Go to Netlify dashboard
   - Drag and drop the zip file to the deploy area
   - Site will be deployed automatically

## ⚙️ Environment Configuration

### Required Environment Variables

Set these in Netlify Dashboard → Site Settings → Environment Variables:

```bash
# API Configuration (Optional - Demo mode works without these)
VITE_API_PROVIDER=demo
VITE_GROQ_API_KEY=your_groq_api_key_here
VITE_OPENROUTER_API_KEY=your_openrouter_api_key_here

# Application Settings
NODE_ENV=production
VITE_APP_VERSION=1.0.0
```

### Getting API Keys

#### Groq (Free & Fast)
1. Visit [console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Generate an API key
4. Add to Netlify: `VITE_GROQ_API_KEY=gsk_...`

#### OpenRouter (Multiple Models)
1. Visit [openrouter.ai](https://openrouter.ai)
2. Create an account
3. Generate an API key
4. Add to Netlify: `VITE_OPENROUTER_API_KEY=sk-or-...`

## 🔧 Advanced Configuration

### Custom Domain Setup

1. **Add Custom Domain**
   - Go to Site Settings → Domain management
   - Click "Add custom domain"
   - Enter your domain (e.g., `fertivision.yourdomain.com`)

2. **DNS Configuration**
   ```
   Type: CNAME
   Name: fertivision
   Value: your-site-name.netlify.app
   ```

3. **SSL Certificate**
   - Netlify automatically provides free SSL certificates
   - Certificate will be provisioned within minutes

### Performance Optimization

The `netlify.toml` file includes optimizations:

```toml
# Caching for static assets
[[headers]]
  for = "/static/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

# Security headers
[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-XSS-Protection = "1; mode=block"
```

### Build Hooks (Optional)

Set up automatic deployments:

1. **Webhook URL**
   - Go to Site Settings → Build & deploy → Build hooks
   - Create a new build hook
   - Use the webhook URL in your CI/CD pipeline

2. **GitHub Actions Example**
   ```yaml
   name: Deploy to Netlify
   on:
     push:
       branches: [netlify-deployment]
   jobs:
     deploy:
       runs-on: ubuntu-latest
       steps:
         - name: Trigger Netlify Deploy
           run: curl -X POST -d {} ${{ secrets.NETLIFY_BUILD_HOOK }}
   ```

## 🔒 Security Configuration

### Content Security Policy

The application includes a strict CSP in `netlify.toml`:

```toml
Content-Security-Policy = """
  default-src 'self';
  script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com;
  connect-src 'self' https://api.groq.com https://openrouter.ai;
"""
```

### API Key Security

- ✅ API keys are stored as environment variables
- ✅ Keys are not exposed in client-side code
- ✅ Keys are loaded at build time and injected securely
- ✅ Demo mode works without any API keys

## 📊 Monitoring and Analytics

### Netlify Analytics

Enable built-in analytics:
1. Go to Site Settings → Analytics
2. Enable Netlify Analytics (paid feature)
3. View traffic, performance, and user data

### Error Monitoring

The application includes error logging:
- Errors are logged to browser console
- Error details stored in localStorage
- Can be integrated with external services (Sentry, LogRocket)

## 🧪 Testing Deployment

### Pre-deployment Checklist

- [ ] All JavaScript modules load correctly
- [ ] API configuration works in demo mode
- [ ] Image upload and analysis functions work
- [ ] Settings modal opens and saves preferences
- [ ] All tabs navigate correctly
- [ ] Responsive design works on mobile
- [ ] Demo analyses run successfully

### Testing Commands

```bash
# Test locally before deployment
python -m http.server 8000
# Open http://localhost:8000

# Test with different API providers
# Set VITE_API_PROVIDER=demo in browser console
# Test image upload and analysis
```

## 🚨 Troubleshooting

### Common Issues

1. **Blank Page After Deployment**
   ```bash
   # Check browser console for JavaScript errors
   # Verify all file paths are correct (case-sensitive)
   # Check netlify.toml redirects configuration
   ```

2. **API Calls Failing**
   ```bash
   # Verify environment variables are set correctly
   # Check CORS settings for external APIs
   # Test with demo mode first
   ```

3. **Images Not Loading**
   ```bash
   # Check file paths in HTML
   # Verify static assets are in correct directories
   # Check browser network tab for 404 errors
   ```

### Debug Mode

Enable debug logging:
```javascript
// In browser console
localStorage.setItem('fertivision-debug', 'true');
location.reload();
```

## 📈 Performance Optimization

### Lighthouse Scores

Target scores for production:
- Performance: >90
- Accessibility: >95
- Best Practices: >90
- SEO: >85

### Optimization Techniques

1. **Image Optimization**
   - Use WebP format when possible
   - Implement lazy loading
   - Compress images before upload

2. **Code Splitting**
   - Load modules on demand
   - Use dynamic imports for large features

3. **Caching Strategy**
   - Static assets cached for 1 year
   - HTML cached for 1 hour
   - API responses cached appropriately

## 🔄 Continuous Deployment

### Automatic Deployments

1. **Branch Protection**
   ```bash
   # Only deploy from netlify-deployment branch
   git checkout netlify-deployment
   git merge main
   git push origin netlify-deployment
   ```

2. **Deploy Previews**
   - Netlify automatically creates deploy previews for pull requests
   - Test changes before merging to main branch

3. **Rollback Strategy**
   - Netlify keeps deployment history
   - One-click rollback to previous versions
   - Atomic deployments ensure no downtime

## 📞 Support and Maintenance

### Monitoring

- Set up Netlify notifications for failed deployments
- Monitor site performance with Netlify Analytics
- Set up uptime monitoring (UptimeRobot, Pingdom)

### Updates

```bash
# Regular update process
git checkout main
# Make changes
git commit -m "Update: description"
git checkout netlify-deployment
git merge main
git push origin netlify-deployment
```

### Backup

- Git repository serves as primary backup
- Netlify keeps deployment snapshots
- Export environment variables regularly

## 🎯 Production Checklist

Before going live:

- [ ] Custom domain configured with SSL
- [ ] Environment variables set correctly
- [ ] API keys tested and working
- [ ] All features tested in production environment
- [ ] Performance optimized (Lighthouse scores >90)
- [ ] Security headers configured
- [ ] Error monitoring set up
- [ ] Analytics configured
- [ ] Backup strategy in place
- [ ] Documentation updated
- [ ] Team access configured

## 📚 Additional Resources

- [Netlify Documentation](https://docs.netlify.com/)
- [Groq API Documentation](https://console.groq.com/docs)
- [OpenRouter API Documentation](https://openrouter.ai/docs)
- [FertiVision GitHub Repository](https://github.com/satishskid/fertivision-codelm)

---

**🎉 Congratulations!** Your FertiVision application is now deployed and ready for production use.

For support, contact: support@greybrain.ai
