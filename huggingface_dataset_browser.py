#!/usr/bin/env python3
"""
FertiVision powered by greybrain.ai - Hugging Face Dataset Browser

This module provides functionality to:
1. Browse and discover medical datasets on Hugging Face
2. Download and test datasets with LLaVA
3. Generate comprehensive performance reports
4. Prepare data for fine-tuning

© 2025 FertiVision powered by greybrain.ai - Advanced AI for Reproductive Medicine
"""

import os
import json
import requests
from datetime import datetime
from typing import Dict, List, Optional
from datasets import load_dataset, get_dataset_config_names
from huggingface_hub import list_datasets, DatasetInfo
from dataset_testing import MedicalDatasetTester

class HuggingFaceDatasetBrowser:
    """Browse and test medical datasets from Hugging Face"""
    
    def __init__(self):
        self.tester = MedicalDatasetTester()
        self.medical_keywords = [
            'medical', 'ultrasound', 'xray', 'x-ray', 'ct', 'mri', 'scan',
            'microscopy', 'pathology', 'radiology', 'chest', 'lung', 'heart',
            'brain', 'cancer', 'tumor', 'cell', 'blood', 'tissue', 'organ',
            'diagnosis', 'clinical', 'hospital', 'patient', 'disease',
            'sperm', 'embryo', 'oocyte', 'follicle', 'ovarian', 'reproductive',
            'fertility', 'ivf', 'gynecology', 'obstetrics', 'endometrial'
        ]
        
        # Curated medical datasets for FertiVision
        self.featured_datasets = {
            "Ultrasound & Radiology": [
                {
                    "name": "keremberke/ultrasound-image-classification",
                    "description": "Ultrasound image classification dataset",
                    "analysis_type": "ultrasound_follicle",
                    "tags": ["ultrasound", "medical", "classification"]
                },
                {
                    "name": "alkzar90/NIH-Chest-X-ray-dataset",
                    "description": "NIH Chest X-ray dataset with pathology labels",
                    "analysis_type": "general_medical",
                    "tags": ["xray", "chest", "pathology"]
                },
                {
                    "name": "keremberke/chest-xray-classification",
                    "description": "Chest X-ray classification dataset",
                    "analysis_type": "general_medical",
                    "tags": ["xray", "classification", "pneumonia"]
                }
            ],
            "Microscopy & Cell Biology": [
                {
                    "name": "keremberke/blood-cell-object-detection",
                    "description": "Blood cell microscopy images for object detection",
                    "analysis_type": "general_medical",
                    "tags": ["microscopy", "blood", "cells"]
                },
                {
                    "name": "Francesco/skin-cancer",
                    "description": "Skin cancer classification dataset",
                    "analysis_type": "general_medical",
                    "tags": ["dermatology", "cancer", "classification"]
                }
            ],
            "Reproductive Medicine": [
                {
                    "name": "custom/embryo-grading",
                    "description": "Embryo grading dataset (placeholder)",
                    "analysis_type": "embryo_analysis",
                    "tags": ["embryo", "ivf", "grading"]
                },
                {
                    "name": "custom/sperm-analysis",
                    "description": "Sperm analysis dataset (placeholder)",
                    "analysis_type": "sperm_analysis",
                    "tags": ["sperm", "fertility", "morphology"]
                }
            ]
        }
    
    def search_medical_datasets(self, query: str = "", limit: int = 20) -> List[Dict]:
        """Search for medical datasets on Hugging Face"""
        print(f"🔍 Searching Hugging Face for medical datasets...")
        
        try:
            # Search datasets with medical keywords
            search_terms = query.split() if query else self.medical_keywords[:5]
            
            datasets = []
            for term in search_terms:
                try:
                    results = list_datasets(search=term, limit=limit//len(search_terms))
                    for dataset in results:
                        if any(keyword in dataset.id.lower() or 
                              (dataset.description and keyword in dataset.description.lower())
                              for keyword in self.medical_keywords):
                            
                            dataset_info = {
                                "name": dataset.id,
                                "description": dataset.description or "No description available",
                                "tags": getattr(dataset, 'tags', []),
                                "downloads": getattr(dataset, 'downloads', 0),
                                "likes": getattr(dataset, 'likes', 0)
                            }
                            
                            # Determine analysis type based on tags and description
                            desc_lower = dataset_info["description"].lower()
                            if any(word in desc_lower for word in ['ultrasound', 'follicle', 'ovarian']):
                                dataset_info["analysis_type"] = "ultrasound_follicle"
                            elif any(word in desc_lower for word in ['sperm', 'semen']):
                                dataset_info["analysis_type"] = "sperm_analysis"
                            elif any(word in desc_lower for word in ['embryo', 'blastocyst']):
                                dataset_info["analysis_type"] = "embryo_analysis"
                            elif any(word in desc_lower for word in ['oocyte', 'egg']):
                                dataset_info["analysis_type"] = "oocyte_analysis"
                            else:
                                dataset_info["analysis_type"] = "general_medical"
                            
                            datasets.append(dataset_info)
                            
                except Exception as e:
                    print(f"Error searching for '{term}': {e}")
                    continue
            
            # Remove duplicates
            unique_datasets = []
            seen_names = set()
            for dataset in datasets:
                if dataset["name"] not in seen_names:
                    unique_datasets.append(dataset)
                    seen_names.add(dataset["name"])
            
            print(f"Found {len(unique_datasets)} unique medical datasets")
            return unique_datasets[:limit]
            
        except Exception as e:
            print(f"Error searching datasets: {e}")
            return []
    
    def get_featured_datasets(self) -> Dict:
        """Get curated medical datasets for FertiVision"""
        return self.featured_datasets
    
    def preview_dataset(self, dataset_name: str, max_samples: int = 3) -> Dict:
        """Preview a dataset without full testing"""
        print(f"👀 Previewing dataset: {dataset_name}")
        
        try:
            # Try to load dataset info
            configs = get_dataset_config_names(dataset_name)
            print(f"Available configurations: {configs}")
            
            # Load a small sample
            dataset = load_dataset(dataset_name, split="train[:3]")
            
            preview_info = {
                "name": dataset_name,
                "num_samples_preview": len(dataset),
                "features": list(dataset.features.keys()),
                "sample_data": []
            }
            
            # Extract sample information
            for i, sample in enumerate(dataset):
                sample_info = {
                    "index": i,
                    "has_image": "image" in sample or "img" in sample,
                    "has_label": "label" in sample,
                    "has_text": "text" in sample or "caption" in sample,
                    "keys": list(sample.keys())
                }
                
                # Get image info if available
                if "image" in sample and sample["image"]:
                    img = sample["image"]
                    if hasattr(img, 'size'):
                        sample_info["image_size"] = img.size
                    if hasattr(img, 'mode'):
                        sample_info["image_mode"] = img.mode
                
                preview_info["sample_data"].append(sample_info)
            
            return preview_info
            
        except Exception as e:
            return {
                "name": dataset_name,
                "error": str(e),
                "preview_failed": True
            }
    
    def test_dataset_with_llava(self, dataset_name: str, analysis_type: str, 
                               max_samples: int = 10) -> Dict:
        """Test a dataset with LLaVA and generate comprehensive report"""
        print(f"🧪 Testing dataset '{dataset_name}' with LLaVA...")
        print(f"Analysis type: {analysis_type}")
        print(f"Max samples: {max_samples}")
        
        try:
            # Test the dataset
            results = self.tester.test_dataset(
                dataset_name=dataset_name,
                analysis_type=analysis_type,
                max_samples=max_samples
            )
            
            if not results:
                return {
                    "dataset_name": dataset_name,
                    "success": False,
                    "error": "No results generated"
                }
            
            # Generate comprehensive report
            report = self.tester.generate_performance_report()
            
            # Add dataset-specific analysis
            successful_results = [r for r in results if r.success]
            failed_results = [r for r in results if not r.success]
            
            # Extract medical metrics
            extracted_metrics = []
            for result in successful_results:
                if result.extracted_metrics:
                    extracted_metrics.append(result.extracted_metrics)
            
            dataset_report = {
                "dataset_info": {
                    "name": dataset_name,
                    "analysis_type": analysis_type,
                    "test_timestamp": datetime.now().isoformat()
                },
                "performance_summary": report["summary"],
                "detailed_analysis": {
                    "total_samples": len(results),
                    "successful_samples": len(successful_results),
                    "failed_samples": len(failed_results),
                    "success_rate": len(successful_results) / len(results) if results else 0,
                    "extracted_metrics_count": len(extracted_metrics)
                },
                "medical_insights": {
                    "metrics_extracted": extracted_metrics,
                    "common_failures": [r.llava_response[:100] for r in failed_results[:3]],
                    "successful_responses": [r.llava_response[:100] for r in successful_results[:3]]
                },
                "recommendations": self._generate_recommendations(results, analysis_type)
            }
            
            # Save detailed report
            report_filename = f"dataset_test_{dataset_name.replace('/', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            report_path = os.path.join(self.tester.output_dir, report_filename)
            
            with open(report_path, 'w') as f:
                json.dump(dataset_report, f, indent=2)
            
            print(f"📊 Dataset test completed!")
            print(f"Success rate: {dataset_report['detailed_analysis']['success_rate']:.1%}")
            print(f"Report saved: {report_path}")
            
            return dataset_report
            
        except Exception as e:
            return {
                "dataset_name": dataset_name,
                "success": False,
                "error": str(e)
            }
    
    def _generate_recommendations(self, results: List, analysis_type: str) -> List[str]:
        """Generate recommendations based on test results"""
        recommendations = []
        
        if not results:
            return ["No results to analyze"]
        
        success_rate = sum(1 for r in results if r.success) / len(results)
        avg_time = sum(r.processing_time for r in results if r.processing_time > 0) / len(results)
        
        if success_rate < 0.5:
            recommendations.append("Low success rate - consider prompt optimization or different analysis type")
        elif success_rate > 0.8:
            recommendations.append("High success rate - excellent dataset for training/evaluation")
        
        if avg_time > 30:
            recommendations.append("High processing time - consider image preprocessing or model optimization")
        
        # Analysis-specific recommendations
        if analysis_type == "ultrasound_follicle":
            metrics_with_counts = [r for r in results if r.success and r.extracted_metrics.get('follicle_count')]
            if len(metrics_with_counts) > len(results) * 0.7:
                recommendations.append("Good follicle count extraction - suitable for reproductive medicine training")
        
        if not recommendations:
            recommendations.append("Dataset shows good compatibility with LLaVA analysis")
        
        return recommendations

def main():
    """Main CLI interface for Hugging Face dataset browser"""
    print("🤗 FertiVision powered by greybrain.ai - Hugging Face Dataset Browser")
    print("=" * 80)
    print("Discover and test medical datasets for AI-powered reproductive medicine")
    print("© 2025 FertiVision powered by greybrain.ai")
    print("=" * 80)

    browser = HuggingFaceDatasetBrowser()

    while True:
        print("\n📋 Available Options:")
        print("1. 🔍 Search medical datasets")
        print("2. 📚 Browse featured datasets")
        print("3. 👀 Preview a specific dataset")
        print("4. 🧪 Test dataset with LLaVA")
        print("5. 📊 Run comprehensive dataset evaluation")
        print("6. ❌ Exit")

        try:
            choice = input("\nSelect an option (1-6): ").strip()

            if choice == "1":
                # Search datasets
                query = input("Enter search terms (or press Enter for general medical search): ").strip()
                limit = int(input("Number of results to show (default 10): ") or "10")

                datasets = browser.search_medical_datasets(query, limit)

                if datasets:
                    print(f"\n🔍 Found {len(datasets)} medical datasets:")
                    for i, dataset in enumerate(datasets, 1):
                        print(f"\n{i}. {dataset['name']}")
                        print(f"   Description: {dataset['description'][:100]}...")
                        print(f"   Analysis Type: {dataset['analysis_type']}")
                        print(f"   Downloads: {dataset.get('downloads', 'N/A')}")
                        print(f"   Tags: {', '.join(dataset.get('tags', [])[:5])}")
                else:
                    print("❌ No medical datasets found")

            elif choice == "2":
                # Browse featured datasets
                featured = browser.get_featured_datasets()

                print("\n📚 Featured Medical Datasets for FertiVision:")
                for category, datasets in featured.items():
                    print(f"\n📂 {category}:")
                    for dataset in datasets:
                        print(f"  • {dataset['name']}")
                        print(f"    {dataset['description']}")
                        print(f"    Analysis: {dataset['analysis_type']}")
                        print(f"    Tags: {', '.join(dataset['tags'])}")

            elif choice == "3":
                # Preview dataset
                dataset_name = input("Enter dataset name (e.g., keremberke/ultrasound-image-classification): ").strip()

                if dataset_name:
                    preview = browser.preview_dataset(dataset_name)

                    print(f"\n👀 Dataset Preview: {dataset_name}")
                    if "error" in preview:
                        print(f"❌ Error: {preview['error']}")
                    else:
                        print(f"Features: {', '.join(preview['features'])}")
                        print(f"Sample count (preview): {preview['num_samples_preview']}")

                        for sample in preview['sample_data']:
                            print(f"\nSample {sample['index']}:")
                            print(f"  Has image: {sample['has_image']}")
                            print(f"  Has label: {sample['has_label']}")
                            print(f"  Keys: {', '.join(sample['keys'])}")
                            if 'image_size' in sample:
                                print(f"  Image size: {sample['image_size']}")

            elif choice == "4":
                # Test dataset with LLaVA
                dataset_name = input("Enter dataset name: ").strip()

                if dataset_name:
                    print("\nAnalysis types:")
                    analysis_types = ["ultrasound_follicle", "sperm_analysis", "embryo_analysis",
                                    "oocyte_analysis", "general_medical"]
                    for i, atype in enumerate(analysis_types, 1):
                        print(f"{i}. {atype}")

                    type_choice = input("Select analysis type (1-5): ").strip()
                    try:
                        analysis_type = analysis_types[int(type_choice) - 1]
                    except (ValueError, IndexError):
                        analysis_type = "general_medical"

                    max_samples = int(input("Max samples to test (default 5): ") or "5")

                    print(f"\n🧪 Testing {dataset_name} with {analysis_type} analysis...")
                    result = browser.test_dataset_with_llava(dataset_name, analysis_type, max_samples)

                    if result.get("success", True):
                        print(f"\n✅ Test completed successfully!")
                        if "detailed_analysis" in result:
                            analysis = result["detailed_analysis"]
                            print(f"Success rate: {analysis['success_rate']:.1%}")
                            print(f"Samples tested: {analysis['total_samples']}")
                            print(f"Metrics extracted: {analysis['extracted_metrics_count']}")

                        if "recommendations" in result:
                            print(f"\n💡 Recommendations:")
                            for rec in result["recommendations"]:
                                print(f"  • {rec}")
                    else:
                        print(f"❌ Test failed: {result.get('error', 'Unknown error')}")

            elif choice == "5":
                # Comprehensive evaluation
                print("\n📊 Running comprehensive dataset evaluation...")

                # Test featured datasets
                featured = browser.get_featured_datasets()
                all_results = []

                for category, datasets in featured.items():
                    print(f"\n📂 Testing {category} datasets:")

                    for dataset in datasets:
                        if not dataset['name'].startswith('custom/'):  # Skip placeholder datasets
                            print(f"Testing {dataset['name']}...")
                            result = browser.test_dataset_with_llava(
                                dataset['name'],
                                dataset['analysis_type'],
                                max_samples=3
                            )
                            all_results.append(result)

                # Generate summary
                print(f"\n📈 Comprehensive Evaluation Summary:")
                successful_tests = [r for r in all_results if r.get("success", True)]
                print(f"Datasets tested: {len(all_results)}")
                print(f"Successful tests: {len(successful_tests)}")

                if successful_tests:
                    avg_success_rate = sum(r.get("detailed_analysis", {}).get("success_rate", 0)
                                         for r in successful_tests) / len(successful_tests)
                    print(f"Average success rate: {avg_success_rate:.1%}")

            elif choice == "6":
                print("\n👋 Thank you for using FertiVision Dataset Browser!")
                print("© 2025 FertiVision powered by greybrain.ai")
                break

            else:
                print("❌ Invalid option. Please select 1-6.")

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Please try again.")

if __name__ == "__main__":
    main()
