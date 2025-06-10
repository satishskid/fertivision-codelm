# FertiVision-CodeLM User Manual

## Table of Contents
1. [Introduction](#introduction)
2. [System Requirements](#system-requirements)
3. [Installation](#installation)
4. [Getting Started](#getting-started)
5. [Main Features](#main-features)
6. [Using the Analysis Modules](#using-the-analysis-modules)
7. [Report Generation](#report-generation)
8. [PDF Export](#pdf-export)
9. [Authentication](#authentication)
10. [File Format Support](#file-format-support)
11. [Advanced Configuration](#advanced-configuration)
12. [Troubleshooting](#troubleshooting)
13. [FAQ](#faq)

## Introduction <a name="introduction"></a>

FertiVision-CodeLM is an AI-Enhanced Reproductive Classification System designed for reproductive medicine professionals. The system combines advanced image analysis with medical expertise to provide comprehensive assessments across multiple reproductive disciplines.

The platform offers five specialized analysis modules:
- Sperm Analysis
- Oocyte Grading
- Embryo Classification
- Follicle Scan Analysis
- Hysteroscopy Analysis

Each module integrates with DeepSeek AI to provide detailed insights and generate professional medical reports.

## System Requirements <a name="system-requirements"></a>

### Hardware Requirements
- CPU: Quad-core processor (or better)
- RAM: 8GB minimum, 16GB recommended
- Storage: 10GB free space for application and data
- Network: Internet connection for initial setup

### Software Requirements
- Operating System: macOS, Linux, or Windows 10/11
- Python 3.9+ with pip
- Web browser: Chrome, Firefox, Safari, or Edge (latest versions)
- Ollama (for AI-powered analysis)

## Installation <a name="installation"></a>

### Standard Installation

1. Clone the repository:
   ```
   git clone https://github.com/username/fertivision-codelm.git
   cd fertivision-codelm
   ```

2. Run the installation script:
   ```
   ./start.sh
   ```

   This script will:
   - Create and activate a Python virtual environment
   - Install all dependencies
   - Create necessary directories
   - Set up the Ollama service and DeepSeek model

3. For manual installation:
   ```
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements_enhanced.txt
   mkdir -p uploads exports
   ```

### DeepSeek/Ollama Setup

To enable AI-powered analysis:

1. Install Ollama: 
   ```
   curl -fsSL https://ollama.ai/install.sh | sh
   ```

2. Pull the DeepSeek model:
   ```
   ollama pull deepseek-coder
   ```

3. Run the Ollama service:
   ```
   ollama serve
   ```

## Getting Started <a name="getting-started"></a>

### Starting the Application

1. Run the application:
   ```
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:5002
   ```

3. If authentication is enabled, log in with:
   - Username: doctor
   - Password: fertility2025

### User Interface

The FertiVision interface features a modern, light-themed design with:

- **Navigation Tabs**: Select between the five analysis modules
- **Upload Section**: Upload images or input parameter data
- **Progress Indicators**: Visual feedback during analysis
- **Results View**: Display analysis results and classifications
- **Report Section**: View and export detailed reports

## Main Features <a name="main-features"></a>

### 1. AI-Enhanced Analysis

- **DeepSeek Integration**: Local AI processing of medical images
- **Medical Parameter Extraction**: Automated detection of key parameters
- **Classification System**: Evidence-based categorization of results
- **Mock Mode**: For testing and demonstration without AI

### 2. Multi-disciplinary Support

- **Andrology**: Complete sperm analysis with motility and morphology
- **Embryology**: Embryo grading with cell counting and fragmentation analysis
- **Reproductive Endocrinology**: Follicle counting and ovarian reserve assessment
- **Gynecology**: Hysteroscopy with endometrial and pathology detection
- **Radiology**: Support for medical imaging formats

### 3. Professional Reporting

- **Structured Reports**: Clinically relevant format
- **Customized Outputs**: Discipline-specific report templates
- **PDF Export**: Professional medical documentation
- **Batch Processing**: Multiple analyses in combined reports

### 4. Security Features

- **Authentication**: Username/password protection
- **Session Management**: Automatic timeouts for security
- **Configurable Access**: Enable/disable security features

## Using the Analysis Modules <a name="using-the-analysis-modules"></a>

### Sperm Analysis

1. Select the "Sperm Analysis" tab
2. Upload a sperm microscopy image or enter parameters manually:
   - Concentration (million/mL)
   - Progressive motility (%)
   - Normal morphology (%)
   - Volume (mL)
   - pH (optional)
3. Click "Analyze" to process
4. Review results showing:
   - WHO classification
   - Parameter analysis
   - AI-enhanced observations
   - Recommendations

### Oocyte Grading

1. Select the "Oocyte Grading" tab
2. Upload an oocyte microscopy image
3. Select maturity level (MII, MI, GV)
4. Enter morphology score (1-5)
5. Click "Analyze" to process
6. Review detailed maturity and quality assessment

### Embryo Classification

1. Select the "Embryo Classification" tab
2. Upload an embryo microscopy image
3. Enter:
   - Development day (1-6)
   - Cell count
   - Fragmentation percentage
   - Multinucleation status
4. Click "Analyze" to process
5. Review embryo quality classification and development assessment

### Follicle Scan Analysis

1. Select the "Follicle Scan" tab
2. Upload a follicle ultrasound image
3. Enter:
   - Patient age (optional)
   - Cycle day (optional)
4. Click "Analyze" to process
5. Review:
   - Antral follicle count
   - Dominant follicle measurements
   - Ovarian reserve assessment
   - AI-enhanced observations

### Hysteroscopy Analysis

1. Select the "Hysteroscopy" tab
2. Upload a hysteroscopy image/video
3. Enter:
   - Endometrial thickness (mm, optional)
   - Procedure date (optional)
4. Click "Analyze" to process
5. Review:
   - Endometrial assessment
   - Pathology detection
   - Clinical observations
   - Recommendations

## Report Generation <a name="report-generation"></a>

Each analysis generates a detailed report including:

1. **Sample Information**: Identification and timestamp
2. **Classification**: Primary diagnosis or assessment
3. **Parameter Analysis**: Detailed measurements with reference ranges
4. **AI Observations**: DeepSeek-generated insights
5. **Clinical Context**: Relevance to fertility assessment
6. **Next Steps**: Recommended actions or follow-up

To view a report:
1. Complete an analysis
2. Scroll down to the "Report" section
3. Review the generated report

## PDF Export <a name="pdf-export"></a>

### Exporting Individual Reports

1. After completing an analysis, click the "Export to PDF" button
2. The PDF will be generated and downloaded automatically
3. PDFs are also saved to the "exports" folder

### Batch Export

For multiple reports:

1. Navigate to the Batch Processing section
2. Select multiple analyses using the checkboxes
3. Click "Export Selected" to generate a combined PDF
4. The combined report will include all selected analyses

### PDF Format

Exported PDFs include:

- Professional letterhead
- Complete analysis data
- Reference ranges and classifications
- Any uploaded images with AI annotations
- Date and time of analysis
- Customized formatting for each analysis type

## Authentication <a name="authentication"></a>

### Enabling Authentication

By default, authentication is disabled. To enable:

1. Edit `config.py`
2. Set `ENABLE_AUTH = True`
3. Restart the application

### Login Process

1. When accessing the application, you'll be redirected to a login page
2. Enter username and password
3. Sessions expire after 1 hour of inactivity

### Changing Credentials

To change default login credentials:

1. Edit `config.py`
2. Update:
   ```python
   DEFAULT_USERNAME = "your_username"
   DEFAULT_PASSWORD = "your_password"
   ```
3. Restart the application

## File Format Support <a name="file-format-support"></a>

### Supported Image Formats

- **Standard Images**: png, jpg, jpeg, tiff, bmp, gif, webp
- **Medical Formats**: DICOM (dcm, dcm30, ima), NIfTI (nii, nii.gz)
- **Video Formats**: mp4, avi, mov, mkv, wmv

### File Size Limits

- Images: 50MB
- Videos: 500MB
- Medical Files: 100MB

### Medical Discipline Detection

The system automatically detects disciplines based on:
1. File extension
2. Filename keywords
3. File content patterns

## Advanced Configuration <a name="advanced-configuration"></a>

### Switching Between Mock and AI Modes

Use the provided script:
```
./toggle_analysis_mode.sh
```

Or manually edit `config.py`:
```python
ANALYSIS_MODE = AnalysisMode.MOCK  # or AnalysisMode.DEEPSEEK
```

### Database Configuration

The system uses SQLite by default. Database settings in `config.py`:
```python
DATABASE_PATH = "reproductive_analysis.db"
BACKUP_DATABASE = True
AUTO_BACKUP_INTERVAL = 24  # hours
```

### UI Customization

Modify UI settings in `config.py`:
```python
THEME = "light"  # or "dark"
SHOW_ADVANCED_OPTIONS = True
```

## Troubleshooting <a name="troubleshooting"></a>

### Common Issues and Solutions

1. **Application won't start**
   - Check if port 5002 is already in use
   - Ensure Python 3.9+ is installed
   - Verify all dependencies are installed

2. **Upload errors**
   - Check if upload directory exists and is writable
   - Verify file format is supported
   - Ensure file size is within limits

3. **AI analysis not working**
   - Check if Ollama is running (`ollama serve`)
   - Verify DeepSeek model is installed
   - Try switching to MOCK mode temporarily

4. **PDF export fails**
   - Ensure ReportLab is properly installed
   - Check if exports directory exists and is writable
   - Verify analysis data is complete

5. **Authentication issues**
   - Clear browser cookies and cache
   - Check configured username/password
   - Verify config.py settings

### Running Diagnostics

Use the diagnostic script:
```
python test_enhanced_features.py
```

This will check:
- Configuration settings
- File format support
- PDF generation
- Authentication
- Enhanced system features

## FAQ <a name="faq"></a>

**Q: Can I use my own AI models?**
A: Yes, modify the `DEEPSEEK_MODEL` in config.py to use another Ollama-compatible model.

**Q: Is my data sent to external servers?**
A: No, all analysis is performed locally using the Ollama service.

**Q: Can I import data from other systems?**
A: Currently not supported directly, but you can upload files from other systems.

**Q: How accurate is the AI analysis?**
A: The AI provides assistance but should always be verified by qualified medical professionals.

**Q: Can I customize report templates?**
A: Yes, edit the templates in the pdf_export.py file.

**Q: Is there a cloud-hosted version?**
A: Currently FertiVision-CodeLM is designed for local installation only.

---

© 2025 FertiVision-CodeLM | Version 1.0 | Last Updated: June 10, 2025