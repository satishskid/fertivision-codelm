"""
Medical Dataset Testing Module for FertiVision powered by greybrain.ai

This module provides functionality to:
1. Download and test medical image datasets from Hugging Face
2. Evaluate LLaVA performance on different medical image types
3. Generate performance metrics and reports
4. Prepare data for future fine-tuning

Supported medical image types:
- Ultrasound images (ovarian, follicle scans)
- Microscopy images (sperm, oocyte, embryo)
- Hysteroscopy images
- General medical imaging datasets

© 2025 FertiVision powered by greybrain.ai - Advanced AI for Reproductive Medicine
"""

import os
import json
import requests
import base64
import pandas as pd
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import numpy as np

# Try to import Hugging Face datasets
try:
    from datasets import load_dataset, Dataset
    HF_AVAILABLE = True
except ImportError:
    print("Hugging Face datasets not installed. Install with: pip install datasets")
    HF_AVAILABLE = False
    # Create dummy Dataset class for type hints
    class Dataset:
        pass

@dataclass
class DatasetTestResult:
    """Results from testing a dataset"""
    dataset_name: str
    image_path: str
    ground_truth: Optional[str]
    llava_response: str
    analysis_type: str
    success: bool
    processing_time: float
    confidence_score: Optional[float]
    extracted_metrics: Dict
    timestamp: str

