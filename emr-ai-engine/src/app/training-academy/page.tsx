'use client';

import { useState, useEffect } from 'react';
import { useUser } from '@clerk/nextjs';
import Link from 'next/link';
import { 
  AcademicCapIcon,
  BookOpenIcon,
  PlayIcon,
  CheckCircleIcon,
  ClockIcon,
  UserGroupIcon,
  ChartBarIcon,
  BeakerIcon,
  DocumentTextIcon,
  CpuChipIcon,
  CloudIcon,
  ArrowRightIcon,
  StarIcon
} from '@heroicons/react/24/outline';

interface TrainingModule {
  id: string;
  title: string;
  description: string;
  duration: string;
  difficulty: 'Beginner' | 'Intermediate' | 'Advanced';
  category: string;
  completed: boolean;
  progress: number;
  icon: any;
  huggingFaceDatasets?: string[];
  practicalExercises: number;
}

interface HuggingFaceDataset {
  id: string;
  name: string;
  description: string;
  downloads: number;
  size: string;
  task: string;
  language: string;
  license: string;
  tags: string[];
}

export default function TrainingAcademyPage() {
  const { isSignedIn, user } = useUser();
  const [activeTab, setActiveTab] = useState('modules');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [huggingFaceDatasets, setHuggingFaceDatasets] = useState<HuggingFaceDataset[]>([]);

  const trainingModules: TrainingModule[] = [
    {
      id: 'emr-basics',
      title: 'EMR AI Fundamentals',
      description: 'Learn the basics of Electronic Medical Records and AI integration',
      duration: '2 hours',
      difficulty: 'Beginner',
      category: 'Fundamentals',
      completed: false,
      progress: 0,
      icon: BookOpenIcon,
      huggingFaceDatasets: ['medical-qa', 'clinical-notes'],
      practicalExercises: 5
    },
    {
      id: 'history-taking',
      title: 'AI-Powered History Taking',
      description: 'Master automated patient history collection and structuring',
      duration: '3 hours',
      difficulty: 'Intermediate',
      category: 'Clinical AI',
      completed: false,
      progress: 0,
      icon: DocumentTextIcon,
      huggingFaceDatasets: ['patient-histories', 'medical-dialogues'],
      practicalExercises: 8
    },
    {
      id: 'discharge-summaries',
      title: 'Discharge Summary Generation',
      description: 'Create comprehensive discharge summaries using AI',
      duration: '2.5 hours',
      difficulty: 'Intermediate',
      category: 'Clinical AI',
      completed: false,
      progress: 0,
      icon: ClockIcon,
      huggingFaceDatasets: ['discharge-summaries', 'hospital-course'],
      practicalExercises: 6
    },
    {
      id: 'medical-imaging',
      title: 'Medical Image Analysis with AI',
      description: 'Analyze medical images using computer vision and AI',
      duration: '4 hours',
      difficulty: 'Advanced',
      category: 'Computer Vision',
      completed: false,
      progress: 0,
      icon: BeakerIcon,
      huggingFaceDatasets: ['medical-images', 'radiology-reports'],
      practicalExercises: 10
    },
    {
      id: 'clinical-decision',
      title: 'Clinical Decision Support Systems',
      description: 'Build AI systems for clinical decision making',
      duration: '3.5 hours',
      difficulty: 'Advanced',
      category: 'Clinical AI',
      completed: false,
      progress: 0,
      icon: ChartBarIcon,
      huggingFaceDatasets: ['clinical-trials', 'medical-guidelines'],
      practicalExercises: 12
    },
    {
      id: 'local-deployment',
      title: 'Local AI Model Deployment',
      description: 'Deploy and optimize AI models for local EMR systems',
      duration: '3 hours',
      difficulty: 'Advanced',
      category: 'Deployment',
      completed: false,
      progress: 0,
      icon: CpuChipIcon,
      huggingFaceDatasets: ['model-optimization', 'quantization'],
      practicalExercises: 7
    },
    {
      id: 'cloud-scaling',
      title: 'Cloud AI Scaling Strategies',
      description: 'Scale AI workloads in cloud environments',
      duration: '2.5 hours',
      difficulty: 'Intermediate',
      category: 'Deployment',
      completed: false,
      progress: 0,
      icon: CloudIcon,
      huggingFaceDatasets: ['cloud-metrics', 'performance-data'],
      practicalExercises: 5
    },
    {
      id: 'huggingface-integration',
      title: 'Hugging Face Model Integration',
      description: 'Integrate and fine-tune Hugging Face models for medical tasks',
      duration: '4 hours',
      difficulty: 'Advanced',
      category: 'Model Training',
      completed: false,
      progress: 0,
      icon: StarIcon,
      huggingFaceDatasets: ['medical-bert', 'clinical-transformers'],
      practicalExercises: 15
    }
  ];

  const categories = ['all', 'Fundamentals', 'Clinical AI', 'Computer Vision', 'Deployment', 'Model Training'];

  useEffect(() => {
    loadHuggingFaceDatasets();
    setIsLoading(false);
  }, []);

  const loadHuggingFaceDatasets = async () => {
    // Simulate loading Hugging Face datasets
    const mockDatasets: HuggingFaceDataset[] = [
      {
        id: 'medical-qa',
        name: 'Medical Question Answering Dataset',
        description: 'Comprehensive medical Q&A pairs for training conversational AI',
        downloads: 15420,
        size: '2.3 GB',
        task: 'Question Answering',
        language: 'English',
        license: 'MIT',
        tags: ['medical', 'qa', 'healthcare', 'clinical']
      },
      {
        id: 'clinical-notes',
        name: 'Clinical Notes Corpus',
        description: 'Anonymized clinical notes for NLP training',
        downloads: 8930,
        size: '1.8 GB',
        task: 'Text Classification',
        language: 'English',
        license: 'Apache 2.0',
        tags: ['clinical', 'notes', 'nlp', 'medical']
      },
      {
        id: 'medical-images',
        name: 'Medical Image Dataset',
        description: 'Curated medical images with annotations',
        downloads: 12650,
        size: '15.2 GB',
        task: 'Image Classification',
        language: 'N/A',
        license: 'CC BY 4.0',
        tags: ['medical', 'images', 'radiology', 'computer-vision']
      },
      {
        id: 'discharge-summaries',
        name: 'Discharge Summary Templates',
        description: 'Structured discharge summary examples',
        downloads: 5420,
        size: '450 MB',
        task: 'Text Generation',
        language: 'English',
        license: 'MIT',
        tags: ['discharge', 'summaries', 'templates', 'medical']
      }
    ];

    setHuggingFaceDatasets(mockDatasets);
  };

  const filteredModules = trainingModules.filter(module => {
    const matchesCategory = selectedCategory === 'all' || module.category === selectedCategory;
    const matchesSearch = module.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         module.description.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'Beginner': return 'bg-green-100 text-green-800';
      case 'Intermediate': return 'bg-yellow-100 text-yellow-800';
      case 'Advanced': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading Training Academy...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm">
        <div className="container mx-auto px-4 py-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 flex items-center">
                <AcademicCapIcon className="h-8 w-8 text-blue-600 mr-3" />
                EMR AI Training Academy
              </h1>
              <p className="mt-2 text-lg text-gray-600">
                Master AI-powered medical record management with hands-on training
              </p>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-right">
                <p className="text-sm text-gray-500">Your Progress</p>
                <p className="text-2xl font-bold text-blue-600">
                  {Math.round((trainingModules.filter(m => m.completed).length / trainingModules.length) * 100)}%
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="bg-white border-b">
        <div className="container mx-auto px-4">
          <nav className="flex space-x-8">
            <button
              onClick={() => setActiveTab('modules')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'modules'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              Training Modules
            </button>
            <button
              onClick={() => setActiveTab('datasets')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'datasets'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              Hugging Face Datasets
            </button>
            <button
              onClick={() => setActiveTab('progress')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'progress'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              Progress Tracking
            </button>
          </nav>
        </div>
      </div>

      {/* Content */}
      <div className="container mx-auto px-4 py-8">
        {activeTab === 'modules' && (
          <div>
            {/* Filters */}
            <div className="mb-8 flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-4 sm:space-y-0">
              <div className="flex flex-wrap gap-2">
                {categories.map(category => (
                  <button
                    key={category}
                    onClick={() => setSelectedCategory(category)}
                    className={`px-4 py-2 rounded-lg text-sm font-medium ${
                      selectedCategory === category
                        ? 'bg-blue-600 text-white'
                        : 'bg-white text-gray-700 hover:bg-gray-50 border border-gray-300'
                    }`}
                  >
                    {category === 'all' ? 'All Categories' : category}
                  </button>
                ))}
              </div>
              <div className="relative">
                <input
                  type="text"
                  placeholder="Search modules..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-4 pr-10 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
            </div>

            {/* Training Modules Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredModules.map((module) => (
                <div key={module.id} className="bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
                  <div className="p-6">
                    <div className="flex items-center justify-between mb-4">
                      <div className="flex items-center space-x-3">
                        <div className="p-2 bg-blue-100 rounded-lg">
                          <module.icon className="h-6 w-6 text-blue-600" />
                        </div>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getDifficultyColor(module.difficulty)}`}>
                          {module.difficulty}
                        </span>
                      </div>
                      {module.completed && (
                        <CheckCircleIcon className="h-6 w-6 text-green-500" />
                      )}
                    </div>
                    
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">{module.title}</h3>
                    <p className="text-gray-600 text-sm mb-4">{module.description}</p>
                    
                    <div className="space-y-3">
                      <div className="flex items-center justify-between text-sm text-gray-500">
                        <span className="flex items-center">
                          <ClockIcon className="h-4 w-4 mr-1" />
                          {module.duration}
                        </span>
                        <span className="flex items-center">
                          <BeakerIcon className="h-4 w-4 mr-1" />
                          {module.practicalExercises} exercises
                        </span>
                      </div>
                      
                      {module.progress > 0 && (
                        <div>
                          <div className="flex justify-between text-sm text-gray-600 mb-1">
                            <span>Progress</span>
                            <span>{module.progress}%</span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2">
                            <div 
                              className="bg-blue-600 h-2 rounded-full" 
                              style={{ width: `${module.progress}%` }}
                            ></div>
                          </div>
                        </div>
                      )}
                      
                      <div className="pt-4 border-t border-gray-100">
                        <button className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors flex items-center justify-center">
                          <PlayIcon className="h-4 w-4 mr-2" />
                          {module.completed ? 'Review' : module.progress > 0 ? 'Continue' : 'Start Module'}
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'datasets' && (
          <div>
            <div className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Hugging Face Medical Datasets</h2>
              <p className="text-gray-600">
                Explore and download curated medical datasets for training and fine-tuning AI models
              </p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {huggingFaceDatasets.map((dataset) => (
                <div key={dataset.id} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900">{dataset.name}</h3>
                      <p className="text-gray-600 text-sm mt-1">{dataset.description}</p>
                    </div>
                    <span className="bg-orange-100 text-orange-800 text-xs font-medium px-2 py-1 rounded-full">
                      {dataset.task}
                    </span>
                  </div>
                  
                  <div className="grid grid-cols-2 gap-4 mb-4 text-sm">
                    <div>
                      <span className="text-gray-500">Downloads:</span>
                      <span className="ml-2 font-medium">{dataset.downloads.toLocaleString()}</span>
                    </div>
                    <div>
                      <span className="text-gray-500">Size:</span>
                      <span className="ml-2 font-medium">{dataset.size}</span>
                    </div>
                    <div>
                      <span className="text-gray-500">Language:</span>
                      <span className="ml-2 font-medium">{dataset.language}</span>
                    </div>
                    <div>
                      <span className="text-gray-500">License:</span>
                      <span className="ml-2 font-medium">{dataset.license}</span>
                    </div>
                  </div>
                  
                  <div className="mb-4">
                    <div className="flex flex-wrap gap-1">
                      {dataset.tags.map((tag, index) => (
                        <span key={index} className="bg-gray-100 text-gray-700 text-xs px-2 py-1 rounded">
                          {tag}
                        </span>
                      ))}
                    </div>
                  </div>
                  
                  <div className="flex space-x-3">
                    <button className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors text-sm">
                      Download Dataset
                    </button>
                    <button className="flex-1 border border-gray-300 text-gray-700 py-2 px-4 rounded-lg hover:bg-gray-50 transition-colors text-sm">
                      View on HF Hub
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'progress' && (
          <div>
            <div className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Your Learning Progress</h2>
              <p className="text-gray-600">
                Track your progress across all training modules and achievements
              </p>
            </div>

            {/* Progress Overview */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <div className="flex items-center">
                  <CheckCircleIcon className="h-8 w-8 text-green-500" />
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-500">Completed Modules</p>
                    <p className="text-2xl font-bold text-gray-900">
                      {trainingModules.filter(m => m.completed).length} / {trainingModules.length}
                    </p>
                  </div>
                </div>
              </div>
              
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <div className="flex items-center">
                  <ClockIcon className="h-8 w-8 text-blue-500" />
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-500">Total Study Time</p>
                    <p className="text-2xl font-bold text-gray-900">24.5 hours</p>
                  </div>
                </div>
              </div>
              
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <div className="flex items-center">
                  <StarIcon className="h-8 w-8 text-yellow-500" />
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-500">Achievements</p>
                    <p className="text-2xl font-bold text-gray-900">5 / 12</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Detailed Progress */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Module Progress</h3>
              <div className="space-y-4">
                {trainingModules.map((module) => (
                  <div key={module.id} className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <module.icon className="h-5 w-5 text-gray-400" />
                      <div>
                        <p className="font-medium text-gray-900">{module.title}</p>
                        <p className="text-sm text-gray-500">{module.category}</p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-4">
                      <div className="w-32">
                        <div className="flex justify-between text-sm text-gray-600 mb-1">
                          <span>{module.progress}%</span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2">
                          <div 
                            className="bg-blue-600 h-2 rounded-full" 
                            style={{ width: `${module.progress}%` }}
                          ></div>
                        </div>
                      </div>
                      {module.completed && (
                        <CheckCircleIcon className="h-5 w-5 text-green-500" />
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
