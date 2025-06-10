import os
import json
import datetime

def create_complete_project():
    """Create the complete FertiVision-CodeLM project structure"""
    
    # Create all necessary directories
    directories = [
        'templates',
        'static/css',
        'static/js',
        'static/images',
        'uploads',
        'calibration/validation_datasets',
        'docs',
        'tests',
        'scripts'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"📁 Created directory: {directory}")
    
    # Create package.json for project metadata
    package_info = {
        "name": "fertivision-codelm",
        "version": "3.1.0",
        "description": "AI-Enhanced Reproductive Classification System by GreyBrain.ai",
        "main": "app.py",
        "repository": {
            "type": "git",
            "url": "https://github.com/satishskid/fertivision-codelm.git"
        },
        "keywords": [
            "artificial-intelligence",
            "medical-imaging",
            "reproductive-medicine",
            "embryology",
            "computer-vision",
            "deepseek-llm",
            "ivf",
            "sperm-analysis",
            "oocyte-grading",
            "embryo-classification"
        ],
        "author": "GreyBrain.ai",
        "license": "MIT",
        "homepage": "https://github.com/satishskid/fertivision-codelm",
        "bugs": {
            "url": "https://github.com/satishskid/fertivision-codelm/issues"
        }
    }
    
    with open('package.json', 'w') as f:
        json.dump(package_info, f, indent=2)
    
    # Create comprehensive README.md
    readme_content = '''# 🧠 FertiVision-CodeLM | GreyBrain.ai

## AI-Enhanced Reproductive Classification System

[![Version](https://img.shields.io/badge/version-3.1.0-blue.svg)](https://github.com/satishskid/fertivision-codelm)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![AI](https://img.shields.io/badge/AI-DeepSeek%20LLM-purple.svg)](https://deepseek.com)
[![Medical](https://img.shields.io/badge/Medical-ESHRE%20ASRM-red.svg)](https://eshre.eu)

> **Revolutionizing reproductive medicine with AI-powered image analysis**

![FertiVision Banner](https://via.placeholder.com/800x200/667eea/ffffff?text=FertiVision-CodeLM+by+GreyBrain.ai)

## 🌟 Overview

FertiVision-CodeLM is a cutting-edge medical imaging analysis platform that combines traditional ESHRE-ASRM guidelines with advanced AI capabilities. Our system provides automated, accurate, and HIPAA-compliant analysis for reproductive medicine professionals worldwide.

### 🎯 Key Features

- **🔬 Comprehensive Analysis Suite**
  - Sperm Analysis (WHO 2021 compliant)
  - Oocyte Evaluation (ESHRE guidelines)
  - Embryo Grading (Gardner system)
  - Follicle Scanning (AFC assessment)
  - Hysteroscopy Analysis (pathology detection)

- **🤖 AI-Powered Intelligence**
  - Local DeepSeek LLM integration
  - Advanced image preprocessing
  - Pattern recognition algorithms
  - Clinical correlation analysis

- **🏥 Clinical Grade Features**
  - HIPAA compliant (local processing)
  - Professional report generation
  - Accuracy calibration tools
  - Batch processing capabilities

- **💻 Modern Interface**
  - Responsive web-based UI
  - Drag & drop file uploads
  - Real-time progress tracking
  - Mobile-friendly design

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- 4GB+ RAM (8GB recommended)
- Modern web browser

### Installation

1. **Clone Repository**
   ```bash
   git clone https://github.com/satishskid/fertivision-codelm.git
   cd fertivision-codelm
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```bash
   python app.py
   ```

## 📂 Project Structure

- `app.py` - Main application entry point
- `templates/` - HTML templates
- `static/` - CSS, JS, images
- `uploads/` - Uploaded files
- `calibration/` - Calibration and validation datasets
- `docs/` - Documentation
- `tests/` - Unit and integration tests
- `scripts/` - Utility scripts

## 📄 License

This project is licensed under the MIT License.

---

*Made with ❤️ by GreyBrain.ai*
"""
    with open('README.md', 'w') as f:
        f.write(readme_content)

if __name__ == "__main__":
    create_complete_project()