class MedicalDatasetTester:
    """Main class for testing medical datasets with LLaVA"""
    
    def __init__(self, llava_url: str = "http://localhost:11434/api/generate"):
        self.llava_url = llava_url
        self.results = []
        self.test_session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = f"dataset_tests_{self.test_session_id}"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Medical image analysis prompts
        self.prompts = {
            "ultrasound_follicle": """
            Analyze this ovarian ultrasound image for educational purposes:
            1. Count total visible follicles
            2. Estimate antral follicle count (AFC, 2-10mm)
            3. Identify dominant follicle size
            4. Assess ovarian reserve (Low/Normal/High)
            5. Provide clinical classification
            """,
            
            "sperm_analysis": """
            Analyze this sperm microscopy image for educational purposes:
            1. Estimate sperm concentration
            2. Assess motility patterns visible
            3. Evaluate morphology (normal vs abnormal)
            4. Provide WHO classification
            5. Assess fertility potential
            """,
            
            "embryo_analysis": """
            Analyze this embryo microscopy image for educational purposes:
            1. Determine developmental stage (cleavage/blastocyst)
            2. Count cell number if cleavage stage
            3. Assess fragmentation level
            4. Evaluate morphology grade
            5. Predict implantation potential
            """,
            
            "oocyte_analysis": """
            Analyze this oocyte microscopy image for educational purposes:
            1. Assess maturity stage (MII/MI/GV)
            2. Evaluate zona pellucida
            3. Assess cytoplasm quality
            4. Check for polar body
            5. Grade ICSI suitability
            """,
            
            "general_medical": """
            Analyze this medical image for educational purposes:
            1. Identify the type of medical imaging
            2. Describe key anatomical structures
            3. Note any abnormalities
            4. Provide clinical assessment
            5. Suggest follow-up if needed
            """
        }
    
    def download_huggingface_dataset(self, dataset_name: str, subset: Optional[str] = None, 
                                   split: str = "train", max_samples: int = 50) -> Optional[Dataset]:
        """Download dataset from Hugging Face"""
        if not HF_AVAILABLE:
            print("Hugging Face datasets not available")
            return None
            
        try:
            print(f"Downloading dataset: {dataset_name}")
            if subset:
                dataset = load_dataset(dataset_name, subset, split=split)
            else:
                dataset = load_dataset(dataset_name, split=split)
            
            # Limit samples for testing
            if len(dataset) > max_samples:
                dataset = dataset.select(range(max_samples))
                
            print(f"Downloaded {len(dataset)} samples from {dataset_name}")
            return dataset
            
        except Exception as e:
            print(f"Error downloading dataset {dataset_name}: {e}")
            return None
    
    def encode_image_to_base64(self, image_path: str) -> str:
        """Convert image to base64 for LLaVA API"""
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            print(f"Error encoding image {image_path}: {e}")
            return ""
    
    def query_llava(self, prompt: str, image_path: str, timeout: int = 90) -> Dict:
        """Query LLaVA with image and prompt"""
        try:
            base64_image = self.encode_image_to_base64(image_path)
            if not base64_image:
                return {"success": False, "error": "Failed to encode image"}
            
            payload = {
                "model": "llava:7b",
                "prompt": prompt,
                "images": [base64_image],
                "stream": False
            }
            
            start_time = datetime.now()
            response = requests.post(
                self.llava_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=timeout
            )
            processing_time = (datetime.now() - start_time).total_seconds()
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "response": result.get("response", ""),
                    "processing_time": processing_time
                }
            else:
                return {
                    "success": False,
                    "error": f"API Error: {response.status_code}",
                    "processing_time": processing_time
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "processing_time": 0
            }
    
    def extract_metrics_from_response(self, response: str, analysis_type: str) -> Dict:
        """Extract numerical metrics from LLaVA response"""
        import re
        metrics = {}
        response_lower = response.lower()

        if analysis_type == "ultrasound_follicle":
            # Extract follicle counts
            
            # Look for follicle counts
            follicle_patterns = [
                r'total.*?follicles?.*?(\d+)',
                r'(\d+).*?total.*?follicles?',
                r'afc.*?(\d+)',
                r'antral.*?follicle.*?count.*?(\d+)'
            ]
            
            for pattern in follicle_patterns:
                match = re.search(pattern, response_lower)
                if match:
                    metrics['follicle_count'] = int(match.group(1))
                    break
            
            # Look for dominant follicle size
            size_patterns = [
                r'dominant.*?follicle.*?(\d+\.?\d*)\s*mm',
                r'largest.*?follicle.*?(\d+\.?\d*)\s*mm',
                r'(\d+\.?\d*)\s*mm.*?dominant'
            ]
            
            for pattern in size_patterns:
                match = re.search(pattern, response_lower)
                if match:
                    metrics['dominant_size_mm'] = float(match.group(1))
                    break
        
        elif analysis_type == "sperm_analysis":
            # Extract sperm metrics
            concentration_patterns = [
                r'concentration.*?(\d+\.?\d*)\s*million',
                r'(\d+\.?\d*)\s*million.*?ml',
                r'(\d+\.?\d*)\s*m/ml'
            ]
            
            for pattern in concentration_patterns:
                match = re.search(pattern, response_lower)
                if match:
                    metrics['concentration_million_per_ml'] = float(match.group(1))
                    break
        
        return metrics

    def test_single_image(self, image_path: str, analysis_type: str,
                         ground_truth: Optional[str] = None) -> DatasetTestResult:
        """Test a single image with LLaVA"""
        prompt = self.prompts.get(analysis_type, self.prompts["general_medical"])

        # Query LLaVA
        result = self.query_llava(prompt, image_path)

        # Extract metrics
        extracted_metrics = {}
        if result["success"]:
            extracted_metrics = self.extract_metrics_from_response(
                result["response"], analysis_type
            )

        # Create test result
        test_result = DatasetTestResult(
            dataset_name="single_image",
            image_path=image_path,
            ground_truth=ground_truth,
            llava_response=result.get("response", ""),
            analysis_type=analysis_type,
            success=result["success"],
            processing_time=result.get("processing_time", 0),
            confidence_score=None,  # Could be extracted from response
            extracted_metrics=extracted_metrics,
            timestamp=datetime.now().isoformat()
        )

        self.results.append(test_result)
        return test_result

    def test_dataset(self, dataset_name: str, analysis_type: str,
                    subset: Optional[str] = None, max_samples: int = 20) -> List[DatasetTestResult]:
        """Test an entire dataset from Hugging Face"""
        dataset = self.download_huggingface_dataset(
            dataset_name, subset=subset, max_samples=max_samples
        )

        if not dataset:
            print(f"Failed to download dataset: {dataset_name}")
            return []

        results = []
        print(f"Testing {len(dataset)} samples with LLaVA...")

        for i, sample in enumerate(dataset):
            try:
                # Save image temporarily
                image = sample.get('image') or sample.get('img')
                if image is None:
                    print(f"No image found in sample {i}")
                    continue

                # Convert PIL image to file
                temp_image_path = os.path.join(self.output_dir, f"temp_image_{i}.jpg")
                if hasattr(image, 'save'):
                    image.save(temp_image_path)
                else:
                    print(f"Invalid image format in sample {i}")
                    continue

                # Get ground truth if available
                ground_truth = sample.get('label') or sample.get('caption') or sample.get('text')
                if ground_truth and not isinstance(ground_truth, str):
                    ground_truth = str(ground_truth)

                # Test the image
                print(f"Testing sample {i+1}/{len(dataset)}")
                result = self.test_single_image(temp_image_path, analysis_type, ground_truth)
                result.dataset_name = dataset_name
                results.append(result)

                # Clean up temp file
                if os.path.exists(temp_image_path):
                    os.remove(temp_image_path)

            except Exception as e:
                print(f"Error testing sample {i}: {e}")
                continue

        print(f"Completed testing {len(results)} samples")
        return results

    def generate_performance_report(self) -> Dict:
        """Generate comprehensive performance report"""
        if not self.results:
            return {"error": "No test results available"}

        # Basic statistics
        total_tests = len(self.results)
        successful_tests = sum(1 for r in self.results if r.success)
        success_rate = successful_tests / total_tests if total_tests > 0 else 0

        # Processing time statistics
        processing_times = [r.processing_time for r in self.results if r.processing_time > 0]
        avg_processing_time = np.mean(processing_times) if processing_times else 0

        # Analysis type breakdown
        analysis_types = {}
        for result in self.results:
            analysis_type = result.analysis_type
            if analysis_type not in analysis_types:
                analysis_types[analysis_type] = {"total": 0, "successful": 0}
            analysis_types[analysis_type]["total"] += 1
            if result.success:
                analysis_types[analysis_type]["successful"] += 1

        # Calculate success rates by type
        for analysis_type in analysis_types:
            stats = analysis_types[analysis_type]
            stats["success_rate"] = stats["successful"] / stats["total"] if stats["total"] > 0 else 0

        report = {
            "test_session_id": self.test_session_id,
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_tests": total_tests,
                "successful_tests": successful_tests,
                "success_rate": success_rate,
                "average_processing_time": avg_processing_time
            },
            "analysis_type_breakdown": analysis_types,
            "detailed_results": [
                {
                    "dataset": r.dataset_name,
                    "image": os.path.basename(r.image_path),
                    "type": r.analysis_type,
                    "success": r.success,
                    "processing_time": r.processing_time,
                    "metrics": r.extracted_metrics
                }
                for r in self.results
            ]
        }

        return report

    def save_results(self, filename: Optional[str] = None) -> str:
        """Save test results to JSON file"""
        if filename is None:
            filename = f"test_results_{self.test_session_id}.json"

        filepath = os.path.join(self.output_dir, filename)
        report = self.generate_performance_report()

        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"Results saved to: {filepath}")
        return filepath

    def create_visualizations(self) -> List[str]:
        """Create performance visualization charts"""
        if not self.results:
            print("No results to visualize")
            return []

        plt.style.use('seaborn-v0_8')
        fig_paths = []

        # 1. Success Rate by Analysis Type
        analysis_types = {}
        for result in self.results:
            analysis_type = result.analysis_type
            if analysis_type not in analysis_types:
                analysis_types[analysis_type] = {"total": 0, "successful": 0}
            analysis_types[analysis_type]["total"] += 1
            if result.success:
                analysis_types[analysis_type]["successful"] += 1

        types = list(analysis_types.keys())
        success_rates = [analysis_types[t]["successful"] / analysis_types[t]["total"]
                        for t in types]

        plt.figure(figsize=(10, 6))
        bars = plt.bar(types, success_rates, color='skyblue', alpha=0.7)
        plt.title('LLaVA Success Rate by Analysis Type')
        plt.ylabel('Success Rate')
        plt.xlabel('Analysis Type')
        plt.xticks(rotation=45)
        plt.ylim(0, 1)

        # Add value labels on bars
        for bar, rate in zip(bars, success_rates):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                    f'{rate:.2%}', ha='center', va='bottom')

        plt.tight_layout()
        fig_path = os.path.join(self.output_dir, 'success_rates.png')
        plt.savefig(fig_path, dpi=300, bbox_inches='tight')
        plt.close()
        fig_paths.append(fig_path)

        # 2. Processing Time Distribution
        processing_times = [r.processing_time for r in self.results if r.processing_time > 0]
        if processing_times:
            plt.figure(figsize=(10, 6))
            plt.hist(processing_times, bins=20, color='lightgreen', alpha=0.7, edgecolor='black')
            plt.title('LLaVA Processing Time Distribution')
            plt.xlabel('Processing Time (seconds)')
            plt.ylabel('Frequency')
            plt.axvline(np.mean(processing_times), color='red', linestyle='--',
                       label=f'Mean: {np.mean(processing_times):.2f}s')
            plt.legend()
            plt.tight_layout()
            fig_path = os.path.join(self.output_dir, 'processing_times.png')
            plt.savefig(fig_path, dpi=300, bbox_inches='tight')
            plt.close()
            fig_paths.append(fig_path)

        print(f"Visualizations saved: {fig_paths}")
        return fig_paths

