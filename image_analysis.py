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
            You are an expert andrologist with subspecialty training in male reproductive medicine analyzing a sperm microscopy image for educational purposes. Please provide a comprehensive technical assessment following WHO 2021 laboratory manual guidelines.

            TECHNICAL SPERM ANALYSIS PROTOCOL:

            1. CONCENTRATION ASSESSMENT (WHO 2021 Standards):
            - Estimated concentration (million/ml): [provide estimate - normal >15 million/ml]
            - Sperm density per field: [count visible sperm in field]
            - Distribution pattern: [uniform/clustered/sparse/aggregated]
            - Sample dilution factor: [if applicable]

            2. MOTILITY ASSESSMENT (WHO Categories):
            - Progressive motility (PR) %: [fast/slow forward progression - normal >32%]
            - Non-progressive motility (NP) %: [all other patterns - normal >40% total motile]
            - Immotile sperm (IM) %: [no movement]
            - Motility grade: [Grade A/B/C/D classification]

            3. MORPHOLOGY ASSESSMENT (Kruger Strict Criteria):
            - Normal morphology estimate %: [normal >4% by strict criteria]
            - Head defects: [large/small/tapered/pyriform/round/amorphous/vacuolated/double]
            - Midpiece defects: [bent/thick/thin/asymmetric/cytoplasmic droplets]
            - Tail defects: [short/long/coiled/bent/double/absent]
            - Teratozoospermia index: [average number of defects per abnormal sperm]

            4. CLINICAL CORRELATION (WHO 2021 Reference Values):
            - Concentration classification: [normozoospermia >15M/ml / oligozoospermia <15M/ml / severe <5M/ml]
            - Motility classification: [normozoospermia >32%PR / asthenozoospermia <32%PR]
            - Morphology classification: [normozoospermia >4% / teratozoospermia <4%]
            - Overall WHO classification: [normozoospermia/oligozoospermia/asthenozoospermia/teratozoospermia/combinations]
            - Fertility potential: [excellent/good/reduced/severely compromised]
            - ART recommendation: [IUI suitable/IVF recommended/ICSI required]

            Please provide specific numerical estimates and clinical correlations based on current evidence-based standards.
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
                You are an expert embryologist with 15+ years of experience analyzing Day {day} blastocyst microscopy images for educational purposes. Please provide a comprehensive assessment using the Gardner grading system (Gardner & Schoolcraft, 1999) following ASRM/ESHRE guidelines.

                TECHNICAL BLASTOCYST ANALYSIS PROTOCOL (Day {day}):

                1. EXPANSION ASSESSMENT (Gardner Scale 1-6):
                - Expansion grade: [1=early blastocyst / 2=blastocyst / 3=full blastocyst / 4=expanded / 5=hatching / 6=hatched]
                - Blastocoel cavity: [<50% embryo volume / ≥50% volume / complete / expanded beyond zona / partial hatching / complete hatching]
                - Zona pellucida: [thick/normal/thin/partially dissolved/absent]
                - Overall diameter: [estimate in micrometers]

                2. INNER CELL MASS (ICM) ASSESSMENT (A/B/C):
                - ICM grade: [A=many tightly packed cells / B=several loosely grouped cells / C=very few cells]
                - ICM prominence: [prominent/moderate/barely visible]
                - Cell cohesion: [tightly packed/loosely cohesive/fragmented]
                - ICM position: [optimal/suboptimal/eccentric]

                3. TROPHECTODERM (TE) ASSESSMENT (A/B/C):
                - TE grade: [A=many cells forming cohesive epithelium / B=few cells forming loose epithelium / C=very few large cells]
                - Cell number: [many >64 cells / moderate 32-64 cells / few <32 cells]
                - Epithelial integrity: [cohesive/partially cohesive/fragmented]
                - Cell size uniformity: [uniform/variable/highly variable]

                4. GARDNER GRADING SYSTEM:
                - Complete Gardner grade: [expansion grade][ICM grade][TE grade] (e.g., 4AA, 3BB, 5AB)
                - Quality classification: [Excellent (4-6AA, 4-6AB, 4-6BA) / Good (3-6BB, 1-3AA, 1-3AB, 1-3BA) / Fair (any C grade) / Poor (degenerate)]
                - Implantation potential: [Very High >60% / High 40-60% / Moderate 20-40% / Low <20%]
                - Transfer priority: [First choice / Second choice / Third choice / Not recommended]

                5. CLINICAL RECOMMENDATIONS:
                - Fresh transfer suitability: [Excellent/Good/Marginal/Not suitable]
                - Cryopreservation viability: [Excellent/Good/Fair/Poor]
                - Single embryo transfer (SET) candidate: [Yes/No - justify]
                - Expected clinical pregnancy rate: [estimate percentage based on morphology]

                Please provide precise morphological assessments and evidence-based clinical correlations.
                """
            return self._query_deepseek(prompt, base64_image)
        except Exception as e:
            return {
                "success": False,
                "error": f"Image analysis failed: {str(e)}",
                "analysis": ""
            }
    def _query_deepseek(self, prompt: str, base64_image: str) -> Dict:
        """Query Vision LLM with image and prompt"""
        try:
            # For Ollama local installation - use vision-capable model
            payload = {
                "model": "llava:7b",  # Changed to llava for better vision support
                "prompt": prompt,
                "images": [base64_image],
                "stream": False
            }
            response = requests.post(
                self.deepseek_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=90  # Increased timeout for LLaVA vision analysis
            )
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "analysis": result.get("response", ""),
                    "model": "llava"
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
                "error": "Vision LLM not available. Please start Ollama service and ensure LLaVA model is installed.",
                "analysis": ""
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "analysis": ""
            }
