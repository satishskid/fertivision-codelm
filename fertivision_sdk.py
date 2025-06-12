"""
FertiVision SDK for IVF EMR Integration
======================================

Python SDK for integrating FertiVision analysis capabilities
into IVF Electronic Medical Record (EMR) systems.

Features:
- Simple Python API for image analysis
- Automatic error handling and retries
- Batch processing capabilities
- Async support for high-throughput scenarios
- Type hints for better IDE support
- Comprehensive logging and debugging

Usage Example:
    from fertivision_sdk import FertiVisionClient
    
    client = FertiVisionClient(
        api_key="your_api_key",
        base_url="https://api.fertivision.com"
    )
    
    # Analyze sperm sample
    result = client.analyze_sperm("sperm_image.jpg", patient_id="P12345")
    print(f"Classification: {result.classification}")

© 2025 FertiVision powered by AI | Made by greybrain.ai
"""

import requests
import json
import os
import time
from typing import Optional, Dict, List, Union, Any
from dataclasses import dataclass
from pathlib import Path
import logging

# Configure SDK logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('FertiVision-SDK')

@dataclass
class AnalysisResult:
    """Standardized analysis result from FertiVision API"""
    success: bool
    analysis_id: str
    analysis_type: str
    classification: str
    parameters: Dict[str, Any]
    timestamp: str
    patient_id: Optional[str] = None
    case_id: Optional[str] = None
    ai_analysis: Optional[str] = None
    processing_mode: Optional[str] = None
    error: Optional[str] = None
    error_code: Optional[str] = None
    # Additional fields that may be returned by API
    client_name: Optional[str] = None
    sample_id: Optional[str] = None
    oocyte_id: Optional[str] = None
    embryo_id: Optional[str] = None
    scan_id: Optional[str] = None
    image_filename: Optional[str] = None
    notes: Optional[str] = None

@dataclass
class SpermAnalysisResult(AnalysisResult):
    """Specialized result for sperm analysis"""
    @property
    def concentration(self) -> Optional[float]:
        return self.parameters.get('concentration')
    
    @property
    def progressive_motility(self) -> Optional[float]:
        return self.parameters.get('progressive_motility')
    
    @property
    def normal_morphology(self) -> Optional[float]:
        return self.parameters.get('normal_morphology')
    
    @property
    def volume(self) -> Optional[float]:
        return self.parameters.get('volume')

@dataclass
class EmbryoAnalysisResult(AnalysisResult):
    """Specialized result for embryo analysis"""
    @property
    def day(self) -> Optional[int]:
        return self.parameters.get('day')
    
    @property
    def cell_count(self) -> Optional[int]:
        return self.parameters.get('cell_count')
    
    @property
    def fragmentation(self) -> Optional[float]:
        return self.parameters.get('fragmentation')
    
    @property
    def grade(self) -> Optional[str]:
        return self.parameters.get('grade')

class FertiVisionError(Exception):
    """Base exception for FertiVision SDK errors"""
    def __init__(self, message: str, error_code: str = None, status_code: int = None):
        super().__init__(message)
        self.error_code = error_code
        self.status_code = status_code

