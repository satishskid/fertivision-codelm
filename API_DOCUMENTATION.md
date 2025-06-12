# 🔌 FertiVision API Documentation

**RESTful API for IVF EMR Integration**

The FertiVision API provides secure, scalable access to AI-powered reproductive medicine analysis capabilities for integration with IVF Electronic Medical Record (EMR) systems.

## 🚀 Quick Start

### Base URL
```
Production: https://api.fertivision.com/api/v1
Development: http://localhost:5003/api/v1
```

### Authentication
All API requests require an API key provided in the request header:
```http
X-API-Key: your_api_key_here
```

### Example Request
```bash
curl -X POST \
  http://localhost:5003/api/v1/analyze/sperm \
  -H 'X-API-Key: fv_demo_key_12345' \
  -F 'image=@sperm_sample.jpg' \
  -F 'patient_id=P12345' \
  -F 'case_id=C001'
```

## 📋 API Endpoints

### Health Check
**GET** `/health`

Check API server status and availability.

**Response:**
```json
{
  "status": "healthy",
  "version": "v1",
  "timestamp": "2025-01-01T12:00:00Z",
  "service": "FertiVision API"
}
```

### API Information
**GET** `/info`

Get client information and available permissions.

**Headers:** `X-API-Key: required`

**Response:**
```json
{
  "success": true,
  "api_version": "v1",
  "client_name": "Demo IVF Clinic",
  "permissions": ["sperm", "oocyte", "embryo", "follicle"],
  "rate_limit": 1000,
  "available_endpoints": {
    "sperm_analysis": "/api/v1/analyze/sperm",
    "oocyte_analysis": "/api/v1/analyze/oocyte",
    "embryo_analysis": "/api/v1/analyze/embryo",
    "follicle_analysis": "/api/v1/analyze/follicle"
  }
}
```

## 🧬 Analysis Endpoints

### Sperm Analysis
**POST** `/analyze/sperm`

Analyze sperm microscopy images according to WHO 2021 criteria.

**Headers:** `X-API-Key: required`

**Form Data:**
- `image` (file, required): Sperm microscopy image
- `patient_id` (string, optional): Patient identifier
- `case_id` (string, optional): Case identifier
- `notes` (string, optional): Analysis notes

**Response:**
```json
{
  "success": true,
  "analysis_id": "uuid-string",
  "analysis_type": "sperm",
  "sample_id": "sample-id",
  "classification": "Normozoospermia",
  "parameters": {
    "concentration": 45.0,
    "progressive_motility": 65.0,
    "normal_morphology": 8.0,
    "volume": 3.0
  },
  "timestamp": "2025-01-01T12:00:00Z",
  "patient_id": "P12345",
  "case_id": "C001",
  "ai_analysis": "Detailed AI analysis text",
  "processing_mode": "mock"
}
```

### Oocyte Analysis
**POST** `/analyze/oocyte`

Analyze oocyte maturity and quality according to ESHRE guidelines.

**Headers:** `X-API-Key: required`

**Form Data:**
- `image` (file, required): Oocyte microscopy image
- `patient_id` (string, optional): Patient identifier
- `case_id` (string, optional): Case identifier
- `notes` (string, optional): Analysis notes

**Response:**
```json
{
  "success": true,
  "analysis_id": "uuid-string",
  "analysis_type": "oocyte",
  "oocyte_id": "oocyte-id",
  "classification": "Metaphase II (MII)",
  "parameters": {
    "maturity": "MII",
    "morphology_score": 8.5
  },
  "timestamp": "2025-01-01T12:00:00Z",
  "patient_id": "P12345",
  "ai_analysis": "Detailed AI analysis text"
}
```

### Embryo Analysis
**POST** `/analyze/embryo`

Analyze embryo development and grading using Gardner criteria.

**Headers:** `X-API-Key: required`

**Form Data:**
- `image` (file, required): Embryo microscopy image
- `day` (integer, optional): Development day (default: 3)
- `patient_id` (string, optional): Patient identifier
- `case_id` (string, optional): Case identifier
- `notes` (string, optional): Analysis notes

**Response:**
```json
{
  "success": true,
  "analysis_id": "uuid-string",
  "analysis_type": "embryo",
  "embryo_id": "embryo-id",
  "classification": "Grade A Embryo",
  "parameters": {
    "day": 3,
    "cell_count": 8,
    "fragmentation": 5.0,
    "grade": "A"
  },
  "timestamp": "2025-01-01T12:00:00Z",
  "patient_id": "P12345",
  "ai_analysis": "Detailed AI analysis text"
}
```

### Follicle Scan Analysis
**POST** `/analyze/follicle`

Analyze ultrasound images for follicle counting and ovarian reserve assessment.

**Headers:** `X-API-Key: required`

**Form Data:**
- `image` (file, required): Ultrasound image
- `patient_id` (string, optional): Patient identifier
- `case_id` (string, optional): Case identifier
- `notes` (string, optional): Analysis notes

