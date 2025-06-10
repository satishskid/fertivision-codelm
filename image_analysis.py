import base64
import requests
import json
import os
from PIL import Image
import io
from typing import Dict, List, Optional, Tuple
import cv2
import numpy as np

class ImageAnalyzer:
    def __init__(self, deepseek_api_key: str = None, deepseek_url: str = "http://localhost:11434/api/generate", mock_mode: bool = False):
        """
        Initialize image analyzer with DeepSeek LLM
        For local DeepSeek installation via Ollama
        Set mock_mode=True for testing without LLM service
        """
        self.deepseek_url = deepseek_url
        self.api_key = deepseek_api_key
        self.mock_mode = mock_mode
    def encode_image_to_base64(self, image_path: str) -> str:
        """Convert image to base64 for LLM processing"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    def preprocess_image(self, image_path: str, analysis_type: str) -> str:
        """Preprocess microscopy images for better analysis"""
        try:
            # Load image
            image = cv2.imread(image_path)
            if image is None:
                return image_path  # Return original if can't process
            if analysis_type == "sperm":
                # Enhance contrast for sperm analysis
                lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
                l, a, b = cv2.split(lab)
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
                l = clahe.apply(l)
                enhanced = cv2.merge([l, a, b])
                enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
            elif analysis_type == "oocyte":
                # Enhance for oocyte structure visibility
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                enhanced = cv2.equalizeHist(gray)
                enhanced = cv2.cvtColor(enhanced, cv2.COLOR_GRAY2BGR)
            elif analysis_type == "embryo":
                # Enhance for cell boundary detection
                enhanced = cv2.bilateralFilter(image, 9, 75, 75)
            else:
                enhanced = image
            # Save preprocessed image
            processed_path = image_path.replace('.', '_processed.')
            cv2.imwrite(processed_path, enhanced)
            return processed_path
        except Exception as e:
            print(f"Error preprocessing image: {e}")
            return image_path  # Return original path if processing fails
    def analyze_sperm_image(self, image_path: str) -> Dict:
        """Analyze sperm microscopy image using DeepSeek LLM"""
        try:
            # Mock mode for testing without LLM service
            if self.mock_mode:
                return {
                    "success": True,
                    "analysis": """
SPERM ANALYSIS REPORT:

1. CONCENTRATION ASSESSMENT:
- Estimated concentration (million/ml): 45.2 million/ml
- Distribution pattern: uniform

2. MOTILITY ASSESSMENT:
- Progressive motility estimate (%): 62%
- Non-progressive motility (%): 15%
- Immotile sperm (%): 23%

3. MORPHOLOGY ASSESSMENT:
- Normal morphology (%): 78%
- Head defects (%): 12%
- Midpiece defects (%): 6%
- Tail defects (%): 4%

4. OVERALL ASSESSMENT:
- Sample quality: Good
- Fertility potential: High
- Recommendations: Suitable for IVF/ICSI procedures

DETAILED OBSERVATIONS:
- Sperm concentration appears adequate for natural conception
- Majority of sperm show normal morphology
- Good progressive motility observed
- No significant abnormalities detected
"""
                }
            
            processed_image = self.preprocess_image(image_path, "sperm")
            base64_image = self.encode_image_to_base64(processed_image)
            prompt = """
            You are an expert embryologist analyzing a sperm microscopy image. Please analyze this image and provide detailed assessment in the following format:

            SPERM ANALYSIS REPORT:
            
            1. CONCENTRATION ASSESSMENT:
            - Estimated concentration (million/ml): [provide estimate]
            - Distribution pattern: [uniform/clustered/sparse]
            
            2. MOTILITY ASSESSMENT:
            - Progressive motility estimate (%): [0-100]
            - Non-progressive motility (%): [0-100]
            - Immotile sperm (%): [0-100]
            
            3. MORPHOLOGY ASSESSMENT:
            - Normal morphology estimate (%): [0-100]
            - Head defects observed: [list defects]
            - Midpiece defects: [list defects]
            - Tail defects: [list defects]
            
            4. OVERALL ASSESSMENT:
            - Quality grade: [excellent/good/fair/poor]
            - WHO 2021 classification: [normozoospermia/oligozoospermia/asthenozoospermia/teratozoospermia]
            
            Please be specific and provide numerical estimates where possible.
            """
            return self._query_deepseek(prompt, base64_image)
        except Exception as e:
            return {
                "success": False,
                "error": f"Image analysis failed: {str(e)}",
                "analysis": ""
            }
    def analyze_oocyte_image(self, image_path: str) -> Dict:
        """Analyze oocyte microscopy image using DeepSeek LLM"""
        try:
            # Mock mode for testing without LLM service
            if self.mock_mode:
                return {
                    "success": True,
                    "analysis": """
