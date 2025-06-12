#!/usr/bin/env python3
"""
Configuration file for FertiVision-CodeLM AI-Enhanced Reproductive Classification System
"""

import os
from enum import Enum

class AnalysisMode(Enum):
    MOCK = "mock"
    DEEPSEEK = "deepseek"

class MedicalDiscipline(Enum):
    EMBRYOLOGY = "embryology"
    ANDROLOGY = "andrology"
    REPRODUCTIVE_ENDOCRINOLOGY = "reproductive_endocrinology"
    GYNECOLOGY = "gynecology"
    RADIOLOGY = "radiology"

# Application Configuration
class Config:
    # Mode Configuration
    ANALYSIS_MODE = AnalysisMode.MOCK  # Default to MOCK for testing (change to DEEPSEEK for production)
    
    # DeepSeek/Ollama Configuration
    DEEPSEEK_URL = "http://localhost:11434/api/generate"
    DEEPSEEK_MODEL = "deepseek-coder"  # or "llava" for vision
    DEEPSEEK_TIMEOUT = 60  # seconds
    
    # File Support Configuration
    SUPPORTED_IMAGE_FORMATS = {
        'png', 'jpg', 'jpeg', 'tiff', 'tif', 'bmp', 'gif', 'webp'
    }
    
    SUPPORTED_MEDICAL_FORMATS = {
        'dcm',      # DICOM - medical imaging standard
        'dcm30',    # DICOM 3.0
        'ima',      # DICOM IMA format
        'nii',      # NIfTI - neuroimaging
        'nii.gz',   # Compressed NIfTI
    }
    
    SUPPORTED_VIDEO_FORMATS = {
        'mp4', 'avi', 'mov', 'mkv', 'wmv'  # For time-lapse embryo analysis
    }
    
    # File size limits (in MB)
    MAX_IMAGE_SIZE = 50
    MAX_VIDEO_SIZE = 500
    MAX_MEDICAL_SIZE = 100
    
    # Discipline-specific file associations
    DISCIPLINE_FILE_TYPES = {
        MedicalDiscipline.EMBRYOLOGY: {
            'extensions': {'jpg', 'jpeg', 'png', 'tiff', 'mp4', 'avi'},
            'description': 'Embryo images, time-lapse videos, blastocyst photos',
            'analysis_types': ['embryo', 'blastocyst', 'time_lapse']
        },
        MedicalDiscipline.ANDROLOGY: {
            'extensions': {'jpg', 'jpeg', 'png', 'tiff', 'mp4'},
            'description': 'Sperm analysis images, motility videos',
            'analysis_types': ['sperm', 'sperm_motility', 'sperm_morphology']
        },
        MedicalDiscipline.REPRODUCTIVE_ENDOCRINOLOGY: {
            'extensions': {'dcm', 'jpg', 'jpeg', 'png', 'tiff'},
            'description': 'Ultrasound images, follicle scans, ovarian imaging',
            'analysis_types': ['follicle', 'ovarian', 'endometrial']
        },
        MedicalDiscipline.GYNECOLOGY: {
            'extensions': {'jpg', 'jpeg', 'png', 'tiff', 'dcm', 'mp4'},
            'description': 'Hysteroscopy images/videos, cervical imaging',
            'analysis_types': ['hysteroscopy', 'cervical', 'uterine']
        },
        MedicalDiscipline.RADIOLOGY: {
            'extensions': {'dcm', 'dcm30', 'ima', 'nii', 'nii.gz'},
            'description': 'Medical imaging files, CT, MRI, ultrasound',
            'analysis_types': ['ultrasound', 'ct', 'mri', 'xray']
        }
    }
    
    # Authentication Configuration (Basic)
    ENABLE_AUTH = False  # Set to True to enable basic authentication
    DEFAULT_USERNAME = "doctor"
    DEFAULT_PASSWORD = "fertility2025"
    SESSION_TIMEOUT = 3600  # 1 hour in seconds
    
    # Export Configuration
    ENABLE_PDF_EXPORT = True
    PDF_TEMPLATE_PATH = "templates/pdf"
    EXPORT_FOLDER = "exports"
    
    # Database Configuration
    DATABASE_PATH = "reproductive_analysis.db"
    BACKUP_DATABASE = True
    AUTO_BACKUP_INTERVAL = 24  # hours
    
    # UI Configuration
    THEME = "light"  # light or dark
    SHOW_ADVANCED_OPTIONS = True
    ENABLE_BATCH_PROCESSING = True
    
    # Security Configuration
    ALLOWED_UPLOAD_EXTENSIONS = (
        SUPPORTED_IMAGE_FORMATS | 
        SUPPORTED_MEDICAL_FORMATS | 
        SUPPORTED_VIDEO_FORMATS
    )
    
    UPLOAD_FOLDER = "uploads"
    PROCESSED_FOLDER = "processed"
    
    @classmethod
    def get_max_file_size(cls, file_extension):
        """Get maximum file size based on file type"""
        ext = file_extension.lower().lstrip('.')
        
        if ext in cls.SUPPORTED_VIDEO_FORMATS:
            return cls.MAX_VIDEO_SIZE * 1024 * 1024
        elif ext in cls.SUPPORTED_MEDICAL_FORMATS:
            return cls.MAX_MEDICAL_SIZE * 1024 * 1024
        else:
            return cls.MAX_IMAGE_SIZE * 1024 * 1024
    
    @classmethod
    def get_discipline_for_file(cls, filename):
        """Determine medical discipline based on file type and name"""
        ext = filename.lower().split('.')[-1]
        filename_lower = filename.lower()
        
        # Check specific keywords in filename
        if any(word in filename_lower for word in ['sperm', 'semen', 'motility']):
            return MedicalDiscipline.ANDROLOGY
        elif any(word in filename_lower for word in ['embryo', 'blastocyst', 'cleavage']):
            return MedicalDiscipline.EMBRYOLOGY
        elif any(word in filename_lower for word in ['follicle', 'ovarian', 'ovary']):
            return MedicalDiscipline.REPRODUCTIVE_ENDOCRINOLOGY
        elif any(word in filename_lower for word in ['hysteroscopy', 'uterine', 'cervical']):
            return MedicalDiscipline.GYNECOLOGY
        elif ext in cls.SUPPORTED_MEDICAL_FORMATS:
            return MedicalDiscipline.RADIOLOGY
        
        # Default fallback based on file extension
        for discipline, config in cls.DISCIPLINE_FILE_TYPES.items():
            if ext in config['extensions']:
                return discipline
        
        return MedicalDiscipline.EMBRYOLOGY  # Default
    
    @classmethod
    def is_file_supported(cls, filename):
        """Check if file is supported"""
        ext = filename.lower().split('.')[-1]
        return ext in cls.ALLOWED_UPLOAD_EXTENSIONS

# Environment-specific overrides
if os.getenv('FERTIVISION_ENV') == 'production':
    Config.ANALYSIS_MODE = AnalysisMode.DEEPSEEK
    Config.ENABLE_AUTH = True
elif os.getenv('FERTIVISION_ENV') == 'demo':
    Config.ANALYSIS_MODE = AnalysisMode.DEEPSEEK
    Config.ENABLE_AUTH = False
