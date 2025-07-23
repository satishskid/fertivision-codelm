# FertiVision Business Website

Professional business website for FertiVision - Deep Vision AI for IVF Laboratory Research & Clinical Analysis.

## 🔬 Clinical Research Focus

The business website emphasizes FertiVision as an advanced computer vision research platform for reproductive medicine, highlighting:

- **WHO 2021 Standards**: Complete morphological parameter analysis per WHO 2021 guidelines
- **Gardner Criteria**: Automated embryo classification using Gardner morphological criteria  
- **Multi-Sample Analysis**: Sperm, oocyte, embryo, and follicle assessment capabilities
- **Deep Learning Research**: Custom CNN models trained on reproductive cell imagery
- **Clinical Grade Validation**: Comprehensive validation studies and performance metrics

## 📋 Website Structure

### Main Website (`index.html`)
- Professional business presentation for clinic directors and executives
- Complete documentation suite with working GitHub Pages links
- System capabilities and performance metrics
- Research platform access and quick navigation

### Clinical Research Site (`clinical-research.html`)  
- **NEW**: Specialized clinical research-focused website
- Emphasis on morphological research capabilities
- Detailed research documentation and validation studies
- Technical implementation guides for research teams
- Laboratory integration protocols

## 🔗 Fixed Documentation Links

All documentation links now properly point to GitHub Pages:

- **Clinical Manual**: https://satishskid.github.io/fertivision-codelm/FERTIVISION_COMPLETE_USER_MANUAL
- **Technical Guide**: https://satishskid.github.io/fertivision-codelm/DEVELOPER_MANUAL_COMPLETE
- **API Documentation**: https://satishskid.github.io/fertivision-codelm/API_DOCUMENTATION_COMPLETE
- **Lab Integration**: https://satishskid.github.io/fertivision-codelm/CLINIC_INTEGRATION_GUIDE
- **Validation Studies**: https://satishskid.github.io/fertivision-codelm/ENDPOINT_TESTING_COMPLETE

## 🚀 Deployment Instructions

### Local Development
```bash
# Navigate to business website folder
cd /Users/spr/fertivisiion\ codelm/business-website/

# Start local web server (Python 3)
python3 -m http.server 8080

# Or using Node.js
npx http-server -p 8080

# Access websites:
# Main: http://localhost:8080/
# Clinical Research: http://localhost:8080/clinical-research.html
```

### Production Deployment Options

1. **Netlify** (Recommended for business sites)
```bash
# Deploy directly from GitHub
# Connect repository: satishskid/fertivision-codelm
# Build directory: business-website/
# Domain: fertivision.netlify.app
```

2. **Vercel**
```bash
vercel --cwd business-website/
```

3. **GitHub Pages** (Static hosting)
```bash
# Copy files to docs/ folder for GitHub Pages
cp -r business-website/* docs/
git add docs/
git commit -m "Deploy business website"
git push
```

## 🎨 Design Features

### Research-Focused Design
- **Clinical gradient themes** emphasizing medical research
- **Performance metrics** showcasing research capabilities  
- **WHO 2021 & Gardner criteria** prominent branding
- **Computer vision research** positioning

### Professional Elements
- Medical-grade color schemes and typography
- Interactive cards with hover animations
- Responsive design for all devices
- Professional loading animations
- Smooth scrolling navigation

### Research Platform Integration
- Direct links to live research platform
- GitHub repository integration
- Complete documentation access
- API reference integration

## 📊 Key Features Highlighted

### Clinical Research Capabilities
- **Sperm Morphological Analysis**: WHO 2021 compliant with 15+ parameters
- **Oocyte Maturation Assessment**: ESHRE guidelines-based classification
- **Embryo Development Grading**: Gardner criteria implementation
- **Follicular Assessment**: Automated AFC counting and PCOS detection
- **Deep Learning Models**: Custom CNNs for reproductive cell imagery
- **Statistical Analysis**: Research-grade data analysis tools

### Performance Metrics
- **Analysis Time**: < 8 seconds real-time processing
- **Accuracy Rates**: 95% sperm, 92% oocyte, 89% embryo, 87% follicle
- **WHO Parameters**: 15+ morphological metrics
- **Validation Studies**: Comprehensive clinical validation
- **Research Documentation**: 200+ pages of methodology

## 🔧 Technical Stack

- **Frontend**: Vanilla HTML5, CSS3, JavaScript
- **Styling**: Custom CSS with medical-grade design system
- **Icons**: Font Awesome 6.4.0 for medical/research icons
- **Typography**: Inter font family for professional appearance
- **Animations**: CSS animations and JavaScript intersection observers
- **Responsive**: Mobile-first responsive design

## 📝 Content Strategy

### Target Audiences
1. **Clinical Researchers**: Morphological analysis capabilities
2. **Laboratory Directors**: Integration and validation studies  
3. **Embryologists**: WHO 2021 and Gardner criteria features
4. **IT/Technical Teams**: API documentation and implementation
5. **Executive Leadership**: Business benefits and ROI

### Content Positioning
- **Research-First**: Emphasizes scientific research capabilities
- **Clinical Grade**: Highlights validation and accuracy
- **Standards Compliant**: WHO 2021, Gardner, ESHRE compliance
- **Evidence-Based**: Performance metrics and validation studies

## 🌐 Live URLs

- **Research Platform**: https://fertivision-ai-514605543640.us-central1.run.app
- **Documentation**: https://satishskid.github.io/fertivision-codelm/
- **GitHub Repository**: https://github.com/satishskid/fertivision-codelm
- **Business Website**: http://localhost:8080 (local development)

---

**Made by greybrain.ai** | Advancing reproductive medicine through computer vision research
