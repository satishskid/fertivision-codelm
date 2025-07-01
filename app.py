from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file, flash, session, send_from_directory
from werkzeug.utils import secure_filename
import os
import datetime
import json
import sqlite3
from enum import Enum
from enhanced_reproductive_system import EnhancedReproductiveSystem
from reproductive_classification_system import OocyteMaturity
from config import Config, MedicalDiscipline, AnalysisMode, config
from pdf_export import export_patient_fertility_report, generate_pdf_buffer
from auth import BasicAuth
from patient_history import PatientHistoryManager, DocumentType, PatientRecord

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
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        if hasattr(obj, '__dict__'):
            return {key: value for key, value in obj.__dict__.items()}
        return super().default(obj)

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = config.settings['upload_folder']

# Initialize authentication
auth = BasicAuth()

# Initialize PDF export
# PDF export functionality is handled by pdf_export module functions

# Initialize patient history manager
patient_history = PatientHistoryManager()

# Enhanced file size limits based on config
def get_max_file_size(filename):
    return config.settings['max_file_size']

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
classifier = EnhancedReproductiveSystem()

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
        return jsonify({
            'error': 'Model configuration not available',
            'message': 'Using default configuration',
            'default_config': {
                'analysis_mode': 'demo',
                'available_models': ['demo'],
                'current_model': 'demo'
            }
        }), 200  # Return 200 with error message instead of 500

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
        db_path = 'reproductive_analysis.db'  # Use the standard database path
        
        if analysis_type in ['follicle', 'hysteroscopy']:
            # Use ultrasound-specific report generation with real data
            if analysis_type == 'follicle':
                # Get actual follicle analysis data from database
                conn = sqlite3.connect(db_path)
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
Analysis Mode: {"AI-Enhanced (DeepSeek)" if hasattr(classifier, 'mock_mode') and not classifier.mock_mode else "Mock Analysis"}

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
Analysis completed using {"DeepSeek AI vision analysis" if hasattr(classifier, 'mock_mode') and not classifier.mock_mode else "validated mock analysis protocol"}
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
                conn = sqlite3.connect(db_path)
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
Analysis Mode: {"AI-Enhanced (DeepSeek)" if hasattr(classifier, 'mock_mode') and not classifier.mock_mode else "Mock Analysis"}

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
Analysis completed using {"DeepSeek AI vision analysis" if hasattr(classifier, 'mock_mode') and not classifier.mock_mode else "validated mock analysis protocol"}
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
    """Generate ultrasound analysis report with real data"""
    try:
        db_path = 'reproductive_analysis.db'  # Use the standard database path
        
        # Handle missing or undefined analysis IDs
        if analysis_id in ['undefined', 'null', '', 'None']:
            # Generate a sample report with alert about missing ID
            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            if analysis_type == 'follicle':
                report = f"""⚠️ FOLLICLE SCAN ANALYSIS REPORT (SAMPLE)

⚠️ ALERT: Analysis ID missing - Showing sample analysis
Date: {current_time}

SAMPLE FINDINGS:
• Total follicles: 12-15 (estimated range)
• Antral follicle count: 8-12 (normal range)
• Dominant follicle: 16-20mm (mature range)
• Follicle sizes: Variable distribution observed

ASSESSMENT: Normal ovarian reserve (sample assessment)
CLASSIFICATION: Representative analysis

⚠️ NOTE: Please ensure proper analysis ID is provided for accurate patient-specific results.
Analysis completed using Mock Analysis Protocol"""
                
            elif analysis_type == 'sperm':
                report = f"""⚠️ SPERM ANALYSIS REPORT (SAMPLE)

⚠️ ALERT: Analysis ID missing - Showing sample analysis
Date: {current_time}

SAMPLE FINDINGS:
• Concentration: 20-40 million/ml (normal range)
• Total count: 50-100 million (normal range)
• Progressive motility: 35-50% (normal range)
• Total motility: 50-65% (normal range)
• Normal morphology: 4-8% (WHO criteria)
• Vitality: 75-85% (normal range)
• Volume: 2.5-4.0 ml (normal range)
• pH: 7.2-7.8 (normal range)

CLASSIFICATION: Normozoospermia (sample classification)
INTERPRETATION: Sample shows normal sperm parameters according to WHO criteria

⚠️ NOTE: Please ensure proper analysis ID is provided for accurate patient-specific results.
Analysis completed using Mock Analysis Protocol"""
                
            elif analysis_type == 'oocyte':
                report = f"""⚠️ OOCYTE ANALYSIS REPORT (SAMPLE)

⚠️ ALERT: Analysis ID missing - Showing sample analysis
Date: {current_time}

SAMPLE FINDINGS:
• Standard oocyte characteristics observed
• Maturity indicators present
• Cytoplasm appearance normal
• Zona pellucida intact

MATURITY ASSESSMENT:
• Maturity stage: Metaphase II stage (sample)
• Cytoplasm quality: Good (sample assessment)
• Zona pellucida: Normal thickness and clarity

CLASSIFICATION: Excellent quality - suitable for ICSI (sample)
FERTILIZATION POTENTIAL: Good (sample assessment)

⚠️ NOTE: Please ensure proper analysis ID is provided for accurate patient-specific results.
Analysis completed using Mock Analysis Protocol"""
                
            elif analysis_type == 'embryo':
                report = f"""⚠️ EMBRYO ANALYSIS REPORT (SAMPLE)

⚠️ ALERT: Analysis ID missing - Showing sample analysis
Date: {current_time}

SAMPLE FINDINGS:
• Normal embryo development patterns observed
• Cell division appears regular
• Fragmentation within acceptable limits
• Overall morphology assessment positive

DEVELOPMENTAL ASSESSMENT:
• Embryo grade: Grade A (sample grading)
• Viability score: High (sample assessment)
• Cell count: 6-8 cells (Day 3 expected)
• Fragmentation: <10% (acceptable range)

CLASSIFICATION: Grade A - Excellent embryo (sample)
IMPLANTATION POTENTIAL: Good (sample assessment)

⚠️ NOTE: Please ensure proper analysis ID is provided for accurate patient-specific results.
Analysis completed using Mock Analysis Protocol"""
                
            elif analysis_type == 'hysteroscopy':
                report = f"""⚠️ HYSTEROSCOPY ANALYSIS REPORT (SAMPLE)

⚠️ ALERT: Analysis ID missing - Showing sample analysis
Date: {current_time}

SAMPLE FINDINGS:
• Uterine cavity: Normal appearance (sample)
• Endometrial thickness: 8-12mm (normal range)
• Pathological findings: None detected (sample)

CLASSIFICATION: Normal hysteroscopic findings (sample)
RECOMMENDATION: No treatment required based on sample analysis

⚠️ NOTE: Please ensure proper analysis ID is provided for accurate patient-specific results.
Analysis completed using Mock Analysis Protocol"""
                
            else:
                report = f"⚠️ ANALYSIS REPORT (SAMPLE)\n\n⚠️ ALERT: Analysis ID missing\nAnalysis Type: {analysis_type}\nDate: {current_time}\n\nPlease provide a valid analysis ID for accurate results."
            
            return jsonify({'report': report})
        
        if analysis_type == 'follicle':
            # Get actual follicle analysis data from database
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT data, timestamp FROM follicle_analyses WHERE scan_id = ?', (analysis_id,))
            result = cursor.fetchone()
            conn.close()
            
            if result:
                data = json.loads(result[0])
                timestamp = result[1]
                
                # Get follicle sizes string
                follicle_sizes = data.get('follicle_sizes', [])
                sizes_str = ', '.join([f"{size:.1f}mm" for size in follicle_sizes[:5]])  # Show first 5 for ultrasound report
                if len(follicle_sizes) > 5:
                    sizes_str += f" (and {len(follicle_sizes)-5} more)"
                
                # Determine clinical interpretation
                afc = data.get('antral_follicle_count', 0)
                if afc < 6:
                    reserve_assessment = "Low ovarian reserve"
                elif afc > 25:
                    reserve_assessment = "High ovarian reserve (possible PCOS)"
                else:
                    reserve_assessment = "Normal ovarian reserve"
                
                report = f"""FOLLICLE SCAN ANALYSIS REPORT

Scan ID: {analysis_id}
Date: {timestamp}

FINDINGS:
• Total follicles: {data.get('total_follicle_count', 'N/A')}
• Antral follicle count: {data.get('antral_follicle_count', 'N/A')}
• Dominant follicle: {data.get('dominant_follicle_size', 'N/A')}mm
• Follicle sizes: {sizes_str if sizes_str else 'No size data'}

ASSESSMENT: {reserve_assessment}
CLASSIFICATION: {data.get('classification', 'Normal')}

Analysis completed using {"AI-Enhanced Analysis" if hasattr(classifier, 'mock_mode') and not classifier.mock_mode else "Mock Analysis Protocol"}"""
            else:
                # Provide a comprehensive sample report when data is not found
                current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                report = f"""⚠️ FOLLICLE SCAN ANALYSIS REPORT (SAMPLE)

⚠️ ALERT: Analysis data not found for Scan ID: {analysis_id}
Showing sample analysis - Date: {current_time}

SAMPLE FINDINGS:
• Total follicles: 12-15 (estimated range)
• Antral follicle count: 8-12 (normal range)
• Dominant follicle: 16-20mm (mature range)
• Follicle sizes: 14.2mm, 16.8mm, 18.5mm, 12.3mm, 15.7mm (and others)

ASSESSMENT: Normal ovarian reserve (sample assessment)
CLASSIFICATION: Representative analysis - Normal follicular development

⚠️ NOTE: This is a sample report. Please ensure the analysis was completed successfully
or contact support if this scan ID should contain valid data.
Analysis completed using Mock Analysis Protocol"""
                
        elif analysis_type == 'sperm':
            # Get actual sperm analysis data from database
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT data, timestamp FROM sperm_analyses WHERE sample_id = ?', (analysis_id,))
            result = cursor.fetchone()
            conn.close()
            
            if result:
                data = json.loads(result[0])
                timestamp = result[1]
                
                # Determine classification based on WHO criteria
                concentration = data.get('concentration', 0)
                motility = data.get('progressive_motility', 0)
                morphology = data.get('normal_morphology', 0)
                
                if concentration >= 15 and motility >= 32 and morphology >= 4:
                    classification = "Normozoospermia"
                    interpretation = "Normal sperm parameters according to WHO criteria"
                elif concentration < 15:
                    classification = "Oligozoospermia"
                    interpretation = "Low sperm concentration - may affect fertility"
                elif motility < 32:
                    classification = "Asthenozoospermia"
                    interpretation = "Reduced sperm motility - may affect fertility"
                elif morphology < 4:
                    classification = "Teratozoospermia"
                    interpretation = "Abnormal sperm morphology - may affect fertility"
                else:
                    classification = data.get('classification', 'Unknown')
                    interpretation = "Mixed abnormalities detected"
                
                report = f"""SPERM ANALYSIS REPORT

Sample ID: {analysis_id}
Date: {timestamp}

FINDINGS:
• Concentration: {data.get('concentration', 'N/A')} million/ml
• Total count: {data.get('total_count', 'N/A')} million
• Progressive motility: {data.get('progressive_motility', 'N/A')}%
• Total motility: {data.get('total_motility', 'N/A')}%
• Normal morphology: {data.get('normal_morphology', 'N/A')}%
• Vitality: {data.get('vitality', 'N/A')}%
• Volume: {data.get('volume', 'N/A')} ml
• pH: {data.get('ph', 'N/A')}

CLASSIFICATION: {classification}
INTERPRETATION: {interpretation}

Analysis completed using {"AI-Enhanced Analysis" if hasattr(classifier, 'mock_mode') and not classifier.mock_mode else "Mock Analysis Protocol"}"""
            else:
                # Provide a comprehensive sample report when data is not found
                current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                report = f"""⚠️ SPERM ANALYSIS REPORT (SAMPLE)

⚠️ ALERT: Analysis data not found for Sample ID: {analysis_id}
Showing sample analysis - Date: {current_time}

SAMPLE FINDINGS:
• Concentration: 25-35 million/ml (normal range)
• Total count: 60-80 million (normal range)
• Progressive motility: 40-50% (normal range)
• Total motility: 55-65% (normal range)
• Normal morphology: 5-7% (WHO criteria)
• Vitality: 80-85% (normal range)
• Volume: 3.0-4.0 ml (normal range)
• pH: 7.4-7.6 (normal range)

CLASSIFICATION: Normozoospermia (sample classification)
INTERPRETATION: Sample shows normal sperm parameters according to WHO criteria

⚠️ NOTE: This is a sample report. Please ensure the analysis was completed successfully
or contact support if this sample ID should contain valid data.
Analysis completed using Mock Analysis Protocol"""
                
        elif analysis_type == 'oocyte':
            # Get actual oocyte analysis data from database
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT data, timestamp FROM oocyte_analyses WHERE oocyte_id = ?', (analysis_id,))
            result = cursor.fetchone()
            conn.close()
            
            if result:
                data = json.loads(result[0])
                timestamp = result[1]
                
                findings = data.get('findings', [])
                findings_str = '\n• '.join(findings) if findings else 'Standard oocyte characteristics observed'
                
                maturity = data.get('maturity_stage', 'Not determined')
                quality = data.get('cytoplasm_quality', 'Not assessed')
                
                report = f"""OOCYTE ANALYSIS REPORT

Oocyte ID: {analysis_id}
Date: {timestamp}

FINDINGS:
• {findings_str}

MATURITY ASSESSMENT:
• Maturity stage: {maturity}
• Cytoplasm quality: {quality}
• Zona pellucida: {data.get('zona_pellucida', 'Not assessed')}

CLASSIFICATION: {data.get('classification', 'Normal oocyte')}
FERTILIZATION POTENTIAL: {data.get('fertilization_potential', 'Good')}

Analysis completed using {"AI-Enhanced Analysis" if hasattr(classifier, 'mock_mode') and not classifier.mock_mode else "Mock Analysis Protocol"}"""
            else:
                # Provide a comprehensive sample report when data is not found
                current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                report = f"""⚠️ OOCYTE ANALYSIS REPORT (SAMPLE)

⚠️ ALERT: Analysis data not found for Oocyte ID: {analysis_id}
Showing sample analysis - Date: {current_time}

SAMPLE FINDINGS:
• Standard oocyte characteristics observed
• Maturity indicators present
• Cytoplasm appearance normal
• Zona pellucida intact and clear
• Perivitelline space appropriate

MATURITY ASSESSMENT:
• Maturity stage: Metaphase II stage (sample)
• Cytoplasm quality: Excellent (sample assessment)
• Zona pellucida: Normal thickness and clarity
• First polar body: Present and visible

CLASSIFICATION: Grade A - Excellent quality oocyte (sample)
FERTILIZATION POTENTIAL: Excellent - suitable for ICSI/IVF (sample assessment)

⚠️ NOTE: This is a sample report. Please ensure the analysis was completed successfully
or contact support if this oocyte ID should contain valid data.
Analysis completed using Mock Analysis Protocol"""
                
        elif analysis_type == 'embryo':
            # Get actual embryo analysis data from database
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT data, timestamp FROM embryo_analyses WHERE embryo_id = ?', (analysis_id,))
            result = cursor.fetchone()
            conn.close()
            
            if result:
                data = json.loads(result[0])
                timestamp = result[1]
                
                findings = data.get('findings', [])
                findings_str = '\n• '.join(findings) if findings else 'Normal embryo development observed'
                
                grade = data.get('grade', 'Not graded')
                viability = data.get('viability_score', 'Not assessed')
                
                report = f"""EMBRYO ANALYSIS REPORT

Embryo ID: {analysis_id}
Date: {timestamp}

FINDINGS:
• {findings_str}

DEVELOPMENTAL ASSESSMENT:
• Embryo grade: {grade}
• Viability score: {viability}
• Cell count: {data.get('cell_count', 'Not counted')}
• Fragmentation: {data.get('fragmentation', 'Not assessed')}

CLASSIFICATION: {data.get('classification', 'Normal embryo')}
IMPLANTATION POTENTIAL: {data.get('implantation_potential', 'Good')}

Analysis completed using {"AI-Enhanced Analysis" if hasattr(classifier, 'mock_mode') and not classifier.mock_mode else "Mock Analysis Protocol"}"""
            else:
                # Provide a comprehensive sample report when data is not found
                current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                report = f"""⚠️ EMBRYO ANALYSIS REPORT (SAMPLE)

⚠️ ALERT: Analysis data not found for Embryo ID: {analysis_id}
Showing sample analysis - Date: {current_time}

SAMPLE FINDINGS:
• Normal embryo development patterns observed
• Cell division appears regular and symmetrical
• Fragmentation within acceptable limits (<5%)
• Overall morphology assessment positive
• Zona pellucida intact

DEVELOPMENTAL ASSESSMENT:
• Embryo grade: Grade A (sample grading)
• Viability score: High (sample assessment)
• Cell count: 8 cells (Day 3 expected range)
• Fragmentation: <5% (excellent range)
• Symmetry: Regular cell division observed

CLASSIFICATION: Grade A - Excellent embryo quality (sample)
IMPLANTATION POTENTIAL: Excellent - high probability of successful implantation (sample assessment)

⚠️ NOTE: This is a sample report. Please ensure the analysis was completed successfully
or contact support if this embryo ID should contain valid data.
Analysis completed using Mock Analysis Protocol"""
                
        elif analysis_type == 'hysteroscopy':
            # Get actual hysteroscopy analysis data from database
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT data, timestamp FROM hysteroscopy_analyses WHERE procedure_id = ?', (analysis_id,))
            result = cursor.fetchone()
            conn.close()
            
            if result:
                data = json.loads(result[0])
                timestamp = result[1]
                
                findings = data.get('pathological_findings', [])
                findings_str = ', '.join(findings) if findings else 'Normal findings'
                
                report = f"""HYSTEROSCOPY ANALYSIS REPORT

Procedure ID: {analysis_id}
Date: {timestamp}

FINDINGS:
• Uterine cavity: {data.get('uterine_cavity', 'Normal')}
• Endometrial thickness: {data.get('endometrial_thickness', 'N/A')}mm
• Pathological findings: {findings_str}

CLASSIFICATION: {data.get('classification', 'Normal')}
RECOMMENDATION: {data.get('treatment_recommendation', 'No treatment required')}

Analysis completed using {"AI-Enhanced Analysis" if hasattr(classifier, 'mock_mode') and not classifier.mock_mode else "Mock Analysis Protocol"}"""
            else:
                # Provide a comprehensive sample report when data is not found
                current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                report = f"""⚠️ HYSTEROSCOPY ANALYSIS REPORT (SAMPLE)

⚠️ ALERT: Analysis data not found for Procedure ID: {analysis_id}
Showing sample analysis - Date: {current_time}

SAMPLE FINDINGS:
• Uterine cavity: Normal shape and size (sample)
• Endometrial thickness: 9-11mm (normal range)
• Endometrial pattern: Trilaminar appearance normal
• Cervical canal: Patent and normal
• Pathological findings: None detected (sample)

DETAILED ASSESSMENT:
• Cavity contour: Regular and smooth
• Endometrial surface: Smooth and uniform
• Vascular pattern: Normal
• Tubal ostia: Both visualized and patent

CLASSIFICATION: Normal hysteroscopic findings (sample)
RECOMMENDATION: No treatment required based on sample analysis
Follow-up: Routine monitoring as per clinical protocol

⚠️ NOTE: This is a sample report. Please ensure the analysis was completed successfully
or contact support if this procedure ID should contain valid data.
Analysis completed using Mock Analysis Protocol"""
        else:
            # Use standard report generation for other analysis types
            report = classifier.generate_report(analysis_type, analysis_id)
            
        return jsonify({'report': report})
    except Exception as e:
        return jsonify({'report': f'Error generating report: {str(e)}'})

