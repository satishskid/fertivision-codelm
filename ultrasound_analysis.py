import base64
import requests
import json
import os
from PIL import Image
import io
from typing import Dict, List, Optional, Tuple
import cv2
import numpy as np
import datetime
from dataclasses import dataclass, asdict
from enum import Enum

class FollicleStage(Enum):
    PRIMORDIAL = "primordial"
    PRIMARY = "primary"
    SECONDARY = "secondary"
    ANTRAL = "antral"
    PREOVULATORY = "preovulatory"
    CORPUS_LUTEUM = "corpus_luteum"

class HysteroscopyFinding(Enum):
    NORMAL = "normal"
    POLYP = "polyp"
    FIBROID = "fibroid"
    ADHESION = "adhesion"
    SEPTUM = "septum"
    HYPERPLASIA = "hyperplasia"
    ATROPHY = "atrophy"

@dataclass
class FollicleAnalysis:
    scan_id: str
    patient_id: str
    ovary_side: str  # left/right/bilateral
    total_follicle_count: int
    antral_follicle_count: int
    dominant_follicle_size: float  # mm
    follicle_sizes: List[float]  # all measured follicles
    ovarian_volume: float  # ml
    stromal_echogenicity: str  # normal/increased/decreased
    blood_flow: str  # normal/increased/decreased
    classification: str
    amh_correlation: str
    ivf_prognosis: str
    notes: str
    timestamp: str

@dataclass
class HysteroscopyAnalysis:
    procedure_id: str
    patient_id: str
    uterine_cavity: str  # normal/abnormal
    endometrial_thickness: float  # mm
    endometrial_pattern: str  # proliferative/secretory/atrophic
    cervical_canal: str  # normal/stenotic/dilated
    tubal_ostia: str  # bilateral_patent/unilateral_patent/bilateral_blocked
    pathological_findings: List[HysteroscopyFinding]
    lesion_locations: List[str]
    lesion_sizes: List[float]
    vascularization: str  # normal/increased/decreased
    classification: str
    treatment_recommendation: str
    biopsy_indicated: bool
    notes: str
    timestamp: str

