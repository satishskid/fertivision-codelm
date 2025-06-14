# 🔬 FertiVision Local Development Edition

**AI-Enhanced Reproductive Medicine Analysis Platform - Local Development Version**

This is the **local development and testing version** of FertiVision, designed for:
- 🏥 **Local clinic deployments**
- 🧪 **Research and development**
- 📚 **Educational purposes**
- 🔧 **Custom integrations**

---

## 🎯 **What's Included**

### 🌐 **Frontend Web Application**
- Complete UI for manual image analysis
- 5 analysis types: Sperm, Oocyte, Embryo, Follicle, Hysteroscopy
- Settings, training modules, and datasets
- Responsive design for desktop and mobile

### 🔌 **EMR API Server**
- RESTful API for EMR integration
- Python SDK for easy integration
- Secure authentication with API keys
- Batch processing capabilities

### 📊 **Analysis Capabilities**
- **Sperm Analysis**: WHO 2021 compliant semen analysis
- **Oocyte Assessment**: ESHRE guidelines-based maturity evaluation
- **Embryo Grading**: Gardner grading system for Day 3-6 embryos
- **Follicle Counting**: AFC and ovarian reserve assessment
- **Hysteroscopy**: Endometrial morphology and pathology analysis

---

## 🚀 **Quick Start**

### Prerequisites
- Python 3.8+
- Node.js (for development)
- Modern web browser

### 1. Clone Repository
```bash
git clone https://github.com/your-username/fertivision-local-dev.git
cd fertivision-local-dev
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Start Frontend (Static Files)
```bash
cd netlify-deploy-fixed
python -m http.server 8001
```
**Access**: http://localhost:8001

### 4. Start API Server
```bash
python api_server.py
```
**Access**: http://localhost:5004

---

## 🔧 **Configuration**

### Frontend Configuration
- Edit `static/js/config.js` for AI provider settings
- Supports Demo mode, Groq, and OpenRouter APIs
- No API keys required for demo mode

### API Server Configuration
- Edit `api_server.py` for API settings
- Default demo API key: `fv_demo_key_12345`
- Configure rate limits and permissions

---

## 🏥 **EMR Integration**

### Python SDK Example
```python
from fertivision_sdk import FertiVisionClient

# Initialize client
client = FertiVisionClient(
    api_key="fv_demo_key_12345",
    base_url="http://localhost:5004"
)

# Analyze sperm sample
result = client.analyze_sperm(
    "sperm_image.jpg",
    patient_id="P12345",
    case_id="C001"
)

print(f"Classification: {result.classification}")
print(f"Confidence: {result.confidence}%")
```

### REST API Example
```bash
curl -X POST http://localhost:5004/api/v1/analyze/sperm \
  -H 'X-API-Key: fv_demo_key_12345' \
  -F 'image=@sperm_sample.jpg' \
  -F 'patient_id=P12345'
```

### Available Endpoints
- `POST /api/v1/analyze/sperm` - WHO 2021 sperm analysis
- `POST /api/v1/analyze/oocyte` - ESHRE oocyte assessment
- `POST /api/v1/analyze/embryo` - Gardner embryo grading
- `POST /api/v1/analyze/follicle` - AFC ovarian reserve assessment
- `POST /api/v1/analyze/hysteroscopy` - Endometrial analysis
- `POST /api/v1/analyze/batch` - Batch processing
- `GET /api/v1/report/{id}` - Analysis reports
- `GET /api/v1/export/pdf/{id}` - PDF generation

---

## 📚 **Documentation**

- **API Documentation**: `API_DOCUMENTATION.md`
- **EMR Integration Guide**: `examples/emr_integration_example.py`
- **Python SDK Reference**: `fertivision_sdk.py`

---

## 🔒 **Security & Privacy**

- ✅ Local data processing (no cloud dependencies)
- ✅ HIPAA-compliant data handling
- ✅ API key authentication
- ✅ Rate limiting and audit logging
- ✅ No external data transmission in demo mode

---

## 🎯 **Use Cases**

### 🏥 **Clinical Deployment**
- Install on local clinic servers
- Integrate with existing EMR systems
- Process patient data locally for privacy

### 🧪 **Research & Development**
- Test new AI models
- Validate analysis algorithms
- Custom integration development

### 📚 **Educational**
- Medical training and education
- Demonstrate AI capabilities
- Research collaboration

---

## 🆚 **Local vs Cloud Versions**

| Feature | Local Development | Cloud Production |
|---------|------------------|------------------|
| **Deployment** | Local servers | Cloud hosted |
| **Authentication** | API keys | Clerk Auth + Subscriptions |
| **Payments** | None | Razorpay integration |
| **Scaling** | Manual | Auto-scaling |
| **Updates** | Manual | Automatic |
| **Support** | Community | Enterprise |
| **Cost** | Free | Subscription-based |

---

## 🔗 **Related Projects**

- **Cloud Production Version**: [fertivision-cloud-saas](https://github.com/your-username/fertivision-cloud-saas)
- **Documentation**: [fertivision-docs](https://github.com/your-username/fertivision-docs)

---

## 📄 **License**

MIT License - See `LICENSE` file for details

---

## 🤝 **Contributing**

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📞 **Support**

- **Issues**: [GitHub Issues](https://github.com/your-username/fertivision-local-dev/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/fertivision-local-dev/discussions)
- **Email**: support@greybrain.ai

---

**© 2025 FertiVision powered by AI | Made by greybrain.ai**

*Advancing reproductive medicine through artificial intelligence*
