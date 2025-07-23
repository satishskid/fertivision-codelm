"""
FertiVision Model Configuration System
Provides model management and configuration for AI analysis
"""

import logging
import json
from typing import Dict, List, Optional
from enum import Enum

logger = logging.getLogger(__name__)

class ModelStatus(Enum):
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    LOADING = "loading"
    ERROR = "error"

class ModelManager:
    """Manages available AI models for FertiVision analysis"""
    
    def __init__(self):
        self.models = {
            "demo-analysis": {
                "name": "Demo Analysis Model",
                "description": "Demonstration model for testing",
                "status": ModelStatus.AVAILABLE,
                "type": "demo"
            },
            "basic-fertility": {
                "name": "Basic Fertility Analysis",
                "description": "Basic reproductive health analysis",
                "status": ModelStatus.AVAILABLE,
                "type": "medical"
            },
            "advanced-fertility": {
                "name": "Advanced Fertility Analysis", 
                "description": "Advanced AI-powered fertility assessment",
                "status": ModelStatus.UNAVAILABLE,
                "type": "medical"
            }
        }
        self.current_model = "demo-analysis"
        
    def get_available_models(self) -> List[str]:
        """Get list of available model IDs"""
        return [
            model_id for model_id, config in self.models.items() 
            if config["status"] == ModelStatus.AVAILABLE
        ]
    
    def get_model_info(self, model_id: str) -> Optional[Dict]:
        """Get detailed information about a specific model"""
        return self.models.get(model_id)
    
    def get_current_model(self) -> str:
        """Get currently selected model ID"""
        return self.current_model
    
    def set_current_model(self, model_id: str) -> bool:
        """Set the current model if available"""
        if model_id in self.get_available_models():
            self.current_model = model_id
            logger.info(f"Model switched to: {model_id}")
            return True
        else:
            logger.warning(f"Model not available: {model_id}")
            return False
    
    def is_model_available(self, model_id: str) -> bool:
        """Check if a specific model is available"""
        model_info = self.models.get(model_id)
        return model_info and model_info["status"] == ModelStatus.AVAILABLE
    
    def get_model_capabilities(self, model_id: str = None) -> Dict:
        """Get capabilities of specified model or current model"""
        if model_id is None:
            model_id = self.current_model
            
        model_info = self.models.get(model_id)
        if not model_info:
            return {"error": "Model not found"}
            
        return {
            "name": model_info["name"],
            "type": model_info["type"],
            "status": model_info["status"].value,
            "features": {
                "oocyte_analysis": True,
                "follicle_detection": True,
                "maturity_assessment": True,
                "report_generation": True,
                "batch_processing": model_info["type"] == "medical"
            }
        }

# Global model manager instance
model_manager = ModelManager()

def initialize_models():
    """Initialize model configuration system"""
    logger.info("🤖 Model configuration system initialized")
    logger.info(f"Available models: {model_manager.get_available_models()}")
    logger.info(f"Current model: {model_manager.get_current_model()}")

# Initialize on import
initialize_models()
