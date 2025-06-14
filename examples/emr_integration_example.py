"""
IVF EMR Integration Example
==========================

Example code showing how to integrate FertiVision analysis
into an IVF Electronic Medical Record (EMR) system.

This example demonstrates:
- Patient data integration
- Image analysis workflows
- Report generation and storage
- Error handling and logging
- Batch processing capabilities

© 2025 FertiVision powered by AI | Made by greybrain.ai
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fertivision_sdk import FertiVisionClient, FertiVisionError
import json
import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class Patient:
    """Patient data structure for EMR integration"""
    patient_id: str
    name: str
    age: int
    medical_record_number: str
    cycle_number: int
    treatment_protocol: str

@dataclass
class AnalysisRequest:
    """Analysis request structure"""
    patient: Patient
    image_path: str
    analysis_type: str
    case_id: str
    notes: Optional[str] = None
    day: Optional[int] = None  # For embryo analysis

class IVFEMRIntegration:
    """
    Example IVF EMR integration class
    
    This class demonstrates how to integrate FertiVision
    analysis capabilities into an existing EMR system.
    """
    
    def __init__(self, api_key: str, base_url: str = "http://localhost:5003"):
        """Initialize EMR integration"""
        self.client = FertiVisionClient(api_key=api_key, base_url=base_url)
        self.analysis_history = []
        
        # Test API connection
        try:
            health = self.client.health_check()
            api_info = self.client.get_api_info()
            print(f"✅ Connected to FertiVision API")
            print(f"📋 Client: {api_info['client_name']}")
            print(f"🔑 Permissions: {', '.join(api_info['permissions'])}")
        except FertiVisionError as e:
            print(f"❌ Failed to connect to FertiVision API: {e}")
            raise
    
    def process_sperm_analysis(self, request: AnalysisRequest) -> Dict:
        """Process sperm analysis for EMR workflow"""
        print(f"🧬 Processing sperm analysis for patient {request.patient.patient_id}")
        
        try:
            result = self.client.analyze_sperm(
                image_path=request.image_path,
                patient_id=request.patient.patient_id,
                case_id=request.case_id,
                notes=request.notes
            )
            
            # Create EMR-compatible report
            emr_report = {
                'patient_id': request.patient.patient_id,
                'analysis_id': result.analysis_id,
                'analysis_type': 'sperm',
                'timestamp': result.timestamp,
                'classification': result.classification,
                'who_parameters': {
                    'concentration_million_per_ml': result.concentration,
                    'progressive_motility_percent': result.progressive_motility,
                    'normal_morphology_percent': result.normal_morphology,
                    'volume_ml': result.volume
                },
                'clinical_interpretation': self._interpret_sperm_results(result),
                'recommendations': self._generate_sperm_recommendations(result),
                'ai_analysis': result.ai_analysis,
                'processing_mode': result.processing_mode
            }
            
            # Store in analysis history
            self.analysis_history.append(emr_report)
            
            print(f"✅ Sperm analysis completed: {result.classification}")
            return emr_report
            
        except FertiVisionError as e:
            print(f"❌ Sperm analysis failed: {e}")
            return {'error': str(e), 'error_code': e.error_code}
    
    def process_embryo_analysis(self, request: AnalysisRequest) -> Dict:
        """Process embryo analysis for EMR workflow"""
        print(f"👶 Processing embryo analysis for patient {request.patient.patient_id}")
        
        try:
            result = self.client.analyze_embryo(
                image_path=request.image_path,
                day=request.day or 3,
                patient_id=request.patient.patient_id,
                case_id=request.case_id,
                notes=request.notes
            )
            
            # Create EMR-compatible report
            emr_report = {
                'patient_id': request.patient.patient_id,
                'analysis_id': result.analysis_id,
                'analysis_type': 'embryo',
                'timestamp': result.timestamp,
                'classification': result.classification,
                'embryo_parameters': {
                    'development_day': result.day,
                    'cell_count': result.cell_count,
                    'fragmentation_percent': result.fragmentation,
                    'gardner_grade': result.grade
                },
                'clinical_interpretation': self._interpret_embryo_results(result),
                'transfer_recommendation': self._generate_transfer_recommendation(result),
                'ai_analysis': result.ai_analysis,
                'processing_mode': result.processing_mode
            }
            
            # Store in analysis history
            self.analysis_history.append(emr_report)
            
            print(f"✅ Embryo analysis completed: {result.classification}")
            return emr_report
            
        except FertiVisionError as e:
            print(f"❌ Embryo analysis failed: {e}")
            return {'error': str(e), 'error_code': e.error_code}
    
    def process_follicle_scan(self, request: AnalysisRequest) -> Dict:
        """Process follicle scan analysis for EMR workflow"""
        print(f"🔬 Processing follicle scan for patient {request.patient.patient_id}")
        
        try:
            result = self.client.analyze_follicle_scan(
                image_path=request.image_path,
                patient_id=request.patient.patient_id,
                case_id=request.case_id,
                notes=request.notes
            )
            
            # Create EMR-compatible report
            emr_report = {
                'patient_id': request.patient.patient_id,
                'analysis_id': result.analysis_id,
                'analysis_type': 'follicle_scan',
                'timestamp': result.timestamp,
                'classification': result.classification,
                'ovarian_parameters': {
                    'antral_follicle_count': result.parameters.get('afc'),
                    'ovarian_volume': result.parameters.get('ovarian_volume'),
                    'largest_follicle_size': result.parameters.get('largest_follicle')
                },
                'clinical_interpretation': self._interpret_follicle_results(result),
                'stimulation_recommendation': self._generate_stimulation_recommendation(result),
                'ai_analysis': result.ai_analysis,
                'processing_mode': result.processing_mode
            }
            
            # Store in analysis history
            self.analysis_history.append(emr_report)
            
            print(f"✅ Follicle scan completed: {result.classification}")
            return emr_report
            
        except FertiVisionError as e:
            print(f"❌ Follicle scan failed: {e}")
            return {'error': str(e), 'error_code': e.error_code}
    
    def batch_process_cycle(self, patient: Patient, analyses: List[AnalysisRequest]) -> Dict:
        """Process multiple analyses for a complete IVF cycle"""
        print(f"🔄 Processing complete cycle for patient {patient.patient_id}")
        
        cycle_results = {
            'patient_id': patient.patient_id,
            'cycle_number': patient.cycle_number,
            'start_time': datetime.datetime.now().isoformat(),
            'analyses': [],
            'summary': {}
        }
        
        for request in analyses:
            if request.analysis_type == 'sperm':
                result = self.process_sperm_analysis(request)
            elif request.analysis_type == 'embryo':
                result = self.process_embryo_analysis(request)
            elif request.analysis_type == 'follicle':
                result = self.process_follicle_scan(request)
            else:
                result = {'error': f'Unsupported analysis type: {request.analysis_type}'}
            
            cycle_results['analyses'].append(result)
        
        # Generate cycle summary
        cycle_results['summary'] = self._generate_cycle_summary(cycle_results['analyses'])
        cycle_results['end_time'] = datetime.datetime.now().isoformat()
        
        return cycle_results
    
    def _interpret_sperm_results(self, result) -> str:
        """Generate clinical interpretation for sperm analysis"""
        if result.concentration and result.concentration >= 15:
            if result.progressive_motility and result.progressive_motility >= 32:
                if result.normal_morphology and result.normal_morphology >= 4:
                    return "Normal sperm parameters according to WHO 2021 criteria. Excellent fertility potential."
                else:
                    return "Teratozoospermia detected. Consider ICSI for optimal fertilization."
            else:
                return "Asthenozoospermia detected. Reduced motility may affect natural conception."
        else:
            return "Oligozoospermia detected. Low concentration may require assisted reproduction."
    
    def _generate_sperm_recommendations(self, result) -> List[str]:
        """Generate clinical recommendations for sperm analysis"""
        recommendations = []
        
        if result.concentration and result.concentration >= 15:
            recommendations.append("Sperm concentration within normal range")
        else:
            recommendations.append("Consider lifestyle modifications and repeat analysis")
        
        if result.progressive_motility and result.progressive_motility >= 32:
            recommendations.append("Progressive motility adequate for natural conception")
        else:
            recommendations.append("Consider IUI or IVF based on female factors")
        
        if result.normal_morphology and result.normal_morphology >= 4:
            recommendations.append("Normal morphology supports natural fertilization")
        else:
            recommendations.append("ICSI recommended for optimal fertilization rates")
        
        return recommendations
    
    def _interpret_embryo_results(self, result) -> str:
        """Generate clinical interpretation for embryo analysis"""
        if result.grade and 'A' in result.grade:
            return "Excellent quality embryo with high implantation potential."
        elif result.grade and 'B' in result.grade:
            return "Good quality embryo suitable for transfer."
        else:
            return "Lower grade embryo. Consider extended culture or genetic testing."
    
    def _generate_transfer_recommendation(self, result) -> str:
        """Generate transfer recommendation for embryo"""
        if result.grade and 'A' in result.grade:
            return "Recommend single embryo transfer to avoid multiple pregnancy"
        elif result.grade and 'B' in result.grade:
            return "Suitable for transfer. Consider patient age and history"
        else:
            return "Consider extended culture to blastocyst stage"
    
    def _interpret_follicle_results(self, result) -> str:
        """Generate clinical interpretation for follicle scan"""
        afc = result.parameters.get('afc', 0)
        if afc >= 12:
            return "Normal ovarian reserve. Good response to stimulation expected."
        elif afc >= 7:
            return "Adequate ovarian reserve. Standard stimulation protocol recommended."
        else:
            return "Diminished ovarian reserve. Consider high-dose stimulation protocol."
    
    def _generate_stimulation_recommendation(self, result) -> str:
        """Generate stimulation recommendation based on follicle scan"""
        afc = result.parameters.get('afc', 0)
        if afc >= 15:
            return "Risk of OHSS. Consider mild stimulation protocol."
        elif afc >= 7:
            return "Standard stimulation protocol with 150-225 IU FSH."
        else:
            return "High-dose stimulation protocol with 300-450 IU FSH."
    
    def _generate_cycle_summary(self, analyses: List[Dict]) -> Dict:
        """Generate summary for complete IVF cycle"""
        summary = {
            'total_analyses': len(analyses),
            'successful_analyses': len([a for a in analyses if 'error' not in a]),
            'failed_analyses': len([a for a in analyses if 'error' in a]),
            'analysis_types': list(set([a.get('analysis_type', 'unknown') for a in analyses if 'error' not in a]))
        }
        
        return summary
    
    def export_patient_report(self, patient_id: str) -> Dict:
        """Export comprehensive patient report"""
        patient_analyses = [a for a in self.analysis_history if a.get('patient_id') == patient_id]
        
        return {
            'patient_id': patient_id,
            'total_analyses': len(patient_analyses),
            'analyses': patient_analyses,
            'generated_at': datetime.datetime.now().isoformat()
        }

# Example usage
if __name__ == "__main__":
    # Initialize EMR integration
    emr = IVFEMRIntegration(api_key="fv_demo_key_12345")
    
    # Create sample patient
    patient = Patient(
        patient_id="P12345",
        name="Jane Doe",
        age=32,
        medical_record_number="MRN789",
        cycle_number=1,
        treatment_protocol="Long GnRH agonist"
    )
    
    # Example analysis requests
    analyses = [
        AnalysisRequest(
            patient=patient,
            image_path="sample_sperm.jpg",
            analysis_type="sperm",
            case_id="C001",
            notes="Day 0 sperm analysis"
        ),
        AnalysisRequest(
            patient=patient,
            image_path="sample_embryo.jpg",
            analysis_type="embryo",
            case_id="C002",
            day=3,
            notes="Day 3 embryo assessment"
        )
    ]
    
    # Process complete cycle
    print("🏥 Starting IVF EMR Integration Example")
    print("=" * 50)
    
    try:
        cycle_results = emr.batch_process_cycle(patient, analyses)
        print("\n📊 Cycle Summary:")
        print(json.dumps(cycle_results['summary'], indent=2))
        
        # Export patient report
        patient_report = emr.export_patient_report(patient.patient_id)
        print(f"\n📋 Generated report for patient {patient.patient_id}")
        print(f"Total analyses: {patient_report['total_analyses']}")
        
    except Exception as e:
        print(f"❌ Integration example failed: {e}")
    
    print("\n✅ IVF EMR Integration Example Complete")
    print("© 2025 FertiVision powered by AI | Made by greybrain.ai")
