"""
Enhanced Flask Application with Performance Optimizations
Integrates all performance improvements for cloud deployment
"""

import os
import asyncio
import time
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, send_file
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_compress import Compress
from werkzeug.utils import secure_filename
import redis
from celery import Celery
import logging
from datetime import datetime

# Import our performance optimization modules
from performance_optimization import CloudPerformanceManager, performance_monitor
from patient_history import PatientHistoryManager, PatientRecord, DocumentAnalysis
from auth import require_auth, get_current_user
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app with optimizations
app = Flask(__name__)
app.config.from_object(Config)

# Initialize performance optimizations
Compress(app)  # Enable gzip compression

# Rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["1000 per hour"]
)

# Initialize Redis for caching
try:
    redis_client = redis.Redis(
        host=os.getenv('REDIS_HOST', 'localhost'),
        port=int(os.getenv('REDIS_PORT', 6379)),
        db=0,
        decode_responses=True
    )
    redis_client.ping()
    logger.info("Redis connection established")
except Exception as e:
    logger.warning(f"Redis connection failed: {e}")
    redis_client = None

# Initialize Celery for background processing
celery = Celery(
    app.import_name,
    broker=os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0'),
    backend=os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
)

# Initialize performance manager
perf_manager = CloudPerformanceManager()

# Background tasks
@celery.task
def analyze_document_async(patient_id: str, file_path: str, document_type: str):
    """Asynchronous document analysis task"""
    try:
        start_time = time.time()
        
        # Initialize patient manager
        patient_manager = PatientHistoryManager()
        
        # Perform analysis (this would use real AI in production)
        analysis_result = {
            'document_id': f"doc_{int(time.time())}",
            'document_type': document_type,
            'analysis_status': 'completed',
            'confidence_score': 0.95,
            'key_findings': ['Analysis completed successfully'],
            'processed_at': datetime.now().isoformat()
        }
        
        # Update document with analysis results
        patient_manager.update_document_analysis(patient_id, analysis_result)
        
        processing_time = time.time() - start_time
        logger.info(f"Document analysis completed in {processing_time:.2f}s for patient {patient_id}")
        
        return {
            'status': 'completed',
            'patient_id': patient_id,
            'processing_time': processing_time
        }
        
    except Exception as e:
        logger.error(f"Document analysis failed: {e}")
        return {'status': 'failed', 'error': str(e)}

@celery.task
def generate_pdf_report_async(patient_id: str):
    """Asynchronous PDF report generation"""
    try:
        start_time = time.time()
        
        patient_manager = PatientHistoryManager()
        pdf_path = patient_manager.generate_pdf_report(patient_id)
        
        processing_time = time.time() - start_time
        logger.info(f"PDF report generated in {processing_time:.2f}s for patient {patient_id}")
        
        return {
            'status': 'completed',
            'pdf_path': pdf_path,
            'processing_time': processing_time
        }
        
    except Exception as e:
        logger.error(f"PDF generation failed: {e}")
        return {'status': 'failed', 'error': str(e)}

# Performance monitoring middleware
@app.before_request
def before_request():
    """Track request start time for performance monitoring"""
    request.start_time = time.time()

@app.after_request
def after_request(response):
    """Log request performance metrics"""
    if hasattr(request, 'start_time'):
        duration = time.time() - request.start_time
        if duration > 1.0:  # Log slow requests
            logger.warning(f"Slow request: {request.method} {request.path} took {duration:.2f}s")
    
    # Add security headers
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    return response

# Health check endpoint
@app.route('/health')
def health_check():
    """Health check endpoint for load balancer"""
    try:
        # Check database connection
        patient_manager = PatientHistoryManager()
        
        # Check Redis connection
        redis_status = "connected" if redis_client and redis_client.ping() else "disconnected"
        
        # Get performance metrics
        performance_report = perf_manager.get_performance_report()
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'redis': redis_status,
            'performance': performance_report
        }), 200
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 503

# Enhanced API endpoints with performance optimizations