# Predefined medical datasets for testing
MEDICAL_DATASETS = {
    "ultrasound": [
        {
            "name": "keremberke/ultrasound-image-classification",
            "description": "Ultrasound image classification dataset",
            "analysis_type": "ultrasound_follicle",
            "subset": None
        }
    ],
    "microscopy": [
        {
            "name": "keremberke/blood-cell-object-detection",
            "description": "Blood cell microscopy images",
            "analysis_type": "general_medical",
            "subset": None
        }
    ],
    "medical_general": [
        {
            "name": "alkzar90/NIH-Chest-X-ray-dataset",
            "description": "NIH Chest X-ray dataset",
            "analysis_type": "general_medical",
            "subset": None
        },
        {
            "name": "keremberke/chest-xray-classification",
            "description": "Chest X-ray classification",
            "analysis_type": "general_medical",
            "subset": None
        }
    ]
}

def discover_medical_datasets() -> Dict:
    """Discover available medical datasets on Hugging Face"""
    print("🔍 Discovering medical datasets on Hugging Face...")

    # This would ideally use the Hugging Face Hub API to search
    # For now, return our curated list
    return MEDICAL_DATASETS

def run_comprehensive_test(max_samples_per_dataset: int = 10) -> str:
    """Run comprehensive testing on multiple medical datasets"""
    print("🧪 Starting Comprehensive Medical Dataset Testing")
    print("=" * 60)

    tester = MedicalDatasetTester()
    datasets = discover_medical_datasets()

    total_datasets = sum(len(category) for category in datasets.values())
    current_dataset = 0

    for category, dataset_list in datasets.items():
        print(f"\n📂 Testing {category.upper()} datasets:")

        for dataset_info in dataset_list:
            current_dataset += 1
            print(f"\n[{current_dataset}/{total_datasets}] Testing: {dataset_info['name']}")
            print(f"Description: {dataset_info['description']}")

            try:
                results = tester.test_dataset(
                    dataset_name=dataset_info['name'],
                    analysis_type=dataset_info['analysis_type'],
                    subset=dataset_info['subset'],
                    max_samples=max_samples_per_dataset
                )

                if results:
                    success_rate = sum(1 for r in results if r.success) / len(results)
                    print(f"✅ Completed: {len(results)} samples, {success_rate:.1%} success rate")
                else:
                    print("❌ Failed to test dataset")

            except Exception as e:
                print(f"❌ Error testing dataset: {e}")

    # Generate final report
    print("\n📊 Generating comprehensive report...")
    report_path = tester.save_results("comprehensive_test_results.json")
    viz_paths = tester.create_visualizations()

    # Print summary
    report = tester.generate_performance_report()
    summary = report["summary"]

    print("\n" + "=" * 60)
    print("🎯 COMPREHENSIVE TEST SUMMARY")
    print("=" * 60)
    print(f"Total Tests: {summary['total_tests']}")
    print(f"Successful Tests: {summary['successful_tests']}")
    print(f"Overall Success Rate: {summary['success_rate']:.1%}")
    print(f"Average Processing Time: {summary['average_processing_time']:.2f}s")
    print(f"\nResults saved to: {tester.output_dir}")
    print("=" * 60)

    return tester.output_dir

