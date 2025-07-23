"""
FertiVision Model Service Management
Handles model service availability and health monitoring
"""

import logging
import time
from typing import Dict, Optional, List
from enum import Enum

logger = logging.getLogger(__name__)

class ServiceStatus(Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    DEGRADED = "degraded"
    MAINTENANCE = "maintenance"

class ModelService:
    """Manages model service health and availability"""
    
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.status = ServiceStatus.ONLINE
        self.last_check = time.time()
        self.response_time = 0.0
        self.error_count = 0
        
    def check_health(self) -> bool:
        """Perform health check on the service"""
        try:
            start_time = time.time()
            # Simulate health check - in production this would ping actual service
            self.response_time = time.time() - start_time
            self.last_check = time.time()
            self.status = ServiceStatus.ONLINE
            return True
        except Exception as e:
            logger.error(f"Health check failed for {self.service_name}: {e}")
            self.error_count += 1
            self.status = ServiceStatus.OFFLINE if self.error_count > 3 else ServiceStatus.DEGRADED
            return False
    
    def get_status(self) -> Dict:
        """Get current service status"""
        return {
            "service": self.service_name,
            "status": self.status.value,
            "last_check": self.last_check,
            "response_time": self.response_time,
            "error_count": self.error_count
        }

class ServiceManager:
    """Manages all model services"""
    
    def __init__(self):
        self.services = {
            "demo-service": ModelService("demo-service"),
            "fertility-analysis": ModelService("fertility-analysis"),
            "image-processing": ModelService("image-processing"),
            "report-generator": ModelService("report-generator")
        }
        
    def is_available(self) -> bool:
        """Check if any services are available"""
        return any(
            service.status in [ServiceStatus.ONLINE, ServiceStatus.DEGRADED]
            for service in self.services.values()
        )
    
    def get_service_status(self, service_name: str) -> Optional[Dict]:
        """Get status of a specific service"""
        service = self.services.get(service_name)
        return service.get_status() if service else None
    
    def get_all_services_status(self) -> Dict:
        """Get status of all services"""
        return {
            name: service.get_status() 
            for name, service in self.services.items()
        }
    
    def health_check_all(self) -> Dict:
        """Perform health check on all services"""
        results = {}
        for name, service in self.services.items():
            results[name] = service.check_health()
        return results
    
    def get_healthy_services(self) -> List[str]:
        """Get list of healthy service names"""
        return [
            name for name, service in self.services.items()
            if service.status == ServiceStatus.ONLINE
        ]
    
    def get_degraded_services(self) -> List[str]:
        """Get list of degraded service names"""
        return [
            name for name, service in self.services.items()
            if service.status == ServiceStatus.DEGRADED
        ]
    
    def get_offline_services(self) -> List[str]:
        """Get list of offline service names"""
        return [
            name for name, service in self.services.items()
            if service.status == ServiceStatus.OFFLINE
        ]

# Global service manager instance
service_manager = ServiceManager()

def initialize_services():
    """Initialize service management system"""
    logger.info("🔧 Model service management system initialized")
    
    # Perform initial health checks
    health_results = service_manager.health_check_all()
    healthy_count = sum(1 for result in health_results.values() if result)
    
    logger.info(f"Services health check: {healthy_count}/{len(health_results)} services healthy")
    
    if healthy_count == 0:
        logger.warning("⚠️ No model services are currently healthy")
    elif healthy_count < len(health_results):
        logger.warning(f"⚠️ {len(health_results) - healthy_count} services are experiencing issues")
    else:
        logger.info("✅ All model services are healthy")

# Initialize on import
initialize_services()
