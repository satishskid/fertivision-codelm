#!/usr/bin/env python3
"""
Patient History Management System with Document Analysis
Supports importing, uploading, and analyzing medical documents
"""

import os
import json
import sqlite3
import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
from enum import Enum
import uuid
import PyPDF2
import cv2
import numpy as np
from PIL import Image
import base64

class DocumentType(Enum):
    LAB_REPORT = "lab_report"
    ULTRASOUND_IMAGE = "ultrasound_image"
    MICROSCOPY_IMAGE = "microscopy_image"
    MEDICAL_REPORT = "medical_report"
    PRESCRIPTION = "prescription"
    CONSULTATION_NOTES = "consultation_notes"
    SURGICAL_REPORT = "surgical_report"
    IMAGING_STUDY = "imaging_study"
    PATHOLOGY_REPORT = "pathology_report"
    HORMONE_PANEL = "hormone_panel"

class FertilityDomain(Enum):
    MALE_FACTOR = "male_factor"
    FEMALE_FACTOR = "female_factor"
    OVARIAN_FUNCTION = "ovarian_function"
    TUBAL_FACTOR = "tubal_factor"
    UTERINE_FACTOR = "uterine_factor"
    HORMONAL_BALANCE = "hormonal_balance"
    GENETIC_FACTORS = "genetic_factors"
    LIFESTYLE_FACTORS = "lifestyle_factors"

@dataclass
class DocumentAnalysis:
    document_id: str
    document_type: DocumentType
    file_path: str
    extracted_text: str
    key_findings: List[str]
    numerical_values: Dict[str, float]
    fertility_domains: List[FertilityDomain]
    confidence_score: float
    analysis_date: str
    ai_summary: str

@dataclass
class PatientRecord:
    patient_id: str
    name: str
    age: int
    gender: str
    medical_record_number: str
    created_date: str
    last_updated: str
    documents: List[DocumentAnalysis]
    fertility_score: Optional[float] = None
    fertility_breakdown: Optional[Dict[str, float]] = None

@dataclass
class FertilityScoreBreakdown:
    overall_score: float
    male_factor_score: float
    female_factor_score: float
    ovarian_function_score: float
    tubal_factor_score: float
    uterine_factor_score: float
    hormonal_balance_score: float
    genetic_factor_score: float
    lifestyle_factor_score: float
    recommendations: List[str]
    critical_findings: List[str]
    positive_indicators: List[str]
    areas_for_improvement: List[str]