class UltrasoundAnalyzer:
    def __init__(self, deepseek_api_key: str = None, deepseek_url: str = "http://localhost:11434/api/generate", mock_mode: bool = False):
        """Initialize ultrasound analyzer with DeepSeek LLM"""
        self.deepseek_url = deepseek_url
        self.api_key = deepseek_api_key
        self.mock_mode = mock_mode
        
    def encode_image_to_base64(self, image_path: str) -> str:
        """Convert image to base64 for LLM processing"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def preprocess_ultrasound_image(self, image_path: str, scan_type: str) -> str:
        """Preprocess ultrasound images for better analysis"""
        try:
            image = cv2.imread(image_path)
            if image is None:
                return image_path
            
            if scan_type == "follicle":
                # Enhance contrast for follicle detection
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                # Apply CLAHE for better contrast
                clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
                enhanced = clahe.apply(gray)
                # Convert back to BGR
                enhanced = cv2.cvtColor(enhanced, cv2.COLOR_GRAY2BGR)
                
            elif scan_type == "hysteroscopy":
                # Enhance for endometrial structure visibility
                lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
                l, a, b = cv2.split(lab)
                # Apply CLAHE to L channel
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
                l = clahe.apply(l)
                enhanced = cv2.merge([l, a, b])
                enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
                
            else:
                enhanced = image
            
            # Save preprocessed image (robust path handling)
            base, ext = os.path.splitext(image_path)
            processed_path = f"{base}_processed{ext}"
            cv2.imwrite(processed_path, enhanced)
            
            return processed_path
        except Exception as e:
            print(f"Error preprocessing ultrasound image: {e}")
            return image_path

    def analyze_follicle_scan(self, image_path: str, ovary_side: str = "bilateral") -> FollicleAnalysis:
        """Analyze follicle ultrasound scan using LLaVA LLM"""
        try:
            # Mock mode for testing without LLM service
            if self.mock_mode:
                scan_id = f"follicle_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{os.path.basename(image_path).split('.')[0]}"
                
                return FollicleAnalysis(
                    scan_id=scan_id,
                    patient_id="MOCK_PATIENT_001",
                    ovary_side=ovary_side,
                    total_follicle_count=12,
                    antral_follicle_count=8,
                    dominant_follicle_size=16.5,
                    follicle_sizes=[3.2, 4.1, 5.0, 6.3, 7.8, 8.5, 9.2, 10.1, 11.5, 12.8, 14.2, 16.5],
                    ovarian_volume=8.5,
                    stromal_echogenicity="normal",
                    blood_flow="normal",
                    classification="Normal ovarian reserve",
                    amh_correlation="Estimated AMH 2.5-4.0 ng/ml",
                    ivf_prognosis="Good response expected",
                    notes="Mock analysis - normal reproductive age findings",
                    timestamp=datetime.datetime.now().isoformat()
                )

            processed_image = self.preprocess_ultrasound_image(image_path, "follicle")
            base64_image = self.encode_image_to_base64(processed_image)
            
            prompt = f"""
            You are an expert reproductive endocrinologist analyzing an ovarian follicle ultrasound scan for research and educational purposes. This is a training exercise for medical AI systems. Please analyze this {ovary_side} ovarian ultrasound image and provide detailed assessment:

            FOLLICLE SCAN ANALYSIS REPORT:
            
            1. FOLLICLE COUNT AND ASSESSMENT:
            - Total visible follicles: [count all visible follicles]
            - Antral follicle count (AFC, 2-10mm): [count follicles 2-10mm]
            - Small follicles (2-9mm): [count]
            - Medium follicles (10-17mm): [count]
            - Large follicles (>18mm): [count]
            - Dominant follicle size: [largest follicle in mm]
            
            2. FOLLICLE MEASUREMENTS:
            - List all measurable follicle diameters: [e.g., 15mm, 12mm, 8mm, etc.]
            - Follicle distribution: [uniform/clustered/peripheral]
            - Follicle morphology: [round/oval/irregular]
            
            3. OVARIAN ASSESSMENT:
            - Ovarian volume estimate: [length × width × height × 0.523 in ml]
            - Ovarian shape: [normal/enlarged/atrophic]
            - Stromal echogenicity: [normal/increased/decreased]
            - Stromal texture: [homogeneous/heterogeneous]
            
            4. VASCULAR ASSESSMENT:
            - Ovarian blood flow: [normal/increased/decreased]
            - Follicular blood flow: [present/absent around dominant follicle]
            - Stromal vascularity: [normal/increased/decreased]
            
            5. CYCLE ASSESSMENT:
            - Estimated cycle phase: [follicular/ovulatory/luteal]
            - Ovulation prediction: [imminent/24-48hrs/not predicted]
            - Corpus luteum: [present/absent/size if present]
            
            6. CLINICAL CORRELATION:
            - AFC category: [Low <6 / Normal 6-15 / High >15]
            - Ovarian reserve assessment: [Poor/Normal/High]
            - PCOS indicators: [Present/Absent - multiple small follicles, stromal changes]
            - IVF stimulation prediction: [Poor/Normal/High responder]
            
            7. RECOMMENDATIONS:
            - AMH correlation suggested: [yes/no]
            - Follow-up timing: [days]
            - Additional imaging needed: [yes/no]
            - Clinical action: [continue monitoring/trigger ovulation/adjust medication]
            
            Please provide specific measurements and counts based on visual assessment of the ultrasound image.
            """
            
            # Query LLaVA LLM
            deepseek_result = self._query_deepseek(prompt, base64_image)

            if deepseek_result.get("success"):
                # Parse the AI analysis text and create FollicleAnalysis object
                ai_analysis = deepseek_result.get("analysis", "")
                scan_id = f"follicle_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{os.path.basename(image_path).split('.')[0]}"
                
                # Extract values from AI analysis using simple text parsing
                # This is a simplified parser - in production you'd want more robust parsing
                total_count = self._extract_number_from_text(ai_analysis, "total visible follicles", 8)
                afc_count = self._extract_number_from_text(ai_analysis, "antral follicle count", 6)
                dominant_size = self._extract_number_from_text(ai_analysis, "dominant follicle", 14.0)
                ovarian_volume = self._extract_number_from_text(ai_analysis, "ovarian volume", 7.5)
                
                # Determine classification based on AFC
                if afc_count < 6:
                    classification = "Low ovarian reserve"
                    ivf_prognosis = "Poor response expected"
                elif afc_count > 25:
                    classification = "High ovarian reserve (possible PCOS)"
                    ivf_prognosis = "High response risk - monitor for OHSS"
                else:
                    classification = "Normal ovarian reserve"
                    ivf_prognosis = "Good response expected"
                
                return FollicleAnalysis(
                    scan_id=scan_id,
                    patient_id="AI_PATIENT_001",
                    ovary_side=ovary_side,
                    total_follicle_count=total_count,
                    antral_follicle_count=afc_count,
                    dominant_follicle_size=dominant_size,
                    follicle_sizes=self._extract_follicle_sizes_from_text(ai_analysis),
                    ovarian_volume=ovarian_volume,
                    stromal_echogenicity=self._extract_text_value(ai_analysis, "stromal echogenicity", "normal"),
                    blood_flow=self._extract_text_value(ai_analysis, "blood flow", "normal"),
                    classification=classification,
                    amh_correlation=f"AI-estimated correlation based on AFC: {afc_count}",
                    ivf_prognosis=ivf_prognosis,
                    notes=f"AI Analysis by DeepSeek: {ai_analysis[:200]}..." if len(ai_analysis) > 200 else ai_analysis,
                    timestamp=datetime.datetime.now().isoformat()
                )
            else:
                # Fallback to basic analysis if AI fails
                scan_id = f"follicle_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{os.path.basename(image_path).split('.')[0]}"
                return FollicleAnalysis(
                    scan_id=scan_id,
                    patient_id="FALLBACK_PATIENT_001",
                    ovary_side=ovary_side,
                    total_follicle_count=8,
                    antral_follicle_count=6,
                    dominant_follicle_size=14.0,
                    follicle_sizes=[6.2, 7.1, 8.0, 9.3, 10.8, 12.5, 14.0],
                    ovarian_volume=7.5,
                    stromal_echogenicity="normal",
                    blood_flow="normal",
                    classification="AI analysis failed - fallback assessment",
                    amh_correlation="Unable to correlate - AI analysis failed",
                    ivf_prognosis="Requires manual assessment",
                    notes=f"AI analysis failed: {deepseek_result.get('error', 'Unknown error')}",
                    timestamp=datetime.datetime.now().isoformat()
                )
                
        except Exception as e:
            # Exception fallback
            scan_id = f"follicle_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{os.path.basename(image_path).split('.')[0]}"
            return FollicleAnalysis(
                scan_id=scan_id,
                patient_id="ERROR_PATIENT_001",
                ovary_side=ovary_side,
                total_follicle_count=0,
                antral_follicle_count=0,
                dominant_follicle_size=0.0,
                follicle_sizes=[],
                ovarian_volume=0.0,
                stromal_echogenicity="unknown",
                blood_flow="unknown",
                classification="Analysis failed due to exception",
                amh_correlation="Unable to assess",
                ivf_prognosis="Manual assessment required",
                notes=f"Exception during analysis: {str(e)}",
                timestamp=datetime.datetime.now().isoformat()
            )

    def analyze_hysteroscopy_image(self, image_path: str) -> HysteroscopyAnalysis:
        """Analyze hysteroscopy image using DeepSeek LLM"""
        try:
            # Mock mode for testing without LLM service
            if self.mock_mode:
                procedure_id = f"hysteroscopy_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{os.path.basename(image_path).split('.')[0]}"
                
                return HysteroscopyAnalysis(
                    procedure_id=procedure_id,
                    patient_id="MOCK_PATIENT_001",
                    uterine_cavity="normal",
                    endometrial_thickness=8.5,
                    endometrial_pattern="proliferative",
                    cervical_canal="normal",
                    tubal_ostia="bilateral_patent",
                    pathological_findings=[HysteroscopyFinding.NORMAL],
                    lesion_locations=[],
                    lesion_sizes=[],
                    vascularization="normal",
                    classification="Normal hysteroscopic findings",
                    treatment_recommendation="No treatment required",
                    biopsy_indicated=False,
                    notes="Mock analysis - normal uterine cavity and endometrium",
                    timestamp=datetime.datetime.now().isoformat()
                )
            
            processed_image = self.preprocess_ultrasound_image(image_path, "hysteroscopy")
            base64_image = self.encode_image_to_base64(processed_image)
            
            prompt = """
            You are an expert gynecologist with subspecialty training in reproductive endocrinology and hysteroscopy. This is an educational analysis for medical AI training purposes only. Please provide a comprehensive technical assessment of this hysteroscopic image following AAGL (American Association of Gynecologic Laparoscopists) guidelines.

            TECHNICAL HYSTEROSCOPY ANALYSIS PROTOCOL:
            
            1. UTERINE CAVITY ASSESSMENT:
            - Cavity shape: [triangular/irregular/distorted]
            - Cavity size: [normal/enlarged/small]
            - Cavity walls: [smooth/irregular/nodular]
            - Fundal contour: [normal/indented/irregular]
            
            2. ENDOMETRIAL ASSESSMENT (Detailed Morphological Analysis):
            - Endometrial thickness: [measure in mm - normal range 4-14mm depending on cycle phase]
            - Endometrial pattern: [proliferative/secretory/atrophic/hyperplastic/irregular]
            - Endometrial color: [pink/pale/red/white/yellow - assess vascularization]
            - Endometrial texture: [smooth/rough/irregular/nodular/polypoid]
            - Glandular openings: [visible/not visible/enlarged/irregular distribution]
            - Endometrial-myometrial junction: [clear/irregular/disrupted]
            - Surface irregularities: [present/absent - describe location and characteristics]
            
            3. CERVICAL CANAL:
            - Canal appearance: [normal/stenotic/dilated]
            - Canal walls: [smooth/irregular]
            - Cervical mucus: [present/absent/amount]
            
            4. TUBAL OSTIA:
            - Right ostium: [visible/patent/blocked/not visualized]
            - Left ostium: [visible/patent/blocked/not visualized]
            - Ostial appearance: [normal/inflamed/stenotic]
            
            5. PATHOLOGICAL FINDINGS:
            - Polyps: [present/absent - if present: number, size, location]
            - Fibroids: [present/absent - if present: type, size, location]
            - Adhesions: [present/absent - if present: extent, location]
            - Septum: [present/absent - if present: complete/incomplete]
            - Hyperplasia: [present/absent - if present: focal/diffuse]
            - Other lesions: [describe any other abnormalities]
            
            6. VASCULAR ASSESSMENT:
            - Endometrial vascularity: [normal/increased/decreased]
            - Abnormal vessels: [present/absent]
            - Bleeding: [present/absent/location]
            
            7. OVERALL ASSESSMENT:
            - Cavity classification: [normal/abnormal]
            - Primary diagnosis: [normal/polyp/fibroid/adhesions/septum/hyperplasia/other]
            - Severity: [mild/moderate/severe if abnormal]
            
            8. CLINICAL RECOMMENDATIONS:
            - Biopsy indicated: [yes/no - specify location if yes]
            - Treatment needed: [none/polypectomy/myomectomy/adhesiolysis/septoplasty/other]
            - Follow-up required: [yes/no - timing if yes]
            - Fertility impact: [none/mild/moderate/severe]
            
            Please provide specific measurements and detailed descriptions based on visual assessment.
            """

            # Query LLaVA LLM
            deepseek_result = self._query_deepseek(prompt, base64_image)

            if deepseek_result.get("success"):
                # Parse the AI analysis text and create HysteroscopyAnalysis object
                ai_analysis = deepseek_result.get("analysis", "")
                procedure_id = f"hysteroscopy_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{os.path.basename(image_path).split('.')[0]}"

                # Extract values from AI analysis using simple text parsing
                endometrial_thickness = self._extract_number_from_text(ai_analysis, "endometrial thickness", 8.5)

                # Determine pathological findings based on AI analysis
                pathological_findings = []
                if "polyp" in ai_analysis.lower():
                    pathological_findings.append(HysteroscopyFinding.POLYP)
                elif "fibroid" in ai_analysis.lower():
                    pathological_findings.append(HysteroscopyFinding.FIBROID)
                elif "adhesion" in ai_analysis.lower():
                    pathological_findings.append(HysteroscopyFinding.ADHESIONS)
                elif "septum" in ai_analysis.lower():
                    pathological_findings.append(HysteroscopyFinding.SEPTUM)
                elif "hyperplasia" in ai_analysis.lower():
                    pathological_findings.append(HysteroscopyFinding.HYPERPLASIA)
                else:
                    pathological_findings.append(HysteroscopyFinding.NORMAL)

                # Determine classification and recommendations
                if pathological_findings == [HysteroscopyFinding.NORMAL]:
                    classification = "Normal hysteroscopic findings"
                    treatment_recommendation = "No treatment required"
                    biopsy_indicated = False
                else:
                    classification = "Pathological findings detected"
                    treatment_recommendation = "Further evaluation recommended"
                    biopsy_indicated = True

                return HysteroscopyAnalysis(
                    procedure_id=procedure_id,
                    patient_id="AI_PATIENT_001",
                    uterine_cavity=self._extract_text_value(ai_analysis, "cavity", "normal"),
                    endometrial_thickness=endometrial_thickness,
                    endometrial_pattern=self._extract_text_value(ai_analysis, "endometrial pattern", "proliferative"),
                    cervical_canal=self._extract_text_value(ai_analysis, "cervical canal", "normal"),
                    tubal_ostia=self._extract_text_value(ai_analysis, "tubal ostia", "bilateral_patent"),
                    pathological_findings=pathological_findings,
                    lesion_locations=[],
                    lesion_sizes=[],
                    vascularization=self._extract_text_value(ai_analysis, "vascularization", "normal"),
                    classification=classification,
                    treatment_recommendation=treatment_recommendation,
                    biopsy_indicated=biopsy_indicated,
                    notes=f"AI Analysis by LLaVA: {ai_analysis[:200]}..." if len(ai_analysis) > 200 else ai_analysis,
                    timestamp=datetime.datetime.now().isoformat()
                )
            else:
                # Fallback to basic analysis if AI fails
                procedure_id = f"hysteroscopy_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{os.path.basename(image_path).split('.')[0]}"
                return HysteroscopyAnalysis(
                    procedure_id=procedure_id,
                    patient_id="FALLBACK_PATIENT_001",
                    uterine_cavity="unknown",
                    endometrial_thickness=0.0,
                    endometrial_pattern="unknown",
                    cervical_canal="unknown",
                    tubal_ostia="unknown",
                    pathological_findings=[HysteroscopyFinding.NORMAL],
                    lesion_locations=[],
                    lesion_sizes=[],
                    vascularization="unknown",
                    classification="AI analysis failed - fallback assessment",
                    treatment_recommendation="Manual assessment required",
                    biopsy_indicated=False,
                    notes=f"AI analysis failed: {deepseek_result.get('error', 'Unknown error')}",
                    timestamp=datetime.datetime.now().isoformat()
                )
        except Exception as e:
            return {
                "success": False,
                "error": f"Hysteroscopy analysis failed: {str(e)}",
                "analysis": ""
            }

    def _query_deepseek(self, prompt: str, base64_image: str) -> Dict:
        """Query DeepSeek LLM with image and prompt"""
        try:
            payload = {
                "model": "llava:7b",  # Changed to llava for vision support
                "prompt": prompt,
                "images": [base64_image],
                "stream": False
            }
            
            response = requests.post(
                self.deepseek_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=60  # Longer timeout for complex analysis
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
                "error": "DeepSeek LLM not available. Please start Ollama service.",
                "analysis": ""
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "analysis": ""
            }

    def _extract_number_from_text(self, text: str, keyword: str, default: float) -> float:
        """Extract a number from text based on keyword"""
        try:
            import re
            # Look for patterns like "keyword: 12" or "keyword 12" or "keyword is 12"
            pattern = rf"{keyword}[:\s]*(\d+\.?\d*)"
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return float(match.group(1))
            return default
        except:
            return default

    def _extract_follicle_sizes_from_text(self, text: str) -> List[float]:
        """Extract follicle sizes from AI analysis text"""
        try:
            import re
            # Look for patterns like "15mm, 12mm, 8mm" or "15.2mm"
            pattern = r'(\d+\.?\d*)\s*mm'
            matches = re.findall(pattern, text, re.IGNORECASE)
            sizes = [float(match) for match in matches if 2.0 <= float(match) <= 30.0]  # Reasonable follicle size range
            return sorted(sizes, reverse=True)  # Sort largest to smallest
        except:
            return [14.0, 12.5, 10.8, 9.3, 8.0, 7.1, 6.2]  # Default fallback

    def _extract_text_value(self, text: str, keyword: str, default: str) -> str:
        """Extract text value from AI analysis"""
        try:
            import re
            # Look for patterns like "keyword: value" or "keyword is value"
            pattern = rf"{keyword}[:\s]*(normal|increased|decreased|abnormal|good|poor|high|low)"
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).lower()
            return default
        except:
            return default
