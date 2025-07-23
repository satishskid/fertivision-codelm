# 🔬 FertiVision API Documentation - Complete Reference

## 📋 **Table of Contents**
1. [API Overview](#api-overview)
2. [Authentication](#authentication)
3. [Base URLs](#base-urls)
4. [Request/Response Format](#requestresponse-format)
5. [Health & Status Endpoints](#health--status-endpoints)
6. [Analysis Endpoints](#analysis-endpoints)
7. [Patient Management](#patient-management)
8. [Document Management](#document-management)
9. [Report Generation](#report-generation)
10. [Model Configuration](#model-configuration)
11. [Error Handling](#error-handling)
12. [Rate Limiting](#rate-limiting)
13. [SDK Examples](#sdk-examples)
14. [IVF EMR Integration](#ivf-emr-integration)

---

## 🚀 **API Overview**

FertiVision API provides RESTful endpoints for integrating AI-powered reproductive medicine analysis into IVF clinic workflows and EMR systems.

### **Key Features**
- 🧬 **Multi-modal Analysis**: Sperm, oocyte, embryo, follicle analysis
- 🔐 **Secure Authentication**: API key-based authentication
- 📊 **Real-time Results**: Instant AI analysis with confidence scores
- 📋 **Patient Management**: Complete patient record management
- 📄 **Document Processing**: Medical document analysis and storage
- 📈 **Report Generation**: Comprehensive fertility reports
- 🔄 **Batch Processing**: Multiple image analysis in single request
- 📱 **EMR Integration**: Standard medical data exchange formats

---

## 🔐 **Authentication**

All API endpoints (except health checks) require authentication using API keys.

### **API Key Header**
```http
X-API-Key: your_api_key_here
```

### **Demo API Key**
```
fv_demo_key_12345
```

### **Production API Keys**
Contact your FertiVision administrator for production API keys.

---

## 🌐 **Base URLs**

### **Production**
```
https://fertivision-ai-514605543640.us-central1.run.app
```

### **API Endpoints Base**
```
https://fertivision-ai-514605543640.us-central1.run.app/api/v1
```

---

## 📝 **Request/Response Format**

### **Content Types**
- **JSON**: `application/json`
- **Form Data**: `multipart/form-data` (for file uploads)
- **Images**: `image/jpeg`, `image/png`, `image/tiff`

### **Standard Response Format**
```json
{
  "success": true,
  "data": { ... },
  "timestamp": "2025-07-23T07:00:00.000Z",
  "processing_time_ms": 1250
}
```

### **Error Response Format**
```json
{
  "success": false,
  "error": "Error description",
  "code": "ERROR_CODE",
  "timestamp": "2025-07-23T07:00:00.000Z"
}
```

---

## 🏥 **Health & Status Endpoints**

### **GET /health**
Check API health status (no authentication required).

**Response:**
```json
{
  "status": "healthy",
  "service": "FertiVision",
  "timestamp": "2025-07-23T07:00:00.000Z",
  "version": "1.0.0",
  "environment": "production",
  "components": {
    "flask": "operational",
    "file_system": "operational",
    "uploads_directory": "operational",
    "model_config": "operational",
    "database": "operational"
  }
}
```

### **GET /ready**
Check deployment readiness (no authentication required).

**Response:**
```json
{
  "status": "ready",
  "components": {
    "uploads": "ready",
    "config": "ready"
  },
  "timestamp": "2025-07-23T07:09:06.753620"
}
```

---

## 🧬 **Analysis Endpoints**

### **POST /analyze_image/{analysis_type}**
Analyze medical images with AI.

**Supported Analysis Types:**
- `sperm` - Sperm morphology and motility analysis
- `oocyte` - Oocyte maturity assessment
- `embryo` - Embryo grading and quality evaluation
- `follicle` - Follicle counting and ovarian assessment

**Parameters:**
- `image` (file): Medical image file
- `patient_id` (optional): Patient identifier
- `notes` (optional): Clinical notes

**Example Request:**
```bash
curl -X POST \
  -H "X-API-Key: fv_demo_key_12345" \
  -F "image=@sperm_sample.jpg" \
  -F "patient_id=P12345" \
  -F "notes=Pre-IVF analysis" \
  https://fertivision-ai-514605543640.us-central1.run.app/analyze_image/sperm
```

**Response:**
```json
{
  "success": true,
  "analysis_id": "SA_20250723_001",
  "classification": "Normal morphology detected",
  "confidence": 0.94,
  "image_analysis": "AI analysis completed successfully",
  "details": {
    "findings": {
      "total_count": 45,
      "motile_count": 38,
      "progressive_motility": 84.4,
      "morphology_normal": 89.2,
      "concentration": "25.2 million/ml"
    },
    "timestamp": "2025-07-23T07:15:30.123456",
    "analysis_type": "sperm"
  }
}
```

### **POST /analyze_sperm**
Dedicated sperm analysis endpoint.

**WHO 2021 Parameters Analyzed:**
- Concentration (million/ml)
- Total motility (%)
- Progressive motility (%)
- Normal morphology (%)
- Vitality (%)
- Volume (ml)

**Response Example:**
```json
{
  "success": true,
  "classification": "Normozoospermia",
  "sperm_id": "SP_20250723_001",
  "details": {
    "who_parameters": {
      "concentration": 25.2,
      "total_motility": 68.0,
      "progressive_motility": 55.0,
      "normal_morphology": 89.0,
      "vitality": 82.0,
      "volume": 3.5
    },
    "who_classification": "Normal",
    "clinical_significance": "Parameters within WHO 2021 normal ranges"
  }
}
```

### **POST /analyze_oocyte**
Oocyte maturity and quality assessment.

**Analysis Parameters:**
- Maturity stage (GV, MI, MII)
- Cytoplasm quality
- Zona pellucida integrity
- Polar body presence
- Overall viability score

**Response Example:**
```json
{
  "success": true,
  "classification": "Mature Oocyte (MII)",
  "oocyte_id": "OO_20250723_001",
  "details": {
    "maturity_stage": "MII",
    "quality_score": 8.5,
    "cytoplasm_quality": "Excellent",
    "zona_pellucida": "Intact",
    "polar_body": "Present",
    "fertilization_potential": "High"
  }
}
```

### **POST /analyze_embryo**
Embryo grading using Gardner criteria.

**Analysis Parameters:**
- Development stage (Day 3, Day 5, Day 6)
- Cell count and division quality
- Fragmentation percentage
- Blastocyst expansion
- Inner cell mass grade
- Trophectoderm grade

**Request:**
```json
{
  "day": 5,
  "cell_count": 8,
  "fragmentation": 5.0,
  "multinucleation": false
}
```

**Response Example:**
```json
{
  "success": true,
  "classification": "Good Quality Blastocyst",
  "embryo_id": "EM_20250723_001",
  "details": {
    "gardner_grade": "4AA",
    "expansion_grade": 4,
    "icm_grade": "A",
    "te_grade": "A",
    "quality_assessment": "Excellent",
    "implantation_potential": "High",
    "transfer_recommendation": "First choice for transfer"
  }
}
```

---

## 👥 **Patient Management**

### **GET /api/patients**
Get all patients (requires authentication).

**Response:**
```json
{
  "success": true,
  "patients": [
    {
      "patient_id": "P12345",
      "name": "Sarah Johnson",
      "age": 32,
      "gender": "Female",
      "medical_record_number": "MRN-2025-001",
      "fertility_score": 7.8,
      "document_count": 5,
      "last_updated": "2025-07-23T07:00:00Z"
    }
  ]
}
```

### **POST /api/patients**
Create a new patient.

**Request:**
```json
{
  "name": "Sarah Johnson",
  "age": 32,
  "gender": "Female",
  "medical_record_number": "MRN-2025-001"
}
```

**Response:**
```json
{
  "success": true,
  "patient_id": "P12345",
  "message": "Patient created successfully"
}
```

### **GET /api/patients/{patient_id}**
Get detailed patient information.

**Response:**
```json
{
  "success": true,
  "patient": {
    "patient_id": "P12345",
    "name": "Sarah Johnson",
    "age": 32,
    "gender": "Female",
    "medical_record_number": "MRN-2025-001",
    "fertility_score": 7.8,
    "fertility_breakdown": {
      "ovarian_reserve": 8.2,
      "tubal_patency": 9.0,
      "hormonal_profile": 7.5,
      "partner_factors": 6.8
    },
    "documents": [
      {
        "document_id": "DOC_001",
        "document_type": "hormonal_report",
        "key_findings": ["FSH: 6.8 mIU/ml", "AMH: 3.2 ng/ml"],
        "confidence_score": 0.92,
        "analysis_date": "2025-07-20T10:30:00Z"
      }
    ]
  }
}
```

---

## 📄 **Document Management**

### **POST /api/patients/{patient_id}/documents**
Upload and analyze patient documents.

**Supported Document Types:**
- `hormonal_report` - Hormone level reports
- `ultrasound_report` - Ultrasound findings
- `semen_analysis` - Male fertility reports
- `genetic_report` - Genetic testing results
- `surgical_report` - Surgical procedure notes

**Request:**
```bash
curl -X POST \
  -H "X-API-Key: fv_demo_key_12345" \
  -F "file=@hormone_report.pdf" \
  -F "document_type=hormonal_report" \
  -F "patient_id=P12345" \
  https://fertivision-ai-514605543640.us-central1.run.app/api/patients/P12345/documents
```

**Response:**
```json
{
  "success": true,
  "document_id": "DOC_20250723_001",
  "message": "Document uploaded and analyzed successfully",
  "analysis": {
    "key_findings": [
      "FSH: 6.8 mIU/ml (Normal)",
      "AMH: 3.2 ng/ml (Good ovarian reserve)",
      "Estradiol: 45 pg/ml (Follicular phase)"
    ],
    "confidence_score": 0.94,
    "ai_summary": "Hormonal profile indicates good ovarian reserve with normal FSH levels suitable for IVF treatment."
  }
}
```

---

## 📊 **Report Generation**

### **GET /report/{analysis_type}/{analysis_id}**
Generate analysis reports.

**Response:**
```json
{
  "report": {
    "patient_info": {
      "id": "P12345",
      "analysis_date": "2025-07-23"
    },
    "analysis_summary": {
      "type": "sperm_analysis",
      "classification": "Normozoospermia",
      "confidence": 0.94
    },
    "clinical_findings": [
      "Sperm concentration: 25.2 million/ml (Normal)",
      "Progressive motility: 55% (Normal)",
      "Normal morphology: 89% (Excellent)"
    ],
    "recommendations": [
      "Parameters are within normal WHO 2021 ranges",
      "Suitable for natural conception or IVF",
      "Consider lifestyle optimization for continued health"
    ]
  }
}
```

### **GET /api/patients/{patient_id}/fertility_report**
Generate comprehensive fertility reports.

**Response:**
```json
{
  "success": true,
  "fertility_report": {
    "patient_summary": {
      "name": "Sarah Johnson",
      "age": 32,
      "overall_fertility_score": 7.8
    },
    "assessment_breakdown": {
      "ovarian_reserve": {
        "score": 8.2,
        "status": "Good",
        "key_indicators": ["AMH: 3.2 ng/ml", "AFC: 12 follicles"]
      },
      "hormonal_profile": {
        "score": 7.5,
        "status": "Normal",
        "key_indicators": ["FSH: 6.8 mIU/ml", "LH: 4.2 mIU/ml"]
      }
    },
    "treatment_recommendations": [
      "Good candidate for IVF treatment",
      "Consider ovarian stimulation protocol",
      "Monitor follicle development closely"
    ]
  }
}
```

---

## 🔧 **Model Configuration**

### **GET /api/model_config**
Get current AI model configuration.

**Response:**
```json
{
  "sperm": {
    "primary_model": {
      "provider": "ollama_local",
      "model_name": "llava:7b",
      "enabled": true,
      "cost_per_1k_tokens": 0.0,
      "temperature": 0.1
    },
    "fallback_models": [
      {
        "provider": "groq",
        "model_name": "llama-3.2-90b-vision-preview",
        "enabled": false,
        "cost_per_1k_tokens": 0.59
      }
    ],
    "quality_threshold": 0.8,
    "max_retries": 3
  }
}
```

### **POST /api/switch_mode**
Switch between local and API analysis modes.

**Request:**
```json
{
  "mode": "api"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Switched to API Mode - Enhanced accuracy with cloud models",
  "mode": "api",
  "current_model": "llama-3.2-90b-vision-preview",
  "provider": "Groq"
}
```

---

## ❌ **Error Handling**

### **Common Error Codes**
- `MISSING_API_KEY` (401): API key not provided
- `INVALID_API_KEY` (401): Invalid or expired API key
- `DEACTIVATED_KEY` (401): API key has been deactivated
- `RATE_LIMIT_EXCEEDED` (429): Too many requests
- `FILE_TOO_LARGE` (413): Upload file exceeds size limit
- `UNSUPPORTED_FORMAT` (400): Unsupported file format
- `ANALYSIS_FAILED` (500): Analysis processing error
- `PATIENT_NOT_FOUND` (404): Patient record not found

### **Error Response Example**
```json
{
  "success": false,
  "error": "File size exceeds maximum allowed size of 16MB",
  "code": "FILE_TOO_LARGE",
  "timestamp": "2025-07-23T07:00:00.000Z",
  "request_id": "req_abc123def456"
}
```

---

## 🚦 **Rate Limiting**

### **Rate Limits by API Key Type**
- **Demo Key**: 100 requests/hour
- **Basic Plan**: 1,000 requests/hour
- **Professional Plan**: 5,000 requests/hour
- **Enterprise Plan**: Unlimited

### **Rate Limit Headers**
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 995
X-RateLimit-Reset: 1642694400
```

---

## 🔌 **SDK Examples**

### **Python SDK**
```python
from fertivision_sdk import FertiVisionClient

# Initialize client
client = FertiVisionClient(
    api_key="your_api_key",
    base_url="https://fertivision-ai-514605543640.us-central1.run.app"
)

# Analyze sperm sample
result = client.analyze_sperm(
    image_path="sperm_sample.jpg",
    patient_id="P12345",
    notes="Pre-IVF analysis"
)

print(f"Classification: {result.classification}")
print(f"Confidence: {result.confidence}")
print(f"WHO Parameters: {result.who_parameters}")
```

### **JavaScript SDK**
```javascript
const FertiVision = require('fertivision-sdk');

const client = new FertiVision({
    apiKey: 'your_api_key',
    baseUrl: 'https://fertivision-ai-514605543640.us-central1.run.app'
});

// Analyze embryo
const result = await client.analyzeEmbryo({
    imagePath: 'embryo_day5.jpg',
    patientId: 'P12345',
    day: 5,
    notes: 'Day 5 blastocyst assessment'
});

console.log('Gardner Grade:', result.gardner_grade);
console.log('Quality:', result.quality_assessment);
```

---

## 🏥 **IVF EMR Integration**

### **FHIR Compatibility**
FertiVision API supports FHIR R4 standard for medical data exchange.

### **EMR Integration Points**
1. **Patient Registration**: Sync patient demographics
2. **Order Management**: Automated analysis requests
3. **Results Delivery**: Direct results integration
4. **Quality Assurance**: Audit trails and validation
5. **Billing Integration**: Usage tracking and billing codes

### **Sample EMR Integration**
```python
import requests
from datetime import datetime

class EMRIntegration:
    def __init__(self, emr_system, fertivision_api):
        self.emr = emr_system
        self.fertivision = fertivision_api
    
    def process_analysis_order(self, order_id):
        # Get order from EMR
        order = self.emr.get_order(order_id)
        
        # Analyze with FertiVision
        result = self.fertivision.analyze_image(
            image_path=order.image_path,
            analysis_type=order.analysis_type,
            patient_id=order.patient_id
        )
        
        # Send results back to EMR
        self.emr.update_order_results(
            order_id=order_id,
            results=result,
            completed_date=datetime.now()
        )
        
        return result
```

---

## 📋 **API Testing**

### **Health Check Test**
```bash
curl https://fertivision-ai-514605543640.us-central1.run.app/health
```

### **Authentication Test**
```bash
curl -H "X-API-Key: fv_demo_key_12345" \
     https://fertivision-ai-514605543640.us-central1.run.app/api/model_config
```

### **Image Analysis Test**
```bash
curl -X POST \
  -H "X-API-Key: fv_demo_key_12345" \
  -F "image=@test_sample.jpg" \
  -F "patient_id=TEST_001" \
  https://fertivision-ai-514605543640.us-central1.run.app/analyze_image/sperm
```

---

## 📞 **Support & Resources**

### **API Support**
- **Email**: api-support@fertivision.ai
- **Documentation**: Complete guides available
- **Status Page**: Real-time API status monitoring

### **Rate Limiting**
- **Free Tier**: 2M requests/month
- **Paid Plans**: Custom limits available
- **Enterprise**: Dedicated instances

### **SLA Guarantees**
- **Uptime**: 99.9% availability
- **Response Time**: <2 seconds average
- **Support**: 24/7 technical support

---

**© 2025 FertiVision powered by AI | Complete API Documentation**

*This documentation covers all available API endpoints and integration patterns for FertiVision AI-enhanced reproductive medicine analysis system.*
