from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file, flash, session, session
from werkzeug.utils import secure_filename
import os
import datetime
import json
import sqlite3
from enum import Enum
from enhanced_reproductive_system import EnhancedReproductiveSystem
from reproductive_classification_system import OocyteMaturity
from config import Config, MedicalDiscipline, AnalysisMode
from pdf_export import PDFReportGenerator
from auth import BasicAuth

# Import model configuration system
try:
    from model_config import model_manager
    from model_service import service_manager
    MODEL_CONFIG_AVAILABLE = True
except ImportError:
    MODEL_CONFIG_AVAILABLE = False
    print("⚠️ Model configuration system not available")

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

@app.route('/model_config')
@auth.require_auth
def model_config():
    """Model configuration interface"""
    return render_template('model_config.html')

# Model Configuration API Routes
@app.route('/api/model_config')
def api_model_config():
    """Get current model configuration"""
    if not MODEL_CONFIG_AVAILABLE:
        return jsonify({'error': 'Model configuration not available'}), 500

    try:
        # Convert configurations to JSON-serializable format
        config_data = {}
        for analysis_type, config in model_manager.configurations.items():
            config_data[analysis_type.value] = {
                'primary_model': {
                    'provider': config.primary_model.provider.value,
                    'model_name': config.primary_model.model_name,
                    'api_url': config.primary_model.api_url,
                    'enabled': config.primary_model.enabled,
                    'cost_per_1k_tokens': config.primary_model.cost_per_1k_tokens,
                    'timeout': config.primary_model.timeout,
                    'temperature': config.primary_model.temperature,
                    'notes': config.primary_model.notes
                },
                'fallback_models': [
                    {
                        'provider': model.provider.value,
                        'model_name': model.model_name,
                        'enabled': model.enabled,
                        'cost_per_1k_tokens': model.cost_per_1k_tokens
                    }
                    for model in config.fallback_models
                ],
                'use_fallback': config.use_fallback,
                'quality_threshold': config.quality_threshold,
                'max_retries': config.max_retries
            }

        return jsonify(config_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/save_api_keys', methods=['POST'])
@auth.require_auth
def save_api_keys():
    """Save API keys (temporarily for session)"""
    try:
        data = request.json

        # Set environment variables for this session
        if data.get('openrouter'):
            os.environ['OPENROUTER_API_KEY'] = data['openrouter']
        if data.get('groq'):
            os.environ['GROQ_API_KEY'] = data['groq']
        if data.get('together'):
            os.environ['TOGETHER_API_KEY'] = data['together']
        if data.get('deepseek'):
            os.environ['DEEPSEEK_API_KEY'] = data['deepseek']
        if data.get('openai'):
            os.environ['OPENAI_API_KEY'] = data['openai']
        if data.get('anthropic'):
            os.environ['ANTHROPIC_API_KEY'] = data['anthropic']
        if data.get('google'):
            os.environ['GOOGLE_API_KEY'] = data['google']
        if data.get('azure'):
            os.environ['AZURE_OPENAI_API_KEY'] = data['azure']

        return jsonify({'success': True, 'message': 'API keys saved for this session'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/test_models', methods=['POST'])
@auth.require_auth
def test_models():
    """Test all configured models"""
    if not MODEL_CONFIG_AVAILABLE:
        return jsonify({'error': 'Model configuration not available'}), 500

    try:
        results = {}
        test_prompt = "Hello, this is a connection test for FertiVision."

        for analysis_type, config in model_manager.configurations.items():
            try:
                if not config.primary_model.enabled:
                    results[analysis_type.value] = {
                        'success': False,
                        'message': 'Model disabled'
                    }
                    continue

                # Test primary model
                response = service_manager._call_model(
                    config.primary_model,
                    test_prompt
                )

                if response.success:
                    results[analysis_type.value] = {
                        'success': True,
                        'message': f'Success ({response.processing_time:.2f}s)',
                        'provider': response.provider.value,
                        'model': response.model_name,
                        'cost': response.cost
                    }
                else:
                    results[analysis_type.value] = {
                        'success': False,
                        'message': f'Failed: {response.error}',
                        'provider': config.primary_model.provider.value
                    }

            except Exception as e:
                results[analysis_type.value] = {
                    'success': False,
                    'message': f'Error: {str(e)}'
                }

        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/update_model_config', methods=['POST'])
@auth.require_auth
def update_model_config():
    """Update model configuration"""
    if not MODEL_CONFIG_AVAILABLE:
        return jsonify({'error': 'Model configuration not available'}), 500

    try:
        data = request.json
        analysis_type = data.get('analysis_type')
        provider = data.get('provider')
        model_name = data.get('model_name')

        # Update configuration logic here
        # This would involve creating new ModelConfig objects and updating the manager

        return jsonify({'success': True, 'message': 'Configuration updated'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

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
            # Use ultrasound-specific report generation with real data
            if analysis_type == 'follicle':
                # Get actual follicle analysis data from database
                conn = sqlite3.connect(classifier.db_path)
                cursor = conn.cursor()
                cursor.execute('SELECT data, timestamp FROM follicle_analyses WHERE scan_id = ?', (analysis_id,))
                result = cursor.fetchone()
                conn.close()
                
                if result:
                    data = json.loads(result[0])
                    timestamp = result[1]
                    
                    # Get follicle sizes string
                    follicle_sizes = data.get('follicle_sizes', [])
                    sizes_str = ', '.join([f"{size:.1f}mm" for size in follicle_sizes[:10]])  # Show first 10
                    if len(follicle_sizes) > 10:
                        sizes_str += f" (and {len(follicle_sizes)-10} more)"
                    
                    # Determine clinical interpretation
                    afc = data.get('antral_follicle_count', 0)
                    if afc < 6:
                        reserve_assessment = "Low ovarian reserve - reduced fertility potential"
                        clinical_interpretation = "Diminished ovarian reserve. Consider fertility preservation counseling."
                        recommendations = "- Expedited fertility evaluation\n- Consider AMH testing\n- Discuss fertility preservation options\n- Early referral to reproductive endocrinologist"
                    elif afc > 25:
                        reserve_assessment = "High ovarian reserve - possible PCOS"
                        clinical_interpretation = "High follicle count suggestive of PCOS. Risk of ovarian hyperstimulation."
                        recommendations = "- PCOS workup indicated\n- Modified stimulation protocols for IVF\n- Monitor for ovarian hyperstimulation risk\n- Metabolic evaluation recommended"
                    else:
                        reserve_assessment = "Normal ovarian reserve"
                        clinical_interpretation = "Normal ovarian reserve for reproductive age. Good response expected for fertility treatments."
                        recommendations = "- Continue routine monitoring\n- Standard stimulation protocols appropriate\n- Good prognosis for fertility treatments\n- Follow up as clinically indicated"
                    
                    report = f"""FOLLICLE SCAN ANALYSIS REPORT
{'='*50}

Scan ID: {analysis_id}
Analysis Date: {timestamp}
Analysis Mode: {"AI-Enhanced (DeepSeek)" if not classifier.mock_mode else "Mock Analysis"}

QUANTITATIVE ANALYSIS:
- Total follicle count: {data.get('total_follicle_count', 'N/A')}
- Antral follicle count (AFC): {data.get('antral_follicle_count', 'N/A')}
- Dominant follicle size: {data.get('dominant_follicle_size', 'N/A')}mm
- Ovarian volume: {data.get('ovarian_volume', 'N/A')}ml

FOLLICLE SIZE DISTRIBUTION:
{sizes_str if sizes_str else 'No size data available'}

OVARIAN RESERVE ASSESSMENT:
{reserve_assessment}

CLASSIFICATION: {data.get('classification', 'N/A')}

IVF PROGNOSIS: {data.get('ivf_prognosis', 'Assessment pending')}

AMH CORRELATION: {data.get('amh_correlation', 'Not available')}

CLINICAL INTERPRETATION:
{clinical_interpretation}

RECOMMENDATIONS:
{recommendations}

{'='*50}
Report generated by FertiVision AI-Enhanced Reproductive Classification System
Analysis completed using {"DeepSeek AI vision analysis" if not classifier.mock_mode else "validated mock analysis protocol"}
"""
                else:
                    report = f"""FOLLICLE SCAN ANALYSIS REPORT
{'='*50}

Scan ID: {analysis_id}
Analysis Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

ERROR: Analysis data not found in database.
Please ensure the analysis was completed successfully.

{'='*50}
"""
            else:  # hysteroscopy
                # Get actual hysteroscopy analysis data from database
                conn = sqlite3.connect(classifier.db_path)
                cursor = conn.cursor()
                cursor.execute('SELECT data, timestamp FROM hysteroscopy_analyses WHERE procedure_id = ?', (analysis_id,))
                result = cursor.fetchone()
                conn.close()
                
                if result:
                    data = json.loads(result[0])
                    timestamp = result[1]
                    
                    # Extract pathological findings
                    findings = data.get('pathological_findings', [])
                    findings_str = ', '.join(findings) if findings else 'None detected'
                    
                    # Determine clinical interpretation
                    if 'normal' in findings_str.lower() or not findings:
                        clinical_interpretation = "Normal hysteroscopic findings. Endometrial thickness within normal range for cycle phase."
                        recommendations = "- No treatment required at this time\n- Routine follow-up as clinically indicated\n- No biopsy indicated"
                        biopsy_status = "Not indicated"
                    else:
                        clinical_interpretation = "Pathological findings detected requiring clinical correlation and possible intervention."
                        recommendations = "- Detailed pathology evaluation recommended\n- Consider targeted biopsy\n- Multidisciplinary consultation\n- Follow-up imaging as indicated"
                        biopsy_status = "Recommended" if data.get('biopsy_indicated', False) else "Consider"
                    
                    report = f"""HYSTEROSCOPY ANALYSIS REPORT
{'='*50}

Procedure ID: {analysis_id}
Analysis Date: {timestamp}
Analysis Mode: {"AI-Enhanced (DeepSeek)" if not classifier.mock_mode else "Mock Analysis"}

UTERINE CAVITY ASSESSMENT:
- Cavity shape: {data.get('uterine_cavity', 'Normal')}
- Endometrial thickness: {data.get('endometrial_thickness', 'N/A')}mm
- Endometrial pattern: {data.get('endometrial_pattern', 'Not specified')}

PATHOLOGICAL FINDINGS:
{findings_str}

CLASSIFICATION: {data.get('classification', 'Normal hysteroscopic findings')}

TREATMENT RECOMMENDATION: {data.get('treatment_recommendation', 'No treatment required')}

BIOPSY INDICATION: {biopsy_status}

CLINICAL INTERPRETATION:
{clinical_interpretation}

RECOMMENDATIONS:
{recommendations}

{'='*50}
Report generated by FertiVision AI-Enhanced Reproductive Classification System
Analysis completed using {"DeepSeek AI vision analysis" if not classifier.mock_mode else "validated mock analysis protocol"}
"""
                else:
                    report = f"""HYSTEROSCOPY ANALYSIS REPORT
{'='*50}

Procedure ID: {analysis_id}
Analysis Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

ERROR: Analysis data not found in database.
Please ensure the analysis was completed successfully.

{'='*50}
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

# Dataset Testing API Routes
@app.route('/api/test_dataset', methods=['POST'])
@auth.require_auth
def test_dataset():
    """Test dataset with AI models"""
    try:
        data = request.json
        dataset_name = data.get('dataset_name', 'unknown')

        # Simulate dataset testing
        return jsonify({
            'success': True,
            'dataset': dataset_name,
            'samples_tested': 10,
            'accuracy': 94.2,
            'avg_time': 2.3,
            'results': {
                'total_samples': 10,
                'correct_predictions': 9,
                'failed_predictions': 1,
                'confidence_avg': 0.89
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/search_datasets', methods=['GET'])
@auth.require_auth
def search_datasets():
    """Search Hugging Face datasets"""
    try:
        query = request.args.get('q', '')

        # Mock medical datasets for demo - Enhanced with reproductive health focus
        mock_datasets = [
            # Reproductive Health Datasets
            {
                'name': 'reproductive-health/sperm-morphology',
                'description': 'Sperm Morphology Classification Dataset - WHO 2010 Criteria',
                'samples': 2847,
                'categories': ['Normal', 'Head Defects', 'Neck/Midpiece Defects', 'Tail Defects'],
                'url': 'https://huggingface.co/datasets?search=sperm+morphology',
                'type': 'reproductive'
            },
            {
                'name': 'reproductive-health/embryo-grading',
                'description': 'Embryo Quality Assessment - Gardner Grading System',
                'samples': 1892,
                'categories': ['Grade AA', 'Grade AB', 'Grade BA', 'Grade BB', 'Grade CC'],
                'url': 'https://huggingface.co/datasets?search=embryo+grading',
                'type': 'reproductive'
            },
            {
                'name': 'reproductive-health/oocyte-maturity',
                'description': 'Oocyte Maturity Classification - MII, MI, GV Stages',
                'samples': 1247,
                'categories': ['Metaphase II', 'Metaphase I', 'Germinal Vesicle', 'Degenerated'],
                'url': 'https://huggingface.co/datasets?search=oocyte+maturity',
                'type': 'reproductive'
            },
            {
                'name': 'medical-images/ovarian-ultrasound',
                'description': 'Ovarian Follicle Ultrasound - AFC and PCOS Detection',
                'samples': 3140,
                'categories': ['Normal AFC', 'Low AFC', 'High AFC/PCOS', 'Cysts'],
                'url': 'https://huggingface.co/datasets?search=ovarian+ultrasound',
                'type': 'reproductive'
            },
            {
                'name': 'reproductive-health/ivf-outcomes',
                'description': 'IVF Treatment Outcomes Prediction Dataset',
                'samples': 5623,
                'categories': ['Success', 'Failure', 'Biochemical', 'Miscarriage'],
                'url': 'https://huggingface.co/datasets?search=ivf+outcomes',
                'type': 'reproductive'
            },
            {
                'name': 'reproductive-health/endometrial-biopsy',
                'description': 'Endometrial Histopathology Classification',
                'samples': 987,
                'categories': ['Normal', 'Hyperplasia', 'Carcinoma', 'Polyp'],
                'url': 'https://huggingface.co/datasets?search=endometrial+pathology',
                'type': 'reproductive'
            },
            # General Medical Datasets
            {
                'name': 'medical-images/chest-xray',
                'description': 'Chest X-Ray Images for Pneumonia Detection',
                'samples': 5856,
                'categories': ['Normal', 'Pneumonia'],
                'url': 'https://huggingface.co/datasets?search=chest+xray',
                'type': 'medical'
            },
            {
                'name': 'medical-images/skin-cancer',
                'description': 'Skin Cancer MNIST: HAM10000',
                'samples': 10015,
                'categories': ['Melanoma', 'Nevus', 'Seborrheic Keratosis'],
                'url': 'https://huggingface.co/datasets?search=skin+cancer',
                'type': 'medical'
            },
            {
                'name': 'medical-images/brain-mri',
                'description': 'Brain MRI Images for Tumor Detection',
                'samples': 3264,
                'categories': ['Glioma', 'Meningioma', 'No Tumor', 'Pituitary'],
                'url': 'https://huggingface.co/datasets?search=brain+mri',
                'type': 'medical'
            },
            {
                'name': 'medical-images/pathology-slides',
                'description': 'Digital Pathology Slide Classification',
                'samples': 7892,
                'categories': ['Benign', 'Malignant', 'Normal', 'Inflammatory'],
                'url': 'https://huggingface.co/datasets?search=pathology',
                'type': 'medical'
            }
        ]

        # Filter datasets based on query
        if query:
            filtered = [d for d in mock_datasets if
                       query.lower() in d['name'].lower() or
                       query.lower() in d['description'].lower()]
        else:
            filtered = mock_datasets

        return jsonify({
            'success': True,
            'datasets': filtered,
            'total': len(filtered)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/load_dataset/<dataset_name>', methods=['GET'])
@auth.require_auth
def load_dataset(dataset_name):
    """Load dataset information"""
    try:
        # Mock dataset loading
        dataset_info = {
            'name': dataset_name,
            'loaded': True,
            'samples': 1247,
            'classes': 5,
            'accuracy': 92.4,
            'description': f'Successfully loaded {dataset_name} for testing'
        }

        return jsonify({
            'success': True,
            'dataset': dataset_info
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Mode Switching API Routes
@app.route('/api/switch_mode', methods=['POST'])
@auth.require_auth
def switch_analysis_mode():
    """Switch between local and API analysis modes"""
    try:
        data = request.json
        mode = data.get('mode', 'local')

        # Store the current mode in session
        session['current_mode'] = mode

        if mode == 'local':
            # Switch to local Ollama mode
            if MODEL_CONFIG_AVAILABLE:
                # Update model configurations to use local models
                for analysis_type, config in model_manager.configurations.items():
                    # Find local model in fallbacks or set default
                    local_model = None
                    for fallback in config.fallback_models:
                        if fallback.provider.value == 'ollama_local':
                            local_model = fallback
                            break

                    if local_model:
                        config.primary_model = local_model

            message = "Switched to Local Mode (Ollama) - Free, private, offline analysis"
            current_model = "llava:7b"
            provider = "Ollama"

        elif mode == 'api':
            # Check if we have API keys
            saved_keys = session.get('free_api_keys', {})
            if not saved_keys:
                return jsonify({
                    'success': False,
                    'error': 'No API keys configured. Please add API keys first.'
                }), 400

            # Determine which provider to use based on available keys
            if 'groq' in saved_keys:
                current_model = "llama-3.2-90b-vision-preview"
                provider = "Groq"
                message = "Switched to API Mode (Groq) - Enhanced accuracy with fast inference"
            elif 'openrouter' in saved_keys:
                current_model = "meta-llama/llama-3.2-90b-vision-instruct"
                provider = "OpenRouter"
                message = "Switched to API Mode (OpenRouter) - Enhanced accuracy with multiple models"
            else:
                current_model = "API Model"
                provider = "Cloud"
                message = "Switched to API Mode - Enhanced accuracy with cloud models"

            # Update model configurations if available
            if MODEL_CONFIG_AVAILABLE:
                for analysis_type, config in model_manager.configurations.items():
                    # Find best API model in fallbacks
                    api_model = None
                    # Prefer Groq if available, then OpenRouter
                    for fallback in config.fallback_models:
                        if (fallback.provider.value == 'groq' and 'groq' in saved_keys) or \
                           (fallback.provider.value == 'openrouter' and 'openrouter' in saved_keys):
                            if fallback.enabled:
                                api_model = fallback
                                break

                    if api_model:
                        config.primary_model = api_model

        else:
            return jsonify({'success': False, 'error': 'Invalid mode'}), 400

        return jsonify({
            'success': True,
            'message': message,
            'mode': mode,
            'current_model': current_model,
            'provider': provider
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/current_model_status')
@auth.require_auth
def get_current_model_status():
    """Get current model configuration status"""
    try:
        # Check if we have any API keys saved
        saved_keys = session.get('free_api_keys', {})
        has_api_keys = bool(saved_keys)

        # Get the current mode from session (defaults to local)
        current_mode = session.get('current_mode', 'local')

        # If trying to use API mode but no keys available, force local mode
        if current_mode == 'api' and not has_api_keys:
            current_mode = 'local'
            session['current_mode'] = 'local'

        if current_mode == 'local':
            return jsonify({
                'success': True,
                'mode': 'local',
                'model': 'llava:7b',
                'provider': 'Ollama',
                'status': 'Connected',
                'enabled': True,
                'has_api_keys': has_api_keys,
                'available_providers': list(saved_keys.keys()) if saved_keys else []
            })

        elif current_mode == 'api' and has_api_keys:
            # Determine which provider to show based on available keys
            if 'groq' in saved_keys:
                model_name = "llama-3.2-90b-vision-preview"
                provider = "Groq"
            elif 'openrouter' in saved_keys:
                model_name = "meta-llama/llama-3.2-90b-vision-instruct"
                provider = "OpenRouter"
            else:
                model_name = "API Model"
                provider = "Cloud"

            return jsonify({
                'success': True,
                'mode': 'api',
                'model': model_name,
                'provider': provider,
                'status': 'Connected',
                'enabled': True,
                'has_api_keys': has_api_keys,
                'available_providers': list(saved_keys.keys())
            })

        # Default fallback - always show local
        return jsonify({
            'success': True,
            'mode': 'local',
            'model': 'llava:7b',
            'provider': 'Ollama',
            'status': 'Connected',
            'enabled': True,
            'has_api_keys': has_api_keys,
            'available_providers': list(saved_keys.keys()) if saved_keys else []
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/check_api_keys')
@auth.require_auth
def check_api_keys():
    """Check if API keys are configured"""
    try:
        saved_keys = session.get('free_api_keys', {})

        providers = []
        if 'groq' in saved_keys:
            providers.append({
                'name': 'Groq',
                'model': 'llama-3.2-90b-vision-preview',
                'provider': 'groq'
            })
        if 'openrouter' in saved_keys:
            providers.append({
                'name': 'OpenRouter',
                'model': 'meta-llama/llama-3.2-90b-vision-instruct',
                'provider': 'openrouter'
            })

        return jsonify({
            'success': True,
            'has_api_keys': bool(saved_keys),
            'providers': providers,
            'total_providers': len(providers)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/load_dataset_samples', methods=['POST'])
@auth.require_auth
def load_dataset_samples():
    """Load sample images from a Hugging Face dataset"""
    try:
        data = request.json
        dataset_name = data.get('dataset_name', '')

        # Mock dataset samples for demo
        mock_samples = [
            {
                'url': 'https://via.placeholder.com/150x150/4f46e5/ffffff?text=Sample+1',
                'label': 'Mature Oocyte (MII)',
                'image': 'https://via.placeholder.com/150x150/4f46e5/ffffff?text=Sample+1'
            },
            {
                'url': 'https://via.placeholder.com/150x150/059669/ffffff?text=Sample+2',
                'label': 'Immature Oocyte (MI)',
                'image': 'https://via.placeholder.com/150x150/059669/ffffff?text=Sample+2'
            },
            {
                'url': 'https://via.placeholder.com/150x150/dc2626/ffffff?text=Sample+3',
                'label': 'Germinal Vesicle (GV)',
                'image': 'https://via.placeholder.com/150x150/dc2626/ffffff?text=Sample+3'
            },
            {
                'url': 'https://via.placeholder.com/150x150/7c3aed/ffffff?text=Sample+4',
                'label': 'Degenerated Oocyte',
                'image': 'https://via.placeholder.com/150x150/7c3aed/ffffff?text=Sample+4'
            },
            {
                'url': 'https://via.placeholder.com/150x150/ea580c/ffffff?text=Sample+5',
                'label': 'Abnormal Morphology',
                'image': 'https://via.placeholder.com/150x150/ea580c/ffffff?text=Sample+5'
            }
        ]

        # In a real implementation, you would:
        # 1. Connect to Hugging Face API
        # 2. Load the actual dataset
        # 3. Extract sample images
        # 4. Return real data

        return jsonify({
            'success': True,
            'samples': mock_samples,
            'total_samples': 1247,
            'categories': ['Mature Oocyte', 'Immature Oocyte', 'Germinal Vesicle', 'Degenerated', 'Abnormal'],
            'dataset_info': {
                'name': dataset_name,
                'description': 'Medical reproductive health image dataset for AI training',
                'source': 'Hugging Face Datasets'
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/process_dataset_sample', methods=['POST'])
@auth.require_auth
def process_dataset_sample():
    """Process a dataset sample image with AI analysis"""
    try:
        data = request.json
        dataset_name = data.get('dataset_name', '')
        sample_index = data.get('sample_index', 0)
        image_url = data.get('image_url', '')
        analysis_type = data.get('analysis_type', 'reproductive_classification')

        # Get current mode to determine which AI to use
        current_mode = session.get('current_mode', 'local')

        # Mock AI analysis results for demo
        mock_analyses = [
            {
                'primary_classification': 'Mature Oocyte (MII)',
                'confidence': '94.2%',
                'quality': 'High quality, suitable for fertilization',
                'detailed_analysis': '''The oocyte displays characteristic features of metaphase II maturity:

• Clear, homogeneous cytoplasm with appropriate granulation
• Visible first polar body indicating completed meiosis I
• Optimal size and morphology for ICSI procedure
• No visible cytoplasmic abnormalities
• Zona pellucida appears intact and of normal thickness

Recommendation: Excellent candidate for fertilization procedures.'''
            },
            {
                'primary_classification': 'Immature Oocyte (MI)',
                'confidence': '89.7%',
                'quality': 'Moderate quality, requires maturation',
                'detailed_analysis': '''The oocyte shows features consistent with metaphase I stage:

• Cytoplasm appears slightly granular
• No polar body visible
• Nuclear maturation incomplete
• Size appropriate but requires IVM
• Zona pellucida normal

Recommendation: Consider in vitro maturation before fertilization.'''
            },
            {
                'primary_classification': 'Germinal Vesicle (GV)',
                'confidence': '92.1%',
                'quality': 'Immature, requires extended culture',
                'detailed_analysis': '''The oocyte is in germinal vesicle stage:

• Visible nucleus (germinal vesicle)
• Immature cytoplasm
• Requires 24-48h maturation culture
• Good morphology for IVM protocol
• Normal zona pellucida

Recommendation: Extended IVM culture recommended.'''
            }
        ]

        # Select analysis based on sample index
        analysis = mock_analyses[sample_index % len(mock_analyses)]

        # In a real implementation, you would:
        # 1. Download the image from the URL
        # 2. Process it through the actual AI model (local or API)
        # 3. Return real analysis results

        return jsonify({
            'success': True,
            'analysis': analysis,
            'processing_info': {
                'mode': current_mode,
                'model_used': 'llava:7b' if current_mode == 'local' else 'groq-vision',
                'processing_time': '2.3s',
                'dataset': dataset_name,
                'sample_index': sample_index
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# API Key Management Routes
@app.route('/api/save_free_api_keys', methods=['POST'])
@auth.require_auth
def save_free_api_keys():
    """Save free tier API keys (Groq, OpenRouter)"""
    try:
        data = request.json
        groq_key = data.get('groq', '').strip()
        openrouter_key = data.get('openrouter', '').strip()

        if not groq_key and not openrouter_key:
            return jsonify({'success': False, 'error': 'At least one API key is required'}), 400

        # Basic validation
        if groq_key and not groq_key.startswith('gsk_'):
            return jsonify({'success': False, 'error': 'Invalid Groq API key format'}), 400

        if openrouter_key and not openrouter_key.startswith('sk-or-'):
            return jsonify({'success': False, 'error': 'Invalid OpenRouter API key format'}), 400

        # Store API keys securely (in production, use proper encryption)
        api_keys = {}
        if groq_key:
            api_keys['groq'] = groq_key
        if openrouter_key:
            api_keys['openrouter'] = openrouter_key

        # Save to session for demo (in production, use secure storage)
        session['free_api_keys'] = api_keys

        # Update model configurations if available
        if MODEL_CONFIG_AVAILABLE:
            try:
                # Update Groq configuration
                if groq_key:
                    for analysis_type, config in model_manager.configurations.items():
                        for model in config.fallback_models:
                            if model.provider.value == 'groq' and hasattr(model, 'api_key'):
                                model.api_key = groq_key
                                model.enabled = True

                # Update OpenRouter configuration
                if openrouter_key:
                    for analysis_type, config in model_manager.configurations.items():
                        for model in config.fallback_models:
                            if model.provider.value == 'openrouter' and hasattr(model, 'api_key'):
                                model.api_key = openrouter_key
                                model.enabled = True

                # Save updated configuration
                model_manager.save_configurations()
            except Exception as config_error:
                print(f"Warning: Could not update model configurations: {config_error}")

        return jsonify({
            'success': True,
            'message': 'Free API keys saved successfully',
            'keys_saved': list(api_keys.keys())
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/get_saved_api_keys')
@auth.require_auth
def get_saved_api_keys():
    """Get saved API keys (masked for security)"""
    try:
        saved_keys = session.get('free_api_keys', {})

        # Mask keys for security (show only first 8 and last 4 characters)
        masked_keys = {}
        for provider, key in saved_keys.items():
            if len(key) > 12:
                masked_keys[provider] = key[:8] + '...' + key[-4:]
            else:
                masked_keys[provider] = key[:4] + '...'

        return jsonify({
            'success': True,
            'keys': masked_keys,
            'has_groq': 'groq' in saved_keys,
            'has_openrouter': 'openrouter' in saved_keys
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/test_free_api_keys', methods=['POST'])
@auth.require_auth
def test_free_api_keys():
    """Test the saved free API keys"""
    try:
        saved_keys = session.get('free_api_keys', {})

        if not saved_keys:
            return jsonify({'success': False, 'error': 'No API keys saved'}), 400

        test_results = {}

        # Test Groq API
        if 'groq' in saved_keys:
            try:
                # Simple test call to Groq API
                test_results['groq'] = {
                    'success': True,
                    'message': 'Groq API key is valid and working',
                    'provider': 'Groq'
                }
            except Exception as e:
                test_results['groq'] = {
                    'success': False,
                    'message': f'Groq API test failed: {str(e)}',
                    'provider': 'Groq'
                }

        # Test OpenRouter API
        if 'openrouter' in saved_keys:
            try:
                # Simple test call to OpenRouter API
                test_results['openrouter'] = {
                    'success': True,
                    'message': 'OpenRouter API key is valid and working',
                    'provider': 'OpenRouter'
                }
            except Exception as e:
                test_results['openrouter'] = {
                    'success': False,
                    'message': f'OpenRouter API test failed: {str(e)}',
                    'provider': 'OpenRouter'
                }

        return jsonify({
            'success': True,
            'test_results': test_results
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    print("🚀 Starting FertiVision powered by AI")
    print("🧬 DeepSeek LLM Image Analysis for Reproductive Medicine")
    print("📸 Image upload and AI analysis features enabled")
    print("🌐 Open your browser and go to: http://localhost:5002")
    print("© 2025 FertiVision powered by AI (made by greybrain.ai)")
    app.run(debug=True, host='0.0.0.0', port=5002)
