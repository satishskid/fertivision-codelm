#!/usr/bin/env python3
"""
Quick debug test for follicle analysis
"""

import sys
import os
sys.path.append('/Users/spr/fertivisiion codelm')

from enhanced_reproductive_system import EnhancedReproductiveSystem

def test_follicle_analysis():
    print("🧪 Testing EnhancedReproductiveSystem follicle analysis directly")
    
    # Initialize with mock mode enabled
    classifier = EnhancedReproductiveSystem(mock_mode=True)
    
    # Test image path
    image_path = "/Users/spr/fertivisiion codelm/uploads/download (2).jpeg"
    
    try:
        print(f"📸 Testing with image: {image_path}")
        result = classifier.analyze_follicle_scan_with_image(image_path)
        print(f"✅ Result type: {type(result)}")
        print(f"📊 Result keys: {result.keys() if isinstance(result, dict) else 'Not a dict'}")
        print(f"📋 Result: {result}")
        
    except Exception as e:
        print(f"❌ Exception: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_follicle_analysis()