# CLI Interface
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Medical Dataset Testing for FertiVision AI")
    parser.add_argument("--mode", choices=["single", "dataset", "comprehensive"],
                       default="comprehensive", help="Testing mode")
    parser.add_argument("--image", type=str, help="Path to single image for testing")
    parser.add_argument("--analysis-type", choices=list(MedicalDatasetTester({}).prompts.keys()),
                       default="general_medical", help="Type of analysis")
    parser.add_argument("--dataset", type=str, help="Hugging Face dataset name")
    parser.add_argument("--max-samples", type=int, default=10,
                       help="Maximum samples to test per dataset")
    parser.add_argument("--output-dir", type=str, help="Output directory for results")

    args = parser.parse_args()

    if args.mode == "single":
        if not args.image:
            print("Error: --image required for single mode")
            exit(1)

        tester = MedicalDatasetTester()
        result = tester.test_single_image(args.image, args.analysis_type)

        print(f"\n🔬 Single Image Test Results:")
        print(f"Image: {args.image}")
        print(f"Analysis Type: {args.analysis_type}")
        print(f"Success: {result.success}")
        print(f"Processing Time: {result.processing_time:.2f}s")
        print(f"Extracted Metrics: {result.extracted_metrics}")
        print(f"\nLLaVA Response:")
        print("-" * 50)
        print(result.llava_response)

    elif args.mode == "dataset":
        if not args.dataset:
            print("Error: --dataset required for dataset mode")
            exit(1)

        tester = MedicalDatasetTester()
        results = tester.test_dataset(args.dataset, args.analysis_type, max_samples=args.max_samples)

        if results:
            success_rate = sum(1 for r in results if r.success) / len(results)
            print(f"\n📊 Dataset Test Results:")
            print(f"Dataset: {args.dataset}")
            print(f"Samples Tested: {len(results)}")
            print(f"Success Rate: {success_rate:.1%}")

            report_path = tester.save_results()
            viz_paths = tester.create_visualizations()
            print(f"Results saved to: {tester.output_dir}")

    elif args.mode == "comprehensive":
        output_dir = run_comprehensive_test(args.max_samples)
        print(f"\n🎉 Comprehensive testing completed!")
        print(f"All results available in: {output_dir}")

