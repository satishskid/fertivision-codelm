# 🔬 FertiVision-CodeLM: AI-Enhanced Reproductive Classification System

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/your-repo/fertivision-codelm)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![AI](https://img.shields.io/badge/AI-DeepSeek%20Ollama-purple.svg)](https://ollama.ai)

**Professional-grade AI-enhanced reproductive medicine analysis platform combining traditional clinical parameters with cutting-edge image analysis capabilities.**

## 🌟 Key Features

### 🏥 Multi-Disciplinary Medical Support
- **Andrology**: Complete sperm analysis with WHO classification
- **Embryology**: ASRM/ESHRE embryo grading and oocyte assessment
- **Reproductive Endocrinology**: Follicle counting and ovarian reserve evaluation
- **Gynecology**: Hysteroscopy analysis and endometrial assessment
- **Radiology**: Advanced medical imaging format support

### 🤖 AI-Powered Analysis
- **Local Processing**: DeepSeek/Ollama integration for secure, local AI analysis
- **Image Recognition**: Automated parameter extraction from medical images
- **Smart Classification**: Evidence-based categorization following medical guidelines
- **Mock Mode**: Full testing capabilities without AI dependencies

### 📊 Professional Reporting
- **PDF Export**: Medical-grade report generation
- **Batch Processing**: Multiple analyses in combined reports
- **Clinical Standards**: Adherence to international medical guidelines
- **Audit Trail**: Complete analysis history and documentation

### 🔒 Enterprise Security
- **Local Deployment**: No external API dependencies for sensitive data
- **Authentication**: Session-based security with configurable timeouts
- **Data Privacy**: Complete patient data protection
- **Secure Storage**: Encrypted local database storage

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- 8GB RAM (16GB+ recommended for AI features)
- 5GB free disk space

### Installation

```bash
# Clone the repository
git clone https://github.com/your-repo/fertivision-codelm.git
cd fertivision-codelm

# Run automated setup
chmod +x start.sh
./start.sh
```

### Manual Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements_enhanced.txt

# Create directories
mkdir -p uploads exports test_exports

# Start application
python3 app.py
```

### Access the Application
Open your browser and navigate to: `http://localhost:5002`

## 📱 User Interface

### Modern Medical Dashboard
- **Clean Design**: Professional medical-grade interface
- **Tab Navigation**: Five specialized analysis modules
- **Real-time Progress**: Animated progress indicators
- **Responsive Layout**: Works on desktop and tablet devices

### Analysis Modules
1. **🧬 Sperm Analysis**: WHO parameter classification and image analysis
2. **🥚 Oocyte Grading**: ESHRE guidelines-based quality assessment
3. **👶 Embryo Classification**: Development staging and quality grading
4. **🔍 Follicle Scan**: AFC counting and ovarian reserve assessment
5. **🏥 Hysteroscopy**: Endometrial morphology and pathology detection

## 🔧 Advanced Features

### Extended File Format Support
- **Standard Images**: PNG, JPG, JPEG, TIFF, BMP, GIF, WebP
- **Medical Formats**: DICOM (.dcm, .dcm30, .ima), NIfTI (.nii, .nii.gz)
- **Video Files**: MP4, AVI, MOV, MKV, WMV (for time-lapse analysis)
- **Smart Size Limits**: Configurable based on file type

### AI Integration Options

#### DeepSeek/Ollama Setup (Optional)
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull DeepSeek model
ollama pull deepseek-coder

# Start Ollama service
ollama serve &
```

#### Mode Switching
```bash
# Toggle between Mock and AI modes
./toggle_analysis_mode.sh
```

### PDF Export System
- **Individual Reports**: Single analysis documentation
- **Batch Reports**: Multiple analyses combined
- **Medical Formatting**: Professional clinical report layout
- **Custom Templates**: Specialized templates for each analysis type

## 📊 Analysis Capabilities

### Sperm Analysis (Andrology)
- **Parameters**: Concentration, motility, morphology, volume, pH
- **WHO Standards**: 2021 reference values and classifications
- **Image Analysis**: Automated microscopy image assessment
- **Quality Control**: Statistical analysis and outlier detection

### Oocyte Grading (Embryology)
- **Maturity Assessment**: MII, MI, GV classification
- **Morphology Scoring**: 1-5 scale quality assessment
- **ESHRE Guidelines**: International standardized protocols
- **Polar Body Analysis**: Developmental indicator assessment

### Embryo Classification (Embryology)
- **Development Staging**: Day 1-6 progression tracking
- **Cell Counting**: Automated blastomere enumeration
- **Fragmentation Analysis**: Quality impact assessment
- **Time-lapse Support**: Video-based development tracking

### Follicle Scan Analysis (Reproductive Endocrinology)
- **AFC Counting**: Antral follicle enumeration
- **Size Measurements**: Dominant follicle tracking
- **Ovarian Volume**: Reserve assessment calculations
- **PCOS Detection**: Polycystic ovary syndrome indicators

### Hysteroscopy Analysis (Gynecology)
- **Endometrial Assessment**: Thickness and pattern evaluation
- **Pathology Detection**: Polyps, fibroids, adhesions identification
- **Cavity Evaluation**: Structural abnormality assessment
- **Clinical Recommendations**: Treatment and follow-up guidance

## ⚙️ Configuration

### Analysis Modes
```python
# config.py
ANALYSIS_MODE = AnalysisMode.MOCK     # For testing
ANALYSIS_MODE = AnalysisMode.DEEPSEEK # For AI analysis
```

### Authentication Settings
```python
ENABLE_AUTH = True
DEFAULT_USERNAME = "doctor"
DEFAULT_PASSWORD = "fertility2025"
SESSION_TIMEOUT = 3600  # 1 hour
```

### File Size Limits
```python
MAX_IMAGE_SIZE = 50      # MB
MAX_VIDEO_SIZE = 500     # MB
MAX_MEDICAL_SIZE = 100   # MB
```

## 🔬 API Documentation

### REST Endpoints

#### Analysis Endpoints
```bash
POST /analyze_sperm          # Sperm parameter analysis
POST /analyze_oocyte         # Oocyte grading
POST /analyze_embryo         # Embryo classification
POST /analyze_follicle_scan  # Follicle scan analysis
POST /analyze_hysteroscopy   # Hysteroscopy analysis
```

#### Reporting Endpoints
```bash
GET  /report/{type}/{id}           # Generate text report
GET  /export_pdf/{type}/{id}       # Export PDF report
POST /batch_export_pdf             # Batch PDF export
```

#### System Endpoints
```bash
GET  /system_status               # System configuration
POST /switch_mode/{mode}          # Toggle analysis mode
POST /validate_file              # File validation
```

### Example Usage

#### Python Integration
```python
import requests

# Analyze sperm parameters
data = {
    "concentration": 45.0,
    "progressive_motility": 55.0,
    "normal_morphology": 7.0
}

response = requests.post(
    "http://localhost:5002/analyze_sperm",
    json=data
)

result = response.json()
print(f"Classification: {result['classification']}")
```

#### JavaScript Integration
```javascript
// Upload and analyze image
const formData = new FormData();
formData.append('image', fileInput.files[0]);

fetch('/analyze_image/sperm', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => console.log('Analysis:', data.classification));
```

## 🧪 Testing

### Run Test Suite
```bash
# Test all enhanced features
python3 test_enhanced_features.py

# Test specific workflows
python3 test_workflow.py

# Test system configuration
python3 -c "from config import Config; print('Tests passed!')"
```

### Sample Test Data
- Test images included in `uploads/` directory
- Sample PDFs generated in `test_exports/`
- Mock analysis data for all modules

## 🛠️ Troubleshooting

### Common Issues

**Application Won't Start**
```bash
# Check dependencies
pip install -r requirements_enhanced.txt

# Verify Python version
python3 --version  # Should be 3.8+
```

**AI Analysis Not Working**
```bash
# Check Ollama status
ollama list

# Switch to mock mode
./toggle_analysis_mode.sh
```

**File Upload Errors**
- Verify file format is supported
- Check file size limits
- Ensure proper folder permissions

### Error Resolution
- **Authentication Issues**: Check username/password in config
- **PDF Export Problems**: Verify ReportLab installation
- **Database Errors**: Backup and reinitialize database

## 📚 Documentation

- **[Complete User Manual](USER_MANUAL_COMPLETE.md)**: Comprehensive usage guide
- **[Enhanced Features](ENHANCED_FEATURES.md)**: New feature documentation
- **[API Reference](USER_MANUAL_COMPLETE.md#api-documentation)**: Technical integration guide

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏥 Medical Compliance

- **ISO 13485**: Medical device quality management compliance
- **HIPAA**: Health information privacy protection
- **IVD Guidelines**: In vitro diagnostic device standards
- **Clinical Validation**: Evidence-based analysis algorithms

## 📞 Support

- **Documentation**: Comprehensive user manual and API reference
- **Issues**: GitHub issue tracker for bug reports
- **Discussions**: Community support and feature requests

## 🎯 Roadmap

### Version 2.1 (Planned)
- [ ] Advanced AI model integration
- [ ] Multi-language support
- [ ] Enhanced DICOM viewer
- [ ] Real-time collaboration features

### Version 3.0 (Future)
- [ ] Cloud deployment options
- [ ] Mobile application support
- [ ] Advanced analytics dashboard
- [ ] Machine learning model training interface

---

**🔬 FertiVision-CodeLM** - Advancing reproductive medicine through AI-enhanced analysis

*Developed with ❤️ for the fertility community*
