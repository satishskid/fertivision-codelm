# 🔬 FertiVision-CodeLM: AI-Enhanced Reproductive Classification System

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](#)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://python.org)
[![AI](https://img.shields.io/badge/AI-DeepSeek%20Ollama-purple.svg)](https://ollama.ai)
[![Status](https://img.shields.io/badge/status-Production%20Ready-success.svg)](#)

**Professional-grade AI-enhanced reproductive medicine analysis platform combining traditional clinical parameters with cutting-edge image analysis capabilities.**

## 🌟 Overview

FertiVision-CodeLM is a comprehensive AI-powered solution for reproductive medicine, integrating advanced image analysis with specialized medical expertise across multiple disciplines. The system provides real-time analysis, professional reporting, and secure data handling for clinical environments.

## ✨ Key Features

### 🏥 Multi-Disciplinary Medical Support
- **Andrology**: Complete sperm analysis with WHO classification
- **Embryology**: ASRM/ESHRE embryo grading and oocyte assessment  
- **Reproductive Endocrinology**: Follicle counting and ovarian reserve evaluation
- **Gynecology**: Hysteroscopy analysis and endometrial assessment
- **Radiology**: Advanced medical imaging format support (DICOM, NIfTI)

### 🤖 AI-Powered Analysis
- **Local Processing**: DeepSeek/Ollama integration for secure, local AI analysis
- **Image Recognition**: Automated parameter extraction from medical images
- **Smart Classification**: Evidence-based categorization following medical guidelines
- **Mock Mode**: Full testing capabilities without AI dependencies

### 📊 Professional Features
- **PDF Export**: Medical-grade report generation with professional formatting
- **Batch Processing**: Multiple analyses in combined reports
- **Authentication**: Session-based security with configurable timeouts
- **Extended File Support**: Images, DICOM, NIfTI, video formats
- **Real-time Progress**: Animated progress indicators and status updates

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

### Access the Application
Open your browser and navigate to: **http://localhost:5002**

## 📱 Analysis Modules
- 📁 **Extended Format Support**: Handle standard images, DICOM, and video formats

## Quick Start

### Prerequisites

- Python 3.9+ with pip
- [Ollama](https://ollama.ai) (for AI-powered mode)

### Installation

```bash
# Clone the repository
git clone https://github.com/username/fertivision-codelm.git
cd fertivision-codelm

# Run installation script
./start.sh
```

Or install manually:

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements_enhanced.txt

# Create necessary directories
mkdir -p uploads exports
```

### Running the Application

```bash
# Start the Flask application
python app.py

# Open in browser: http://localhost:5002
```

## Documentation

- [User Manual](USER_MANUAL.md): Comprehensive guide for users
- [Enhanced Features](ENHANCED_FEATURES.md): Details on new capabilities
- [License](LICENSE): MIT License information

## Technical Architecture

FertiVision-CodeLM is built on a Flask backend with modules for:

- **Image Analysis**: AI-powered microscopy and ultrasound processing
- **Medical Classification**: Evidence-based reproductive parameter analysis
- **PDF Export**: Professional medical report generation
- **Authentication**: Session-based security system
- **Configuration**: Comprehensive settings management

## Development

- Toggle between Mock and DeepSeek modes:
  ```
  ./toggle_analysis_mode.sh
  ```

- Run tests:
  ```
  python test_enhanced_features.py
  ```

## Screenshots

![Sperm Analysis Module](https://via.placeholder.com/400x300?text=Sperm+Analysis)
![Follicle Scan Analysis](https://via.placeholder.com/400x300?text=Follicle+Scan)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Citation

If you use FertiVision-CodeLM in your research, please cite:

```
@software{fertivision-codelm,
  title = {FertiVision-CodeLM: AI-Enhanced Reproductive Classification System},
  author = {FertiVision Team},
  year = {2025},
  url = {https://github.com/username/fertivision-codelm}
}
```