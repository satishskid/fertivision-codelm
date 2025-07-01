# Patient History & Document Analysis System

## Overview

The FertiVision Patient History & Document Analysis System provides comprehensive fertility assessment and medical document management capabilities. It allows healthcare providers to:

- Manage patient demographics and medical records
- Upload and analyze medical documents (PDFs, images, lab reports)
- Generate AI-powered fertility assessments
- Export comprehensive fertility reports as PDF documents

## Features

### 1. Patient Management
- **Create Patient Records**: Add new patients with demographic information
- **Patient Demographics**: Store name, date of birth, gender, contact information
- **Medical Record Numbers**: Automatic or manual medical ID assignment
- **Patient History**: Track all interactions and document uploads

### 2. Document Upload & Analysis
- **Supported Formats**: PDF, JPG, PNG, TIFF files (up to 10MB)
- **Document Types**:
  - Lab Reports
  - Ultrasound Images
  - Microscopy Images
  - Medical Reports
  - Prescriptions
  - Consultation Notes
  - Surgical Reports
  - Imaging Studies
  - Pathology Reports
  - Hormone Panels

### 3. AI-Powered Analysis
- **Text Extraction**: Automatic text extraction from PDFs and images
- **Key Findings**: AI identification of important clinical findings
- **Numerical Values**: Extraction of lab values and measurements
- **Confidence Scoring**: Analysis confidence assessment
- **DeepSeek Integration**: Advanced AI model for medical document analysis

### 4. Fertility Scoring System
- **Overall Fertility Score**: Comprehensive 0-100 fertility assessment
- **Domain-Specific Scoring**:
  - Male Factor Analysis
  - Female Factor Analysis
  - Ovarian Function Assessment
  - Tubal Factor Evaluation
  - Uterine Factor Analysis
  - Hormonal Balance Assessment
  - Genetic Factor Considerations
  - Lifestyle Factor Impact

### 5. Report Generation
- **Comprehensive Reports**: Detailed fertility assessment reports
- **PDF Export**: Professional PDF reports for clinical use
- **Clinical Recommendations**: AI-generated recommendations based on findings
- **Visual Charts**: Score breakdowns and trends visualization

## Getting Started

### 1. Access the System
- Navigate to the main FertiVision dashboard
- Click on the "Patient History" tab
- Or directly access: `http://localhost:5000/patient_history`

### 2. Create a Patient
1. Go to the "Patient Management" tab
2. Fill in the patient information form:
   - Patient Name (required)
   - Date of Birth (required)
   - Gender (required)
   - Contact Number (optional)
   - Email (optional)
   - Medical ID (optional - auto-generated if not provided)
3. Click "Create Patient"

### 3. Upload Documents
1. Go to the "Document Upload" tab
2. Select the patient from the dropdown
3. Choose the document type
4. Drag and drop files or click to browse
5. Click "Upload & Analyze Documents"

### 4. View Analysis Results
1. Go to the "Analysis & Reports" tab
2. Select a patient to view their fertility analysis
3. Review the overall fertility score and domain breakdowns
4. Examine uploaded documents and their analysis results

### 5. Export Reports
1. Select a patient in the "Analysis & Reports" tab
2. Click "Export PDF Report"
3. The comprehensive fertility report will be downloaded

## API Documentation

### Patient Management

#### Create Patient
```bash
POST /api/patients
Content-Type: application/json

{
  "name": "Patient Name",
  "date_of_birth": "1985-06-15",
  "gender": "male|female|other",
  "contact_number": "+1-555-0123",
  "email": "patient@example.com",
  "medical_id": "MED001"
}
```

#### Get All Patients
```bash
GET /api/patients
```

#### Get Patient Details
```bash
GET /api/patients/{patient_id}
```

### Document Management

#### Upload Document
```bash
POST /api/patients/{patient_id}/documents
Content-Type: multipart/form-data

file: [binary file data]
document_type: "lab_report|ultrasound_image|medical_report|..."
```

### Report Generation

#### Get Fertility Report
```bash
GET /api/patients/{patient_id}/fertility_report
```

#### Export PDF Report
```bash
GET /api/patients/{patient_id}/export_report
```

## Configuration

### Analysis Modes
- **DEMO**: Demo mode with mock data
- **DEEPSEEK**: AI-powered analysis using DeepSeek/Ollama
- **MOCK**: Mock analysis for testing

### File Upload Limits
- Maximum file size: 10MB
- Supported formats: PDF, JPG, JPEG, PNG, TIFF, TIF
- Storage location: `uploads/` directory

### Database
- SQLite database: `reproductive_analysis.db`
- Automatic schema creation on first run
- Patient and document data persistence

## AI Analysis Details

### Document Processing
1. **Text Extraction**: OCR for images, direct text for PDFs
2. **Content Analysis**: AI analysis of extracted text and images
3. **Key Findings Extraction**: Important clinical findings identification
4. **Numerical Values**: Lab values and measurements extraction
5. **Confidence Assessment**: Analysis reliability scoring

### Fertility Scoring Algorithm
The fertility scoring system evaluates multiple domains:

- **Male Factor (0-100)**: Sperm analysis, hormonal factors
- **Female Factor (0-100)**: Ovarian reserve, uterine factors
- **Ovarian Function (0-100)**: Hormone levels, imaging findings
- **Tubal Factor (0-100)**: Fallopian tube assessment
- **Uterine Factor (0-100)**: Uterine morphology and function
- **Hormonal Balance (0-100)**: Reproductive hormone levels
- **Genetic Factors (0-100)**: Genetic testing results
- **Lifestyle Factors (0-100)**: BMI, smoking, exercise, diet

The overall fertility score is calculated as a weighted average of domain scores.

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all required dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **Database Issues**: Delete and recreate the database file
   ```bash
   rm reproductive_analysis.db
   ```

3. **File Upload Errors**: Check file size and format restrictions

4. **AI Analysis Not Working**: Verify DeepSeek/Ollama installation and configuration

### Debug Mode
Start the application in debug mode:
```bash
python app.py
```

### Log Files
Check the application logs for detailed error information.

## Security Considerations

- **File Validation**: All uploaded files are validated for type and size
- **Authentication**: Basic authentication system (enhance for production)
- **Data Privacy**: Patient data is stored locally in SQLite database
- **File Storage**: Uploaded files are stored in secure upload directory

## Future Enhancements

- **Multi-user Support**: Role-based access control
- **Cloud Storage**: Integration with cloud storage services
- **Advanced AI Models**: Integration with specialized medical AI models
- **Telemedicine Integration**: Video consultation features
- **Mobile App**: Mobile application for document upload
- **DICOM Support**: Medical imaging standard support
- **HL7 Integration**: Healthcare data exchange standards

## Support

For technical support or feature requests, please refer to the project documentation or contact the development team.

---

*This document is part of the FertiVision AI-Enhanced Reproductive Medicine System.*
