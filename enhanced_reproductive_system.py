import os
import sqlite3
import datetime
import json
from typing import Dict
from werkzeug.utils import secure_filename
from reproductive_classification_system import ReproductiveClassificationSystem, OocyteMaturity
from image_analysis import ImageAnalyzer
import re
from ultrasound_analysis import UltrasoundAnalyzer, FollicleAnalysis, HysteroscopyAnalysis, FollicleStage, HysteroscopyFinding
from enum import Enum

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value
        if hasattr(obj, '__dict__'):
            return {key: value for key, value in obj.__dict__.items()}
        return super().default(obj)

class EnhancedReproductiveSystem(ReproductiveClassificationSystem):
    def __init__(self, db_path: str = "reproductive_analysis.db", upload_folder: str = "uploads", mock_mode: bool = True):
        super().__init__(db_path)
        self.upload_folder = upload_folder
        self.image_analyzer = ImageAnalyzer(mock_mode=mock_mode)
        self.ultrasound_analyzer = UltrasoundAnalyzer(mock_mode=mock_mode)
        self.mock_mode = mock_mode
        self.allowed_extensions = {'png', 'jpg', 'jpeg', 'tiff', 'bmp', 'dcm', 'nii', 'mp4', 'avi', 'mov'}  # Extended format support
        # Create upload directory
        os.makedirs(upload_folder, exist_ok=True)
        # Add image analysis table to database
        self._init_image_tables()
    def _init_image_tables(self):
        """Initialize tables for image analysis storage"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Existing tables...
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS image_analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sample_id TEXT,
                analysis_type TEXT,
                image_path TEXT,
                llm_analysis TEXT,
                processed_data TEXT,
                timestamp TEXT
            )
        ''')
        # Add ultrasound analysis tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS follicle_analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_id TEXT UNIQUE,
                data TEXT,
                timestamp TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS hysteroscopy_analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                procedure_id TEXT UNIQUE,
                data TEXT,
                timestamp TEXT
            )
        ''')
        conn.commit()
        conn.close()
    def allowed_file(self, filename):
        """Check if file extension is allowed"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.allowed_extensions
    def analyze_sperm_with_image(self, image_path: str, **kwargs) -> dict:
        image_result = self.image_analyzer.analyze_sperm_image(image_path)
        if image_result["success"]:
            llm_analysis = image_result["analysis"]
            extracted_params = self._extract_sperm_parameters(llm_analysis)
            merged_params = {**extracted_params, **kwargs}
            classification_result = self.classify_sperm(**merged_params)
            self._store_image_analysis(
                classification_result.sample_id,
                "sperm",
                image_path,
                llm_analysis,
                merged_params
            )
            classification_result.image_analysis = llm_analysis
            classification_result.image_path = image_path
            return classification_result
        else:
            raise Exception(f"Image analysis failed: {image_result['error']}")
    def analyze_oocyte_with_image(self, image_path: str, **kwargs) -> dict:
        image_result = self.image_analyzer.analyze_oocyte_image(image_path)
        if image_result["success"]:
            llm_analysis = image_result["analysis"]
            extracted_params = self._extract_oocyte_parameters(llm_analysis)
            merged_params = {**extracted_params, **kwargs}
            classification_result = self.classify_oocyte(**merged_params)
            self._store_image_analysis(
                classification_result.oocyte_id,
                "oocyte",
                image_path,
                llm_analysis,
                merged_params
            )
            classification_result.image_analysis = llm_analysis
            classification_result.image_path = image_path
            return classification_result
        else:
            raise Exception(f"Image analysis failed: {image_result['error']}")
    def analyze_embryo_with_image(self, image_path: str, day: int, **kwargs) -> dict:
        image_result = self.image_analyzer.analyze_embryo_image(image_path, day)
        if image_result["success"]:
            llm_analysis = image_result["analysis"]
            extracted_params = self._extract_embryo_parameters(llm_analysis, day)
            merged_params = {**extracted_params, **kwargs}
            merged_params['day'] = day
            classification_result = self.classify_embryo(**merged_params)
            self._store_image_analysis(
                classification_result.embryo_id,
                "embryo",
                image_path,
                llm_analysis,
                merged_params
            )
            classification_result.image_analysis = llm_analysis
            classification_result.image_path = image_path
            return classification_result
        else:
            raise Exception(f"Image analysis failed: {image_result['error']}")
    def _extract_sperm_parameters(self, llm_analysis: str) -> dict:
        params = {}
        lines = llm_analysis.split('\n')
        for line in lines:
            if 'concentration' in line.lower() and 'million/ml' in line.lower():
                try:
                    import re
                    match = re.search(r'(\d+\.?\d*)\s*million/ml', line)
                    if match:
                        params['concentration'] = float(match.group(1))
                except:
                    pass
            if 'progressive motility' in line.lower() and '%' in line:
                try:
                    match = re.search(r'(\d+\.?\d*)\s*%', line)
                    if match:
                        params['progressive_motility'] = float(match.group(1))
                except:
                    pass
            if 'normal morphology' in line.lower() and '%' in line:
                try:
                    match = re.search(r'(\d+\.?\d*)\s*%', line)
                    if match:
                        params['normal_morphology'] = float(match.group(1))
                except:
                    pass
        return params
    def _extract_oocyte_parameters(self, llm_analysis: str) -> dict:
        params = {}
        if 'MII' in llm_analysis or 'Metaphase II' in llm_analysis:
            params['maturity'] = OocyteMaturity.MII
        elif 'MI' in llm_analysis or 'Metaphase I' in llm_analysis:
            params['maturity'] = OocyteMaturity.MI
        elif 'GV' in llm_analysis or 'Germinal Vesicle' in llm_analysis:
            params['maturity'] = OocyteMaturity.GV
        import re
        score_match = re.search(r'score.*?(\d)', llm_analysis)
        if score_match:
            params['morphology_score'] = int(score_match.group(1))
        return params
    def _extract_embryo_parameters(self, llm_analysis: str, day: int) -> dict:
        params = {}
        import re
        cell_match = re.search(r'(\d+)\s*(?:blastomeres?|cells?)', llm_analysis)
        if cell_match:
            params['cell_count'] = int(cell_match.group(1))
        frag_match = re.search(r'(\d+\.?\d*)\s*%.*fragmentation', llm_analysis)
        if frag_match:
            params['fragmentation'] = float(frag_match.group(1))
        if day >= 5:
            expansion_match = re.search(r'expansion.*?(\d)', llm_analysis)
            if expansion_match:
                params['expansion'] = expansion_match.group(1)
            icm_match = re.search(r'ICM.*?([ABC])', llm_analysis)
            if icm_match:
                params['inner_cell_mass'] = icm_match.group(1)
            te_match = re.search(r'TE.*?([ABC])', llm_analysis)
            if te_match:
                params['trophectoderm'] = te_match.group(1)
        return params
    def _store_image_analysis(self, sample_id: str, analysis_type: str, image_path: str, llm_analysis: str, processed_data: dict):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO image_analyses 
            (sample_id, analysis_type, image_path, llm_analysis, processed_data, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (sample_id, analysis_type, image_path, llm_analysis, json.dumps(processed_data, cls=CustomJSONEncoder), datetime.datetime.now().isoformat()))
        conn.commit()
        conn.close()
    def generate_enhanced_report(self, analysis_type: str, analysis_id: str) -> str:
        standard_report = self.generate_report(analysis_type, analysis_id)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT image_path, llm_analysis FROM image_analyses 
            WHERE sample_id = ? AND analysis_type = ?
        ''', (analysis_id, analysis_type))
        image_result = cursor.fetchone()
        conn.close()
        if image_result:
            image_path, llm_analysis = image_result
            enhanced_report = standard_report + f"""

IMAGE ANALYSIS SECTION
{'='*50}

Image File: {os.path.basename(image_path)}
Analysis Method: DeepSeek LLM Vision Analysis

DETAILED IMAGE ASSESSMENT:
{llm_analysis}

{'='*50}
"""
            return enhanced_report
        else:
            return standard_report

    def analyze_follicle_scan_with_image(self, image_path: str, **kwargs) -> dict:
        """Analyze follicle scan using LLM vision and ultrasound analysis"""
        try:
            # Use ultrasound analyzer for follicle analysis
            analysis_result = self.ultrasound_analyzer.analyze_follicle_scan(image_path)
            
            # Store the analysis
            self._store_follicle_analysis(analysis_result.scan_id, analysis_result)
            
            # Also store in image analysis table for consistency
            self._store_image_analysis(
                analysis_result.scan_id,
                "follicle",
                image_path,
                f"Follicle count: {analysis_result.total_follicle_count}, Dominant follicle: {analysis_result.dominant_follicle_size}mm",
                {
                    'total_follicle_count': analysis_result.total_follicle_count,
                    'antral_follicle_count': analysis_result.antral_follicle_count,
                    'dominant_follicle_size': analysis_result.dominant_follicle_size,
                    'classification': analysis_result.classification
                }
            )
            
            return {
                'success': True,
                'analysis_id': analysis_result.scan_id,
                'analysis_type': 'follicle',
                'result': analysis_result,
                'image_path': image_path
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'analysis_type': 'follicle'
            }

    def analyze_hysteroscopy_with_image(self, image_path: str, **kwargs) -> dict:
        """Analyze hysteroscopy image using LLM vision and ultrasound analysis"""
        try:
            # Use ultrasound analyzer for hysteroscopy analysis
            analysis_result = self.ultrasound_analyzer.analyze_hysteroscopy_image(image_path)
            
            # Store the analysis
            self._store_hysteroscopy_analysis(analysis_result.procedure_id, analysis_result)
            
            # Also store in image analysis table for consistency
            findings_text = ", ".join([f.value for f in analysis_result.pathological_findings]) if analysis_result.pathological_findings else "Normal"
            self._store_image_analysis(
                analysis_result.procedure_id,
                "hysteroscopy",
                image_path,
                f"Endometrial thickness: {analysis_result.endometrial_thickness}mm, Findings: {findings_text}",
                {
                    'endometrial_thickness': analysis_result.endometrial_thickness,
                    'pathological_findings': [f.value for f in analysis_result.pathological_findings] if analysis_result.pathological_findings else [],
                    'uterine_cavity': analysis_result.uterine_cavity,
                    'classification': analysis_result.classification
                }
            )
            
            return {
                'success': True,
                'analysis_id': analysis_result.procedure_id,
                'analysis_type': 'hysteroscopy',
                'result': analysis_result,
                'image_path': image_path
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'analysis_type': 'hysteroscopy'
            }

    def _store_follicle_analysis(self, scan_id: str, analysis: FollicleAnalysis):
        """Store follicle analysis in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        analysis_data = {
            'total_follicle_count': analysis.total_follicle_count,
            'antral_follicle_count': analysis.antral_follicle_count,
            'dominant_follicle_size': analysis.dominant_follicle_size,
            'follicle_sizes': analysis.follicle_sizes,
            'classification': analysis.classification,
            'ovarian_volume': analysis.ovarian_volume,
            'ivf_prognosis': analysis.ivf_prognosis
        }
        
        cursor.execute('''
            INSERT OR REPLACE INTO follicle_analyses 
            (scan_id, data, timestamp)
            VALUES (?, ?, ?)
        ''', (scan_id, json.dumps(analysis_data), datetime.datetime.now().isoformat()))
        
        conn.commit()
        conn.close()

    def _store_hysteroscopy_analysis(self, procedure_id: str, analysis: HysteroscopyAnalysis):
        """Store hysteroscopy analysis in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        analysis_data = {
            'endometrial_thickness': analysis.endometrial_thickness,
            'pathological_findings': [f.value for f in analysis.pathological_findings] if analysis.pathological_findings else [],
            'uterine_cavity': analysis.uterine_cavity,
            'endometrial_pattern': analysis.endometrial_pattern,
            'classification': analysis.classification,
            'treatment_recommendation': analysis.treatment_recommendation,
            'biopsy_indicated': analysis.biopsy_indicated
        }
        
        cursor.execute('''
            INSERT OR REPLACE INTO hysteroscopy_analyses 
            (procedure_id, data, timestamp)
            VALUES (?, ?, ?)
        ''', (procedure_id, json.dumps(analysis_data), datetime.datetime.now().isoformat()))
        
        conn.commit()
        conn.close()

    def set_mock_mode(self, mock_mode: bool):
        """Switch between mock and real AI analysis"""
        self.mock_mode = mock_mode
        self.image_analyzer.mock_mode = mock_mode
        self.ultrasound_analyzer.mock_mode = mock_mode
    
    def get_analysis_by_id(self, analysis_type: str, analysis_id: str):
        """Get analysis data by ID for PDF export"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        table_map = {
            'sperm': 'sperm_analyses',
            'oocyte': 'oocyte_analyses', 
            'embryo': 'embryo_analyses',
            'follicle': 'follicle_analyses',
            'hysteroscopy': 'hysteroscopy_analyses'
        }
        
        table = table_map.get(analysis_type)
        if not table:
            return None
            
        cursor.execute(f'SELECT * FROM {table} WHERE id = ? OR sample_id = ?', (analysis_id, analysis_id))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            # Convert to dict with column names
            columns = [description[0] for description in cursor.description]
            return dict(zip(columns, result))
        return None
