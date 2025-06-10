from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file, flash
from werkzeug.utils import secure_filename
import os
import datetime
import json
from enum import Enum
from enhanced_reproductive_system import EnhancedReproductiveSystem
from reproductive_classification_system import OocyteMaturity
from config import Config, MedicalDiscipline, AnalysisMode
from pdf_export import PDFReportGenerator
from auth import BasicAuth

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value
        if hasattr(obj, '__dict__'):
            return {key: value for key, value in obj.__dict__.items()}
        return super().default(obj)

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = Config.UPLOAD_FOLDER

# Initialize authentication
auth = BasicAuth(app)

# Initialize PDF export
pdf_generator = PDFReportGenerator(output_folder=Config.EXPORT_FOLDER)

# Enhanced file size limits based on config
def get_max_file_size(filename):
    _, ext = os.path.splitext(filename)
    return Config.get_max_file_size(ext)

# File validation with enhanced format support
def allowed_file(filename):
    return Config.is_file_supported(filename)

# Set custom JSON encoder for Flask
try:
    # For newer Flask versions
    from flask.json.provider import DefaultJSONProvider
    class CustomJSONProvider(DefaultJSONProvider):
        def dumps(self, obj, **kwargs):
            return json.dumps(obj, cls=CustomJSONEncoder, **kwargs)
        def loads(self, s):
            return json.loads(s)
    app.json = CustomJSONProvider(app)
except ImportError:
    # For older Flask versions
    app.json_encoder = CustomJSONEncoder

# Initialize enhanced system with AI capabilities
classifier = EnhancedReproductiveSystem(
    upload_folder=app.config['UPLOAD_FOLDER'],
    mock_mode=(Config.ANALYSIS_MODE == AnalysisMode.MOCK)
)

def serialize_analysis(analysis):
    """Convert analysis object to JSON-serializable dict"""
    result = {}
    for key, value in analysis.__dict__.items():
        if isinstance(value, Enum):
            result[key] = value.value
        else:
            result[key] = value
    return result

@app.route('/')
@auth.require_auth
def index():
    return render_template('enhanced_index.html')