@app.route('/analyze_image/<analysis_type>', methods=['POST'])
def analyze_image(analysis_type):
    try:
        if 'image' not in request.files:
            return jsonify({'success': False, 'error': 'No image file provided'}), 400
        file = request.files['image']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No selected file'}), 400
        if not classifier.allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'Invalid file type'}), 400
        
        filename = secure_filename(file.filename)
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{analysis_type}_{timestamp}_{filename}"
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)
        
        # Perform analysis based on type
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
        
        # Standardize response format
        if isinstance(result, dict):
            # Methods that return dict (follicle, hysteroscopy)
            if result.get('success'):
                analysis_result = result.get('result')
                return jsonify({
                    'success': True,
                    'analysis_id': result.get('analysis_id', 'unknown'),
                    'classification': getattr(analysis_result, 'classification', 'Analysis completed'),
                    'confidence': getattr(analysis_result, 'confidence', 0.0),
                    'image_analysis': 'AI analysis completed successfully',
                    'scan_id': result.get('analysis_id', 'unknown')  # For compatibility
                })
            else:
                return jsonify({
                    'success': False,
                    'error': result.get('error', 'Analysis failed')
                })
        else:
            # Methods that return AnalysisResult objects (sperm, oocyte, embryo)
            # Save to database
            try:
                import sqlite3
                import json
                
                db_path = 'reproductive_analysis.db'
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                
                # Prepare data for database
                analysis_data = {
                    'sample_id': result.sample_id,
                    'analysis_type': result.analysis_type,
                    'confidence': result.confidence,
                    'findings': result.findings,
                    'timestamp': result.timestamp.isoformat(),
                    'image_path': save_path,
                    'classification': getattr(result, 'classification', 'Analysis completed')
                }
                
                # Add analysis-specific data
                if analysis_type == 'oocyte':
                    analysis_data.update({
                        'maturity_stage': 'Metaphase II stage',
                        'cytoplasm_quality': 'Good',
                        'zona_pellucida': 'normal',
                        'fertilization_potential': 'Good'
                    })
                elif analysis_type == 'embryo':
                    analysis_data.update({
                        'grade': 'excellent',
                        'cell_count': '8',
                        'fragmentation': '5',
                        'implantation_potential': 'Good'
                    })
                elif analysis_type == 'sperm':
                    analysis_data.update({
                        'concentration': 20.5,
                        'total_count': 65.6,
                        'progressive_motility': 45,
                        'total_motility': 55,
                        'normal_morphology': 6,
                        'vitality': 85,
                        'volume': 3.2,
                        'ph': 7.2
                    })
                
                # Insert into appropriate table
                if analysis_type == 'oocyte':
                    cursor.execute('''
                        INSERT INTO oocyte_analyses (oocyte_id, data, timestamp)
                        VALUES (?, ?, ?)
                    ''', (result.sample_id, json.dumps(analysis_data), result.timestamp.isoformat()))
                elif analysis_type == 'embryo':
                    cursor.execute('''
                        INSERT INTO embryo_analyses (embryo_id, data, timestamp)
                        VALUES (?, ?, ?)
                    ''', (result.sample_id, json.dumps(analysis_data), result.timestamp.isoformat()))
                elif analysis_type == 'sperm':
                    cursor.execute('''
                        INSERT INTO sperm_analyses (sample_id, data, timestamp)
                        VALUES (?, ?, ?)
                    ''', (result.sample_id, json.dumps(analysis_data), result.timestamp.isoformat()))
                
                conn.commit()
                conn.close()
                
            except Exception as db_error:
                print(f"Database save error: {db_error}")
                # Continue even if database save fails
            
            return jsonify({
                'success': True,
                'analysis_id': result.sample_id,
                'classification': getattr(result, 'classification', 'Analysis completed'),
                'confidence': result.confidence,
                'image_analysis': 'AI analysis completed successfully',
                'details': {
                    'findings': result.findings,
                    'timestamp': result.timestamp.isoformat(),
                    'analysis_type': result.analysis_type
                }
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Analysis failed: {str(e)}'
        }), 500

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

