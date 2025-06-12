# 🔬 FertiVision - AI-Enhanced Reproductive Classification System

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](#)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://python.org)
[![AI](https://img.shields.io/badge/AI-DeepSeek%20LLM-purple.svg)](https://deepseek.com)
[![Status](https://img.shields.io/badge/status-Production%20Ready-success.svg)](#)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**🧬 Powered by AI | Made by greybrain.ai**

FertiVision is a comprehensive AI-powered medical imaging analysis platform specifically designed for reproductive medicine. It provides automated classification and analysis of sperm, oocytes, embryos, and ultrasound images using advanced deep learning models.

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
http://localhost:5002
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

## 📊 Sample Analysis Results

### Sperm Analysis Example
```
Classification: Normozoospermia
Technical Details:
- Concentration: 45.0 × 10⁶/ml (Ref: >15)
- Progressive Motility: 65% (Ref: >32%)
- Normal Morphology: 8% (Ref: >4%)
- Volume: 3.0ml (Ref: >1.5ml)

Clinical Recommendations:
- Excellent fertility potential
- Suitable for all ART procedures
- Natural conception likely
```

### Embryo Grading Example
```
Classification: Grade A Embryo - Excellent Quality
Technical Details:
- Developmental Stage: Day 3 (72 hours)
- Cell Count: 8 cells (optimal)
- Fragmentation: <5% (minimal)
- Implantation Potential: High (>60%)

Clinical Recommendations:
- Excellent transfer candidate
- High implantation probability
- Consider single embryo transfer
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

## 📞 Support

For technical support, feature requests, or collaboration opportunities:
- **Email**: support@greybrain.ai
- **GitHub Issues**: [Report bugs or request features](https://github.com/satishskid/fertivision-codelm/issues)
- **Documentation**: [Comprehensive guides and tutorials](https://github.com/satishskid/fertivision-codelm/wiki)

---

**© 2025 FertiVision powered by AI | Made by greybrain.ai**

*Advancing reproductive medicine through artificial intelligence*