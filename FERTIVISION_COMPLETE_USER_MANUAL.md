# 📚 FertiVision Complete User Manual

## 📋 **Table of Contents**
1. [Getting Started](#getting-started)
2. [System Overview](#system-overview)
3. [User Interface Guide](#user-interface-guide)
4. [Analysis Features](#analysis-features)
5. [Patient Management](#patient-management)
6. [Document Processing](#document-processing)
7. [Report Generation](#report-generation)
8. [Settings & Configuration](#settings--configuration)
9. [Troubleshooting](#troubleshooting)
10. [Best Practices](#best-practices)

---

## 🚀 **Getting Started**

### **System Requirements**
- **Internet Connection**: Stable broadband connection
- **Browser**: Chrome, Firefox, Safari, or Edge (latest versions)
- **Screen Resolution**: Minimum 1024x768, recommended 1920x1080
- **File Formats**: JPEG, PNG, TIFF for images; PDF for documents

### **Accessing FertiVision**
1. **Open your web browser**
2. **Navigate to**: `https://fertivision-ai-514605543640.us-central1.run.app`
3. **Login with your credentials**:
   - Default Username: `fertivision`
   - Default Password: `fertivision2024`

### **First Time Setup**
1. **Login** to the system
2. **Configure analysis mode** (Local/API)
3. **Set up patient templates** (optional)
4. **Test with sample images** (recommended)

---

## 🔬 **System Overview**

### **What is FertiVision?**
FertiVision is an AI-powered reproductive medicine analysis platform that provides:

- 🧬 **Sperm Analysis**: WHO 2021 compliant sperm parameter assessment
- 🥚 **Oocyte Evaluation**: Maturity and quality grading
- 👶 **Embryo Grading**: Gardner criteria-based embryo assessment
- 🫧 **Follicle Analysis**: Ovarian reserve and follicle counting
- 📋 **Patient Management**: Comprehensive fertility record keeping
- 📊 **Report Generation**: Professional medical reports

### **Key Benefits**
- ⚡ **Instant Results**: Real-time AI analysis
- 🎯 **High Accuracy**: Medical-grade precision
- 📱 **Easy Integration**: Works with existing workflows
- 🔒 **Secure**: HIPAA-compliant data handling
- 💰 **Cost-Effective**: Reduces manual analysis time

---

## 🖥️ **User Interface Guide**

### **Main Dashboard**
The main dashboard provides access to all key features:

#### **Navigation Menu**
- 🏠 **Home**: Main dashboard and quick actions
- 🧬 **Analysis**: Image analysis tools
- 👥 **Patients**: Patient management system
- 📄 **Documents**: Document upload and management
- 📊 **Reports**: Report generation and export
- ⚙️ **Settings**: System configuration

#### **Quick Actions Panel**
- **New Analysis**: Start immediate image analysis
- **Add Patient**: Create new patient record
- **Upload Document**: Process medical documents
- **Generate Report**: Create comprehensive reports

### **Analysis Workspace**
The analysis workspace includes:
- **Image Upload Area**: Drag-and-drop or browse files
- **Analysis Controls**: Select analysis type and parameters
- **Results Panel**: Real-time analysis results
- **History Sidebar**: Previous analyses and quick access

---

## 🧬 **Analysis Features**

### **Sperm Analysis**

#### **How to Perform Sperm Analysis**
1. **Navigate** to the main page
2. **Select "Sperm Analysis"** from the analysis options
3. **Upload Image**: 
   - Click "Choose File" or drag-and-drop
   - Supported formats: JPEG, PNG, TIFF
   - Maximum size: 16MB
4. **Set Parameters**:
   - Patient ID (optional)
   - Clinical notes (optional)
5. **Start Analysis**: Click "Analyze Sample"
6. **Review Results**: Analysis appears in real-time

#### **WHO 2021 Parameters Analyzed**
- **Concentration**: Sperm count per ml
- **Total Motility**: Percentage of moving sperm
- **Progressive Motility**: Forward-moving sperm percentage
- **Normal Morphology**: Normally shaped sperm percentage
- **Vitality**: Live sperm percentage
- **Volume**: Sample volume in ml

#### **Result Interpretation**
```
🟢 Normal (Normozoospermia): All parameters within WHO ranges
🟡 Mild Issues (Oligozoospermia): Slight parameter deviations
🟠 Moderate Issues: Multiple parameters affected
🔴 Severe Issues (Azoospermia): Significant abnormalities
```

### **Oocyte Analysis**

#### **Oocyte Maturity Assessment**
1. **Select "Oocyte Analysis"** from the main page
2. **Upload** high-resolution oocyte image
3. **Review** automated assessment:
   - **GV (Germinal Vesicle)**: Immature oocyte
   - **MI (Metaphase I)**: Partially mature
   - **MII (Metaphase II)**: Fully mature, ready for fertilization

#### **Quality Grading Scale**
- **Grade A**: Excellent quality, high fertilization potential
- **Grade B**: Good quality, suitable for ICSI
- **Grade C**: Fair quality, may require special handling
- **Grade D**: Poor quality, not recommended for use

### **Embryo Analysis**

#### **Gardner Criteria Grading**
FertiVision uses the internationally recognized Gardner criteria:

**Development Stage:**
- **Day 3**: Cell count and fragmentation assessment
- **Day 5/6**: Blastocyst expansion and quality grading

**Input Parameters:**
- **Day of development** (3, 5, or 6)
- **Cell count** (for Day 3 embryos)
- **Fragmentation percentage**
- **Multinucleation** (present/absent)

**Grading Components:**
1. **Expansion Grade** (1-6):
   - 1: Early blastocyst
   - 2: Blastocyst
   - 3: Full blastocyst
   - 4: Expanded blastocyst
   - 5: Hatching blastocyst
   - 6: Hatched blastocyst

2. **Inner Cell Mass (ICM)** Grade:
   - **A**: Many cells, tightly packed
   - **B**: Several cells, loosely grouped
   - **C**: Very few cells

3. **Trophectoderm (TE)** Grade:
   - **A**: Many cells, cohesive epithelium
   - **B**: Few cells, loose epithelium
   - **C**: Very few cells

#### **Transfer Recommendations**
- **Grade 4AA/4AB**: Excellent, first choice for transfer
- **Grade 4BA/4BB**: Good, suitable for transfer
- **Grade 3AA-3BC**: Fair, consider culture extension
- **Grade 1-2**: Poor, extended culture recommended

### **Follicle Analysis**

#### **Ovarian Reserve Assessment**
1. **Select "Follicle Analysis"** from options
2. **Upload** ultrasound images of ovaries
3. **Automated counting** of antral follicles
4. **Size classification**:
   - Small follicles: 2-5mm
   - Medium follicles: 6-9mm
   - Large follicles: >10mm

#### **AFC (Antral Follicle Count) Interpretation**
- **>20 follicles**: Excellent ovarian reserve
- **10-20 follicles**: Good ovarian reserve
- **5-9 follicles**: Fair ovarian reserve
- **<5 follicles**: Poor ovarian reserve

---

## 👥 **Patient Management**

### **Creating New Patients**
1. **Navigate** to "Patient History" in the menu
2. **Click "Add New Patient"**
3. **Enter Patient Information**:
   - Full name
   - Age or Date of birth
   - Gender
   - Medical record number
4. **Save** patient record

### **Patient Dashboard**
Each patient has a comprehensive dashboard showing:
- **Demographics**: Basic patient information
- **Analysis History**: All performed analyses
- **Documents**: Uploaded medical documents
- **Fertility Score**: Calculated fertility assessment (0-10)
- **Treatment Timeline**: Chronological treatment view

### **Fertility Scoring System**
FertiVision calculates an overall fertility score based on:
- **Ovarian Reserve** (25%): AMH, FSH, AFC
- **Tubal Patency** (20%): HSG, laparoscopy results
- **Hormonal Profile** (20%): LH, FSH, thyroid function
- **Partner Factors** (20%): Sperm parameters
- **Age Factor** (15%): Age-related fertility decline

---

## 📄 **Document Processing**

### **Supported Document Types**
- **Hormonal Reports**: FSH, LH, AMH, Estradiol levels
- **Ultrasound Reports**: Ovarian and uterine assessments
- **Semen Analysis**: Laboratory sperm reports
- **Genetic Reports**: Karyotype and genetic testing
- **Surgical Reports**: Laparoscopy, hysteroscopy notes

### **Document Upload Process**
1. **Navigate** to "Document Upload" section
2. **Select Patient**: Choose existing patient
3. **Choose Document Type**: Select appropriate category
4. **Upload File**: 
   - Drag-and-drop or browse files
   - Supported formats: PDF, JPG, PNG
   - Maximum size: 50MB
5. **AI Processing**: Automatic analysis begins
6. **Review Results**: Key findings extracted and summarized

### **AI Document Analysis Features**
- **Text Extraction**: OCR for scanned documents
- **Value Recognition**: Automatic numerical value extraction
- **Reference Ranges**: Comparison with normal values
- **Clinical Significance**: AI-generated interpretations
- **Trend Analysis**: Historical value comparisons

---

## 📊 **Report Generation**

### **Analysis Reports**
Each analysis generates a comprehensive report:

#### **Executive Summary**
- Patient identification
- Analysis type and date
- Overall assessment and grade
- Key findings highlight

#### **Detailed Results**
- Complete parameter measurements
- Reference range comparisons
- Quality scores and confidence levels
- AI analysis comments

#### **Clinical Recommendations**
- Treatment suggestions
- Follow-up recommendations
- Additional testing suggestions
- Prognostic indicators

### **Fertility Assessment Reports**
Comprehensive evaluations include:
- **Overall Fertility Score**: Numerical assessment (0-10)
- **Factor Breakdown**: Detailed component analysis
- **Treatment Options**: Personalized recommendations
- **Success Predictions**: Evidence-based prognosis

### **Report Export Options**
- **PDF**: Professional medical report format
- **Print**: Direct printing capability
- **Share**: Email or secure sharing options

---

## ⚙️ **Settings & Configuration**

### **Analysis Mode Selection**
Choose between different analysis modes:

#### **Local Mode (Default)**
- Uses local AI models (Ollama)
- No internet required for analysis
- Free and private
- Good accuracy for most cases

#### **API Mode (Enhanced)**
- Uses cloud-based AI models
- Requires API keys (Groq, OpenRouter)
- Higher accuracy and speed
- Requires internet connection

### **API Key Configuration**
1. **Navigate** to Settings → API Configuration
2. **Add API Keys**:
   - **Groq**: Fast, accurate analysis
   - **OpenRouter**: Multiple model access
3. **Test Connection**: Verify functionality
4. **Switch Mode**: Choose between Local/API

### **Quality Thresholds**
Configure minimum requirements:
- **Image Quality**: Resolution and clarity standards
- **Analysis Confidence**: Minimum AI confidence level
- **Automatic Retry**: Failed analysis retry attempts

---

## 🔧 **Troubleshooting**

### **Common Issues**

#### **Login Problems**
**Problem**: Cannot access the system
**Solutions**:
1. Verify internet connection
2. Check browser compatibility (use Chrome/Firefox)
3. Clear browser cache and cookies
4. Try incognito/private browsing mode
5. Verify correct URL

#### **Image Upload Issues**
**Problem**: Images won't upload
**Solutions**:
1. Check file format (JPEG, PNG, TIFF only)
2. Verify file size (<16MB)
3. Ensure stable internet connection
4. Try different browser
5. Compress large images

#### **Analysis Failures**
**Problem**: Analysis doesn't complete
**Solutions**:
1. Check image quality and clarity
2. Verify sufficient lighting in image
3. Ensure proper magnification
4. Retry with different image
5. Switch analysis mode (Local ↔ API)

#### **Slow Performance**
**Problem**: System responds slowly
**Solutions**:
1. Check internet connection speed
2. Close unnecessary browser tabs
3. Clear browser cache
4. Restart browser
5. Try during off-peak hours

### **Error Messages**

#### **"Analysis Failed: Insufficient Image Quality"**
- **Cause**: Image too dark, blurry, or low resolution
- **Solution**: Retake image with better lighting and focus

#### **"Authentication Required"**
- **Cause**: Not logged in or session expired
- **Solution**: Login with credentials (fertivision/fertivision2024)

#### **"File Too Large"**
- **Cause**: Upload file exceeds size limit
- **Solution**: Compress image or reduce file size

---

## 💡 **Best Practices**

### **Image Capture Guidelines**

#### **For Sperm Analysis**
- **Magnification**: 400x minimum
- **Focus**: Sharp, clear sperm visibility
- **Lighting**: Even, bright illumination
- **Background**: Clean, uniform background
- **Sample**: Representative field selection

#### **For Oocyte Analysis**
- **Magnification**: 200-400x
- **Contrast**: High contrast for structure visibility
- **Centering**: Oocyte centered in frame
- **Debris**: Minimal background debris
- **Quality**: High-resolution capture

#### **For Embryo Analysis**
- **Time Point**: Appropriate development stage
- **Focus**: All cells in focus plane
- **Lighting**: Consistent illumination
- **Documentation**: Record development day and time

### **Workflow Optimization**

#### **Daily Workflow**
1. **Morning Setup**: Check system status
2. **Sample Processing**: Batch similar analyses
3. **Quality Review**: Validate results
4. **Documentation**: Complete records same day
5. **Report Generation**: Create daily summaries

#### **Data Security**
- **Regular Backups**: Export important data
- **Access Control**: Use secure passwords
- **Patient Privacy**: Follow HIPAA guidelines
- **Session Management**: Logout when finished

---

## 📈 **Advanced Features**

### **Custom Analysis Parameters**
- **Quality Thresholds**: Set minimum standards
- **Confidence Levels**: Adjust AI sensitivity
- **Report Templates**: Customize output formats
- **Integration Settings**: Connect with EMR systems

### **Data Analytics**
- **Trend Analysis**: Track clinic performance
- **Quality Metrics**: Monitor analysis accuracy
- **Usage Statistics**: Review system utilization
- **Performance Reports**: Generate summaries

---

## 📞 **Support & Resources**

### **Getting Help**
- **User Manual**: This comprehensive guide
- **Technical Support**: Contact system administrator
- **FAQ Section**: Common questions and answers
- **Updates**: Regular system improvements

### **Training Resources**
- **Video Tutorials**: Step-by-step demonstrations
- **Best Practices**: Clinical workflow optimization
- **Case Studies**: Real-world usage examples
- **Certification**: User training programs

### **System Information**
- **Version**: 1.0.0
- **Last Updated**: July 23, 2025
- **Support**: Available during business hours
- **Documentation**: Regularly updated

---

## 🎯 **Quick Reference**

### **Common Tasks**
- **New Analysis**: Main page → Select type → Upload image → Analyze
- **Add Patient**: Patient History → Add New Patient → Enter details → Save
- **Upload Document**: Select patient → Upload document → Choose type → Process
- **Generate Report**: Complete analysis → View results → Export/Print
- **Switch Mode**: Settings → Analysis Mode → Select Local/API → Apply

### **File Requirements**
- **Images**: JPEG, PNG, TIFF (max 16MB)
- **Documents**: PDF, DOC (max 50MB)
- **Resolution**: Minimum 640x480, recommended 1920x1080
- **Quality**: Clear, well-lit, properly focused

### **Key URLs**
- **Main Application**: https://fertivision-ai-514605543640.us-central1.run.app
- **Health Check**: https://fertivision-ai-514605543640.us-central1.run.app/health
- **System Status**: Available in main interface

---

**© 2025 FertiVision powered by AI | Complete User Manual**

*This manual provides comprehensive guidance for using FertiVision AI-enhanced reproductive medicine analysis system. For additional support, contact your system administrator.*

**Version**: 1.0  
**Last Updated**: July 23, 2025