@app.route('/api/patients', methods=['POST'])
@require_auth
@limiter.limit("10 per minute")
@performance_monitor
def create_patient():
    """Create new patient with rate limiting and monitoring"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'age', 'gender']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        patient_manager = PatientHistoryManager()
        patient = PatientRecord(
            name=data['name'],
            age=data['age'],
            gender=data['gender'],
            email=data.get('email'),
            phone=data.get('phone')
        )
        
        patient_id = patient_manager.create_patient(patient)
        
        # Cache patient data
        if redis_client:
            cache_key = f"patient:{patient_id}"
            redis_client.setex(cache_key, 3600, jsonify(patient.__dict__).data)
        
        logger.info(f"Patient created: {patient_id}")
        return jsonify({
            'success': True,
            'patient_id': patient_id,
            'message': 'Patient created successfully'
        }), 201
        
    except Exception as e:
        logger.error(f"Patient creation failed: {e}")
        return jsonify({'error': 'Failed to create patient'}), 500

@app.route('/api/patients/<patient_id>/documents', methods=['POST'])
@require_auth
@limiter.limit("5 per minute")
@performance_monitor
def upload_document(patient_id):
    """Upload and analyze document asynchronously"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Validate file type and size
        allowed_extensions = {'pdf', 'jpg', 'jpeg', 'png', 'txt'}
        max_file_size = 10 * 1024 * 1024  # 10MB
        
        if not file.filename.lower().split('.')[-1] in allowed_extensions:
            return jsonify({'error': 'Invalid file type'}), 400
        
        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > max_file_size:
            return jsonify({'error': 'File too large (max 10MB)'}), 400
        
        # Save file securely
        filename = secure_filename(file.filename)
        timestamp = int(time.time())
        safe_filename = f"{patient_id}_{timestamp}_{filename}"
        
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)
        os.makedirs(os.path.dirname(upload_path), exist_ok=True)
        file.save(upload_path)
        
        # Start asynchronous analysis
        document_type = request.form.get('document_type', 'medical_report')
        task = analyze_document_async.delay(patient_id, upload_path, document_type)
        
        # Store document metadata
        patient_manager = PatientHistoryManager()
        document_id = patient_manager.add_document(
            patient_id=patient_id,
            filename=filename,
            file_path=upload_path,
            document_type=document_type,
            file_size=file_size
        )
        
        logger.info(f"Document uploaded for patient {patient_id}: {filename}")
        
        return jsonify({
            'success': True,
            'document_id': document_id,
            'task_id': task.id,
            'message': 'Document uploaded and analysis started',
            'status': 'processing'
        }), 202
        
    except Exception as e:
        logger.error(f"Document upload failed: {e}")
        return jsonify({'error': 'Failed to upload document'}), 500

@app.route('/api/patients/<patient_id>/report', methods=['POST'])
@require_auth
@limiter.limit("3 per minute")
@performance_monitor
def generate_report(patient_id):
    """Generate PDF report asynchronously"""
    try:
        # Start asynchronous PDF generation
        task = generate_pdf_report_async.delay(patient_id)
        
        logger.info(f"PDF report generation started for patient {patient_id}")
        
        return jsonify({
            'success': True,
            'task_id': task.id,
            'message': 'Report generation started',
            'status': 'processing'
        }), 202
        
    except Exception as e:
        logger.error(f"Report generation failed: {e}")
        return jsonify({'error': 'Failed to start report generation'}), 500

@app.route('/api/tasks/<task_id>/status', methods=['GET'])
@require_auth
@performance_monitor
def get_task_status(task_id):
    """Get status of asynchronous task"""
    try:
        task = celery.AsyncResult(task_id)
        
        response = {
            'task_id': task_id,
            'status': task.status,
            'timestamp': datetime.now().isoformat()
        }
        
        if task.status == 'SUCCESS':
            response['result'] = task.result
        elif task.status == 'FAILURE':
            response['error'] = str(task.info)
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Task status check failed: {e}")
        return jsonify({'error': 'Failed to get task status'}), 500

@app.route('/api/performance/metrics', methods=['GET'])
@require_auth
@performance_monitor
def get_performance_metrics():
    """Get current performance metrics"""
    try:
        metrics = perf_manager.get_performance_report()
        return jsonify(metrics), 200
        
    except Exception as e:
        logger.error(f"Performance metrics failed: {e}")
        return jsonify({'error': 'Failed to get performance metrics'}), 500

# Keep existing routes but add performance monitoring
@app.route('/')
@performance_monitor
def index():
    return render_template('index.html')

@app.route('/patient-history')
@require_auth
@performance_monitor
def patient_history():
    return render_template('patient_history.html')

# Error handlers
@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({
        'error': 'Rate limit exceeded',
        'message': str(e.description)
    }), 429

@app.errorhandler(500)
def internal_error(e):
    logger.error(f"Internal server error: {e}")
    return jsonify({
        'error': 'Internal server error',
        'message': 'Please try again later'
    }), 500

if __name__ == '__main__':
    # Initialize performance optimizations
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(perf_manager.initialize())
    
    # Run with performance optimizations
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') != 'production'
    
    if debug:
        app.run(host='0.0.0.0', port=port, debug=True)
    else:
        # Production settings
        import gunicorn
        app.run(host='0.0.0.0', port=port, debug=False)
