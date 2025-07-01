#!/usr/bin/env python3
"""
Test script to verify the analysis functionality works correctly
"""

import requests
import json
import os
from io import BytesIO
from PIL import Image

def create_test_image():
    """Create a simple test image"""
    # Create a simple 100x100 test image
    img = Image.new('RGB', (100, 100), color='white')
    
    # Save to bytes
    img_bytes = BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    
    return img_bytes

def test_analysis_endpoint():
    """Test the analysis endpoint with a sample image"""
    base_url = "http://127.0.0.1:5001"
    
    print("🔬 Testing FertiVision Analysis System")
    print("=" * 50)
    
    # Test 1: Check if server is running
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        print("✅ Server is running")
    except requests.exceptions.RequestException as e:
        print(f"❌ Server connection failed: {e}")
        return False
    
    # Test 2: Test follicle analysis endpoint
    print("\n🔬 Testing follicle scan analysis...")
    
    # Create test image
    test_image = create_test_image()
    
    # Prepare request
    files = {
        'image': ('test_follicle.jpg', test_image, 'image/jpeg')
    }
    
    data = {
        'ovary_side': 'left',
        'cycle_day': '12'
    }
    
    try:
        response = requests.post(
            f"{base_url}/analyze_follicle_scan",
            files=files,
            data=data,
            timeout=30
        )
        
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Follicle analysis successful!")
            print(f"   Success: {result.get('success')}")
            print(f"   Classification: {result.get('classification')}")
            print(f"   Scan ID: {result.get('scan_id')}")
            return True
        else:
            print(f"❌ Analysis failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}")
        print(f"   Response: {response.text}")
        return False

def test_image_upload():
    """Test the general image upload endpoint"""
    base_url = "http://127.0.0.1:5001"
    
    print("\n📤 Testing image upload endpoint...")
    
    # Create test image
    test_image = create_test_image()
    
    # Prepare request
    files = {
        'image': ('test_upload.jpg', test_image, 'image/jpeg')
    }
    
    data = {
        'analysis_type': 'follicle'
    }
    
    try:
        response = requests.post(
            f"{base_url}/upload",
            files=files,
            data=data,
            timeout=30
        )
        
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Image upload successful!")
            print(f"   Success: {result.get('success')}")
            return True
        else:
            print(f"❌ Upload failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Upload request failed: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}")
        print(f"   Response: {response.text}")
        return False

if __name__ == "__main__":
    print("🚀 Starting FertiVision Analysis Tests")
    print("=" * 50)
    
    # Test analysis endpoints
    analysis_success = test_analysis_endpoint()
    upload_success = test_image_upload()
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"   Follicle Analysis: {'✅ PASS' if analysis_success else '❌ FAIL'}")
    print(f"   Image Upload: {'✅ PASS' if upload_success else '❌ FAIL'}")
    
    if analysis_success and upload_success:
        print("\n🎉 All tests passed! The system is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Please check the server logs.")