class DocumentAnalyzer:
    """AI-powered document analysis for medical records"""
    
    def __init__(self, deepseek_url: str = "http://localhost:11434/api/generate"):
        self.deepseek_url = deepseek_url
        
    def analyze_pdf_document(self, file_path: str, document_type: DocumentType) -> DocumentAnalysis:
        """Analyze PDF medical documents"""
        document_id = str(uuid.uuid4())
        
        # Extract text from PDF
        extracted_text = self._extract_pdf_text(file_path)
        
        # AI analysis of the document
        ai_analysis = self._analyze_with_ai(extracted_text, document_type)
        
        return DocumentAnalysis(
            document_id=document_id,
            document_type=document_type,
            file_path=file_path,
            extracted_text=extracted_text,
            key_findings=ai_analysis.get('key_findings', []),
            numerical_values=ai_analysis.get('numerical_values', {}),
            fertility_domains=ai_analysis.get('fertility_domains', []),
            confidence_score=ai_analysis.get('confidence_score', 0.0),
            analysis_date=datetime.datetime.now().isoformat(),
            ai_summary=ai_analysis.get('summary', '')
        )
    
    def analyze_image_document(self, file_path: str, document_type: DocumentType) -> DocumentAnalysis:
        """Analyze medical images and scanned documents"""
        document_id = str(uuid.uuid4())
        
        # Extract text using OCR if needed
        extracted_text = self._extract_image_text(file_path)
        
        # AI analysis of the image/document
        ai_analysis = self._analyze_image_with_ai(file_path, document_type)
        
        return DocumentAnalysis(
            document_id=document_id,
            document_type=document_type,
            file_path=file_path,
            extracted_text=extracted_text,
            key_findings=ai_analysis.get('key_findings', []),
            numerical_values=ai_analysis.get('numerical_values', {}),
            fertility_domains=ai_analysis.get('fertility_domains', []),
            confidence_score=ai_analysis.get('confidence_score', 0.0),
            analysis_date=datetime.datetime.now().isoformat(),
            ai_summary=ai_analysis.get('summary', '')
        )
    
    def _extract_pdf_text(self, file_path: str) -> str:
        """Extract text from PDF files"""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            return f"Error extracting PDF text: {str(e)}"
    
    def _extract_image_text(self, file_path: str) -> str:
        """Extract text from images using OCR"""
        try:
            # Basic OCR implementation - in production, use Tesseract OCR
            img = cv2.imread(file_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Placeholder for OCR - would integrate Tesseract here
            return "OCR text extraction would be implemented here"
        except Exception as e:
            return f"Error extracting image text: {str(e)}"
    
    def _analyze_with_ai(self, text: str, document_type: DocumentType) -> Dict[str, Any]:
        """Analyze document text with AI"""
        prompt = f"""
        Analyze this {document_type.value} medical document and extract key fertility-related information:

        Document Text:
        {text}

        Please provide:
        1. Key clinical findings related to fertility
        2. Numerical values (hormone levels, counts, measurements)
        3. Fertility domains affected (male/female factors, ovarian function, etc.)
        4. Confidence score for the analysis (0-1)
        5. Summary of fertility implications

        Format as JSON with keys: key_findings, numerical_values, fertility_domains, confidence_score, summary
        """
        
        # Mock AI response for now - would call DeepSeek/Ollama API
        return {
            "key_findings": [
                "Normal hormone levels detected",
                "Adequate sperm concentration",
                "Regular ovulation patterns"
            ],
            "numerical_values": {
                "FSH": 7.2,
                "LH": 5.1,
                "AMH": 2.8,
                "sperm_concentration": 45.0
            },
            "fertility_domains": [
                FertilityDomain.HORMONAL_BALANCE,
                FertilityDomain.MALE_FACTOR,
                FertilityDomain.OVARIAN_FUNCTION
            ],
            "confidence_score": 0.85,
            "summary": "Overall positive fertility indicators with normal hormonal profile and adequate male factor parameters."
        }
    
    def _analyze_image_with_ai(self, file_path: str, document_type: DocumentType) -> Dict[str, Any]:
        """Analyze medical images with AI vision"""
        # Convert image to base64 for AI analysis
        with open(file_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        
        prompt = f"""
        Analyze this {document_type.value} medical image for fertility-related findings:
        
        Please identify:
        1. Anatomical structures visible
        2. Abnormalities or pathological findings
        3. Quantitative measurements if possible
        4. Fertility implications
        5. Confidence in the analysis
        
        Format as JSON with appropriate keys.
        """
        
        # Mock response - would call DeepSeek vision API
        return {
            "key_findings": [
                "Follicles visible in ovarian tissue",
                "Normal uterine morphology",
                "No obvious pathology detected"
            ],
            "numerical_values": {
                "follicle_count": 12,
                "endometrial_thickness": 8.5
            },
            "fertility_domains": [
                FertilityDomain.OVARIAN_FUNCTION,
                FertilityDomain.UTERINE_FACTOR
            ],
            "confidence_score": 0.78,
            "summary": "Normal reproductive anatomy with adequate follicular development."
        }

class FertilityScoreCalculator:
    """Calculate comprehensive fertility scores from all patient data"""
    
    def __init__(self):
        self.domain_weights = {
            FertilityDomain.MALE_FACTOR: 0.25,
            FertilityDomain.FEMALE_FACTOR: 0.25,
            FertilityDomain.OVARIAN_FUNCTION: 0.15,
            FertilityDomain.TUBAL_FACTOR: 0.10,
            FertilityDomain.UTERINE_FACTOR: 0.10,
            FertilityDomain.HORMONAL_BALANCE: 0.10,
            FertilityDomain.GENETIC_FACTORS: 0.03,
            FertilityDomain.LIFESTYLE_FACTORS: 0.02
        }
    
    def calculate_fertility_score(self, patient_record: PatientRecord) -> FertilityScoreBreakdown:
        """Calculate comprehensive fertility score from all documents"""
        domain_scores = {}
        all_findings = []
        all_numerical_values = {}
        
        # Aggregate data from all documents
        for doc in patient_record.documents:
            all_findings.extend(doc.key_findings)
            all_numerical_values.update(doc.numerical_values)
            
            # Calculate domain-specific scores
            for domain in doc.fertility_domains:
                if domain not in domain_scores:
                    domain_scores[domain] = []
                domain_scores[domain].append(doc.confidence_score)
        
        # Calculate weighted scores for each domain
        final_domain_scores = {}
        for domain, weight in self.domain_weights.items():
            if domain in domain_scores:
                avg_score = sum(domain_scores[domain]) / len(domain_scores[domain])
                final_domain_scores[domain.value] = avg_score * 100
            else:
                final_domain_scores[domain.value] = 50.0  # Neutral score if no data
        
        # Calculate overall fertility score
        overall_score = sum(
            final_domain_scores[domain.value] * weight 
            for domain, weight in self.domain_weights.items()
        )
        
        # Generate recommendations and findings
        recommendations = self._generate_recommendations(final_domain_scores, all_numerical_values)
        critical_findings = self._identify_critical_findings(all_findings, all_numerical_values)
        positive_indicators = self._identify_positive_indicators(all_findings, all_numerical_values)
        areas_for_improvement = self._identify_improvement_areas(final_domain_scores)
        
        return FertilityScoreBreakdown(
            overall_score=round(overall_score, 1),
            male_factor_score=final_domain_scores.get('male_factor', 50.0),
            female_factor_score=final_domain_scores.get('female_factor', 50.0),
            ovarian_function_score=final_domain_scores.get('ovarian_function', 50.0),
            tubal_factor_score=final_domain_scores.get('tubal_factor', 50.0),
            uterine_factor_score=final_domain_scores.get('uterine_factor', 50.0),
            hormonal_balance_score=final_domain_scores.get('hormonal_balance', 50.0),
            genetic_factor_score=final_domain_scores.get('genetic_factors', 50.0),
            lifestyle_factor_score=final_domain_scores.get('lifestyle_factors', 50.0),
            recommendations=recommendations,
            critical_findings=critical_findings,
            positive_indicators=positive_indicators,
            areas_for_improvement=areas_for_improvement
        )
    
    def _generate_recommendations(self, domain_scores: Dict[str, float], numerical_values: Dict[str, float]) -> List[str]:
        """Generate personalized recommendations based on scores and values"""
        recommendations = []
        
        if domain_scores.get('male_factor', 50) < 60:
            recommendations.append("Consider male fertility evaluation and lifestyle modifications")
        
        if domain_scores.get('ovarian_function', 50) < 60:
            recommendations.append("Ovarian reserve testing and reproductive counseling recommended")
        
        if 'AMH' in numerical_values and numerical_values['AMH'] < 1.0:
            recommendations.append("Low AMH levels suggest expedited fertility treatment consideration")
        
        if domain_scores.get('hormonal_balance', 50) < 60:
            recommendations.append("Endocrine evaluation and hormone optimization may be beneficial")
        
        recommendations.append("Regular monitoring and follow-up assessments recommended")
        
        return recommendations
    
    def _identify_critical_findings(self, findings: List[str], numerical_values: Dict[str, float]) -> List[str]:
        """Identify critical findings requiring immediate attention"""
        critical = []
        
        # Check for critical numerical values
        if 'AMH' in numerical_values and numerical_values['AMH'] < 0.5:
            critical.append("Severely diminished ovarian reserve (AMH < 0.5)")
        
        if 'sperm_concentration' in numerical_values and numerical_values['sperm_concentration'] < 5:
            critical.append("Severe oligozoospermia (sperm concentration < 5M/ml)")
        
        # Check for critical findings in text
        critical_keywords = ['azoospermia', 'blocked tubes', 'severe endometriosis', 'ovarian failure']
        for finding in findings:
            for keyword in critical_keywords:
                if keyword.lower() in finding.lower():
                    critical.append(f"Critical finding: {finding}")
        
        return critical
    
    def _identify_positive_indicators(self, findings: List[str], numerical_values: Dict[str, float]) -> List[str]:
        """Identify positive fertility indicators"""
        positive = []
        
        if 'AMH' in numerical_values and numerical_values['AMH'] > 2.0:
            positive.append("Good ovarian reserve (AMH > 2.0)")
        
        if 'sperm_concentration' in numerical_values and numerical_values['sperm_concentration'] > 20:
            positive.append("Normal sperm concentration")
        
        positive_keywords = ['normal', 'adequate', 'good', 'regular ovulation']
        for finding in findings:
            for keyword in positive_keywords:
                if keyword.lower() in finding.lower():
                    positive.append(finding)
        
        return positive
    
    def _identify_improvement_areas(self, domain_scores: Dict[str, float]) -> List[str]:
        """Identify areas that could be improved"""
        areas = []
        
        for domain, score in domain_scores.items():
            if score < 70:
                areas.append(f"{domain.replace('_', ' ').title()}: Score {score:.1f}/100")
        
        return areas

class PatientHistoryManager:
    """Main class for managing patient history and document analysis"""
    
    def __init__(self, db_path: str = "patient_history.db"):
        self.db_path = db_path
        self.document_analyzer = DocumentAnalyzer()
        self.score_calculator = FertilityScoreCalculator()
        self._init_database()
    
    def _init_database(self):
        """Initialize the patient history database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                patient_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER,
                gender TEXT,
                medical_record_number TEXT,
                created_date TEXT,
                last_updated TEXT,
                fertility_score REAL,
                fertility_breakdown TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                document_id TEXT PRIMARY KEY,
                patient_id TEXT,
                document_type TEXT,
                file_path TEXT,
                extracted_text TEXT,
                key_findings TEXT,
                numerical_values TEXT,
                fertility_domains TEXT,
                confidence_score REAL,
                analysis_date TEXT,
                ai_summary TEXT,
                FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_patient(self, name: str, age: int, gender: str, medical_record_number: str = None) -> PatientRecord:
        """Create a new patient record"""
        patient_id = str(uuid.uuid4())
        current_time = datetime.datetime.now().isoformat()
        
        patient = PatientRecord(
            patient_id=patient_id,
            name=name,
            age=age,
            gender=gender,
            medical_record_number=medical_record_number or f"MR-{patient_id[:8]}",
            created_date=current_time,
            last_updated=current_time,
            documents=[]
        )
        
        self._save_patient(patient)
        return patient
    
    def add_document(self, patient_id: str, file_path: str, document_type: DocumentType) -> DocumentAnalysis:
        """Add and analyze a new document for a patient"""
        # Determine file type and analyze accordingly
        if file_path.lower().endswith('.pdf'):
            document_analysis = self.document_analyzer.analyze_pdf_document(file_path, document_type)
        else:
            document_analysis = self.document_analyzer.analyze_image_document(file_path, document_type)
        
        # Save document analysis
        self._save_document(patient_id, document_analysis)
        
        # Update patient's fertility score
        self.update_fertility_score(patient_id)
        
        return document_analysis
    
    def update_fertility_score(self, patient_id: str):
        """Recalculate and update patient's fertility score"""
        patient = self.get_patient(patient_id)
        if patient:
            score_breakdown = self.score_calculator.calculate_fertility_score(patient)
            patient.fertility_score = score_breakdown.overall_score
            patient.fertility_breakdown = asdict(score_breakdown)
            self._save_patient(patient)
    
    def get_patient(self, patient_id: str) -> Optional[PatientRecord]:
        """Get patient record with all documents"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM patients WHERE patient_id = ?', (patient_id,))
        patient_row = cursor.fetchone()
        
        if not patient_row:
            conn.close()
            return None
        
        # Get all documents for this patient
        cursor.execute('SELECT * FROM documents WHERE patient_id = ?', (patient_id,))
        document_rows = cursor.fetchall()
        
        documents = []
        for doc_row in document_rows:
            documents.append(DocumentAnalysis(
                document_id=doc_row[0],
                document_type=DocumentType(doc_row[2]),
                file_path=doc_row[3],
                extracted_text=doc_row[4],
                key_findings=json.loads(doc_row[5]) if doc_row[5] else [],
                numerical_values=json.loads(doc_row[6]) if doc_row[6] else {},
                fertility_domains=[FertilityDomain(d) for d in json.loads(doc_row[7])] if doc_row[7] else [],
                confidence_score=doc_row[8],
                analysis_date=doc_row[9],
                ai_summary=doc_row[10]
            ))
        
        patient = PatientRecord(
            patient_id=patient_row[0],
            name=patient_row[1],
            age=patient_row[2],
            gender=patient_row[3],
            medical_record_number=patient_row[4],
            created_date=patient_row[5],
            last_updated=patient_row[6],
            documents=documents,
            fertility_score=patient_row[7],
            fertility_breakdown=json.loads(patient_row[8]) if patient_row[8] else None
        )
        
        conn.close()
        return patient
    
    def get_all_patients(self) -> List[PatientRecord]:
        """Get all patients (summary only, without documents)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM patients ORDER BY last_updated DESC')
        patient_rows = cursor.fetchall()
        
        patients = []
        for row in patient_rows:
            patients.append(PatientRecord(
                patient_id=row[0],
                name=row[1],
                age=row[2],
                gender=row[3],
                medical_record_number=row[4],
                created_date=row[5],
                last_updated=row[6],
                documents=[],  # Don't load documents for summary
                fertility_score=row[7],
                fertility_breakdown=json.loads(row[8]) if row[8] else None
            ))
        
        conn.close()
        return patients
    
    def create_patient(self, name: str, age: int, gender: str, medical_record_number: str = None) -> PatientRecord:
        """Create a new patient record"""
        patient_id = str(uuid.uuid4())
        current_time = datetime.datetime.now().isoformat()
        
        patient = PatientRecord(
            patient_id=patient_id,
            name=name,
            age=age,
            gender=gender,
            medical_record_number=medical_record_number or f"MR-{patient_id[:8]}",
            created_date=current_time,
            last_updated=current_time,
            documents=[]
        )
        
        self._save_patient(patient)
        return patient
    
    def add_document(self, patient_id: str, file_path: str, document_type: DocumentType) -> DocumentAnalysis:
        """Add and analyze a new document for a patient"""
        # Determine file type and analyze accordingly
        if file_path.lower().endswith('.pdf'):
            document_analysis = self.document_analyzer.analyze_pdf_document(file_path, document_type)
        else:
            document_analysis = self.document_analyzer.analyze_image_document(file_path, document_type)
        
        # Save document analysis
        self._save_document(patient_id, document_analysis)
        
        # Update patient's fertility score
        self.update_fertility_score(patient_id)
        
        return document_analysis
    
    def update_fertility_score(self, patient_id: str):
        """Recalculate and update patient's fertility score"""
        patient = self.get_patient(patient_id)
        if patient:
            score_breakdown = self.score_calculator.calculate_fertility_score(patient)
            patient.fertility_score = score_breakdown.overall_score
            patient.fertility_breakdown = asdict(score_breakdown)
            self._save_patient(patient)
    
    def get_patient(self, patient_id: str) -> Optional[PatientRecord]:
        """Get patient record with all documents"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM patients WHERE patient_id = ?', (patient_id,))
        patient_row = cursor.fetchone()
        
        if not patient_row:
            conn.close()
            return None
        
        # Get all documents for this patient
        cursor.execute('SELECT * FROM documents WHERE patient_id = ?', (patient_id,))
        document_rows = cursor.fetchall()
        
        documents = []
        for doc_row in document_rows:
            documents.append(DocumentAnalysis(
                document_id=doc_row[0],
                document_type=DocumentType(doc_row[2]),
                file_path=doc_row[3],
                extracted_text=doc_row[4],
                key_findings=json.loads(doc_row[5]) if doc_row[5] else [],
                numerical_values=json.loads(doc_row[6]) if doc_row[6] else {},
                fertility_domains=[FertilityDomain(d) for d in json.loads(doc_row[7])] if doc_row[7] else [],
                confidence_score=doc_row[8],
                analysis_date=doc_row[9],
                ai_summary=doc_row[10]
            ))
        
        patient = PatientRecord(
            patient_id=patient_row[0],
            name=patient_row[1],
            age=patient_row[2],
            gender=patient_row[3],
            medical_record_number=patient_row[4],
            created_date=patient_row[5],
            last_updated=patient_row[6],
            documents=documents,
            fertility_score=patient_row[7],
            fertility_breakdown=json.loads(patient_row[8]) if patient_row[8] else None
        )
        
        conn.close()
        return patient
    
    def get_all_patients(self) -> List[PatientRecord]:
        """Get all patients (summary only, without documents)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM patients ORDER BY last_updated DESC')
        patient_rows = cursor.fetchall()
        
        patients = []
        for row in patient_rows:
            patients.append(PatientRecord(
                patient_id=row[0],
                name=row[1],
                age=row[2],
                gender=row[3],
                medical_record_number=row[4],
                created_date=row[5],
                last_updated=row[6],
                documents=[],  # Don't load documents for summary
                fertility_score=row[7],
                fertility_breakdown=json.loads(row[8]) if row[8] else None
            ))
        
        conn.close()
        return patients
    
    def _save_patient(self, patient: PatientRecord):
        """Save patient record to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO patients 
            (patient_id, name, age, gender, medical_record_number, created_date, last_updated, fertility_score, fertility_breakdown)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            patient.patient_id,
            patient.name,
            patient.age,
            patient.gender,
            patient.medical_record_number,
            patient.created_date,
            datetime.datetime.now().isoformat(),
            patient.fertility_score,
            json.dumps(patient.fertility_breakdown) if patient.fertility_breakdown else None
        ))
        
        conn.commit()
        conn.close()
    
    def _save_document(self, patient_id: str, document: DocumentAnalysis):
        """Save document analysis to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO documents
            (document_id, patient_id, document_type, file_path, extracted_text, key_findings, 
             numerical_values, fertility_domains, confidence_score, analysis_date, ai_summary)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            document.document_id,
            patient_id,
            document.document_type.value,
            document.file_path,
            document.extracted_text,
            json.dumps(document.key_findings),
            json.dumps(document.numerical_values),
            json.dumps([d.value for d in document.fertility_domains]),
            document.confidence_score,
            document.analysis_date,
            document.ai_summary
        ))
        
        conn.commit()
        conn.close()
    
    def generate_comprehensive_report(self, patient_id: str) -> str:
        """Generate a comprehensive fertility report for a patient"""
        patient = self.get_patient(patient_id)
        if not patient:
            return "Patient not found"
        
        if not patient.fertility_breakdown:
            return "No fertility analysis available for this patient"
        
        breakdown = FertilityScoreBreakdown(**patient.fertility_breakdown)
        
        report = f"""
COMPREHENSIVE FERTILITY ASSESSMENT REPORT
{'='*60}

PATIENT INFORMATION:
- Name: {patient.name}
- Medical Record: {patient.medical_record_number}
- Age: {patient.age}
- Gender: {patient.gender}
- Assessment Date: {patient.last_updated[:10]}

OVERALL FERTILITY SCORE: {breakdown.overall_score}/100
{'='*60}

DOMAIN-SPECIFIC SCORES:
- Male Factor: {breakdown.male_factor_score:.1f}/100
- Female Factor: {breakdown.female_factor_score:.1f}/100
- Ovarian Function: {breakdown.ovarian_function_score:.1f}/100
- Tubal Factor: {breakdown.tubal_factor_score:.1f}/100
- Uterine Factor: {breakdown.uterine_factor_score:.1f}/100
- Hormonal Balance: {breakdown.hormonal_balance_score:.1f}/100
- Genetic Factors: {breakdown.genetic_factor_score:.1f}/100
- Lifestyle Factors: {breakdown.lifestyle_factor_score:.1f}/100

CRITICAL FINDINGS:
{self._format_list(breakdown.critical_findings)}

POSITIVE INDICATORS:
{self._format_list(breakdown.positive_indicators)}

AREAS FOR IMPROVEMENT:
{self._format_list(breakdown.areas_for_improvement)}

RECOMMENDATIONS:
{self._format_list(breakdown.recommendations)}

DOCUMENT ANALYSIS SUMMARY:
{'-'*40}
Total Documents Analyzed: {len(patient.documents)}
"""

        for i, doc in enumerate(patient.documents, 1):
            report += f"""
Document {i}: {doc.document_type.value.replace('_', ' ').title()}
- Analysis Date: {doc.analysis_date[:10]}
- Confidence Score: {doc.confidence_score:.2f}
- Key Findings: {'; '.join(doc.key_findings[:3])}
- AI Summary: {doc.ai_summary[:100]}...
"""

        report += f"""
{'='*60}
Report generated by FertiVision AI-Enhanced Reproductive Classification System
Analysis based on {len(patient.documents)} medical documents
Assessment Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return report
    
    def _format_list(self, items: List[str]) -> str:
        """Format list items for report"""
        if not items:
            return "- None identified"
        return '\n'.join(f"- {item}" for item in items)
    
    def generate_fertility_score_data(self, patient_id: str) -> Dict[str, Any]:
        """Generate fertility score data as a dictionary"""
        patient = self.get_patient(patient_id)
        if not patient:
            return {
                'overall_score': 0,
                'domain_scores': {},
                'recommendations': ['Patient not found'],
                'patient_name': 'Unknown',
                'analysis_date': datetime.datetime.now().isoformat()
            }
        
        # Calculate fertility scores if not already calculated
        if not patient.fertility_breakdown:
            fertility_score = self.score_calculator.calculate_fertility_score(patient)
            patient.fertility_score = fertility_score.overall_score
            patient.fertility_breakdown = {
                'overall_score': fertility_score.overall_score,
                'male_factor_score': fertility_score.male_factor_score,
                'female_factor_score': fertility_score.female_factor_score,
                'ovarian_function_score': fertility_score.ovarian_function_score,
                'tubal_factor_score': fertility_score.tubal_factor_score,
                'uterine_factor_score': fertility_score.uterine_factor_score,
                'hormonal_balance_score': fertility_score.hormonal_balance_score,
                'genetic_factor_score': fertility_score.genetic_factor_score,
                'lifestyle_factor_score': fertility_score.lifestyle_factor_score,
                'recommendations': fertility_score.recommendations
            }
            self._save_patient(patient)
        
        breakdown = patient.fertility_breakdown
        
        return {
            'overall_score': breakdown.get('overall_score', 0),
            'domain_scores': {
                'male_factor': breakdown.get('male_factor_score', 0),
                'female_factor': breakdown.get('female_factor_score', 0),
                'ovarian_function': breakdown.get('ovarian_function_score', 0),
                'tubal_factor': breakdown.get('tubal_factor_score', 0),
                'uterine_factor': breakdown.get('uterine_factor_score', 0),
                'hormonal_balance': breakdown.get('hormonal_balance_score', 0),
                'genetic_factors': breakdown.get('genetic_factor_score', 0),
                'lifestyle_factors': breakdown.get('lifestyle_factor_score', 0)
            },
            'recommendations': breakdown.get('recommendations', [
                'Upload medical documents for detailed analysis',
                'Consult with fertility specialist',
                'Maintain healthy lifestyle'
            ]),
            'patient_name': patient.name,
            'patient_id': patient.patient_id,
            'analysis_date': patient.last_updated,
            'document_count': len(patient.documents)
        }