**Response:**
```json
{
  "success": true,
  "analysis_id": "uuid-string",
  "analysis_type": "follicle",
  "scan_id": "scan-id",
  "classification": "Normal Ovarian Reserve",
  "parameters": {
    "afc": 12,
    "ovarian_volume": 8.4,
    "largest_follicle": 9.2
  },
  "timestamp": "2025-01-01T12:00:00Z",
  "patient_id": "P12345",
  "ai_analysis": "Detailed AI analysis text"
}
```

### Batch Analysis
**POST** `/analyze/batch`

Process multiple images in a single request for efficient workflow integration.

**Headers:** `X-API-Key: required`

**Form Data:**
- `images` (files, required): Multiple image files
- `analysis_types` (array, required): Analysis type for each image

**Response:**
```json
{
  "success": true,
  "batch_id": "batch-uuid",
  "total_images": 3,
  "results": [
    {
      "analysis_id": "batch-uuid_0",
      "analysis_type": "sperm",
      "filename": "sperm1.jpg",
      "status": "completed",
      "classification": "Normozoospermia"
    },
    {
      "analysis_id": "batch-uuid_1",
      "analysis_type": "embryo",
      "filename": "embryo1.jpg",
      "status": "completed",
      "classification": "Grade A Embryo"
    }
  ],
  "timestamp": "2025-01-01T12:00:00Z"
}
```

## 📊 Report Endpoints

### Get Analysis Report
**GET** `/report/{analysis_id}`

Retrieve detailed analysis report for a specific analysis.

**Headers:** `X-API-Key: required`

**Response:**
```json
{
  "success": true,
  "analysis_id": "uuid-string",
  "report": {
    "summary": "Detailed medical analysis report",
    "recommendations": [
      "Clinical recommendation 1",
      "Clinical recommendation 2"
    ],
    "technical_details": {
      "parameter1": "value1",
      "parameter2": "value2"
    }
  }
}
```

### Export PDF Report
**GET** `/export/pdf/{analysis_id}`

Generate and download PDF report for clinical documentation.

**Headers:** `X-API-Key: required`

**Response:**
```json
{
  "success": true,
  "analysis_id": "uuid-string",
  "pdf_url": "/api/v1/download/pdf/uuid-string",
  "message": "PDF report generation initiated"
}
```

## 🔒 Security & Authentication

### API Key Management
- API keys are provided upon account creation
- Keys should be stored securely and never exposed in client-side code
- Keys can be rotated through the admin panel

### Rate Limiting
- Default: 1000 requests per hour for demo accounts
- Production accounts: 5000+ requests per hour
- Rate limits are enforced per API key
- HTTP 429 status returned when limit exceeded

### Data Security
- All API communications use HTTPS in production
- Images are processed securely and not stored permanently
- Patient data is handled according to HIPAA guidelines
- Audit logs maintained for compliance

## ⚠️ Error Handling

### Error Response Format
```json
{
  "success": false,
  "error": "Error description",
  "code": "ERROR_CODE",
  "timestamp": "2025-01-01T12:00:00Z"
}
```

### Common Error Codes
- `MISSING_API_KEY`: API key not provided
- `INVALID_API_KEY`: API key not valid
- `RATE_LIMIT_EXCEEDED`: Too many requests
- `PERMISSION_DENIED`: Analysis type not permitted
- `MISSING_IMAGE`: No image file provided
- `INVALID_FILE_TYPE`: Unsupported file format
- `ANALYSIS_FAILED`: Internal analysis error

### HTTP Status Codes
- `200`: Success
- `400`: Bad Request (invalid parameters)
- `401`: Unauthorized (invalid API key)
- `403`: Forbidden (insufficient permissions)
- `429`: Too Many Requests (rate limit exceeded)
- `500`: Internal Server Error

## 📝 Supported File Formats

### Image Formats
- **JPEG/JPG**: Standard microscopy images
- **PNG**: High-quality images with transparency
- **TIFF**: Medical imaging standard
- **BMP**: Uncompressed images
- **DICOM**: Medical imaging standard (planned)

### File Size Limits
- Maximum file size: 50MB per image
- Recommended: 1-10MB for optimal processing speed
- Minimum resolution: 512x512 pixels
- Maximum resolution: 4096x4096 pixels

## 🔧 SDK Integration

### Python SDK
```python
from fertivision_sdk import FertiVisionClient

client = FertiVisionClient(api_key="your_api_key")

# Analyze sperm sample
result = client.analyze_sperm("sperm_image.jpg", patient_id="P12345")
print(f"Classification: {result.classification}")
print(f"Concentration: {result.concentration} M/ml")
```

### Installation
```bash
pip install fertivision-sdk
```

## 📞 Support

### Technical Support
- **Email**: api-support@greybrain.ai
- **Documentation**: https://docs.fertivision.com
- **Status Page**: https://status.fertivision.com

### Integration Assistance
- **Consultation**: Schedule integration planning session
- **Custom Development**: Tailored EMR integration solutions
- **Training**: API usage and best practices workshops

---

**© 2025 FertiVision powered by AI | Made by greybrain.ai**

*Advancing reproductive medicine through artificial intelligence*
