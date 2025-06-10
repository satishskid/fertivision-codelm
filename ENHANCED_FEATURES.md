# FertiVision-CodeLM Enhanced Features Documentation

## New Features Added

### 1. Extended File Format Support
The system now supports a wider range of file formats beyond standard images:

- **Standard Images**: png, jpg, jpeg, tiff, bmp, gif, webp
- **Medical Formats**: DICOM (dcm, dcm30, ima), NIfTI (nii, nii.gz)
- **Video Formats**: mp4, avi, mov, mkv, wmv (for time-lapse embryology)

File size limits are customized based on file type:
- Images: 50MB
- Videos: 500MB
- Medical Files: 100MB

### 2. Medical Discipline Detection
The system automatically detects the appropriate medical discipline based on file names and formats:

- **Embryology**: embryo images, blastocyst development, time-lapse videos
- **Andrology**: sperm analysis, motility videos, morphology assessments
- **Reproductive Endocrinology**: follicle scans, ovarian imaging, ultrasounds
- **Gynecology**: hysteroscopy images/videos, cervical and uterine imaging
- **Radiology**: DICOM files, medical imaging formats

### 3. PDF Export Functionality
Generate professional medical reports in PDF format:

- **Export Types**: Individual analysis reports or batch reports
- **Customized Templates**: Different templates for each analysis type
- **Professional Formatting**: Medical-grade report layout with tables, images, and analysis

To export a PDF:
- Navigate to a completed analysis
- Use the "Export to PDF" button
- Files are saved to the "exports" folder

### 4. Authentication System
Basic authentication for protecting sensitive medical data:

- **Username/Password**: Default credentials (doctor/fertility2025)
- **Session Management**: 1-hour timeout with automatic logout
- **Configuration**: Enable/disable via Config.ENABLE_AUTH
- **Route Protection**: Protected routes with @auth.require_auth decorator

### 5. DeepSeek/Ollama Integration
AI-powered analysis using DeepSeek models via Ollama:

- **Local Processing**: Processing images locally without sending to external APIs
- **Mock Mode**: Testing without AI for development and demonstrations
- **Mode Switching**: Easy toggle between mock and AI modes

To switch modes:
- Run the `toggle_analysis_mode.sh` script
- Or update `ANALYSIS_MODE` in the config.py file

## Usage Examples

### Example 1: Analyzing a DICOM follicle scan
```python
from config import Config, MedicalDiscipline

# File will be automatically detected as reproductive endocrinology
discipline = Config.get_discipline_for_file("follicle_scan.dcm")
print(f"Detected discipline: {discipline.value}")

# Generate PDF report after analysis
pdf_path = pdf_generator.generate_follicle_report(analysis_data)
```

### Example 2: Setting authentication for a route
```python
@app.route('/secure_report/<analysis_id>')
@auth.require_auth
def secure_report(analysis_id):
    # Only authenticated users can access this route
    return generate_sensitive_report(analysis_id)
```

## Configuration

All system settings can be customized in `config.py`:

- Set default analysis mode (MOCK or DEEPSEEK)
- Configure authentication settings
- Adjust file size limits
- Customize supported file formats
- Set PDF export options

## Troubleshooting

1. **AI Analysis Not Working**: 
   - Ensure Ollama is running (`ollama serve`)
   - Check if DeepSeek model is installed (`ollama list`)
   - Try toggling to MOCK mode for testing

2. **PDF Export Errors**:
   - Check if the exports folder exists and is writable
   - Verify ReportLab is installed (`pip install reportlab`)

3. **File Upload Issues**:
   - Confirm file format is supported
   - Check file size against configured limits
   - Ensure upload folder has proper permissions
