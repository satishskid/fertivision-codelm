#!/usr/bin/env python3
"""
Test workflow for FertiVision AI-Enhanced Reproductive Classification System
This script tests all major functionality including image analysis and report generation.
"""

import requests
import json
import os
import sys

# Test configuration
BASE_URL = "http://localhost:5002"
TEST_IMAGE_PATH = "/Users/spr/fertivisiion codelm/uploads/download (2).jpeg"

def test_endpoint(endpoint, method="GET", files=None, data=None):
    """Test a specific endpoint"""
    try:
        url = f"{BASE_URL}{endpoint}"
        print(f"🧪 Testing {method} {endpoint}")
        
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, files=files, data=data)
        
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            try:
                json_data = response.json()
                print(f"   Response: {json.dumps(json_data, indent=2)[:200]}...")
                return True, json_data
            except:
                print(f"   Response: {response.text[:200]}...")
                return True, response.text
        else:
            print(f"   Error: {response.text}")
            return False, None
            
    except Exception as e:
        print(f"   Exception: {str(e)}")
        return False, None

def main():
    print("🚀 Starting FertiVision Workflow Test")
    print("=" * 50)
    
    # Test 1: Check if main page loads
    print("\n📄 Testing Main Page")
    success, _ = test_endpoint("/")
    
    # Test 2: Test image analysis endpoints
    if os.path.exists(TEST_IMAGE_PATH):
        print(f"\n🖼️  Testing Image Analysis with: {TEST_IMAGE_PATH}")
        
        analysis_types = ['sperm', 'oocyte', 'embryo', 'follicle', 'hysteroscopy']
        
        for analysis_type in analysis_types:
            print(f"\n🔬 Testing {analysis_type.title()} Analysis")
            
            with open(TEST_IMAGE_PATH, 'rb') as f:
                files = {'image': f}
                success, result = test_endpoint(f"/analyze_image/{analysis_type}", "POST", files=files)
                
                if success and result:
                    print(f"   ✅ {analysis_type.title()} analysis successful")
                    
                    # Test enhanced report generation if analysis was successful
                    if isinstance(result, dict) and result.get('success'):
                        analysis_id = result.get('analysis_id', 'test123')
                        print(f"   📊 Testing enhanced report for {analysis_type}")
                        report_success, report_data = test_endpoint(f"/enhanced_report/{analysis_type}/{analysis_id}")
                        
                        if report_success:
                            print(f"   ✅ Enhanced report generated successfully")
                        else:
                            print(f"   ❌ Enhanced report generation failed")
                else:
                    print(f"   ❌ {analysis_type.title()} analysis failed")
    else:
        print(f"❌ Test image not found: {TEST_IMAGE_PATH}")
    
    print("\n" + "=" * 50)
    print("🏁 Workflow test completed!")

if __name__ == "__main__":
    main()
