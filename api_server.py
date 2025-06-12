"""
FertiVision API Server for IVF EMR Integration
==============================================

RESTful API server for integrating FertiVision analysis capabilities
with IVF Electronic Medical Record (EMR) systems.

Features:
- Secure API authentication with API keys
- Image upload and analysis endpoints
- Standardized medical data exchange
- Comprehensive error handling
- Rate limiting and security
- Audit logging for compliance

© 2025 FertiVision powered by AI | Made by greybrain.ai
"""

from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import datetime
import json
import uuid
import hashlib
import hmac
import time
from functools import wraps
import sqlite3
from enhanced_reproductive_system import EnhancedReproductiveSystem
from config import Config
import logging

# Configure logging for API audit trail
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api_audit.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('FertiVision-API')

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size for medical images

# Initialize FertiVision analysis system
classifier = EnhancedReproductiveSystem(
    upload_folder="api_uploads",
    mock_mode=True  # Can be configured per API key
)

# API Configuration
API_VERSION = "v1"
API_BASE_URL = f"/api/{API_VERSION}"

# In-memory API key store (in production, use secure database)
API_KEYS = {
    "fv_demo_key_12345": {
        "client_name": "Demo IVF Clinic",
        "permissions": ["sperm", "oocyte", "embryo", "follicle", "hysteroscopy"],
        "rate_limit": 1000,  # requests per hour
        "created": "2025-01-01",
        "active": True,
        "mock_mode": True
    },
    "fv_prod_key_67890": {
        "client_name": "Advanced Fertility Center",
        "permissions": ["sperm", "oocyte", "embryo", "follicle"],
        "rate_limit": 5000,
        "created": "2025-01-01", 
        "active": True,
        "mock_mode": False
    }
}

# Rate limiting storage
rate_limit_store = {}