OOCYTE ANALYSIS REPORT:

1. MATURITY ASSESSMENT:
- Maturity stage: MII (Metaphase II)
- Polar body: Present and normal
- Perivitelline space: Normal

2. MORPHOLOGICAL ASSESSMENT:
- Oocyte diameter: 120 μm
- Cytoplasm: Homogeneous, dark granular
- Zona pellucida: Normal thickness, smooth
- Morphology score: 8/10

3. QUALITY INDICATORS:
- Cytoplasmic granularity: Normal
- Vacuoles: None observed
- Inclusions: None significant
- Shape: Spherical, normal

4. OVERALL ASSESSMENT:
- Quality grade: Excellent
- Fertilization potential: High
- Suitable for ICSI: Yes

DETAILED OBSERVATIONS:
- Mature MII oocyte with good morphological characteristics
- Optimal for fertilization procedures
- No significant dysmorphisms detected
"""
                }
            
            processed_image = self.preprocess_image(image_path, "oocyte")
            base64_image = self.encode_image_to_base64(processed_image)
            prompt = """
            You are an expert embryologist analyzing an oocyte microscopy image. Please analyze this image following ESHRE guidelines:

            OOCYTE ANALYSIS REPORT:
            
            1. MATURITY ASSESSMENT:
            - Maturity stage: [MII/MI/GV]
            - Polar body: [present/absent/fragmented]
            
            2. MORPHOLOGICAL ASSESSMENT:
            - Zona pellucida: [normal/thick/thin/irregular]
            - Perivitelline space: [normal/enlarged/irregular]
            
            3. CYTOPLASM EVALUATION:
            - Cytoplasm appearance: [homogeneous/granular/vacuolated]
            - Cytoplasmic inclusions: [present/absent]
            
            4. QUALITY GRADING:
            - Morphology score (1-4): [score]
            - ICSI suitability: [excellent/good/fair/poor]
            - Viability assessment: [viable/questionable/non-viable]
            
            Base your assessment on standard ESHRE oocyte grading criteria.
            """
            return self._query_deepseek(prompt, base64_image)
        except Exception as e:
            return {
                "success": False,
                "error": f"Image analysis failed: {str(e)}",
                "analysis": ""
            }
    def analyze_embryo_image(self, image_path: str, day: int) -> Dict:
        """Analyze embryo microscopy image using DeepSeek LLM"""
        try:
            # Mock mode for testing without LLM service
            if self.mock_mode:
                if day <= 3:
                    return {
                        "success": True,
                        "analysis": f"""
CLEAVAGE STAGE EMBRYO ANALYSIS (Day {day}):

1. CELL COUNT AND DIVISION:
- Number of blastomeres: {2**day} cells
- Expected cell number for Day {day}: [{2**day}]
- Division synchrony: synchronous

2. FRAGMENTATION ASSESSMENT:
- Fragmentation level: 8% fragmentation
- Fragment distribution: minimal peripheral
- Grade: Grade 1 (excellent)

3. CELL MORPHOLOGY:
- Blastomere size: uniform
- Blastomere shape: regular
- Cytoplasmic appearance: normal granularity

