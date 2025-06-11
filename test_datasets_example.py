#!/usr/bin/env python3
"""
FertiVision powered by greybrain.ai - Dataset Testing Example

This script demonstrates how to use the dataset testing module to:
1. Test LLaVA performance on medical images
2. Evaluate different types of medical image analysis
3. Generate performance reports and visualizations
4. Prepare data for future fine-tuning

© 2025 FertiVision powered by greybrain.ai - Advanced AI for Reproductive Medicine

Usage:
    python test_datasets_example.py
"""

import os
import sys
from dataset_testing import (
    MedicalDatasetTester, 
    run_comprehensive_test,
    example_test_local_images,
    example_fine_tuning_data_prep,
    discover_medical_datasets
)

def demo_single_image_testing():
    """Demonstrate testing a single image"""
    print("🔬 Demo: Single Image Testing")
    print("=" * 50)
    
    # Check if we have test images
    test_images = []
    if os.path.exists("uploads"):
        for filename in os.listdir("uploads"):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                test_images.append(os.path.join("uploads", filename))
    
    if not test_images:
        print("No test images found in uploads/ directory")
        print("Please add some medical images to test")
        return
    
    tester = MedicalDatasetTester()
    
    # Test the first image with different analysis types
    test_image = test_images[0]
    print(f"Testing image: {test_image}")
    
    analysis_types = ["ultrasound_follicle", "sperm_analysis", "general_medical"]
    
    for analysis_type in analysis_types:
        print(f"\n📊 Testing with {analysis_type} analysis:")
        result = tester.test_single_image(test_image, analysis_type)
        
        print(f"  Success: {result.success}")
        print(f"  Processing Time: {result.processing_time:.2f}s")
        print(f"  Extracted Metrics: {result.extracted_metrics}")
        
        if result.success:
            # Show first 200 characters of response
            response_preview = result.llava_response[:200] + "..." if len(result.llava_response) > 200 else result.llava_response
            print(f"  Response Preview: {response_preview}")
    
    # Save results
    report_path = tester.save_results("single_image_demo.json")
    print(f"\n💾 Results saved to: {tester.output_dir}")

def demo_performance_analysis():
    """Demonstrate performance analysis capabilities"""
    print("\n📈 Demo: Performance Analysis")
    print("=" * 50)
    
    # Test multiple images to generate meaningful statistics
    tester = MedicalDatasetTester()
    
    # Test all images in uploads folder
    if os.path.exists("uploads"):
        image_count = 0
        for filename in os.listdir("uploads"):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                image_path = os.path.join("uploads", filename)
                
                # Test with follicle analysis (most relevant for our system)
                result = tester.test_single_image(image_path, "ultrasound_follicle")
                image_count += 1
                
                print(f"Tested {filename}: {'✅' if result.success else '❌'} ({result.processing_time:.1f}s)")
                
                if image_count >= 5:  # Limit for demo
                    break
    
    if tester.results:
        # Generate performance report
        report = tester.generate_performance_report()
        
        print(f"\n📊 Performance Summary:")
        print(f"  Total Tests: {report['summary']['total_tests']}")
        print(f"  Success Rate: {report['summary']['success_rate']:.1%}")
        print(f"  Avg Processing Time: {report['summary']['average_processing_time']:.2f}s")
        
        # Create visualizations
        viz_paths = tester.create_visualizations()
        print(f"  Visualizations created: {len(viz_paths)}")
        
        # Save comprehensive report
        report_path = tester.save_results("performance_demo.json")
        print(f"  Full report: {tester.output_dir}")

def demo_dataset_discovery():
    """Demonstrate medical dataset discovery"""
    print("\n🔍 Demo: Medical Dataset Discovery")
    print("=" * 50)
    
    datasets = discover_medical_datasets()
    
    print("Available medical dataset categories:")
    for category, dataset_list in datasets.items():
        print(f"\n📂 {category.upper()}:")
        for dataset_info in dataset_list:
            print(f"  • {dataset_info['name']}")
            print(f"    Description: {dataset_info['description']}")
            print(f"    Analysis Type: {dataset_info['analysis_type']}")

def demo_fine_tuning_preparation():
    """Demonstrate fine-tuning data preparation"""
    print("\n🎯 Demo: Fine-tuning Data Preparation")
    print("=" * 50)
    
    print("This demo shows how to prepare data for fine-tuning LLaVA")
    print("on medical images to improve accuracy.")
    
    # Create a mock fine-tuning dataset
    tester = MedicalDatasetTester()
    
    # Test a few images and analyze results
    test_images = []
    if os.path.exists("uploads"):
        for filename in os.listdir("uploads")[:3]:  # Limit to 3 for demo
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                test_images.append(os.path.join("uploads", filename))
    
    if test_images:
        fine_tuning_samples = []
        
        for image_path in test_images:
            result = tester.test_single_image(image_path, "ultrasound_follicle")
            
            # Create fine-tuning sample
            sample = {
                "image": os.path.basename(image_path),
                "prompt": tester.prompts["ultrasound_follicle"],
                "current_response": result.llava_response if result.success else "Failed",
                "needs_improvement": not result.success,
                "target_metrics": {
                    "follicle_count": "Should extract precise count",
                    "dominant_size": "Should measure in mm",
                    "clinical_assessment": "Should provide medical classification"
                }
            }
            fine_tuning_samples.append(sample)
        
        print(f"Created {len(fine_tuning_samples)} fine-tuning samples")
        print("Each sample contains:")
        print("  • Original image")
        print("  • Analysis prompt")
        print("  • Current LLaVA response")
        print("  • Improvement targets")
        
        # Save fine-tuning data
        import json
        ft_path = os.path.join(tester.output_dir, "fine_tuning_demo.json")
        with open(ft_path, 'w') as f:
            json.dump(fine_tuning_samples, f, indent=2)
        
        print(f"\n💾 Fine-tuning data saved to: {ft_path}")
        print("This data can be used to train a specialized medical vision model")

def main():
    """Main demonstration function"""
    print("🧬 FertiVision powered by greybrain.ai - Dataset Testing Module")
    print("=" * 70)
    print("This demo showcases the dataset testing capabilities for")
    print("evaluating and improving LLaVA's medical image analysis.")
    print("© 2025 FertiVision powered by greybrain.ai")
    print("=" * 70)
    
    # Check if LLaVA is available
    tester = MedicalDatasetTester()
    test_result = tester.query_llava("Test connection", "")
    
    if "Connection" in test_result.get("error", ""):
        print("❌ LLaVA service not available at http://localhost:11434")
        print("Please start Ollama and ensure LLaVA model is installed:")
        print("  ollama pull llava:7b")
        print("  ollama serve")
        return
    
    print("✅ LLaVA service is available")
    
    # Run demonstrations
    try:
        demo_single_image_testing()
        demo_performance_analysis()
        demo_dataset_discovery()
        demo_fine_tuning_preparation()
        
        print("\n🎉 Demo completed successfully!")
        print("Check the generated output directories for detailed results.")
        
    except KeyboardInterrupt:
        print("\n⏹️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        print("Please check your setup and try again")

if __name__ == "__main__":
    main()