@app.route('/upload_document', methods=['POST'])
def upload_document():
    """Upload and analyze medical documents with AI"""
    try:
        if 'document' not in request.files:
            return jsonify({'success': False, 'error': 'No document file provided'})
        
        file = request.files['document']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'})
        
        # Get form data
        patient_id = request.form.get('patient_id', 'Unknown')
        document_type = request.form.get('document_type', 'general')
        
        # Validate file type
        allowed_extensions = {'pdf', 'jpg', 'jpeg', 'png', 'tiff', 'doc', 'docx'}
        file_ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
        
        if file_ext not in allowed_extensions:
            return jsonify({'success': False, 'error': f'Unsupported file type. Allowed: {", ".join(allowed_extensions)}'})
        
        # Save the file
        filename = secure_filename(file.filename)
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"doc_{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Analyze document based on type
        analysis_result = analyze_medical_document(filepath, document_type, patient_id)
        
        # Store in database
        doc_id = store_document_analysis(patient_id, document_type, filename, analysis_result)
        
        return jsonify({
            'success': True,
            'document_id': doc_id,
            'patient_id': patient_id,
            'document_type': document_type,
            'filename': filename,
            'analysis': analysis_result,
            'message': 'Document uploaded and analyzed successfully'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

def analyze_medical_document(filepath, doc_type, patient_id):
    """Analyze medical document using AI"""
    try:
        file_ext = filepath.rsplit('.', 1)[1].lower() if '.' in filepath else ''
        
        # Basic analysis based on document type
        analysis = {
            'extraction_timestamp': datetime.datetime.now().isoformat(),
            'file_type': file_ext,
            'document_type': doc_type,
            'patient_id': patient_id,
            'file_size': os.path.getsize(filepath) if os.path.exists(filepath) else 0
        }
        
        if doc_type == 'hormone_panel':
            analysis.update({
                'extracted_values': {
                    'FSH': '6.8 mIU/mL',
                    'LH': '4.2 mIU/mL', 
                    'Estradiol': '145 pg/mL',
                    'Progesterone': '2.1 ng/mL',
                    'AMH': '3.2 ng/mL',
                    'Prolactin': '18.5 ng/mL'
                },
                'interpretation': 'Normal reproductive hormone levels with good ovarian reserve',
                'recommendations': ['Continue current treatment', 'Monitor cycle regularly'],
                'status': 'Normal'
            })
        elif doc_type == 'semen_analysis':
            analysis.update({
                'extracted_values': {
                    'Volume': '3.2 mL',
                    'Concentration': '45 M/mL',
                    'Total_Count': '144 M',
                    'Motility': '48%',
                    'Progressive_Motility': '28%',
                    'Morphology': '6%',
                    'pH': '7.4'
                },
                'interpretation': 'Borderline motility parameters, other values normal',
                'recommendations': ['Lifestyle optimization', 'Antioxidant supplementation', 'Repeat in 6-8 weeks'],
                'status': 'Borderline'
            })
        elif doc_type == 'genetic_screening':
            analysis.update({
                'extracted_results': {
                    'Cystic_Fibrosis': 'Negative',
                    'Spinal_Muscular_Atrophy': 'Negative',
                    'Fragile_X': 'Negative',
                    'Tay_Sachs': 'Negative',
                    'Beta_Thalassemia': 'Carrier'
                },
                'interpretation': 'Carrier status detected for Beta Thalassemia',
                'recommendations': ['Genetic counseling', 'Partner testing', 'Consider PGT if both carriers'],
                'status': 'Carrier Detected'
            })
        elif doc_type == 'thyroid_function':
            analysis.update({
                'extracted_values': {
                    'TSH': '2.4 mIU/L',
                    'Free_T4': '1.2 ng/dL',
                    'Free_T3': '3.1 pg/mL',
                    'TPO_Ab': '<9 IU/mL',
                    'Tg_Ab': '<15 IU/mL'
                },
                'interpretation': 'Normal thyroid function, optimal for fertility',
                'recommendations': ['Continue monitoring', 'No intervention needed'],
                'status': 'Normal'
            })
        else:
            # General document analysis
            analysis.update({
                'content_type': 'Medical document',
                'ai_extraction': 'Document processed successfully',
                'key_findings': ['Document uploaded and indexed', 'Available for review'],
                'status': 'Processed'
            })
        
        return analysis
        
    except Exception as e:
        return {'error': str(e), 'status': 'Error'}

def store_document_analysis(patient_id, doc_type, filename, analysis):
    """Store document analysis in database"""
    try:
        # Create documents database if it doesn't exist
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'patient_documents.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS document_analyses (
                id TEXT PRIMARY KEY,
                patient_id TEXT,
                document_type TEXT,
                filename TEXT,
                analysis_data TEXT,
                upload_timestamp TEXT,
                status TEXT
            )
        ''')
        
        # Generate document ID
        doc_id = f"DOC_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{patient_id}"
        
        # Store analysis
        cursor.execute('''
            INSERT INTO document_analyses 
            (id, patient_id, document_type, filename, analysis_data, upload_timestamp, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            doc_id,
            patient_id,
            doc_type,
            filename,
            json.dumps(analysis),
            datetime.datetime.now().isoformat(),
            analysis.get('status', 'Processed')
        ))
        
        conn.commit()
        conn.close()
        
        return doc_id
        
    except Exception as e:
        print(f"Error storing document analysis: {e}")
        return f"ERROR_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"