# Example usage functions
def example_test_local_images():
    """Example: Test local images in uploads folder"""
    print("🧪 Example: Testing local images")

    tester = MedicalDatasetTester()

    # Test images in uploads folder
    uploads_dir = "uploads"
    if os.path.exists(uploads_dir):
        for filename in os.listdir(uploads_dir):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                image_path = os.path.join(uploads_dir, filename)
                print(f"\nTesting: {filename}")

                # Determine analysis type based on filename
                filename_lower = filename.lower()
                if any(word in filename_lower for word in ['follicle', 'ovarian', 'ultrasound']):
                    analysis_type = "ultrasound_follicle"
                elif any(word in filename_lower for word in ['sperm', 'semen']):
                    analysis_type = "sperm_analysis"
                elif any(word in filename_lower for word in ['embryo', 'blastocyst']):
                    analysis_type = "embryo_analysis"
                elif any(word in filename_lower for word in ['oocyte', 'egg']):
                    analysis_type = "oocyte_analysis"
                else:
                    analysis_type = "general_medical"

                result = tester.test_single_image(image_path, analysis_type)
                print(f"Success: {result.success}, Time: {result.processing_time:.2f}s")
                if result.extracted_metrics:
                    print(f"Metrics: {result.extracted_metrics}")

    # Save results
    if tester.results:
        report_path = tester.save_results("local_images_test.json")
        viz_paths = tester.create_visualizations()
        print(f"\nResults saved to: {tester.output_dir}")

def example_fine_tuning_data_prep():
    """Example: Prepare data for fine-tuning"""
    print("🎯 Example: Preparing data for fine-tuning")

    tester = MedicalDatasetTester()

    # Test a small dataset to understand LLaVA's current performance
    dataset_name = "keremberke/ultrasound-image-classification"
    results = tester.test_dataset(dataset_name, "ultrasound_follicle", max_samples=5)

    if results:
        # Analyze where LLaVA struggles
        failed_results = [r for r in results if not r.success]
        successful_results = [r for r in results if r.success]

        print(f"\nFine-tuning Analysis:")
        print(f"Total samples: {len(results)}")
        print(f"Successful: {len(successful_results)}")
        print(f"Failed: {len(failed_results)}")

        # Create fine-tuning dataset format
        fine_tuning_data = []
        for result in results:
            fine_tuning_sample = {
                "image_path": result.image_path,
                "prompt": tester.prompts["ultrasound_follicle"],
                "expected_response": result.ground_truth or "Professional medical analysis",
                "actual_response": result.llava_response,
                "needs_improvement": not result.success
            }
            fine_tuning_data.append(fine_tuning_sample)

        # Save fine-tuning preparation data
        ft_path = os.path.join(tester.output_dir, "fine_tuning_data.json")
        with open(ft_path, 'w') as f:
            json.dump(fine_tuning_data, f, indent=2)

        print(f"Fine-tuning data prepared: {ft_path}")
        print("This data can be used to improve LLaVA's medical image analysis capabilities")

# Quick test function
def quick_test():
    """Quick test with existing images"""
    print("⚡ Quick Test of Dataset Testing Module")
    example_test_local_images()