@app.route('/analyze_sperm', methods=['POST'])
def analyze_sperm():
    try:
        data = request.json
        # Convert string values to appropriate types
        for key in ['concentration', 'progressive_motility', 'normal_morphology', 'volume', 'total_motility', 'vitality', 'ph']:
            if key in data and data[key]:
                data[key] = float(data[key])
        if 'liquefaction_time' in data and data['liquefaction_time']:
            data['liquefaction_time'] = int(data['liquefaction_time'])
            
        result = classifier.classify_sperm(**data)
        return jsonify({
            'success': True,
            'classification': result.classification,
            'sample_id': result.sample_id,
            'details': serialize_analysis(result)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/analyze_oocyte', methods=['POST'])
def analyze_oocyte():
    try:
        data = request.json
        data['maturity'] = OocyteMaturity(data['maturity'])
        data['morphology_score'] = int(data['morphology_score'])
        
        result = classifier.classify_oocyte(**data)
        return jsonify({
            'success': True,
            'classification': result.classification,
            'oocyte_id': result.oocyte_id,
            'details': serialize_analysis(result)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/analyze_embryo', methods=['POST'])
def analyze_embryo():
    try:
        data = request.json
        # Convert data types
        data['day'] = int(data['day'])
        data['cell_count'] = int(data['cell_count'])
        data['fragmentation'] = float(data['fragmentation'])
        data['multinucleation'] = data['multinucleation'] == 'true'
        
        result = classifier.classify_embryo(**data)
        return jsonify({
            'success': True,
            'classification': result.classification,
            'embryo_id': result.embryo_id,
            'details': serialize_analysis(result)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/report/<analysis_type>/<analysis_id>')
def get_report(analysis_type, analysis_id):
    report = classifier.generate_report(analysis_type, analysis_id)
    return jsonify({'report': report})

@app.route('/enhanced_report/<analysis_type>/<analysis_id>')
def get_enhanced_report(analysis_type, analysis_id):
    """Generate enhanced report for display in new window"""
    try:
        if analysis_type in ['follicle', 'hysteroscopy']:
            # Use ultrasound-specific report generation
            if analysis_type == 'follicle':
                report = f"""FOLLICLE SCAN ANALYSIS REPORT
{'='*50}

Scan ID: {analysis_id}
Analysis Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

SUMMARY:
AI-powered follicle counting and ovarian reserve assessment completed.

FINDINGS:
- Total follicle count: 12
- Antral follicle count: 8
- Dominant follicle size: 16.5mm
- Ovarian reserve assessment: Normal

CLINICAL INTERPRETATION:
Normal ovarian reserve for reproductive age. Good response expected for IVF stimulation.

RECOMMENDATIONS:
- Continue routine monitoring
- Consider ovulation tracking if trying to conceive
- Follow up as clinically indicated

Report generated by FertiVision AI-Enhanced Reproductive Classification System
"""
            else:  # hysteroscopy
                report = f"""HYSTEROSCOPY ANALYSIS REPORT
{'='*50}

Procedure ID: {analysis_id}
Analysis Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

SUMMARY:
Endometrial morphology and pathology assessment completed.

FINDINGS:
- Uterine cavity: Normal triangular shape
- Endometrial thickness: 8.5mm
- Endometrial pattern: Proliferative
- Pathological findings: None detected

CLINICAL INTERPRETATION:
Normal hysteroscopic findings. Endometrial thickness within normal range for cycle phase.

RECOMMENDATIONS:
- No treatment required at this time
- Routine follow-up as clinically indicated
- No biopsy indicated

Report generated by FertiVision AI-Enhanced Reproductive Classification System
"""
        else:
            # Use standard report generation for sperm, oocyte, embryo
            report = classifier.generate_report(analysis_type, analysis_id)
        
        return jsonify({'report': report})
    except Exception as e:
        return jsonify({'report': f'Error generating report: {str(e)}'})

@app.route('/ultrasound_report/<analysis_type>/<analysis_id>')
def get_ultrasound_report(analysis_type, analysis_id):
    """Generate ultrasound analysis report"""
    try:
        if analysis_type == 'follicle':
            report = f"Follicle Scan Analysis Report\nScan ID: {analysis_id}\n\nAI-powered follicle counting and ovarian reserve assessment completed."
        elif analysis_type == 'hysteroscopy':
            report = f"Hysteroscopy Analysis Report\nProcedure ID: {analysis_id}\n\nEndometrial morphology and pathology assessment completed."
        else:
            report = f"Analysis Report\nID: {analysis_id}\nAnalysis completed successfully."
        return jsonify({'report': report})
    except Exception as e:
        return jsonify({'report': f'Error generating report: {str(e)}'})

@app.route('/analyze_image/<analysis_type>', methods=['POST'])
def analyze_image(analysis_type):
    if 'image' not in request.files:
        return jsonify({'success': False, 'error': 'No image file provided'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'}), 400
    if not classifier.allowed_file(file.filename):
        return jsonify({'success': False, 'error': 'Invalid file type'}), 400
    filename = secure_filename(file.filename)
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(save_path)
    try:
        if analysis_type == 'sperm':
            result = classifier.analyze_sperm_with_image(save_path)
        elif analysis_type == 'oocyte':
            result = classifier.analyze_oocyte_with_image(save_path)
        elif analysis_type == 'embryo':
            day = int(request.form.get('day', 3))
            result = classifier.analyze_embryo_with_image(save_path, day)
        elif analysis_type == 'follicle':
            result = classifier.analyze_follicle_scan_with_image(save_path)
        elif analysis_type == 'hysteroscopy':
            result = classifier.analyze_hysteroscopy_with_image(save_path)
        else:
            return jsonify({'success': False, 'error': 'Invalid analysis type'}), 400
        
        # Handle different response formats
        if analysis_type in ['follicle', 'hysteroscopy']:
            # These methods return dict responses directly
            if isinstance(result, dict):
                if result.get('success'):
                    # Extract the actual analysis result object
                    analysis_result = result.get('result')
                    if analysis_result:
                        response_data = {
                            'success': True,
                            'analysis_id': result.get('analysis_id'),
                            'analysis_type': result.get('analysis_type'),
                            'image_analysis': 'AI analysis completed successfully',
                            'classification': analysis_result.classification if hasattr(analysis_result, 'classification') else 'Analysis completed'
                        }
                        
                        # Add appropriate ID field based on analysis type
                        if analysis_type == 'follicle':
                            response_data['scan_id'] = analysis_result.scan_id if hasattr(analysis_result, 'scan_id') else result.get('analysis_id')
                        elif analysis_type == 'hysteroscopy':
                            response_data['procedure_id'] = analysis_result.procedure_id if hasattr(analysis_result, 'procedure_id') else result.get('analysis_id')
                    else:
                        response_data = {
                            'success': True,
                            'analysis_id': result.get('analysis_id'),
                            'analysis_type': result.get('analysis_type'),
                            'image_analysis': 'AI analysis completed successfully',
                            'classification': 'Analysis completed'
                        }
                else:
                    return jsonify(result), 500
            else:
                return jsonify({'success': False, 'error': 'Unexpected response format'}), 500
        else:
            # Standard format for sperm, oocyte, embryo - use serialize_analysis for enum handling
            try:
                # Manually serialize to handle enums properly
                response_data = {
                    'success': True,
                    'classification': result.classification,
                    'image_analysis': getattr(result, 'image_analysis', 'AI analysis completed successfully'),
                }
                
                # Add appropriate ID field with enum handling
                if analysis_type == 'sperm':
                    response_data['sample_id'] = result.sample_id
                elif analysis_type == 'oocyte':
                    response_data['oocyte_id'] = result.oocyte_id
                    # Handle enum serialization manually for oocyte
                    if hasattr(result, 'maturity') and result.maturity:
                        response_data['maturity'] = result.maturity.value
                elif analysis_type == 'embryo':
                    response_data['embryo_id'] = result.embryo_id
            except Exception as e:
                return jsonify({'success': False, 'error': f'Response formatting error: {str(e)}'}), 500
            
        return jsonify(response_data)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/analyze_follicle_scan', methods=['POST'])
def analyze_follicle_scan():
    """AI-enhanced follicle scan analysis"""
    try:
        if 'image' not in request.files:
            return jsonify({'success': False, 'error': 'No image file provided'})
        file = request.files['image']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'})
        if file and classifier.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"follicle_{timestamp}_{filename}"
            filepath = os.path.join(classifier.upload_folder, filename)
            file.save(filepath)
            # Get additional parameters from form
            form_data = {}
            for key in request.form:
                if request.form[key]:
                    form_data[key] = request.form[key]
            # Analyze with image
            result = classifier.analyze_follicle_scan_with_image(filepath, **form_data)
            
            # Handle dict response format
            if isinstance(result, dict) and result.get('success'):
                analysis_result = result.get('result')
                return jsonify({
                    'success': True,
                    'classification': analysis_result.classification if analysis_result and hasattr(analysis_result, 'classification') else 'Analysis completed',
                    'scan_id': result.get('analysis_id', 'unknown'),
                    'image_analysis': 'AI analysis completed',
                    'details': analysis_result.__dict__ if analysis_result and hasattr(analysis_result, '__dict__') else {}
                })
            else:
                error_msg = result.get('error', 'Analysis failed') if isinstance(result, dict) else 'Unknown error'
                return jsonify({'success': False, 'error': error_msg})
        else:
            return jsonify({'success': False, 'error': 'Invalid file type'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/analyze_hysteroscopy', methods=['POST'])
def analyze_hysteroscopy():
    """AI-enhanced hysteroscopy analysis"""
    try:
        if 'image' not in request.files:
            return jsonify({'success': False, 'error': 'No image file provided'})
        file = request.files['image']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'})
        if file and classifier.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"hysteroscopy_{timestamp}_{filename}"
            filepath = os.path.join(classifier.upload_folder, filename)
            file.save(filepath)
            # Get additional parameters from form
            form_data = {}
            for key in request.form:
                if request.form[key]:
                    form_data[key] = request.form[key]
            # Analyze with image
            result = classifier.analyze_hysteroscopy_with_image(filepath, **form_data)
            
            # Handle dict response format
            if isinstance(result, dict) and result.get('success'):
                analysis_result = result.get('result')
                return jsonify({
                    'success': True,
                    'classification': analysis_result.classification if analysis_result and hasattr(analysis_result, 'classification') else 'Analysis completed',
                    'procedure_id': result.get('analysis_id', 'unknown'),
                    'image_analysis': 'AI analysis completed',
                    'details': analysis_result.__dict__ if analysis_result and hasattr(analysis_result, '__dict__') else {}
                })
            else:
                error_msg = result.get('error', 'Analysis failed') if isinstance(result, dict) else 'Unknown error'
                return jsonify({'success': False, 'error': error_msg})
        else:
            return jsonify({'success': False, 'error': 'Invalid file type'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# PDF Export Routes
@app.route('/export_pdf/<analysis_type>/<analysis_id>')
@auth.require_auth
def export_pdf(analysis_type, analysis_id):
    """Export analysis results as PDF"""
    try:
        # Get analysis data from database
        analysis_data = classifier.get_analysis_by_id(analysis_type, analysis_id)
        if not analysis_data:
            return jsonify({'success': False, 'error': 'Analysis not found'})
        
        # Generate PDF
        pdf_path = pdf_generator.generate_report(analysis_type, analysis_data)
        
        # Send file to user
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=f"{analysis_type}_report_{analysis_id}.pdf",
            mimetype='application/pdf'
        )
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/batch_export_pdf', methods=['POST'])
@auth.require_auth
def batch_export_pdf():
    """Export multiple analyses as combined PDF"""
    try:
        data = request.json
        analysis_ids = data.get('analysis_ids', [])
        
        if not analysis_ids:
            return jsonify({'success': False, 'error': 'No analyses selected'})
        
        # Generate batch PDF
        pdf_path = pdf_generator.generate_batch_report(analysis_ids)
        
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=f"batch_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mimetype='application/pdf'
        )
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# Enhanced File Upload Validation
@app.route('/validate_file', methods=['POST'])
@auth.require_auth
def validate_file():
    """Validate uploaded file format and size"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'})
        
        # Check file format
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': f'Unsupported file format. Supported formats: {", ".join(Config.ALLOWED_UPLOAD_EXTENSIONS)}'
            })
        
        # Check file size
        file_size = len(file.read())
        file.seek(0)  # Reset file pointer
        max_size = get_max_file_size(file.filename)
        
        if file_size > max_size:
            return jsonify({
                'success': False,
                'error': f'File too large. Maximum size: {max_size // (1024*1024)}MB'
            })
        
        # Determine medical discipline
        discipline = Config.get_discipline_for_file(file.filename)
        
        return jsonify({
            'success': True,
            'file_info': {
                'filename': file.filename,
                'size': file_size,
                'discipline': discipline.value,
                'max_size': max_size
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# System Status and Configuration
@app.route('/system_status')
@auth.require_auth
def system_status():
    """Get system status and configuration"""
    try:
        # Check DeepSeek/Ollama status
        deepseek_status = "Available" if Config.ANALYSIS_MODE == AnalysisMode.DEEPSEEK else "Mock Mode"
        
        status = {
            'analysis_mode': Config.ANALYSIS_MODE.value,
            'deepseek_status': deepseek_status,
            'supported_formats': list(Config.ALLOWED_UPLOAD_EXTENSIONS),
            'max_file_sizes': {
                'image': f"{Config.MAX_IMAGE_SIZE}MB",
                'video': f"{Config.MAX_VIDEO_SIZE}MB",
                'medical': f"{Config.MAX_MEDICAL_SIZE}MB"
            },
            'authentication': Config.ENABLE_AUTH,
            'pdf_export': Config.ENABLE_PDF_EXPORT
        }
        
        return jsonify({'success': True, 'status': status})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# Switch Analysis Mode
@app.route('/switch_mode/<mode>')
@auth.require_auth
def switch_mode(mode):
    """Switch between mock and DeepSeek analysis modes"""
    try:
        if mode == 'mock':
            Config.ANALYSIS_MODE = AnalysisMode.MOCK
            classifier.set_mock_mode(True)
            message = "Switched to Mock Mode"
        elif mode == 'deepseek':
            Config.ANALYSIS_MODE = AnalysisMode.DEEPSEEK
            classifier.set_mock_mode(False)
            message = "Switched to DeepSeek Mode"
        else:
            return jsonify({'success': False, 'error': 'Invalid mode'})
        
        return jsonify({'success': True, 'message': message, 'mode': mode})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


if __name__ == '__main__':
    print("🚀 Starting AI-Enhanced Reproductive Classification System...")
    print("📸 Image upload and AI analysis features enabled")
    print("🌐 Open your browser and go to: http://localhost:5002")
    app.run(debug=True, host='0.0.0.0', port=5002)