class FertiVisionClient:
    """
    FertiVision API Client for IVF EMR Integration
    
    This client provides a simple interface for integrating FertiVision
    analysis capabilities into IVF EMR systems.
    """
    
    def __init__(
        self,
        api_key: str,
        base_url: str = "http://localhost:5003",
        timeout: int = 300,
        max_retries: int = 3,
        retry_delay: float = 1.0
    ):
        """
        Initialize FertiVision client
        
        Args:
            api_key: Your FertiVision API key
            base_url: API server URL (default: localhost for development)
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
            retry_delay: Delay between retries in seconds
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.api_version = "v1"
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        
        self.session = requests.Session()
        self.session.headers.update({
            'X-API-Key': self.api_key,
            'User-Agent': 'FertiVision-SDK/1.0'
        })
        
        logger.info(f"FertiVision client initialized for {base_url}")
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        files: Dict = None,
        data: Dict = None,
        params: Dict = None
    ) -> Dict:
        """Make HTTP request with retry logic"""
        url = f"{self.base_url}/api/{self.api_version}{endpoint}"
        
        for attempt in range(self.max_retries + 1):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    files=files,
                    data=data,
                    params=params,
                    timeout=self.timeout
                )
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 429:  # Rate limit
                    if attempt < self.max_retries:
                        wait_time = self.retry_delay * (2 ** attempt)
                        logger.warning(f"Rate limited, waiting {wait_time}s before retry")
                        time.sleep(wait_time)
                        continue
                
                # Handle error responses
                try:
                    error_data = response.json()
                    raise FertiVisionError(
                        error_data.get('error', 'Unknown error'),
                        error_data.get('code'),
                        response.status_code
                    )
                except json.JSONDecodeError:
                    raise FertiVisionError(
                        f"HTTP {response.status_code}: {response.text}",
                        status_code=response.status_code
                    )
                    
            except requests.exceptions.RequestException as e:
                if attempt < self.max_retries:
                    logger.warning(f"Request failed, retrying: {e}")
                    time.sleep(self.retry_delay)
                    continue
                raise FertiVisionError(f"Request failed: {e}")
        
        raise FertiVisionError("Max retries exceeded")
    
    def health_check(self) -> Dict:
        """Check API health status"""
        return self._make_request('GET', '/health')
    
    def get_api_info(self) -> Dict:
        """Get API information and client permissions"""
        return self._make_request('GET', '/info')
    
    def _analyze_image(
        self,
        analysis_type: str,
        image_path: Union[str, Path],
        patient_id: Optional[str] = None,
        case_id: Optional[str] = None,
        notes: Optional[str] = None,
        **kwargs
    ) -> AnalysisResult:
        """Generic image analysis method"""
        
        # Validate file exists
        image_path = Path(image_path)
        if not image_path.exists():
            raise FertiVisionError(f"Image file not found: {image_path}")
        
        # Prepare request data
        data = {}
        if patient_id:
            data['patient_id'] = patient_id
        if case_id:
            data['case_id'] = case_id
        if notes:
            data['notes'] = notes
        
        # Add analysis-specific parameters
        data.update(kwargs)
        
        # Prepare file upload
        with open(image_path, 'rb') as f:
            files = {'image': (image_path.name, f, 'image/jpeg')}
            
            response = self._make_request(
                'POST',
                f'/analyze/{analysis_type}',
                files=files,
                data=data
            )
        
        if not response.get('success'):
            raise FertiVisionError(
                response.get('error', 'Analysis failed'),
                response.get('code')
            )
        
        # Create appropriate result object
        if analysis_type == 'sperm':
            return SpermAnalysisResult(**response)
        elif analysis_type == 'embryo':
            return EmbryoAnalysisResult(**response)
        else:
            return AnalysisResult(**response)
    
    def analyze_sperm(
        self,
        image_path: Union[str, Path],
        patient_id: Optional[str] = None,
        case_id: Optional[str] = None,
        notes: Optional[str] = None
    ) -> SpermAnalysisResult:
        """
        Analyze sperm sample image
        
        Args:
            image_path: Path to sperm microscopy image
            patient_id: Optional patient identifier
            case_id: Optional case identifier
            notes: Optional analysis notes
            
        Returns:
            SpermAnalysisResult with WHO-compliant analysis
        """
        return self._analyze_image('sperm', image_path, patient_id, case_id, notes)
    
    def analyze_oocyte(
        self,
        image_path: Union[str, Path],
        patient_id: Optional[str] = None,
        case_id: Optional[str] = None,
        notes: Optional[str] = None
    ) -> AnalysisResult:
        """
        Analyze oocyte maturity and quality
        
        Args:
            image_path: Path to oocyte microscopy image
            patient_id: Optional patient identifier
            case_id: Optional case identifier
            notes: Optional analysis notes
            
        Returns:
            AnalysisResult with ESHRE-compliant analysis
        """
        return self._analyze_image('oocyte', image_path, patient_id, case_id, notes)
    
    def analyze_embryo(
        self,
        image_path: Union[str, Path],
        day: int = 3,
        patient_id: Optional[str] = None,
        case_id: Optional[str] = None,
        notes: Optional[str] = None
    ) -> EmbryoAnalysisResult:
        """
        Analyze embryo development and grading
        
        Args:
            image_path: Path to embryo microscopy image
            day: Embryo development day (3, 5, 6)
            patient_id: Optional patient identifier
            case_id: Optional case identifier
            notes: Optional analysis notes
            
        Returns:
            EmbryoAnalysisResult with Gardner grading
        """
        return self._analyze_image('embryo', image_path, patient_id, case_id, notes, day=day)
    
    def analyze_follicle_scan(
        self,
        image_path: Union[str, Path],
        patient_id: Optional[str] = None,
        case_id: Optional[str] = None,
        notes: Optional[str] = None
    ) -> AnalysisResult:
        """
        Analyze ultrasound for follicle counting
        
        Args:
            image_path: Path to ultrasound image
            patient_id: Optional patient identifier
            case_id: Optional case identifier
            notes: Optional analysis notes
            
        Returns:
            AnalysisResult with AFC and ovarian reserve assessment
        """
        return self._analyze_image('follicle', image_path, patient_id, case_id, notes)
    
    def analyze_hysteroscopy(
        self,
        image_path: Union[str, Path],
        patient_id: Optional[str] = None,
        case_id: Optional[str] = None,
        notes: Optional[str] = None
    ) -> AnalysisResult:
        """
        Analyze hysteroscopy images for endometrial assessment
        
        Args:
            image_path: Path to hysteroscopy image
            patient_id: Optional patient identifier
            case_id: Optional case identifier
            notes: Optional analysis notes
            
        Returns:
            AnalysisResult with endometrial morphology analysis
        """
        return self._analyze_image('hysteroscopy', image_path, patient_id, case_id, notes)

# Convenience functions for quick integration
def quick_sperm_analysis(api_key: str, image_path: str, **kwargs) -> SpermAnalysisResult:
    """Quick sperm analysis without creating client instance"""
    client = FertiVisionClient(api_key)
    return client.analyze_sperm(image_path, **kwargs)

def quick_embryo_analysis(api_key: str, image_path: str, day: int = 3, **kwargs) -> EmbryoAnalysisResult:
    """Quick embryo analysis without creating client instance"""
    client = FertiVisionClient(api_key)
    return client.analyze_embryo(image_path, day=day, **kwargs)
