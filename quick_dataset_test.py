#!/usr/bin/env python3
"""
Quick Dataset Testing Demo

Simple demonstration of the dataset testing capabilities
"""

import os
import json
from datetime import datetime

def quick_test():
    """Quick test of dataset testing functionality"""
    print("🧪 Quick Dataset Testing Demo")
    print("=" * 40)
    
    try:
        from dataset_testing import MedicalDatasetTester
        
        # Initialize tester
        tester = MedicalDatasetTester()
        
        # Find test images
        test_images = []
        if os.path.exists("uploads"):
            for filename in os.listdir("uploads"):
                if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                    test_images.append(os.path.join("uploads", filename))
        
        if not test_images:
            print("❌ No test images found in uploads/ directory")
            return
        
        print(f"Found {len(test_images)} test images")
        
        # Test first image
        test_image = test_images[0]
        print(f"\n🔬 Testing: {os.path.basename(test_image)}")
        
        result = tester.test_single_image(test_image, 'ultrasound_follicle')
        
        print(f"✅ Success: {result.success}")
        print(f"⏱️  Processing Time: {result.processing_time:.2f}s")
        print(f"📊 Extracted Metrics: {result.extracted_metrics}")
        
        if result.success:
            response_preview = result.llava_response[:200] + "..." if len(result.llava_response) > 200 else result.llava_response
            print(f"🤖 LLaVA Response Preview:")
            print(f"   {response_preview}")
        
        # Test multiple analysis types on same image
        print(f"\n🔄 Testing different analysis types:")
        analysis_types = ['ultrasound_follicle', 'sperm_analysis', 'general_medical']
        
        for analysis_type in analysis_types:
            result = tester.test_single_image(test_image, analysis_type)
            status = "✅" if result.success else "❌"
            print(f"   {status} {analysis_type}: {result.processing_time:.1f}s")
        
        # Generate report
        print(f"\n📊 Generating performance report...")
        report = tester.generate_performance_report()
        
        print(f"📈 Performance Summary:")
        print(f"   Total Tests: {report['summary']['total_tests']}")
        print(f"   Success Rate: {report['summary']['success_rate']:.1%}")
        print(f"   Avg Processing Time: {report['summary']['average_processing_time']:.2f}s")
        
        # Save results
        report_path = tester.save_results('quick_test_results.json')
        print(f"\n💾 Results saved to: {tester.output_dir}")
        
        # Show sample extracted data
        if tester.results:
            successful_results = [r for r in tester.results if r.success and r.extracted_metrics]
            if successful_results:
                print(f"\n🎯 Sample Extracted Medical Data:")
                for result in successful_results[:2]:  # Show first 2
                    print(f"   {result.analysis_type}: {result.extracted_metrics}")
        
        print(f"\n🎉 Dataset testing demo completed successfully!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please ensure all required packages are installed")
    except Exception as e:
        print(f"❌ Error during testing: {e}")

if __name__ == "__main__":
    quick_test()
