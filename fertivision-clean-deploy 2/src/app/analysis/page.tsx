'use client';

import { useState, useCallback } from 'react';
import { useAuth, useUser } from '@clerk/nextjs';
import { useRouter } from 'next/navigation';
import { useDropzone } from 'react-dropzone';
import toast from 'react-hot-toast';
import Link from 'next/link';
import { 
  CloudArrowUpIcon, 
  BeakerIcon, 
  DocumentTextIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
  ClockIcon
} from '@heroicons/react/24/outline';

interface AnalysisResult {
  success: boolean;
  analysis_id: string;
  classification: string;
  confidence: number;
  parameters: Record<string, any>;
  technical_details: Record<string, string>;
  clinical_recommendations: string[];
  processing_time: number;
  error?: string;
}

export default function Analysis() {
  const { isSignedIn } = useAuth();
  const { user } = useUser();
  const router = useRouter();
  
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [analysisType, setAnalysisType] = useState<'sperm' | 'oocyte' | 'embryo' | 'follicle' | 'hysteroscopy'>('sperm');
  const [patientId, setPatientId] = useState('');
  const [caseId, setCaseId] = useState('');
  const [additionalNotes, setAdditionalNotes] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [results, setResults] = useState<AnalysisResult[]>([]);
  const [showResults, setShowResults] = useState(false);

  // Redirect if not signed in
  if (!isSignedIn) {
    router.push('/');
    return null;
  }

  const onDrop = useCallback((acceptedFiles: File[]) => {
    // Validate file types
    const validFiles = acceptedFiles.filter(file => {
      if (!file.type.startsWith('image/')) {
        toast.error(`${file.name} is not a valid image file`);
        return false;
      }
      if (file.size > 50 * 1024 * 1024) { // 50MB limit
        toast.error(`${file.name} is too large (max 50MB)`);
        return false;
      }
      return true;
    });

    setSelectedFiles(prev => [...prev, ...validFiles]);
    
    if (validFiles.length > 0) {
      toast.success(`${validFiles.length} file(s) added for analysis`);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.tiff', '.bmp']
    },
    multiple: true
  });

  const removeFile = (index: number) => {
    setSelectedFiles(prev => prev.filter((_, i) => i !== index));
    toast.success('File removed');
  };

  const performAnalysis = async () => {
    if (selectedFiles.length === 0) {
      toast.error('Please select at least one image file');
      return;
    }

    setIsAnalyzing(true);
    setResults([]);

    try {
      const analysisResults: AnalysisResult[] = [];

      for (let i = 0; i < selectedFiles.length; i++) {
        const file = selectedFiles[i];

        toast.loading(`Analyzing ${file.name}... (${i + 1}/${selectedFiles.length})`, {
          id: `analysis-${i}`
        });

        // Simulate analysis with mock data for static deployment
        await new Promise(resolve => setTimeout(resolve, 2000 + Math.random() * 3000));

        const mockResult = {
          success: true,
          analysis_id: `DEMO_${Date.now()}_${i}`,
          classification: `${analysisType.charAt(0).toUpperCase() + analysisType.slice(1)} analysis completed`,
          confidence: Math.floor(85 + Math.random() * 15),
          parameters: {
            'sample_quality': 'Good',
            'image_resolution': '1920x1080',
            'analysis_method': 'AI Deep Learning'
          },
          technical_details: {
            'Model': 'FertiVision AI v2.1',
            'Processing_Time': `${(2 + Math.random() * 3).toFixed(1)}s`,
            'Confidence_Score': `${Math.floor(85 + Math.random() * 15)}%`
          },
          clinical_recommendations: [
            'Analysis completed successfully',
            'Results are for demonstration purposes',
            'Contact support for production analysis'
          ],
          processing_time: parseFloat((2 + Math.random() * 3).toFixed(1))
        };

        analysisResults.push(mockResult);
        toast.success(`${file.name} analyzed successfully`, {
          id: `analysis-${i}`
        });
      }

      setResults(analysisResults);
      setShowResults(true);

      toast.success(`Demo analysis complete! ${analysisResults.length}/${selectedFiles.length} files processed`);

    } catch (error) {
      toast.error('Failed to perform analysis');
      console.error('Analysis error:', error);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const analysisTypes = [
    { id: 'sperm', name: 'Sperm Analysis', icon: '🧬', description: 'WHO 2021 compliant semen analysis' },
    { id: 'oocyte', name: 'Oocyte Assessment', icon: '🥚', description: 'ESHRE guidelines-based evaluation' },
    { id: 'embryo', name: 'Embryo Grading', icon: '👶', description: 'Gardner grading system' },
    { id: 'follicle', name: 'Follicle Counting', icon: '🔬', description: 'AFC and ovarian reserve assessment' },
    { id: 'hysteroscopy', name: 'Hysteroscopy Analysis', icon: '🏥', description: 'Endometrial morphology evaluation' }
  ];

  if (showResults) {
    return (
      <div className="min-h-screen bg-gray-50">
        {/* Navigation */}
        <nav className="bg-white shadow-sm border-b">
          <div className="max-w-7xl mx-auto px-6 py-4">
            <div className="flex justify-between items-center">
              <div className="flex items-center space-x-4">
                <Link href="/" className="flex items-center space-x-2">
                  <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center">
                    <span className="text-white font-bold text-lg">F</span>
                  </div>
                  <span className="text-2xl font-bold text-indigo-900">FertiVision</span>
                </Link>
                <span className="text-gray-400">|</span>
                <h1 className="text-xl font-semibold text-gray-900">Analysis Results</h1>
              </div>
              <div className="flex items-center space-x-4">
                <button
                  onClick={() => {
                    setShowResults(false);
                    setResults([]);
                    setSelectedFiles([]);
                  }}
                  className="text-indigo-600 hover:text-indigo-800 font-medium"
                >
                  New Analysis
                </button>
                <Link href="/dashboard" className="text-indigo-600 hover:text-indigo-800 font-medium">
                  Dashboard
                </Link>
              </div>
            </div>
          </div>
        </nav>

        <div className="max-w-7xl mx-auto px-6 py-8">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Analysis Results</h1>
            <p className="text-gray-600">
              {results.filter(r => r.success).length} of {results.length} analyses completed successfully
            </p>
          </div>

          <div className="space-y-6">
            {results.map((result, index) => (
              <div key={index} className={`bg-white rounded-lg shadow-lg p-6 ${
                result.success ? 'border-l-4 border-green-500' : 'border-l-4 border-red-500'
              }`}>
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center space-x-3">
                    {result.success ? (
                      <CheckCircleIcon className="w-6 h-6 text-green-500" />
                    ) : (
                      <ExclamationTriangleIcon className="w-6 h-6 text-red-500" />
                    )}
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900">
                        {selectedFiles[index]?.name || `Analysis ${index + 1}`}
                      </h3>
                      <p className="text-sm text-gray-500 capitalize">
                        {analysisType} Analysis
                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className={`text-lg font-semibold ${
                      result.success ? 'text-green-600' : 'text-red-600'
                    }`}>
                      {result.success ? `${result.confidence}%` : 'Failed'}
                    </div>
                    <div className="text-sm text-gray-500">
                      {result.processing_time}s processing time
                    </div>
                  </div>
                </div>

                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-3">Classification</h4>
                    <p className="text-gray-700 mb-4">{result.classification}</p>
                    
                    {Object.keys(result.parameters).length > 0 && (
                      <>
                        <h4 className="font-semibold text-gray-900 mb-3">Parameters</h4>
                        <div className="space-y-2">
                          {Object.entries(result.parameters).map(([key, value]) => (
                            <div key={key} className="flex justify-between">
                              <span className="text-gray-600 capitalize">{key.replace('_', ' ')}:</span>
                              <span className="font-medium">{value}</span>
                            </div>
                          ))}
                        </div>
                      </>
                    )}
                  </div>

                  <div>
                    <h4 className="font-semibold text-gray-900 mb-3">Technical Details</h4>
                    <div className="space-y-2 mb-4">
                      {Object.entries(result.technical_details).map(([key, value]) => (
                        <div key={key} className="text-sm">
                          <span className="text-gray-600">{key}:</span>
                          <span className="ml-2 text-gray-800">{value}</span>
                        </div>
                      ))}
                    </div>

                    <h4 className="font-semibold text-gray-900 mb-3">Clinical Recommendations</h4>
                    <ul className="space-y-1">
                      {result.clinical_recommendations.map((rec, i) => (
                        <li key={i} className="text-sm text-gray-700 flex items-start">
                          <span className="text-indigo-500 mr-2">•</span>
                          {rec}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>

                <div className="mt-6 pt-4 border-t border-gray-200 flex justify-between items-center">
                  <div className="text-sm text-gray-500">
                    Analysis ID: {result.analysis_id}
                  </div>
                  <div className="flex space-x-3">
                    <button className="text-indigo-600 hover:text-indigo-800 text-sm font-medium">
                      Download PDF
                    </button>
                    <button className="text-indigo-600 hover:text-indigo-800 text-sm font-medium">
                      Share Results
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>

          <div className="mt-8 text-center">
            <button
              onClick={() => {
                setShowResults(false);
                setResults([]);
                setSelectedFiles([]);
              }}
              className="bg-indigo-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-indigo-700 transition-colors"
            >
              Perform New Analysis
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-4">
              <Link href="/" className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-lg">F</span>
                </div>
                <span className="text-2xl font-bold text-indigo-900">FertiVision</span>
              </Link>
              <span className="text-gray-400">|</span>
              <h1 className="text-xl font-semibold text-gray-900">AI Analysis</h1>
            </div>
            <div className="flex items-center space-x-4">
              <Link href="/dashboard" className="text-indigo-600 hover:text-indigo-800 font-medium">
                Dashboard
              </Link>
              <Link href="/pricing" className="text-indigo-600 hover:text-indigo-800 font-medium">
                Pricing
              </Link>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-4xl mx-auto px-6 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">AI-Powered Medical Analysis</h1>
          <p className="text-gray-600">
            Upload medical images for professional AI analysis following WHO 2021 and ESHRE guidelines.
          </p>
        </div>

        {/* Analysis Type Selection */}
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Select Analysis Type</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
            {analysisTypes.map((type) => (
              <button
                key={type.id}
                onClick={() => setAnalysisType(type.id as any)}
                className={`p-4 rounded-lg border-2 transition-all ${
                  analysisType === type.id
                    ? 'border-indigo-500 bg-indigo-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <div className="text-2xl mb-2">{type.icon}</div>
                <div className="font-medium text-gray-900">{type.name}</div>
                <div className="text-sm text-gray-600 mt-1">{type.description}</div>
              </button>
            ))}
          </div>
        </div>

        {/* File Upload */}
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Upload Medical Images</h2>
          
          <div
            {...getRootProps()}
            className={`border-2 border-dashed rounded-lg p-12 text-center transition-colors ${
              isDragActive
                ? 'border-indigo-500 bg-indigo-50'
                : 'border-gray-300 hover:border-gray-400'
            }`}
          >
            <input {...getInputProps()} />
            <CloudArrowUpIcon className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            {isDragActive ? (
              <p className="text-indigo-600 font-medium">Drop the images here...</p>
            ) : (
              <>
                <p className="text-gray-600 mb-2">
                  Drag and drop medical images here, or click to select files
                </p>
                <p className="text-sm text-gray-500">
                  Supports JPEG, PNG, TIFF, BMP (max 50MB per file)
                </p>
              </>
            )}
          </div>

          {/* Selected Files */}
          {selectedFiles.length > 0 && (
            <div className="mt-6">
              <h3 className="font-medium text-gray-900 mb-3">
                Selected Files ({selectedFiles.length})
              </h3>
              <div className="space-y-2">
                {selectedFiles.map((file, index) => (
                  <div key={index} className="flex items-center justify-between bg-gray-50 p-3 rounded-lg">
                    <div className="flex items-center space-x-3">
                      <DocumentTextIcon className="w-5 h-5 text-gray-400" />
                      <div>
                        <div className="font-medium text-gray-900">{file.name}</div>
                        <div className="text-sm text-gray-500">
                          {(file.size / 1024 / 1024).toFixed(2)} MB
                        </div>
                      </div>
                    </div>
                    <button
                      onClick={() => removeFile(index)}
                      className="text-red-600 hover:text-red-800 text-sm font-medium"
                    >
                      Remove
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Additional Information */}
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Additional Information</h2>
          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Patient ID (Optional)
              </label>
              <input
                type="text"
                value={patientId}
                onChange={(e) => setPatientId(e.target.value)}
                placeholder="Enter patient identifier"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Case ID (Optional)
              </label>
              <input
                type="text"
                value={caseId}
                onChange={(e) => setCaseId(e.target.value)}
                placeholder="Enter case identifier"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500"
              />
            </div>
          </div>
          <div className="mt-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Additional Notes (Optional)
            </label>
            <textarea
              value={additionalNotes}
              onChange={(e) => setAdditionalNotes(e.target.value)}
              placeholder="Enter any additional clinical notes or context"
              rows={3}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>
        </div>

        {/* Analysis Button */}
        <div className="text-center">
          <button
            onClick={performAnalysis}
            disabled={selectedFiles.length === 0 || isAnalyzing}
            className={`px-8 py-4 rounded-lg font-semibold text-lg transition-colors ${
              selectedFiles.length === 0 || isAnalyzing
                ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                : 'bg-indigo-600 text-white hover:bg-indigo-700'
            }`}
          >
            {isAnalyzing ? (
              <div className="flex items-center space-x-2">
                <ClockIcon className="w-5 h-5 animate-spin" />
                <span>Analyzing Images...</span>
              </div>
            ) : (
              `Analyze ${selectedFiles.length} Image${selectedFiles.length !== 1 ? 's' : ''}`
            )}
          </button>
          
          {selectedFiles.length === 0 && (
            <p className="text-sm text-gray-500 mt-2">
              Please select at least one image to begin analysis
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