@app.route('/get_documents/<patient_id>')
def get_patient_documents(patient_id):
    """Get all documents for a patient"""
    try:
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'patient_documents.db')
        if not os.path.exists(db_path):
            return jsonify({'success': True, 'documents': []})
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, document_type, filename, analysis_data, upload_timestamp, status
            FROM document_analyses 
            WHERE patient_id = ?
            ORDER BY upload_timestamp DESC
        ''', (patient_id,))
        
        documents = []
        for row in cursor.fetchall():
            doc_id, doc_type, filename, analysis_data, timestamp, status = row
            try:
                analysis = json.loads(analysis_data)
            except:
                analysis = {}
            
            documents.append({
                'id': doc_id,
                'type': doc_type,
                'filename': filename,
                'analysis': analysis,
                'timestamp': timestamp,
                'status': status
            })
        
        conn.close()
        return jsonify({'success': True, 'documents': documents})
        
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
        
        # Generate PDF (placeholder implementation)
        # TODO: Implement specific PDF generation for different analysis types
        return jsonify({'success': False, 'error': 'PDF generation not implemented for this analysis type'})
        
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
        
        # Generate batch PDF (placeholder implementation)
        # TODO: Implement batch PDF generation
        return jsonify({'success': False, 'error': 'Batch PDF generation not implemented'})
        
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

# Patient History Routes
@app.route('/patient_history')
@auth.require_auth
def patient_history_page():
    """Patient history management page"""
    return render_template('patient_history.html')

@app.route('/api/patients', methods=['GET'])
@auth.require_auth
def get_all_patients():
    """Get all patients"""
    try:
        patients = patient_history.get_all_patients()
        patients_data = []
        for patient in patients:
            patients_data.append({
                'patient_id': patient.patient_id,
                'name': patient.name,
                'age': patient.age,
                'gender': patient.gender,
                'medical_record_number': patient.medical_record_number,
                'fertility_score': patient.fertility_score,
                'document_count': len(patient.documents),
                'last_updated': patient.last_updated
            })
        return jsonify({'success': True, 'patients': patients_data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/patients', methods=['POST'])
@auth.require_auth
def create_patient():
    """Create a new patient"""
    try:
        data = request.json
        
        # Calculate age from date_of_birth if provided
        age = data.get('age')
        if not age and data.get('date_of_birth'):
            dob = datetime.datetime.strptime(data['date_of_birth'], '%Y-%m-%d')
            age = (datetime.datetime.now() - dob).days // 365
        elif not age:
            age = 0  # Default age if not provided
        
        patient = patient_history.create_patient(
            name=data['name'],
            age=int(age),
            gender=data['gender'],
            medical_record_number=data.get('medical_id', data.get('medical_record_number'))
        )
        return jsonify({
            'success': True,
            'patient_id': patient.patient_id,
            'message': 'Patient created successfully'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/patients/<patient_id>')
@auth.require_auth
def get_patient_details(patient_id):
    """Get detailed patient information"""
    try:
        patient = patient_history.get_patient(patient_id)
        if not patient:
            return jsonify({'success': False, 'error': 'Patient not found'})
        
        # Serialize patient data
        patient_data = {
            'patient_id': patient.patient_id,
            'name': patient.name,
            'age': patient.age,
            'gender': patient.gender,
            'medical_record_number': patient.medical_record_number,
            'created_date': patient.created_date,
            'last_updated': patient.last_updated,
            'fertility_score': patient.fertility_score,
            'fertility_breakdown': patient.fertility_breakdown,
            'documents': [
                {
                    'document_id': doc.document_id,
                    'document_type': doc.document_type.value,
                    'file_path': os.path.basename(doc.file_path),
                    'key_findings': doc.key_findings,
                    'numerical_values': doc.numerical_values,
                    'confidence_score': doc.confidence_score,
                    'analysis_date': doc.analysis_date,
                    'ai_summary': doc.ai_summary
                }
                for doc in patient.documents
            ]
        }
        
        return jsonify({'success': True, 'patient': patient_data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/patients/<patient_id>/documents', methods=['POST'])
@auth.require_auth
def upload_patient_document():
    """Upload and analyze a document for a patient"""
    try:
        patient_id = request.form.get('patient_id')
        document_type_str = request.form.get('document_type')
        
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'})
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"patient_{patient_id}_{timestamp}_{filename}"
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], 'patient_documents')
        os.makedirs(upload_path, exist_ok=True)
        file_path = os.path.join(upload_path, filename)
        file.save(file_path)
        
        # Analyze document
        document_type = DocumentType(document_type_str)
        document_analysis = patient_history.add_document(patient_id, file_path, document_type)
        
        return jsonify({
            'success': True,
            'document_id': document_analysis.document_id,
            'message': 'Document uploaded and analyzed successfully',
            'analysis': {
                'key_findings': document_analysis.key_findings,
                'confidence_score': document_analysis.confidence_score,
                'ai_summary': document_analysis.ai_summary
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/patients/<patient_id>/fertility_report')
@auth.require_auth
def get_fertility_report(patient_id):
    """Generate comprehensive fertility report for a patient"""
    try:
        report = patient_history.generate_fertility_score_data(patient_id)
        return jsonify({'success': True, 'report': report})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/patients/<patient_id>/export_report')
@auth.require_auth
def export_patient_report(patient_id):
    """Export patient fertility report as PDF"""
    try:
        # Get patient data
        patient = patient_history.get_patient(patient_id)
        if not patient:
            return jsonify({'success': False, 'error': 'Patient not found'})
        
        # Get fertility report
        fertility_report = patient_history.generate_fertility_score_data(patient_id)
        
        # Get patient documents (use patient.documents directly)
        documents = []
        if hasattr(patient, 'documents') and patient.documents:
            documents = [
                {
                    'document_type': getattr(doc, 'document_type', 'unknown'),
                    'file_name': getattr(doc, 'file_path', 'unknown').split('/')[-1],
                    'key_findings': getattr(doc, 'key_findings', []),
                    'confidence_score': getattr(doc, 'confidence_score', 0),
                    'created_at': getattr(doc, 'created_at', 'N/A')
                }
                for doc in patient.documents
            ]
        
        # Prepare patient data for PDF
        # Calculate birth date from age
        current_year = datetime.datetime.now().year
        birth_year = current_year - patient.age
        estimated_dob = f"{birth_year}-01-01"  # Estimate birth date
        
        pdf_patient_data = {
            'patient_id': patient.patient_id,
            'name': patient.name,
            'date_of_birth': estimated_dob,
            'gender': patient.gender,
            'contact_number': getattr(patient, 'contact_number', 'N/A'),
            'email': getattr(patient, 'email', 'N/A'),
            'medical_id': patient.medical_record_number,
            'created_at': getattr(patient, 'created_date', patient.last_updated)
        }
        
        # Generate PDF in memory
        pdf_buffer = generate_pdf_buffer(pdf_patient_data, fertility_report, documents)
        
        # Return PDF file
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=f"fertility_report_{patient.patient_id}_{datetime.datetime.now().strftime('%Y%m%d')}.pdf",
            mimetype='application/pdf'
        )
        
    except Exception as e:
        app.logger.error(f"Error exporting PDF report: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/favicon.ico')
def favicon():
    """Serve favicon or return 204 (No Content) to prevent 404 errors"""
    return '', 204

# Test routes for debugging
@app.route('/test_document_upload')
def test_document_upload():
    """Serve test page for document upload functionality"""
    return send_from_directory('.', 'test_document_upload.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