4. OVERALL ASSESSMENT:
- Embryo grade: Grade 1 (top quality)
- Development potential: excellent
- Transfer suitability: highly suitable

DETAILED OBSERVATIONS:
- Excellent cleavage stage embryo with optimal cell division
- Minimal fragmentation indicates good developmental potential
- Recommended for fresh transfer or cryopreservation
"""
                    }
                else:
                    return {
                        "success": True,
                        "analysis": f"""
BLASTOCYST ANALYSIS (Day {day}):

1. EXPANSION AND HATCHING:
- Expansion grade: 4 (expanded)
- Hatching status: not hatched
- Zona pellucida: intact, normal thickness

2. INNER CELL MASS (ICM):
- ICM grade: A (many cells, tightly packed)
- Cell morphology: excellent
- Prominence: well-defined

3. TROPHECTODERM (TE):
- TE grade: A (many cells, cohesive epithelium)
- Cell layer: uniform, well-organized
- Quality: excellent

4. OVERALL ASSESSMENT:
- Gardner grade: 4AA (excellent quality)
- Implantation potential: very high
- Transfer recommendation: excellent candidate

DETAILED OBSERVATIONS:
- High-quality expanded blastocyst with excellent morphology
- Both ICM and TE show optimal characteristics
- Strong candidate for single embryo transfer
"""
                    }
            
            processed_image = self.preprocess_image(image_path, "embryo")
            base64_image = self.encode_image_to_base64(processed_image)
            if day <= 3:
                prompt = f"""
                You are an expert embryologist analyzing a Day {day} embryo microscopy image. Please analyze following ASRM/ESHRE guidelines:

                CLEAVAGE STAGE EMBRYO ANALYSIS (Day {day}):
                
                1. CELL COUNT AND DIVISION:
                - Number of blastomeres: [count]
                - Expected cell number for Day {day}: [{2**day}]
                - Division synchrony: [synchronous/asynchronous]
                
                2. FRAGMENTATION ASSESSMENT:
                - Fragmentation percentage: [0-100%]
                - Fragment size: [small/medium/large]
                
                3. GRADING (A-D scale):
                - Grade: [A/B/C/D]
                - Quality assessment: [excellent/good/fair/poor]
                - Transfer suitability: [first choice/suitable/marginal/not suitable]
                """
            else:
                prompt = f"""
                You are an expert embryologist analyzing a Day {day} blastocyst microscopy image. Please analyze using Gardner grading system:

                BLASTOCYST ANALYSIS (Day {day}):
                
                1. EXPANSION ASSESSMENT:
                - Expansion grade (1-6): [grade]
                - Blastocoel cavity: [early/expanding/expanded/hatching/hatched]
                
                2. INNER CELL MASS (ICM):
                - ICM grade (A/B/C): [grade]
                - ICM size: [prominent/moderate/small]
                
                3. TROPHECTODERM (TE):
                - TE grade (A/B/C): [grade]
                - Cell number: [many/several/few]
                
                4. GARDNER GRADING:
                - Complete grade: [expansion][ICM][TE] (e.g., 4AA)
                - Quality category: [top/good/fair/poor]
                """
            return self._query_deepseek(prompt, base64_image)
        except Exception as e:
            return {
                "success": False,
                "error": f"Image analysis failed: {str(e)}",
                "analysis": ""
            }
    def _query_deepseek(self, prompt: str, base64_image: str) -> Dict:
        """Query DeepSeek LLM with image and prompt"""
        try:
            # For Ollama local installation
            payload = {
                "model": "deepseek-coder",
                "prompt": prompt,
                "images": [base64_image],
                "stream": False
            }
            response = requests.post(
                self.deepseek_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "analysis": result.get("response", ""),
                    "model": "deepseek"
                }
            else:
                return {
                    "success": False,
                    "error": f"API Error: {response.status_code}",
                    "analysis": ""
                }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "error": "DeepSeek LLM not available. Please start Ollama service.",
                "analysis": ""
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "analysis": ""
            }
