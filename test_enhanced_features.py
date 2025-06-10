#!/usr/bin/env python3
"""
Test script for enhanced FertiVision features:
- PDF export functionality
- Authentication system
- Extended file format support
- Configuration management
"""

import os
import sys
from config import Config, MedicalDiscipline, AnalysisMode
from pdf_export import PDFReportGenerator
from auth import BasicAuth
from flask import Flask

def test_configuration():
    """Test configuration system"""
    print("🔧 Testing Configuration System...")
    
    # Test file format support
    assert Config.is_file_supported("test.jpg"), "JPG should be supported"
    assert Config.is_file_supported("scan.dcm"), "DICOM should be supported"
    assert Config.is_file_supported("video.mp4"), "MP4 should be supported"
    assert not Config.is_file_supported("doc.txt"), "TXT should not be supported"
    
    # Test discipline detection
    discipline = Config.get_discipline_for_file("sperm_analysis.jpg")
    assert discipline == MedicalDiscipline.ANDROLOGY, f"Expected ANDROLOGY, got {discipline}"
    
    discipline = Config.get_discipline_for_file("embryo_day3.png")
    assert discipline == MedicalDiscipline.EMBRYOLOGY, f"Expected EMBRYOLOGY, got {discipline}"
    
    discipline = Config.get_discipline_for_file("follicle_scan.dcm")
    assert discipline == MedicalDiscipline.REPRODUCTIVE_ENDOCRINOLOGY, f"Expected REPRODUCTIVE_ENDOCRINOLOGY, got {discipline}"
    
    print("✅ Configuration system tests passed!")

def test_pdf_export():
    """Test PDF export functionality"""
    print("📄 Testing PDF Export System...")
    
    try:
        # Create PDF generator
        pdf_gen = PDFReportGenerator(output_folder="test_exports")
        
        # Test sperm analysis report
        sperm_data = {
            'sample_id': 'TEST_SPERM_001',
            'classification': 'Normozoospermia',
            'concentration': 45.0,
            'progressive_motility': 55.0,
            'normal_morphology': 8.0,
            'timestamp': '2025-06-10 14:30:00',
            'image_analysis': 'AI Analysis:\n\nSperm concentration appears normal.\nMotility patterns are within normal range.\nMorphology shows predominantly normal forms.'
        }
        
        pdf_path = pdf_gen.generate_sperm_report(sperm_data)
        assert os.path.exists(pdf_path), "PDF file should be created"
        print(f"✅ Sperm analysis PDF generated: {pdf_path}")
        
        # Test follicle analysis report
        follicle_data = {
            'scan_id': 'TEST_FOLLICLE_001',
            'classification': 'Normal ovarian reserve',
            'antral_follicle_count': 12,
            'ovarian_volume': 8.5,
            'timestamp': '2025-06-10 14:35:00',
            'image_analysis': 'AI Analysis:\n\nFollicle Distribution:\nAntral follicles: 12 (normal range)\nDominant follicle: Present\nOvarian volume: 8.5 mL (normal)'
        }
        
        pdf_path = pdf_gen.generate_follicle_report(follicle_data)
        assert os.path.exists(pdf_path), "Follicle PDF file should be created"
        print(f"✅ Follicle analysis PDF generated: {pdf_path}")
        
        print("✅ PDF export tests passed!")
        
    except Exception as e:
        print(f"❌ PDF export test failed: {e}")
        raise

def test_authentication():
    """Test authentication system"""
    print("🔐 Testing Authentication System...")
    
    try:
        # Create test Flask app
        app = Flask(__name__)
        auth = BasicAuth(app)
        
        # Test credential validation
        valid = auth.validate_credentials(Config.DEFAULT_USERNAME, Config.DEFAULT_PASSWORD)
        assert valid, "Default credentials should be valid"
        
        invalid = auth.validate_credentials("wrong", "password")
        assert not invalid, "Wrong credentials should be invalid"
        
        print("✅ Authentication tests passed!")
        
    except Exception as e:
        print(f"❌ Authentication test failed: {e}")
        raise

def test_enhanced_system():
    """Test enhanced reproductive system features"""
    print("🧬 Testing Enhanced System Features...")
    
    try:
        from enhanced_reproductive_system import EnhancedReproductiveSystem
        
        # Initialize system
        system = EnhancedReproductiveSystem(mock_mode=True)
        
        # Test mock mode switching
        system.set_mock_mode(True)
        assert system.mock_mode == True, "Mock mode should be enabled"
        
        system.set_mock_mode(False)
        assert system.mock_mode == False, "Mock mode should be disabled"
        
        print("✅ Enhanced system tests passed!")
        
    except Exception as e:
        print(f"❌ Enhanced system test failed: {e}")
        raise

def main():
    """Run all tests"""
    print("🚀 Starting Enhanced FertiVision Feature Tests...\n")
    
    try:
        test_configuration()
        print()
        
        test_pdf_export()
        print()
        
        test_authentication()
        print()
        
        test_enhanced_system()
        print()
        
        print("🎉 All enhanced feature tests passed!")
        print("\n📋 FEATURE STATUS:")
        print("✅ Configuration system - Working")
        print("✅ Extended file format support - Working")
        print("✅ Medical discipline detection - Working")
        print("✅ PDF export functionality - Working")
        print("✅ Authentication system - Working")
        print("✅ Enhanced reproductive system - Working")
        
        print("\n🔧 SYSTEM CONFIGURATION:")
        print(f"Analysis Mode: {Config.ANALYSIS_MODE.value}")
        print(f"Authentication: {'Enabled' if Config.ENABLE_AUTH else 'Disabled'}")
        print(f"PDF Export: {'Enabled' if Config.ENABLE_PDF_EXPORT else 'Disabled'}")
        print(f"Supported Formats: {len(Config.ALLOWED_UPLOAD_EXTENSIONS)} formats")
        print(f"DeepSeek URL: {Config.DEEPSEEK_URL}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
