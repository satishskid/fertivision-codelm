# FertiVision-CodeLM Complete User Manual

## Table of Contents
1. [Overview](#overview)
2. [System Requirements](#system-requirements)
3. [Installation](#installation)
4. [Getting Started](#getting-started)
5. [User Interface](#user-interface)
6. [Analysis Modules](#analysis-modules)
7. [Advanced Features](#advanced-features)
8. [Configuration](#configuration)
9. [Troubleshooting](#troubleshooting)
10. [API Documentation](#api-documentation)

## Overview

FertiVision-CodeLM is an AI-enhanced reproductive medicine classification system that provides comprehensive analysis of medical images and laboratory parameters across multiple fertility disciplines. The system combines traditional parameter-based analysis with cutting-edge AI image analysis using DeepSeek/Ollama integration.

### Key Features
- **Multi-disciplinary Support**: Andrology, Embryology, Reproductive Endocrinology, Gynecology, and Radiology
- **AI-Powered Analysis**: Local DeepSeek/Ollama integration for image analysis
- **Professional Reporting**: PDF export with medical-grade documentation
- **Extended File Support**: Standard images, DICOM, NIfTI, and video formats
- **Authentication System**: Secure access for medical environments
- **Real-time Processing**: Instant analysis and classification results

## System Requirements

### Hardware Requirements
- **Processor**: Intel Core i5 or equivalent (i7+ recommended for AI features)
- **Memory**: 8GB RAM minimum (16GB+ recommended for AI processing)
- **Storage**: 5GB free disk space
- **Graphics**: GPU recommended for enhanced AI performance (optional)

### Software Requirements
- **Operating System**: macOS 10.15+, Windows 10+, or Linux Ubuntu 18.04+
- **Python**: Version 3.8 or higher
- **Browser**: Chrome, Firefox, Safari, or Edge (latest versions)
- **Ollama**: For AI-powered analysis (optional for mock mode)

## Installation

### Method 1: Quick Start Script
```bash
# Clone the repository
git clone https://github.com/your-repo/fertivision-codelm.git
cd fertivision-codelm

# Run the automated setup
./start.sh
```

### Method 2: Manual Installation
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements_enhanced.txt

# Create necessary directories
mkdir -p uploads exports test_exports

# Initialize database
python3 enhanced_reproductive_system.py

# Start the application
python3 app.py
```

### Installing DeepSeek/Ollama (Optional)
For AI-powered analysis, install Ollama and the DeepSeek model:

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull DeepSeek model
ollama pull deepseek-coder

# Start Ollama service
ollama serve
```

## Getting Started

### First Launch
1. Start the application by running `python3 app.py`
2. Open your browser and navigate to `http://localhost:5002`
3. You'll see the main dashboard with five analysis modules

### Authentication (If Enabled)
If authentication is enabled in the configuration:
- **Username**: `doctor`
- **Password**: `fertility2025`
- Session timeout: 1 hour

### Quick Test
1. Navigate to the "Sperm Analysis" tab
2. Enter some sample parameters:
   - Concentration: 50 million/mL
   - Progressive Motility: 60%
   - Normal Morphology: 8%
3. Click "Analyze Sperm"
4. Review the classification results

## User Interface

### Main Dashboard
The main interface features a modern, medical-grade design with:
- **Tab-based Navigation**: Five main analysis modules
- **Progress Indicators**: Real-time analysis progress with animations
- **Result Panels**: Immediate display of analysis results
- **Action Buttons**: Export, report generation, and additional options

### Navigation Tabs
1. **Sperm Analysis**: Andrology parameters and WHO classification
2. **Oocyte Grading**: ESHRE guidelines-based oocyte assessment
3. **Embryo Classification**: ASRM/ESHRE embryo grading
4. **Follicle Scan**: Ovarian reserve and AFC assessment
5. **Hysteroscopy**: Endometrial and uterine cavity analysis

### Progress Bar System
- **Animated Progress**: Visual feedback during analysis
- **Shimmer Effects**: Modern loading animations
- **Status Updates**: Real-time processing information
- **Error Handling**: Clear error messages and recovery options

## Analysis Modules

### 1. Sperm Analysis (Andrology)

**Parameters Required:**
- Concentration (million/mL)
- Progressive Motility (%)
- Normal Morphology (%)
- Volume (mL) - optional
- pH - optional
- Liquefaction Time (minutes) - optional

**WHO Classification Results:**
- Normozoospermia: Normal parameters
- Oligozoospermia: Low concentration
- Asthenozoospermia: Poor motility
- Teratozoospermia: Poor morphology
- Combined conditions

**Image Analysis Features:**
- Upload microscopy images for AI analysis
- Automated parameter extraction
- Morphology assessment
- Motility pattern analysis

### 2. Oocyte Grading (Embryology)

**Parameters Required:**
- Maturity Stage: MII (Metaphase II), MI (Metaphase I), GV (Germinal Vesicle)
- Morphology Score: 1-5 scale
- Cytoplasm appearance
- Polar body status
- Zona pellucida assessment

**ESHRE Classification:**
- Grade A: Excellent quality
- Grade B: Good quality
- Grade C: Fair quality
- Grade D: Poor quality

**AI Features:**
- Automated maturity detection
- Morphology scoring
- Cytoplasm analysis
- Polar body assessment

### 3. Embryo Classification (Embryology)

**Parameters Required:**
- Development Day (1-6)
- Cell Count
- Fragmentation Percentage
- Multinucleation Status
- Symmetry Assessment

**ASRM/ESHRE Classification:**
- Grade 1: Excellent (>8 cells, <10% fragmentation)
- Grade 2: Good (6-8 cells, 10-20% fragmentation)
- Grade 3: Fair (4-6 cells, 20-50% fragmentation)
- Grade 4: Poor (<4 cells, >50% fragmentation)

**Time-lapse Analysis:**
- Video format support for development tracking
- Automated cell counting
- Fragmentation assessment
- Development timing analysis

### 4. Follicle Scan Analysis (Reproductive Endocrinology)

**Parameters Detected:**
- Antral Follicle Count (AFC)
- Dominant Follicle Size
- Total Follicle Count
- Ovarian Volume
- Stromal Assessment

**Clinical Classifications:**
- Normal Ovarian Reserve: AFC 6-25
- Low Ovarian Reserve: AFC <6
- High Ovarian Reserve: AFC >25
- PCOS Indicators: Multiple small follicles

**AI Capabilities:**
- DICOM format support
- Automated follicle counting
- Size measurements
- Volume calculations
- Ovarian reserve assessment

### 5. Hysteroscopy Analysis (Gynecology)

**Assessment Parameters:**
- Endometrial Thickness
- Uterine Cavity Shape
- Pathological Findings
- Vascular Patterns
- Cervical Canal Assessment

**Pathology Detection:**
- Polyps
- Fibroids
- Adhesions
- Septum
- Hyperplasia
- Normal findings

**Clinical Recommendations:**
- Biopsy indications
- Treatment options
- Follow-up requirements
- Fertility impact assessment

## Advanced Features

### PDF Export System

**Individual Reports:**
1. Complete an analysis in any module
2. Click the "Export PDF" button
3. Professional medical report is generated
4. File saved to exports folder

**Batch Reports:**
1. Select multiple completed analyses
2. Use batch export feature
3. Combined PDF with all analyses
4. Comprehensive patient documentation

**Report Features:**
- Medical-grade formatting
- Parameter tables with reference ranges
- AI analysis integration
- Clinical recommendations
- Professional header and footer

### Medical Discipline Detection

The system automatically detects the appropriate medical discipline based on:
- **Filename Keywords**: "sperm", "embryo", "follicle", "hysteroscopy"
- **File Extensions**: DICOM (.dcm) for radiology
- **Content Analysis**: Automatic routing to appropriate module

### Extended File Format Support

**Standard Images:**
- PNG, JPG, JPEG, TIFF, BMP, GIF, WebP
- Maximum size: 50MB

**Medical Formats:**
- DICOM (.dcm, .dcm30, .ima)
- NIfTI (.nii, .nii.gz)
- Maximum size: 100MB

**Video Formats:**
- MP4, AVI, MOV, MKV, WMV
- Maximum size: 500MB
- For time-lapse embryo analysis

### Authentication and Security

**Basic Authentication:**
- Username/password protection
- Session management
- Automatic timeout
- Secure route protection

**Data Security:**
- Local processing only
- No external API calls for sensitive data
- Encrypted session storage
- Audit trail logging

## Configuration

### Analysis Mode Switching

**Mock Mode** (Default for testing):
```bash
# Using toggle script
./toggle_analysis_mode.sh

# Manual configuration
# Edit config.py: ANALYSIS_MODE = AnalysisMode.MOCK
```

**DeepSeek Mode** (AI-powered):
```bash
# Ensure Ollama is running
ollama serve

# Switch mode
./toggle_analysis_mode.sh

# Manual configuration
# Edit config.py: ANALYSIS_MODE = AnalysisMode.DEEPSEEK
```

### File Size Limits

Edit `config.py` to modify file size limits:
```python
MAX_IMAGE_SIZE = 50      # MB
MAX_VIDEO_SIZE = 500     # MB
MAX_MEDICAL_SIZE = 100   # MB
```

### Authentication Settings

```python
ENABLE_AUTH = True              # Enable/disable authentication
DEFAULT_USERNAME = "doctor"     # Change default username
DEFAULT_PASSWORD = "your_pass"  # Change default password
SESSION_TIMEOUT = 3600          # Session timeout in seconds
```

### Database Configuration

```python
DATABASE_PATH = "reproductive_analysis.db"
BACKUP_DATABASE = True
AUTO_BACKUP_INTERVAL = 24  # hours
```

## Troubleshooting

### Common Issues

**1. Application Won't Start**
```bash
# Check Python version
python3 --version

# Verify dependencies
pip install -r requirements_enhanced.txt

# Check port availability
lsof -i :5002
```

**2. AI Analysis Not Working**
```bash
# Check Ollama status
ollama list

# Start Ollama service
ollama serve

# Install DeepSeek model
ollama pull deepseek-coder

# Switch to mock mode for testing
./toggle_analysis_mode.sh
```

**3. File Upload Errors**
- Check file format is supported
- Verify file size is within limits
- Ensure uploads folder has write permissions
- Check disk space availability

**4. PDF Export Issues**
```bash
# Install ReportLab
pip install reportlab

# Check exports folder permissions
chmod 755 exports/

# Verify disk space
df -h
```

**5. Database Errors**
```bash
# Backup existing database
cp reproductive_analysis.db reproductive_analysis.db.backup

# Reinitialize database
python3 enhanced_reproductive_system.py
```

### Error Messages

**"Analysis Error: 'dict' object has no attribute 'classification'"**
- This has been fixed in the latest version
- Restart the application to apply fixes

**"DeepSeek LLM not available"**
- Start Ollama service: `ollama serve`
- Install DeepSeek model: `ollama pull deepseek-coder`
- Or switch to mock mode for testing

**"File too large"**
- Check file size limits in configuration
- Compress large files before upload
- Use appropriate format for file type

### Getting Help

1. **Check Logs**: Application logs show detailed error information
2. **Run Tests**: Use `python3 test_enhanced_features.py` to verify system
3. **Mock Mode**: Switch to mock mode to isolate AI-related issues
4. **Documentation**: Refer to ENHANCED_FEATURES.md for technical details

## API Documentation

### REST Endpoints

**Analysis Endpoints:**
- `POST /analyze_sperm` - Sperm parameter analysis
- `POST /analyze_oocyte` - Oocyte grading analysis
- `POST /analyze_embryo` - Embryo classification
- `POST /analyze_follicle_scan` - Follicle scan with image
- `POST /analyze_hysteroscopy` - Hysteroscopy analysis

**Image Analysis:**
- `POST /analyze_image/<analysis_type>` - Generic image analysis

**Reporting:**
- `GET /report/<analysis_type>/<analysis_id>` - Generate text report
- `GET /export_pdf/<analysis_type>/<analysis_id>` - Export PDF report

**System:**
- `GET /system_status` - Check system configuration
- `POST /switch_mode/<mode>` - Switch analysis mode
- `POST /validate_file` - Validate file format and size

### Response Formats

**Success Response:**
```json
{
    "success": true,
    "classification": "Normozoospermia",
    "sample_id": "SPERM_20250610_123456",
    "details": {
        "concentration": 50.0,
        "progressive_motility": 60.0,
        "normal_morphology": 8.0
    }
}
```

**Error Response:**
```json
{
    "success": false,
    "error": "File format not supported"
}
```

### Integration Examples

**Python Integration:**
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

**JavaScript Integration:**
```javascript
// Upload and analyze image
const formData = new FormData();
formData.append('image', fileInput.files[0]);

fetch('/analyze_image/sperm', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => {
    console.log('Analysis:', data.classification);
});
```

## Conclusion

FertiVision-CodeLM provides a comprehensive, AI-enhanced platform for reproductive medicine analysis. The system combines traditional clinical parameters with modern AI capabilities to deliver accurate, professional-grade medical assessments.

For technical support or feature requests, please refer to the project documentation or contact the development team.

---

**Version**: 2.0.0  
**Last Updated**: June 10, 2025  
**Documentation**: Complete User Manual  
**System**: FertiVision-CodeLM AI-Enhanced Reproductive Classification System