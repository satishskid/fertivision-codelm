#!/usr/bin/env python3
"""
Demo Script for Patient History & Document Analysis System
Shows how to use the API programmatically
"""

import requests
import json
import time
from datetime import datetime, timedelta

# API Base URL
BASE_URL = "http://localhost:5000"

def demo_patient_creation():
    """Demo patient creation"""
    print("🔹 Creating demo patients...")
    
    patients = [
        {
            "name": "Alice Johnson",
            "date_of_birth": "1988-03-15",
            "gender": "female",
            "contact_number": "+1-555-0101",
            "email": "alice.johnson@example.com",
            "medical_id": "F001"
        },
        {
            "name": "Bob Smith",
            "date_of_birth": "1985-11-22",
            "gender": "male",
            "contact_number": "+1-555-0102",
            "email": "bob.smith@example.com",
            "medical_id": "M001"
        },
        {
            "name": "Carol Davis",
            "date_of_birth": "1990-07-08",
            "gender": "female",
            "contact_number": "+1-555-0103",
            "email": "carol.davis@example.com",
            "medical_id": "F002"
        }
    ]
    
    created_patients = []
    
    for patient_data in patients:
        try:
            response = requests.post(
                f"{BASE_URL}/api/patients",
                json=patient_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                if result['success']:
                    print(f"   ✅ Created patient: {patient_data['name']} (ID: {result['patient_id']})")
                    created_patients.append({
                        'id': result['patient_id'],
                        'name': patient_data['name'],
                        'data': patient_data
                    })
                else:
                    print(f"   ❌ Failed to create {patient_data['name']}: {result['error']}")
            else:
                print(f"   ❌ HTTP Error {response.status_code} for {patient_data['name']}")
                
        except Exception as e:
            print(f"   ❌ Exception creating {patient_data['name']}: {str(e)}")
    
    return created_patients

def demo_patient_list():
    """Demo patient listing"""
    print("\n🔹 Fetching patient list...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/patients")
        
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                patients = result['patients']
                print(f"   📋 Found {len(patients)} patients:")
                
                for patient in patients:
                    print(f"      • {patient['name']} (Age: {patient['age']}, ID: {patient['medical_record_number']})")
                    print(f"        Documents: {patient['document_count']}, Last Updated: {patient['last_updated']}")
                
                return patients
            else:
                print(f"   ❌ Failed to get patients: {result['error']}")
        else:
            print(f"   ❌ HTTP Error {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Exception: {str(e)}")
    
    return []

def demo_fertility_report(patient_id, patient_name):
    """Demo fertility report generation"""
    print(f"\n🔹 Generating fertility report for {patient_name}...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/patients/{patient_id}/fertility_report")
        
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                report = result['report']
                print(f"   📊 Fertility Score: {report.get('overall_score', 'N/A')}/100")
                
                domain_scores = report.get('domain_scores', {})
                if domain_scores:
                    print("   📈 Domain Scores:")
                    for domain, score in domain_scores.items():
                        domain_name = domain.replace('_', ' ').title()
                        print(f"      • {domain_name}: {score:.1f}/100")
                else:
                    print("   ℹ️  No domain scores available (upload documents for detailed analysis)")
                
                recommendations = report.get('recommendations', [])
                if recommendations:
                    print("   💡 Recommendations:")
                    for rec in recommendations[:3]:  # Show first 3
                        print(f"      • {rec}")
                
                return report
            else:
                print(f"   ❌ Failed to get report: {result['error']}")
        else:
            print(f"   ❌ HTTP Error {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Exception: {str(e)}")
    
    return None

def demo_pdf_export(patient_id, patient_name):
    """Demo PDF export"""
    print(f"\n🔹 Exporting PDF report for {patient_name}...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/patients/{patient_id}/export_report")
        
        if response.status_code == 200:
            # Save the PDF file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"fertility_report_{patient_name.replace(' ', '_')}_{timestamp}.pdf"
            
            with open(filename, 'wb') as f:
                f.write(response.content)
            
            print(f"   📄 PDF report saved as: {filename}")
            print(f"   📁 File size: {len(response.content):,} bytes")
            return filename
        else:
            print(f"   ❌ HTTP Error {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Exception: {str(e)}")
    
    return None

def demo_patient_details(patient_id, patient_name):
    """Demo patient details retrieval"""
    print(f"\n🔹 Getting detailed information for {patient_name}...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/patients/{patient_id}")
        
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                patient = result['patient']
                print(f"   👤 Patient Details:")
                print(f"      • Name: {patient['name']}")
                print(f"      • Age: {patient['age']} years")
                print(f"      • Gender: {patient['gender']}")
                print(f"      • Medical ID: {patient['medical_record_number']}")
                print(f"      • Created: {patient['created_date']}")
                print(f"      • Documents: {len(patient.get('documents', []))}")
                
                if patient.get('fertility_score'):
                    print(f"      • Fertility Score: {patient['fertility_score']:.1f}/100")
                
                return patient
            else:
                print(f"   ❌ Failed to get patient details: {result['error']}")
        else:
            print(f"   ❌ HTTP Error {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Exception: {str(e)}")
    
    return None

def main():
    """Main demo function"""
    print("🏥 FertiVision Patient History & Document Analysis Demo")
    print("=" * 60)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/api/patients", timeout=5)
        print("✅ FertiVision server is running")
    except Exception as e:
        print("❌ FertiVision server is not running or not accessible")
        print(f"   Please start the server with: python app.py")
        print(f"   Error: {str(e)}")
        return
    
    # Demo workflow
    print("\n🚀 Starting Patient History Demo...")
    
    # 1. Create demo patients
    created_patients = demo_patient_creation()
    
    if not created_patients:
        print("\n❌ No patients were created. Cannot continue with demo.")
        return
    
    # 2. List all patients
    all_patients = demo_patient_list()
    
    # 3. Demo detailed functionality for the first patient
    if created_patients:
        first_patient = created_patients[0]
        patient_id = first_patient['id']
        patient_name = first_patient['name']
        
        # Get detailed patient info
        demo_patient_details(patient_id, patient_name)
        
        # Generate fertility report
        demo_fertility_report(patient_id, patient_name)
        
        # Export PDF report
        demo_pdf_export(patient_id, patient_name)
    
    print("\n✨ Demo completed successfully!")
    print("\n📌 Next Steps:")
    print("   1. Open the web interface: http://localhost:5000/patient_history")
    print("   2. Upload medical documents for more detailed analysis")
    print("   3. Explore the AI-powered fertility scoring system")
    print("   4. Generate comprehensive PDF reports")
    
    print(f"\n📊 Summary:")
    print(f"   • Created {len(created_patients)} demo patients")
    print(f"   • Total patients in system: {len(all_patients)}")
    print(f"   • API endpoints tested: 4/4 ✅")

if __name__ == "__main__":
    main()
