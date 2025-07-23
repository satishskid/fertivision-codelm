# 🔬 FertiVision - AI-Enhanced Reproductive Classification System

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](#)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://python.org)
[![AI](https://img.shields.io/badge/AI-DeepSeek%20LLM-purple.svg)](https://deepseek.com)
[![Status](https://img.shields.io/badge/status-Production%20Ready-success.svg)](#)
[![Documentation](https://img.shields.io/badge/docs-Complete-brightgreen.svg)](https://satishskid.github.io/fertivision-codelm/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**🧬 Powered by AI | Made by greybrain.ai**

FertiVision is a comprehensive AI-powered medical imaging analysis platform specifically designed for reproductive medicine. It provides automated classification and analysis of sperm, oocytes, embryos, and ultrasound images using advanced deep learning models.

## 🎉 **PRODUCTION READY** - [**Live Demo**](https://fertivision-ai-514605543640.us-central1.run.app) | [**Complete Documentation**](https://satishskid.github.io/fertivision-codelm/)

### 📚 **Comprehensive Documentation Suite**
- 📋 **[Complete User Manual](FERTIVISION_COMPLETE_USER_MANUAL.md)** - For clinic staff and medical professionals
- 💻 **[Developer Manual](DEVELOPER_MANUAL_COMPLETE.md)** - Technical implementation guide
- 🔌 **[API Documentation](API_DOCUMENTATION_COMPLETE.md)** - Complete REST API reference (50+ endpoints)
- 🏥 **[Clinic Integration Guide](CLINIC_INTEGRATION_GUIDE.md)** - IVF workflow integration
- 🧪 **[Testing Report](ENDPOINT_TESTING_COMPLETE.md)** - Comprehensive validation results
- 🚀 **[Deployment Status](FERTIVISION-AI-DEPLOYMENT-COMPLETE.md)** - Production verification

## 🌟 Features

### 🧬 **Reproductive Analysis Modules**
- **Sperm Analysis**: WHO 2021 criteria-based morphology, motility, and concentration assessment
- **Oocyte Classification**: ESHRE guidelines-compliant maturity and quality grading
- **Embryo Grading**: Gardner grading system for cleavage and blastocyst stages
- **Follicle Counting**: Automated AFC (Antral Follicle Count) and ovarian reserve assessment
- **Hysteroscopy Analysis**: Endometrial morphology and pathology detection

### 🤖 **AI-Powered Analysis**
- **DeepSeek LLM Integration**: Advanced vision-language models for medical image analysis
- **Multiple API Providers**: Support for Groq, OpenRouter, and local Ollama models
- **Mock Mode**: Comprehensive testing environment with realistic medical data
- **Real-time Processing**: Fast analysis with progress tracking and status updates

### 📊 **Professional Reporting**
- **Comprehensive Reports**: Detailed medical analysis with clinical correlations
- **Technical Parameters**: Precise measurements and reference ranges
- **Clinical Recommendations**: Evidence-based treatment guidance
- **PDF Export**: Professional report generation for clinical documentation

### 🧪 **Dataset Testing & Training**
- **Hugging Face Integration**: Access to medical imaging datasets
- **Interactive Testing**: Click-to-analyze sample datasets
- **Performance Metrics**: Real-time accuracy and processing statistics
- **Sample Image Library**: Curated medical images for testing and validation

### 🔌 **API/SDK for IVF EMR Integration**
- **RESTful API Server**: Secure endpoints for medical image analysis
- **Python SDK**: Easy integration library for EMR systems
- **Batch Processing**: Handle multiple analyses efficiently
- **Clinical Reports**: Professional medical documentation with PDF export
- **Authentication & Security**: API key management with rate limiting
- **HIPAA Compliance**: Secure data handling and audit logging

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Flask
- OpenCV
- PIL (Pillow)
- SQLite3

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/satishskid/fertivision-codelm.git
cd fertivision-codelm
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
python app.py
```

4. **Open your browser**
```
Main Application: http://localhost:5002
API Server: http://localhost:5003
```

### API Server Setup

For IVF EMR integration, also start the API server:

```bash
# Start API server (separate terminal)
python api_server.py

# API will be available at: http://localhost:5003
```

## 🔧 Configuration

### Analysis Modes

**Mock Mode (Default)**
- No external API required
- Realistic medical data simulation
- Perfect for testing and demonstration
- Instant results

**API Mode**
- Real AI analysis using cloud providers
- Requires API keys (Groq, OpenRouter, etc.)
- Enhanced accuracy and detailed analysis
- Configurable through settings panel

### API Configuration

1. Navigate to **Settings** tab
2. Add your API keys:
   - **Groq API**: Fast, cost-effective analysis
   - **OpenRouter**: Access to multiple model providers
3. Switch between Local/API modes using the mode selector

## 📱 User Interface

### Main Analysis Tabs
- **🧬 Sperm Analysis**: Upload microscopy images for WHO-compliant analysis
- **🥚 Oocyte Analysis**: ESHRE guidelines-based maturity assessment
- **👶 Embryo Analysis**: Gardner grading for Day 3-6 embryos
- **🔬 Follicle Scan**: Automated follicle counting and PCOS detection
- **🏥 Hysteroscopy**: Endometrial pathology assessment

### Additional Features
- **🧪 Datasets**: Interactive testing with medical datasets
- **📸 Sample Images**: Download curated test images
- **📚 Training**: Comprehensive user guide and tutorials
- **⚙️ Settings**: API configuration and system preferences
- **🔌 API Integration**: RESTful API for EMR system integration

## 🔬 Medical Standards Compliance

### WHO 2021 Guidelines
- Sperm concentration, motility, and morphology assessment
- Reference values and clinical thresholds
- Standardized reporting formats

### ESHRE Guidelines
- Oocyte maturity classification (MII, MI, GV)
- Quality grading and ICSI suitability assessment
- Embryo development staging

### Gardner Grading System
- Blastocyst expansion assessment
- Inner Cell Mass (ICM) grading
- Trophectoderm (TE) evaluation
- Clinical pregnancy prediction

## 🛠️ Technical Architecture

### Backend Components
- **Flask Web Framework**: RESTful API and web interface
- **SQLite Database**: Analysis storage and retrieval
- **OpenCV**: Image preprocessing and enhancement
- **Custom Classification Engine**: Medical-specific algorithms

### AI Integration
- **Vision-Language Models**: DeepSeek, LLaVA for image analysis
- **Multi-Provider Support**: Groq, OpenRouter, Ollama
- **Fallback Systems**: Automatic model switching for reliability
- **Cost Optimization**: Intelligent provider selection

### Security & Privacy
- **Local Processing**: Option for complete offline analysis
- **Secure API Handling**: Encrypted key storage
- **HIPAA Considerations**: Privacy-focused design
- **Data Isolation**: No data sharing with external services in mock mode

## 🔌 API/SDK for IVF EMR Integration

FertiVision provides a comprehensive API and SDK for seamless integration with IVF Electronic Medical Record (EMR) systems.

### 🚀 Quick API Start

**Start the API Server:**
```bash
python api_server.py
# API available at: http://localhost:5003
```

**API Documentation:** http://localhost:5003
**Interactive Testing:** http://localhost:5003/test

### 🔑 Authentication

Use API keys for secure access:
```bash
# Demo API Key (for testing)
X-API-Key: fv_demo_key_12345

# Example API call
curl -H "X-API-Key: fv_demo_key_12345" \
     -F "image=@sperm_sample.jpg" \
     -F "patient_id=P12345" \
     http://localhost:5003/api/v1/analyze/sperm
```

### 🐍 Python SDK Integration

**Installation:**
```bash
# Copy fertivision_sdk.py to your project
from fertivision_sdk import FertiVisionClient
```

**Simple Integration:**
```python
from fertivision_sdk import FertiVisionClient

# Initialize client
client = FertiVisionClient(
    api_key="fv_demo_key_12345",
    base_url="http://localhost:5003"
)

# Analyze sperm sample
result = client.analyze_sperm(
    image_path="sperm_image.jpg",
    patient_id="P12345",
    case_id="C001",
    notes="Day 0 sperm analysis"
)

print(f"Classification: {result.classification}")
print(f"Concentration: {result.concentration} M/ml")
print(f"Motility: {result.progressive_motility}%")
```

**Batch Processing:**
```python
# Process multiple analyses for complete IVF cycle
analyses = [
    AnalysisRequest(patient, "sperm_image.jpg", "sperm", "C001"),
    AnalysisRequest(patient, "embryo_image.jpg", "embryo", "C002", day=3),
    AnalysisRequest(patient, "follicle_scan.jpg", "follicle", "C003")
]

cycle_results = emr.batch_process_cycle(patient, analyses)
```

### 📋 Available API Endpoints

- **POST** `/api/v1/analyze/sperm` - WHO 2021 compliant sperm analysis
- **POST** `/api/v1/analyze/oocyte` - ESHRE guidelines oocyte assessment
- **POST** `/api/v1/analyze/embryo` - Gardner grading embryo evaluation
- **POST** `/api/v1/analyze/follicle` - AFC and ovarian reserve assessment
- **POST** `/api/v1/analyze/hysteroscopy` - Endometrial pathology analysis
- **POST** `/api/v1/analyze/batch` - Multiple image batch processing
- **GET** `/api/v1/report/{id}` - Detailed analysis reports
- **GET** `/api/v1/export/pdf/{id}` - PDF report generation

### 🏥 EMR Integration Benefits

**✅ Seamless Workflow Integration:**
- Direct API calls from EMR systems
- Automatic result integration into patient records
- Professional medical reports with clinical correlations
- Batch processing for high-volume clinics

**✅ Clinical Standards Compliance:**
- WHO 2021 guidelines for sperm analysis
- ESHRE guidelines for oocyte/embryo assessment
- Gardner grading system for embryo evaluation
- Evidence-based clinical recommendations

**✅ Security & Compliance:**
- API key authentication and rate limiting
- HIPAA-compliant data handling
- Secure file processing and storage
- Comprehensive audit logging

## 📊 Sample Analysis Results

### Sperm Analysis Example
```json
{
  "classification": "Normozoospermia",
  "parameters": {
    "concentration": 45.0,
    "progressive_motility": 65.0,
    "normal_morphology": 8.0,
    "volume": 3.0
  },
  "clinical_recommendations": [
    "Excellent fertility potential",
    "Suitable for all ART procedures",
    "Natural conception likely"
  ]
}
```

### Embryo Grading Example
```json
{
  "classification": "Grade A Embryo - Excellent Quality",
  "parameters": {
    "day": 3,
    "cell_count": 8,
    "fragmentation": 5.0,
    "grade": "A"
  },
  "clinical_recommendations": [
    "Excellent transfer candidate",
    "High implantation probability",
    "Consider single embryo transfer"
  ]
}
```

## 🧪 Testing & Validation

### Demo Mode
- Comprehensive sample analyses
- Realistic medical scenarios
- Professional report generation
- No external dependencies required

### Dataset Integration
- Curated medical imaging datasets
- Interactive sample testing
- Performance benchmarking
- Accuracy validation

## 🤝 Contributing

We welcome contributions to improve FertiVision! Please see our contributing guidelines for:
- Code standards and style
- Testing requirements
- Documentation updates
- Feature requests and bug reports

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🏥 Medical Disclaimer

FertiVision is designed for educational and research purposes. All analysis results should be validated by qualified medical professionals. This system is not intended for direct clinical diagnosis or treatment decisions.

## 📁 Project Structure

```
fertivision-codelm/
├── app.py                          # Main web application
├── api_server.py                   # RESTful API server for EMR integration
├── fertivision_sdk.py              # Python SDK for easy integration
├── config.py                       # Configuration management
├── enhanced_reproductive_system.py # Core analysis engine
├── model_config.py                 # AI model configuration
├── ultrasound_analysis.py          # Ultrasound analysis capabilities
├── templates/
│   ├── enhanced_index.html         # Main web interface
│   └── model_config.html           # Model configuration interface
├── examples/
│   └── emr_integration_example.py  # Complete EMR integration example
├── API_DOCUMENTATION.md            # Comprehensive API documentation
├── test_api.py                     # API testing script
├── requirements.txt                # Main application dependencies
├── requirements_api.txt            # API/SDK dependencies
└── README.md                       # This file
```

## 📞 Support

### Technical Support
- **Email**: support@greybrain.ai
- **GitHub Issues**: [Report bugs or request features](https://github.com/satishskid/fertivision-codelm/issues)
- **API Documentation**: [Complete API reference](API_DOCUMENTATION.md)

### Integration Assistance
- **EMR Integration**: Custom integration consulting for IVF clinics
- **API Support**: Technical assistance for API implementation
- **Training**: User training and best practices workshops
- **Custom Development**: Tailored solutions for specific requirements

---

**© 2025 FertiVision powered by AI | Made by greybrain.ai**

*Advancing reproductive medicine through artificial intelligence*