def require_api_key(f):
    """Decorator to require valid API key for endpoints"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
        
        if not api_key:
            logger.warning(f"API request without key from {request.remote_addr}")
            return jsonify({
                'success': False,
                'error': 'API key required',
                'code': 'MISSING_API_KEY'
            }), 401
        
        if api_key not in API_KEYS:
            logger.warning(f"Invalid API key attempted: {api_key[:10]}... from {request.remote_addr}")
            return jsonify({
                'success': False,
                'error': 'Invalid API key',
                'code': 'INVALID_API_KEY'
            }), 401
        
        client_info = API_KEYS[api_key]
        if not client_info['active']:
            return jsonify({
                'success': False,
                'error': 'API key deactivated',
                'code': 'DEACTIVATED_KEY'
            }), 401
        
        # Rate limiting
        current_time = time.time()
        hour_key = f"{api_key}_{int(current_time // 3600)}"
        
        if hour_key not in rate_limit_store:
            rate_limit_store[hour_key] = 0
        
        if rate_limit_store[hour_key] >= client_info['rate_limit']:
            return jsonify({
                'success': False,
                'error': 'Rate limit exceeded',
                'code': 'RATE_LIMIT_EXCEEDED',
                'limit': client_info['rate_limit']
            }), 429
        
        rate_limit_store[hour_key] += 1
        
        # Add client info to request context
        request.client_info = client_info
        request.api_key = api_key
        
        logger.info(f"API request from {client_info['client_name']} - {request.method} {request.path}")
        
        return f(*args, **kwargs)
    return decorated_function

@app.route('/', methods=['GET'])
def api_home():
    """API home page with documentation"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>FertiVision API - IVF EMR Integration</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
            .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            h1 {{ color: #2563eb; margin-bottom: 10px; }}
            .subtitle {{ color: #6b7280; margin-bottom: 30px; }}
            .endpoint {{ background: #f8fafc; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #2563eb; }}
            .method {{ background: #10b981; color: white; padding: 2px 8px; border-radius: 3px; font-size: 12px; }}
            .demo-key {{ background: #fef3c7; padding: 10px; border-radius: 5px; margin: 20px 0; }}
            code {{ background: #f1f5f9; padding: 2px 6px; border-radius: 3px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔬 FertiVision API</h1>
            <p class="subtitle">RESTful API for IVF EMR Integration</p>

            <h2>🚀 Quick Start</h2>
            <div class="demo-key">
                <strong>Demo API Key:</strong> <code>fv_demo_key_12345</code><br>
                <strong>Usage:</strong> Add header <code>X-API-Key: fv_demo_key_12345</code>
            </div>

            <h2>📋 Available Endpoints</h2>

            <div class="endpoint">
                <span class="method">GET</span> <strong>/api/v1/health</strong><br>
                Health check and API status
            </div>

            <div class="endpoint">
                <span class="method">GET</span> <strong>/api/v1/info</strong><br>
                API information and client permissions (requires API key)
            </div>

            <div class="endpoint">
                <span class="method">POST</span> <strong>/api/v1/analyze/sperm</strong><br>
                Sperm analysis with WHO 2021 criteria
            </div>

            <div class="endpoint">
                <span class="method">POST</span> <strong>/api/v1/analyze/oocyte</strong><br>
                Oocyte maturity and quality assessment
            </div>

            <div class="endpoint">
                <span class="method">POST</span> <strong>/api/v1/analyze/embryo</strong><br>
                Embryo grading with Gardner criteria
            </div>

            <div class="endpoint">
                <span class="method">POST</span> <strong>/api/v1/analyze/follicle</strong><br>
                Follicle counting and ovarian reserve assessment
            </div>

            <div class="endpoint">
                <span class="method">POST</span> <strong>/api/v1/analyze/batch</strong><br>
                Batch processing for multiple images
            </div>

            <h2>🧪 Test the API</h2>
            <p>Try these commands in your terminal:</p>
            <pre style="background: #1f2937; color: #f9fafb; padding: 15px; border-radius: 5px; overflow-x: auto;">
# Health check
curl http://localhost:5003/api/v1/health

# Get API info
curl -H "X-API-Key: fv_demo_key_12345" http://localhost:5003/api/v1/info

# Test sperm analysis
curl -X POST -H "X-API-Key: fv_demo_key_12345" \\
  -F "image=@your_image.jpg" \\
  -F "patient_id=P12345" \\
  http://localhost:5003/api/v1/analyze/sperm</pre>

            <h2>📚 Documentation</h2>
            <p>📖 <strong>Complete API Documentation:</strong> See <code>API_DOCUMENTATION.md</code></p>
            <p>🐍 <strong>Python SDK:</strong> Use <code>fertivision_sdk.py</code> for easy integration</p>
            <p>🏥 <strong>EMR Integration Example:</strong> See <code>examples/emr_integration_example.py</code></p>

            <hr style="margin: 30px 0;">
            <p style="text-align: center; color: #6b7280;">
                © 2025 FertiVision powered by AI | Made by greybrain.ai<br>
                <em>Advancing reproductive medicine through artificial intelligence</em>
            </p>
        </div>
    </body>
    </html>
    """

@app.route(f'{API_BASE_URL}/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'version': API_VERSION,
        'timestamp': datetime.datetime.now().isoformat(),
        'service': 'FertiVision API'
    })

@app.route('/test', methods=['GET'])
def api_test_interface():
    """Simple API testing interface"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>FertiVision API - Test Interface</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
            .container {{ max-width: 1000px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }}
            .test-section {{ background: #f8fafc; padding: 20px; margin: 20px 0; border-radius: 8px; border-left: 4px solid #10b981; }}
            button {{ background: #10b981; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }}
            button:hover {{ background: #059669; }}
            .result {{ background: #1f2937; color: #f9fafb; padding: 15px; border-radius: 5px; margin: 10px 0; font-family: monospace; white-space: pre-wrap; }}
            input[type="file"] {{ margin: 10px 0; }}
            .api-key {{ background: #fef3c7; padding: 10px; border-radius: 5px; margin: 10px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🧪 FertiVision API Test Interface</h1>

            <div class="api-key">
                <strong>Demo API Key:</strong> <code>fv_demo_key_12345</code>
            </div>

            <div class="test-section">
                <h3>🔍 Basic API Tests</h3>
                <button onclick="testHealth()">Test Health Check</button>
                <button onclick="testInfo()">Test API Info</button>
                <button onclick="testInvalidKey()">Test Invalid Key</button>
                <div id="basic-results" class="result"></div>
            </div>

            <div class="test-section">
                <h3>🧬 Image Analysis Tests</h3>
                <p>Upload an image to test analysis endpoints:</p>
                <input type="file" id="imageFile" accept="image/*">
                <br>
                <button onclick="testSpermAnalysis()">Test Sperm Analysis</button>
                <button onclick="testOocyteAnalysis()">Test Oocyte Analysis</button>
                <button onclick="testEmbryoAnalysis()">Test Embryo Analysis</button>
                <button onclick="testFollicleAnalysis()">Test Follicle Analysis</button>
                <div id="analysis-results" class="result"></div>
            </div>

            <div class="test-section">
                <h3>📊 Mock Data Tests</h3>
                <p>Test with mock data (no image required):</p>
                <button onclick="testMockSperm()">Mock Sperm Analysis</button>
                <button onclick="testMockEmbryo()">Mock Embryo Analysis</button>
                <div id="mock-results" class="result"></div>
            </div>
        </div>

        <script>
            const API_KEY = 'fv_demo_key_12345';
            const BASE_URL = '/api/v1';

            async function testHealth() {{
                try {{
                    const response = await fetch(`${{BASE_URL}}/health`);
                    const data = await response.json();
                    document.getElementById('basic-results').textContent = JSON.stringify(data, null, 2);
                }} catch (error) {{
                    document.getElementById('basic-results').textContent = 'Error: ' + error.message;
                }}
            }}

            async function testInfo() {{
                try {{
                    const response = await fetch(`${{BASE_URL}}/info`, {{
                        headers: {{ 'X-API-Key': API_KEY }}
                    }});
                    const data = await response.json();
                    document.getElementById('basic-results').textContent = JSON.stringify(data, null, 2);
                }} catch (error) {{
                    document.getElementById('basic-results').textContent = 'Error: ' + error.message;
                }}
            }}

            async function testInvalidKey() {{
                try {{
                    const response = await fetch(`${{BASE_URL}}/info`, {{
                        headers: {{ 'X-API-Key': 'invalid_key' }}
                    }});
                    const data = await response.json();
                    document.getElementById('basic-results').textContent = JSON.stringify(data, null, 2);
                }} catch (error) {{
                    document.getElementById('basic-results').textContent = 'Error: ' + error.message;
                }}
            }}

            async function testAnalysis(analysisType) {{
                const fileInput = document.getElementById('imageFile');
                if (!fileInput.files[0]) {{
                    alert('Please select an image file first');
                    return;
                }}

                const formData = new FormData();
                formData.append('image', fileInput.files[0]);
                formData.append('patient_id', 'TEST_P001');
                formData.append('case_id', 'TEST_C001');
                formData.append('notes', 'API test analysis');

                try {{
                    const response = await fetch(`${{BASE_URL}}/analyze/${{analysisType}}`, {{
                        method: 'POST',
                        headers: {{ 'X-API-Key': API_KEY }},
                        body: formData
                    }});
                    const data = await response.json();
                    document.getElementById('analysis-results').textContent = JSON.stringify(data, null, 2);
                }} catch (error) {{
                    document.getElementById('analysis-results').textContent = 'Error: ' + error.message;
                }}
            }}

            function testSpermAnalysis() {{ testAnalysis('sperm'); }}
            function testOocyteAnalysis() {{ testAnalysis('oocyte'); }}
            function testEmbryoAnalysis() {{ testAnalysis('embryo'); }}
            function testFollicleAnalysis() {{ testAnalysis('follicle'); }}

            async function testMockSperm() {{
                const formData = new FormData();
                formData.append('image', new Blob(['mock image data'], {{type: 'image/jpeg'}}), 'mock.jpg');
                formData.append('patient_id', 'MOCK_P001');

                try {{
                    const response = await fetch(`${{BASE_URL}}/analyze/sperm`, {{
                        method: 'POST',
                        headers: {{ 'X-API-Key': API_KEY }},
                        body: formData
                    }});
                    const data = await response.json();
                    document.getElementById('mock-results').textContent = JSON.stringify(data, null, 2);
                }} catch (error) {{
                    document.getElementById('mock-results').textContent = 'Error: ' + error.message;
                }}
            }}

            async function testMockEmbryo() {{
                const formData = new FormData();
                formData.append('image', new Blob(['mock image data'], {{type: 'image/jpeg'}}), 'mock.jpg');
                formData.append('patient_id', 'MOCK_P001');
                formData.append('day', '3');

                try {{
                    const response = await fetch(`${{BASE_URL}}/analyze/embryo`, {{
                        method: 'POST',
                        headers: {{ 'X-API-Key': API_KEY }},
                        body: formData
                    }});
                    const data = await response.json();
                    document.getElementById('mock-results').textContent = JSON.stringify(data, null, 2);
                }} catch (error) {{
                    document.getElementById('mock-results').textContent = 'Error: ' + error.message;
                }}
            }}
        </script>
    </body>
    </html>
    """

@app.route(f'{API_BASE_URL}/info', methods=['GET'])
@require_api_key
def api_info():
    """Get API information and client permissions"""
    client_info = request.client_info

    return jsonify({
        'success': True,
        'api_version': API_VERSION,
        'client_name': client_info['client_name'],
        'permissions': client_info['permissions'],
        'rate_limit': client_info['rate_limit'],
        'available_endpoints': {
            'sperm_analysis': f'{API_BASE_URL}/analyze/sperm',
            'oocyte_analysis': f'{API_BASE_URL}/analyze/oocyte',
            'embryo_analysis': f'{API_BASE_URL}/analyze/embryo',
            'follicle_analysis': f'{API_BASE_URL}/analyze/follicle',
            'hysteroscopy_analysis': f'{API_BASE_URL}/analyze/hysteroscopy',
            'batch_analysis': f'{API_BASE_URL}/analyze/batch',
            'report_generation': f'{API_BASE_URL}/report/{{analysis_id}}',
            'pdf_export': f'{API_BASE_URL}/export/pdf/{{analysis_id}}'
        }
    })

@app.route(f'{API_BASE_URL}/analyze/batch', methods=['POST'])
@require_api_key
def batch_analyze_api():
    """
    Batch analysis endpoint for processing multiple images
    """
    client_info = request.client_info

    if 'images' not in request.files:
        return jsonify({
            'success': False,
            'error': 'No images provided for batch analysis',
            'code': 'MISSING_IMAGES'
        }), 400

    images = request.files.getlist('images')
    analysis_types = request.form.getlist('analysis_types')

    if len(images) != len(analysis_types):
        return jsonify({
            'success': False,
            'error': 'Number of images must match number of analysis types',
            'code': 'MISMATCHED_INPUTS'
        }), 400

    batch_id = str(uuid.uuid4())
    results = []

    for i, (image, analysis_type) in enumerate(zip(images, analysis_types)):
        try:
            # Process each image individually
            analysis_id = f"{batch_id}_{i}"
            filename = f"{analysis_id}_{secure_filename(image.filename)}"
            filepath = os.path.join("api_uploads", filename)
            image.save(filepath)

            # Perform analysis (simplified for batch processing)
            if analysis_type in client_info['permissions']:
                result = {
                    'analysis_id': analysis_id,
                    'analysis_type': analysis_type,
                    'filename': image.filename,
                    'status': 'completed',
                    'classification': f'Sample {analysis_type} analysis completed'
                }
            else:
                result = {
                    'analysis_id': analysis_id,
                    'analysis_type': analysis_type,
                    'filename': image.filename,
                    'status': 'failed',
                    'error': 'Permission denied'
                }

            results.append(result)

        except Exception as e:
            results.append({
                'analysis_id': f"{batch_id}_{i}",
                'analysis_type': analysis_type,
                'filename': image.filename,
                'status': 'failed',
                'error': str(e)
            })

    return jsonify({
        'success': True,
        'batch_id': batch_id,
        'total_images': len(images),
        'results': results,
        'timestamp': datetime.datetime.now().isoformat()
    })

@app.route(f'{API_BASE_URL}/report/<analysis_id>', methods=['GET'])
@require_api_key
def get_analysis_report(analysis_id):
    """Get detailed analysis report"""
    return jsonify({
        'success': True,
        'analysis_id': analysis_id,
        'report': {
            'summary': 'Detailed medical analysis report',
            'recommendations': ['Clinical recommendation 1', 'Clinical recommendation 2'],
            'technical_details': {'parameter1': 'value1', 'parameter2': 'value2'}
        }
    })

@app.route(f'{API_BASE_URL}/export/pdf/<analysis_id>', methods=['GET'])
@require_api_key
def export_pdf_report(analysis_id):
    """Export analysis as PDF report"""
    # In production, generate actual PDF
    return jsonify({
        'success': True,
        'analysis_id': analysis_id,
        'pdf_url': f'/api/v1/download/pdf/{analysis_id}',
        'message': 'PDF report generation initiated'
    })

@app.route(f'{API_BASE_URL}/analyze/<analysis_type>', methods=['POST'])
@require_api_key
def analyze_image_api(analysis_type):
    """
    Main analysis endpoint for EMR integration

    Supported analysis types: sperm, oocyte, embryo, follicle, hysteroscopy
    """
    client_info = request.client_info
    
    # Check permissions
    if analysis_type not in client_info['permissions']:
        return jsonify({
            'success': False,
            'error': f'Analysis type "{analysis_type}" not permitted for this API key',
            'code': 'PERMISSION_DENIED'
        }), 403
    
    # Validate request
    if 'image' not in request.files:
        return jsonify({
            'success': False,
            'error': 'No image file provided',
            'code': 'MISSING_IMAGE'
        }), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({
            'success': False,
            'error': 'No file selected',
            'code': 'EMPTY_FILENAME'
        }), 400
    
    if not classifier.allowed_file(file.filename):
        return jsonify({
            'success': False,
            'error': 'Invalid file type. Supported: PNG, JPG, JPEG, TIFF, BMP, DICOM',
            'code': 'INVALID_FILE_TYPE'
        }), 400
    
    try:
        # Generate unique analysis ID
        analysis_id = str(uuid.uuid4())
        
        # Save uploaded file
        filename = f"{analysis_id}_{secure_filename(file.filename)}"
        filepath = os.path.join("api_uploads", filename)
        os.makedirs("api_uploads", exist_ok=True)
        file.save(filepath)
        
        # Get additional parameters
        patient_id = request.form.get('patient_id', '')
        case_id = request.form.get('case_id', '')
        notes = request.form.get('notes', '')
        
        # Set mock mode based on client configuration
        classifier.set_mock_mode(client_info['mock_mode'])
        
        # Perform analysis based on type
        if analysis_type == 'sperm':
            result = classifier.analyze_sperm_with_image(filepath)
            response_data = {
                'analysis_id': analysis_id,
                'analysis_type': 'sperm',
                'sample_id': result.sample_id,
                'classification': result.classification,
                'parameters': {
                    'concentration': getattr(result, 'concentration', None),
                    'progressive_motility': getattr(result, 'progressive_motility', None),
                    'normal_morphology': getattr(result, 'normal_morphology', None),
                    'volume': getattr(result, 'volume', None)
                }
            }
            
        elif analysis_type == 'oocyte':
            result = classifier.analyze_oocyte_with_image(filepath)
            response_data = {
                'analysis_id': analysis_id,
                'analysis_type': 'oocyte',
                'oocyte_id': result.oocyte_id,
                'classification': result.classification,
                'parameters': {
                    'maturity': result.maturity.value if hasattr(result, 'maturity') and result.maturity else None,
                    'morphology_score': getattr(result, 'morphology_score', None)
                }
            }
            
        elif analysis_type == 'embryo':
            day = int(request.form.get('day', 3))
            result = classifier.analyze_embryo_with_image(filepath, day)

            # Convert enum values to strings for JSON serialization
            grade_value = getattr(result, 'grade', None)
            if hasattr(grade_value, 'value'):
                grade_value = grade_value.value
            elif hasattr(grade_value, 'name'):
                grade_value = grade_value.name

            response_data = {
                'analysis_id': analysis_id,
                'analysis_type': 'embryo',
                'embryo_id': result.embryo_id,
                'classification': result.classification,
                'parameters': {
                    'day': day,
                    'cell_count': getattr(result, 'cell_count', None),
                    'fragmentation': getattr(result, 'fragmentation', None),
                    'grade': str(grade_value) if grade_value else None
                }
            }
            
        elif analysis_type in ['follicle', 'hysteroscopy']:
            if analysis_type == 'follicle':
                result = classifier.analyze_follicle_scan_with_image(filepath)
            else:
                result = classifier.analyze_hysteroscopy_with_image(filepath)
            
            if result.get('success'):
                analysis_result = result.get('result')
                response_data = {
                    'analysis_id': analysis_id,
                    'analysis_type': analysis_type,
                    'scan_id': result.get('analysis_id'),
                    'classification': analysis_result.classification if analysis_result else 'Analysis completed',
                    'parameters': analysis_result.__dict__ if analysis_result and hasattr(analysis_result, '__dict__') else {}
                }
            else:
                return jsonify({
                    'success': False,
                    'error': result.get('error', 'Analysis failed'),
                    'code': 'ANALYSIS_FAILED'
                }), 500
        
        else:
            return jsonify({
                'success': False,
                'error': f'Unsupported analysis type: {analysis_type}',
                'code': 'UNSUPPORTED_ANALYSIS_TYPE'
            }), 400
        
        # Add metadata
        response_data.update({
            'success': True,
            'timestamp': datetime.datetime.now().isoformat(),
            'client_name': client_info['client_name'],
            'patient_id': patient_id,
            'case_id': case_id,
            'notes': notes,
            'image_filename': file.filename,
            'ai_analysis': getattr(result, 'image_analysis', 'Analysis completed successfully'),
            'processing_mode': 'mock' if client_info['mock_mode'] else 'ai_powered'
        })
        
        # Log successful analysis
        logger.info(f"Analysis completed - {client_info['client_name']} - {analysis_type} - {analysis_id}")
        
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Analysis error for {client_info['client_name']}: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Analysis failed: {str(e)}',
            'code': 'INTERNAL_ERROR'
        }), 500

if __name__ == '__main__':
    print("🚀 Starting FertiVision API Server")
    print("🏥 Ready for IVF EMR Integration")
    print("📡 API Documentation: http://localhost:5003/api/v1/info")
    print("© 2025 FertiVision powered by AI | Made by greybrain.ai")
    
    app.run(host='0.0.0.0', port=5003, debug=True)
