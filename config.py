#!/usr/bin/env python3
"""
Configuration Management for FertiVision
Handles analysis modes, medical disciplines, and system settings
"""

from enum import Enum
import os
from typing import Dict, Any, Optional

class AnalysisMode(Enum):
    """Analysis modes for the system"""
    MOCK = "mock"
    DEEPSEEK = "deepseek"
    DEMO = "demo"

class MedicalDiscipline(Enum):
    """Medical discipline classifications"""
    REPRODUCTIVE_MEDICINE = "reproductive_medicine"
    EMBRYOLOGY = "embryology"
    ANDROLOGY = "andrology"
    GYNECOLOGY = "gynecology"

class Config:
    """Configuration management class"""
    
    def __init__(self):
        # Set analysis mode from environment or default to DEMO
        mode_env = os.getenv('ANALYSIS_MODE', 'DEMO').upper()
        try:
            self.current_mode = AnalysisMode(mode_env.lower())
        except ValueError:
            self.current_mode = AnalysisMode.DEMO
            
        self.deepseek_model = "deepseek-coder"
        self.ollama_base_url = "http://localhost:11434"
        self.api_keys = {}
        self.settings = {
            'max_file_size': 10 * 1024 * 1024,  # 10MB
            'allowed_extensions': {'.pdf', '.jpg', '.jpeg', '.png', '.tiff', '.tif'},
            'upload_folder': 'uploads',
            'export_folder': 'exports',
            'database_path': 'reproductive_analysis.db',
            'analysis_mode': self.current_mode.value  # Add analysis mode to settings
        }
    
    def get_current_mode(self) -> AnalysisMode:
        """Get current analysis mode"""
        return self.current_mode
    
    def set_analysis_mode(self, mode: AnalysisMode):
        """Set analysis mode"""
        self.current_mode = mode
    
    def is_deepseek_available(self) -> bool:
        """Check if DeepSeek is available"""
        try:
            import requests
            response = requests.get(f"{self.ollama_base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def get_deepseek_config(self) -> Dict[str, Any]:
        """Get DeepSeek configuration"""
        return {
            'model': self.deepseek_model,
            'base_url': self.ollama_base_url,
            'available': self.is_deepseek_available()
        }
    
    def get_upload_config(self) -> Dict[str, Any]:
        """Get file upload configuration"""
        return {
            'max_file_size': self.settings['max_file_size'],
            'allowed_extensions': self.settings['allowed_extensions'],
            'upload_folder': self.settings['upload_folder']
        }
    
    def get_database_path(self) -> str:
        """Get database file path"""
        return self.settings['database_path']

# Global configuration instance
config = Config()
