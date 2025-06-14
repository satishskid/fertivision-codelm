'use client';

import { useState, useEffect } from 'react';
import { useAuth, useUser } from '@clerk/nextjs';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import toast from 'react-hot-toast';
import { 
  CogIcon, 
  KeyIcon, 
  CreditCardIcon, 
  CheckCircleIcon,
  ExclamationTriangleIcon 
} from '@heroicons/react/24/outline';

interface ConfigItem {
  key: string;
  value: string;
  description: string;
  type: 'text' | 'password' | 'textarea';
}

export default function AdminPanel() {
  const { isSignedIn } = useAuth();
  const { user } = useUser();
  const router = useRouter();
  
  const [activeTab, setActiveTab] = useState('api-keys');
  const [isSaving, setIsSaving] = useState(false);
  const [configs, setConfigs] = useState<ConfigItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // Check if user is admin (you can implement your own logic)
  const isAdmin = user?.emailAddresses[0]?.emailAddress === process.env.NEXT_PUBLIC_ADMIN_EMAIL ||
                  user?.id === process.env.NEXT_PUBLIC_ADMIN_USER_ID;

  useEffect(() => {
    if (!isSignedIn) {
      router.push('/');
      return;
    }

    if (!isAdmin) {
      toast.error('Access denied. Admin privileges required.');
      router.push('/dashboard');
      return;
    }

    loadConfigurations();
  }, [isSignedIn, isAdmin, router]);

  const loadConfigurations = async () => {
    try {
      const response = await fetch('/api/admin/config');
      const data = await response.json();
      
      if (data.success) {
        setConfigs(data.configs);
      } else {
        toast.error('Failed to load configurations');
      }
    } catch (error) {
      console.error('Error loading configurations:', error);
      toast.error('Failed to load configurations');
    } finally {
      setIsLoading(false);
    }
  };

  const saveConfiguration = async (key: string, value: string) => {
    setIsSaving(true);
    
    try {
      const response = await fetch('/api/admin/config', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ key, value }),
      });

      const data = await response.json();
      
      if (data.success) {
        toast.success('Configuration saved successfully');
        // Update local state
        setConfigs(prev => prev.map(config => 
          config.key === key ? { ...config, value } : config
        ));
      } else {
        toast.error(data.error || 'Failed to save configuration');
      }
    } catch (error) {
      console.error('Error saving configuration:', error);
      toast.error('Failed to save configuration');
    } finally {
      setIsSaving(false);
    }
  };

  const testAIProviders = async () => {
    try {
      const response = await fetch('/api/admin/test-ai');
      const data = await response.json();
      
      if (data.success) {
        toast.success(`AI Providers Status: Groq: ${data.status.groq ? '✅' : '❌'}, OpenRouter: ${data.status.openrouter ? '✅' : '❌'}`);
      } else {
        toast.error('Failed to test AI providers');
      }
    } catch (error) {
      toast.error('Failed to test AI providers');
    }
  };

  const initializeDatabase = async () => {
    try {
      const response = await fetch('/api/admin/init-db', { method: 'POST' });
      const data = await response.json();
      
      if (data.success) {
        toast.success('Database initialized successfully');
      } else {
        toast.error('Failed to initialize database');
      }
    } catch (error) {
      toast.error('Failed to initialize database');
    }
  };

  if (!isSignedIn || !isAdmin) {
    return null;
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading admin panel...</p>
        </div>
      </div>
    );
  }

  const apiKeyConfigs = configs.filter(c => c.key.includes('api_key') || c.key.includes('secret'));
  const paymentConfigs = configs.filter(c => c.key.includes('razorpay') || c.key.includes('payment'));
  const generalConfigs = configs.filter(c => !apiKeyConfigs.includes(c) && !paymentConfigs.includes(c));

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
              <h1 className="text-xl font-semibold text-gray-900">Admin Panel</h1>
            </div>
            <div className="flex items-center space-x-4">
              <Link href="/dashboard" className="text-indigo-600 hover:text-indigo-800 font-medium">
                Dashboard
              </Link>
              <Link href="/analysis" className="text-indigo-600 hover:text-indigo-800 font-medium">
                Analysis
              </Link>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">System Configuration</h1>
          <p className="text-gray-600">
            Configure API keys, payment settings, and system parameters for FertiVision Cloud SaaS.
          </p>
        </div>

        {/* Quick Actions */}
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <button
            onClick={testAIProviders}
            className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition-shadow text-left"
          >
            <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
              <CheckCircleIcon className="w-6 h-6 text-blue-600" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Test AI Providers</h3>
            <p className="text-gray-600">Check connectivity to Groq and OpenRouter APIs</p>
          </button>

          <button
            onClick={initializeDatabase}
            className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition-shadow text-left"
          >
            <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
              <CogIcon className="w-6 h-6 text-green-600" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Initialize Database</h3>
            <p className="text-gray-600">Set up database tables and indexes</p>
          </button>

          <div className="bg-white p-6 rounded-lg shadow">
            <div className="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center mb-4">
              <ExclamationTriangleIcon className="w-6 h-6 text-yellow-600" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">System Status</h3>
            <p className="text-gray-600">All systems operational</p>
          </div>
        </div>

        {/* Configuration Tabs */}
        <div className="bg-white rounded-lg shadow">
          <div className="border-b border-gray-200">
            <nav className="flex space-x-8 px-6">
              <button
                onClick={() => setActiveTab('api-keys')}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'api-keys'
                    ? 'border-indigo-500 text-indigo-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                }`}
              >
                <KeyIcon className="w-5 h-5 inline mr-2" />
                API Keys
              </button>
              <button
                onClick={() => setActiveTab('payments')}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'payments'
                    ? 'border-indigo-500 text-indigo-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                }`}
              >
                <CreditCardIcon className="w-5 h-5 inline mr-2" />
                Payment Settings
              </button>
              <button
                onClick={() => setActiveTab('general')}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'general'
                    ? 'border-indigo-500 text-indigo-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                }`}
              >
                <CogIcon className="w-5 h-5 inline mr-2" />
                General Settings
              </button>
            </nav>
          </div>

          <div className="p-6">
            {activeTab === 'api-keys' && (
              <div className="space-y-6">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">AI Provider API Keys</h3>
                  <div className="space-y-4">
                    <ConfigField
                      label="Groq API Key"
                      description="API key for Groq AI service (get from console.groq.com)"
                      type="password"
                      value={configs.find(c => c.key === 'groq_api_key')?.value || ''}
                      onSave={(value) => saveConfiguration('groq_api_key', value)}
                      isSaving={isSaving}
                    />
                    <ConfigField
                      label="OpenRouter API Key"
                      description="API key for OpenRouter service (get from openrouter.ai)"
                      type="password"
                      value={configs.find(c => c.key === 'openrouter_api_key')?.value || ''}
                      onSave={(value) => saveConfiguration('openrouter_api_key', value)}
                      isSaving={isSaving}
                    />
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'payments' && (
              <div className="space-y-6">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Razorpay Configuration</h3>
                  <div className="space-y-4">
                    <ConfigField
                      label="Razorpay Key ID"
                      description="Your Razorpay Key ID (starts with rzp_test_ or rzp_live_)"
                      type="text"
                      value={configs.find(c => c.key === 'razorpay_key_id')?.value || ''}
                      onSave={(value) => saveConfiguration('razorpay_key_id', value)}
                      isSaving={isSaving}
                    />
                    <ConfigField
                      label="Razorpay Key Secret"
                      description="Your Razorpay Key Secret (keep this secure)"
                      type="password"
                      value={configs.find(c => c.key === 'razorpay_key_secret')?.value || ''}
                      onSave={(value) => saveConfiguration('razorpay_key_secret', value)}
                      isSaving={isSaving}
                    />
                    <ConfigField
                      label="Razorpay Webhook Secret"
                      description="Webhook secret for verifying Razorpay webhooks"
                      type="password"
                      value={configs.find(c => c.key === 'razorpay_webhook_secret')?.value || ''}
                      onSave={(value) => saveConfiguration('razorpay_webhook_secret', value)}
                      isSaving={isSaving}
                    />
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'general' && (
              <div className="space-y-6">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Application Settings</h3>
                  <div className="space-y-4">
                    <ConfigField
                      label="Support Email"
                      description="Email address for customer support"
                      type="text"
                      value={configs.find(c => c.key === 'support_email')?.value || ''}
                      onSave={(value) => saveConfiguration('support_email', value)}
                      isSaving={isSaving}
                    />
                    <ConfigField
                      label="Admin Email"
                      description="Email address for admin notifications"
                      type="text"
                      value={configs.find(c => c.key === 'admin_email')?.value || ''}
                      onSave={(value) => saveConfiguration('admin_email', value)}
                      isSaving={isSaving}
                    />
                    <ConfigField
                      label="App Name"
                      description="Application name displayed to users"
                      type="text"
                      value={configs.find(c => c.key === 'app_name')?.value || 'FertiVision'}
                      onSave={(value) => saveConfiguration('app_name', value)}
                      isSaving={isSaving}
                    />
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Instructions */}
        <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-blue-900 mb-2">Setup Instructions</h3>
          <div className="text-blue-800 space-y-2">
            <p>1. <strong>API Keys:</strong> Configure your Groq and OpenRouter API keys for AI analysis</p>
            <p>2. <strong>Razorpay:</strong> Set up your Razorpay credentials for payment processing</p>
            <p>3. <strong>Database:</strong> Initialize the database tables if this is a fresh installation</p>
            <p>4. <strong>Testing:</strong> Use the test buttons to verify your configurations</p>
          </div>
        </div>
      </div>
    </div>
  );
}

interface ConfigFieldProps {
  label: string;
  description: string;
  type: 'text' | 'password' | 'textarea';
  value: string;
  onSave: (value: string) => void;
  isSaving: boolean;
}

function ConfigField({ label, description, type, value, onSave, isSaving }: ConfigFieldProps) {
  const [localValue, setLocalValue] = useState(value);
  const [isEditing, setIsEditing] = useState(false);

  const handleSave = () => {
    onSave(localValue);
    setIsEditing(false);
  };

  const handleCancel = () => {
    setLocalValue(value);
    setIsEditing(false);
  };

  return (
    <div className="border border-gray-200 rounded-lg p-4">
      <div className="flex justify-between items-start mb-2">
        <div>
          <h4 className="font-medium text-gray-900">{label}</h4>
          <p className="text-sm text-gray-600">{description}</p>
        </div>
        {!isEditing && (
          <button
            onClick={() => setIsEditing(true)}
            className="text-indigo-600 hover:text-indigo-800 text-sm font-medium"
          >
            Edit
          </button>
        )}
      </div>

      {isEditing ? (
        <div className="mt-3">
          {type === 'textarea' ? (
            <textarea
              value={localValue}
              onChange={(e) => setLocalValue(e.target.value)}
              rows={3}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500"
            />
          ) : (
            <input
              type={type}
              value={localValue}
              onChange={(e) => setLocalValue(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500"
            />
          )}
          <div className="flex space-x-3 mt-3">
            <button
              onClick={handleSave}
              disabled={isSaving}
              className="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-indigo-700 disabled:opacity-50"
            >
              {isSaving ? 'Saving...' : 'Save'}
            </button>
            <button
              onClick={handleCancel}
              className="bg-gray-300 text-gray-700 px-4 py-2 rounded-lg text-sm font-medium hover:bg-gray-400"
            >
              Cancel
            </button>
          </div>
        </div>
      ) : (
        <div className="mt-3">
          <div className="text-sm text-gray-900 font-mono bg-gray-50 p-2 rounded">
            {value ? (type === 'password' ? '••••••••••••' : value) : 'Not configured'}
          </div>
        </div>
      )}
    </div>
  );
}
