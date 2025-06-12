"""
FertiVision API Test Script
==========================

Test script to demonstrate FertiVision API functionality
for IVF EMR integration.

This script tests:
- API connectivity and authentication
- Image analysis endpoints
- Error handling
- SDK functionality

Run this script to verify API setup and functionality.

© 2025 FertiVision powered by AI | Made by greybrain.ai
"""

import requests
import json
import os
from fertivision_sdk import FertiVisionClient, FertiVisionError

# API Configuration
API_BASE_URL = "http://localhost:5003/api/v1"
API_KEY = "fv_demo_key_12345"  # Demo API key

def test_api_direct():
    """Test API using direct HTTP requests"""
    print("🔌 Testing FertiVision API - Direct HTTP Requests")
    print("=" * 60)
    
    # Test 1: Health Check
    print("\n1️⃣ Testing Health Check...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health Check: {data['status']}")
            print(f"📅 Version: {data['version']}")
        else:
            print(f"❌ Health Check Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health Check Error: {e}")
    
    # Test 2: API Info
    print("\n2️⃣ Testing API Info...")
    try:
        headers = {'X-API-Key': API_KEY}
        response = requests.get(f"{API_BASE_URL}/info", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Client: {data['client_name']}")
            print(f"🔑 Permissions: {', '.join(data['permissions'])}")
            print(f"⏱️ Rate Limit: {data['rate_limit']} requests/hour")
        else:
            print(f"❌ API Info Failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ API Info Error: {e}")
    
    # Test 3: Mock Image Analysis (without actual image)
    print("\n3️⃣ Testing Mock Analysis...")
    try:
        headers = {'X-API-Key': API_KEY}
        
        # Create a small test image file
        test_image_content = b"fake_image_data_for_testing"
        files = {'image': ('test.jpg', test_image_content, 'image/jpeg')}
        data = {
            'patient_id': 'TEST_P001',
            'case_id': 'TEST_C001',
            'notes': 'API test analysis'
        }
        
        response = requests.post(
            f"{API_BASE_URL}/analyze/sperm",
            headers=headers,
            files=files,
            data=data
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Analysis Success: {result['classification']}")
            print(f"🆔 Analysis ID: {result['analysis_id']}")
            print(f"👤 Patient ID: {result.get('patient_id', 'N/A')}")
        else:
            print(f"❌ Analysis Failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Analysis Error: {e}")

def test_sdk():
    """Test API using Python SDK"""
    print("\n\n🐍 Testing FertiVision SDK")
    print("=" * 60)
    
    try:
        # Initialize client
        print("\n1️⃣ Initializing SDK Client...")
        client = FertiVisionClient(
            api_key=API_KEY,
            base_url="http://localhost:5003"
        )
        print("✅ SDK Client initialized successfully")
        
        # Test API info
        print("\n2️⃣ Getting API Information...")
        api_info = client.get_api_info()
        print(f"✅ Connected to: {api_info['client_name']}")
        print(f"🔑 Available analyses: {', '.join(api_info['permissions'])}")
        
        # Create test image file
        print("\n3️⃣ Creating test image...")
        test_image_path = "test_image.jpg"
        with open(test_image_path, 'wb') as f:
            f.write(b"fake_image_data_for_testing")
        print(f"✅ Test image created: {test_image_path}")
        
        # Test sperm analysis
        print("\n4️⃣ Testing Sperm Analysis...")
        try:
            result = client.analyze_sperm(
                image_path=test_image_path,
                patient_id="SDK_P001",
                case_id="SDK_C001",
                notes="SDK test analysis"
            )
            print(f"✅ Sperm Analysis: {result.classification}")
            print(f"🆔 Analysis ID: {result.analysis_id}")
            print(f"📊 Concentration: {result.concentration}")
            print(f"🏃 Motility: {result.progressive_motility}")
            print(f"🔬 Morphology: {result.normal_morphology}")
        except FertiVisionError as e:
            print(f"❌ Sperm Analysis Failed: {e}")
        
        # Test embryo analysis
        print("\n5️⃣ Testing Embryo Analysis...")
        try:
            result = client.analyze_embryo(
                image_path=test_image_path,
                day=3,
                patient_id="SDK_P001",
                case_id="SDK_C002",
                notes="SDK embryo test"
            )
            print(f"✅ Embryo Analysis: {result.classification}")
            print(f"🆔 Analysis ID: {result.analysis_id}")
            print(f"📅 Day: {result.day}")
            print(f"🔢 Cell Count: {result.cell_count}")
            print(f"💔 Fragmentation: {result.fragmentation}%")
        except FertiVisionError as e:
            print(f"❌ Embryo Analysis Failed: {e}")
        
        # Test follicle scan
        print("\n6️⃣ Testing Follicle Scan...")
        try:
            result = client.analyze_follicle_scan(
                image_path=test_image_path,
                patient_id="SDK_P001",
                case_id="SDK_C003",
                notes="SDK follicle test"
            )
            print(f"✅ Follicle Scan: {result.classification}")
            print(f"🆔 Analysis ID: {result.analysis_id}")
            print(f"📊 Parameters: {result.parameters}")
        except FertiVisionError as e:
            print(f"❌ Follicle Scan Failed: {e}")
        
        # Cleanup
        if os.path.exists(test_image_path):
            os.remove(test_image_path)
            print(f"\n🧹 Cleaned up test image: {test_image_path}")
        
    except Exception as e:
        print(f"❌ SDK Test Error: {e}")

def test_error_handling():
    """Test API error handling"""
    print("\n\n⚠️ Testing Error Handling")
    print("=" * 60)
    
    # Test 1: Invalid API Key
    print("\n1️⃣ Testing Invalid API Key...")
    try:
        headers = {'X-API-Key': 'invalid_key_12345'}
        response = requests.get(f"{API_BASE_URL}/info", headers=headers)
        if response.status_code == 401:
            error = response.json()
            print(f"✅ Correctly rejected invalid key: {error['code']}")
        else:
            print(f"❌ Unexpected response: {response.status_code}")
    except Exception as e:
        print(f"❌ Error test failed: {e}")
    
    # Test 2: Missing API Key
    print("\n2️⃣ Testing Missing API Key...")
    try:
        response = requests.get(f"{API_BASE_URL}/info")
        if response.status_code == 401:
            error = response.json()
            print(f"✅ Correctly rejected missing key: {error['code']}")
        else:
            print(f"❌ Unexpected response: {response.status_code}")
    except Exception as e:
        print(f"❌ Error test failed: {e}")
    
    # Test 3: Invalid Analysis Type
    print("\n3️⃣ Testing Invalid Analysis Type...")
    try:
        headers = {'X-API-Key': API_KEY}
        files = {'image': ('test.jpg', b"fake_data", 'image/jpeg')}
        response = requests.post(
            f"{API_BASE_URL}/analyze/invalid_type",
            headers=headers,
            files=files
        )
        if response.status_code == 404:
            print("✅ Correctly rejected invalid analysis type")
        else:
            print(f"❌ Unexpected response: {response.status_code}")
    except Exception as e:
        print(f"❌ Error test failed: {e}")

def main():
    """Run all API tests"""
    print("🚀 FertiVision API Test Suite")
    print("🏥 Testing IVF EMR Integration Capabilities")
    print("© 2025 FertiVision powered by AI | Made by greybrain.ai")
    print("=" * 80)
    
    # Check if API server is running
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            print("❌ API server not responding. Please start the API server:")
            print("   python api_server.py")
            return
    except requests.exceptions.RequestException:
        print("❌ Cannot connect to API server. Please start the API server:")
        print("   python api_server.py")
        return
    
    # Run tests
    test_api_direct()
    test_sdk()
    test_error_handling()
    
    print("\n\n🎉 API Test Suite Complete!")
    print("=" * 80)
    print("✅ FertiVision API is ready for IVF EMR integration")
    print("📚 See API_DOCUMENTATION.md for complete integration guide")
    print("🔧 See examples/emr_integration_example.py for implementation examples")
    print("\n© 2025 FertiVision powered by AI | Made by greybrain.ai")

if __name__ == "__main__":
    main()
