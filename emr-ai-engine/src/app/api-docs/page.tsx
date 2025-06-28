'use client';

import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  Code, 
  Copy, 
  ExternalLink, 
  Key,
  Zap,
  Shield,
  Clock,
  CheckCircle
} from 'lucide-react';

export default function APIDocumentation() {
  const [selectedEndpoint, setSelectedEndpoint] = useState('analyze');

  const endpoints = {
    analyze: {
      method: 'POST',
      path: '/api/v1/analyze',
      description: 'Perform AI analysis on reproductive medicine images',
      parameters: {
        image: 'string (base64 encoded image)',
        analysisType: 'string (sperm, oocyte, embryo, follicle)',
        options: 'object (optional analysis parameters)'
      },
      example: `{
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ...",
  "analysisType": "sperm",
  "options": {
    "includeVisualization": true,
    "detailedReport": true
  }
}`,
      response: `{
  "success": true,
  "analysisType": "sperm",
  "result": {
    "concentration": 45,
    "motility": {
      "progressive": 32,
      "nonProgressive": 8,
      "immotile": 60
    },
    "morphology": {
      "normal": 4,
      "abnormal": 96
    },
    "vitality": 75,
    "who2021Compliant": true,
    "confidence": 0.95,
    "processingTime": 1.2
  },
  "usage": {
    "remaining": 4950,
    "resetDate": "2024-02-01T00:00:00Z"
  },
  "timestamp": "2024-01-21T10:30:00Z"
}`
    },
    usage: {
      method: 'GET',
      path: '/api/v1/usage',
      description: 'Get API usage statistics and billing information',
      parameters: {
        period: 'string (hour, day, month, year)',
        detailed: 'boolean (include detailed analytics)'
      },
      example: 'GET /api/v1/usage?period=month&detailed=true',
      response: `{
  "usage": {
    "totalRequests": 1250,
    "successfulRequests": 1238,
    "failedRequests": 12,
    "totalCost": 125.50,
    "averageProcessingTime": 1.2,
    "analysisBreakdown": {
      "sperm": 450,
      "oocyte": 320,
      "embryo": 280,
      "follicle": 200
    }
  },
  "subscription": {
    "plan": "professional",
    "limits": {
      "requestsPerMonth": 5000,
      "requestsPerDay": 200,
      "requestsPerHour": 50
    },
    "status": "active"
  }
}`
    },
    subscription: {
      method: 'GET/POST',
      path: '/api/v1/subscription',
      description: 'Manage API subscription and billing plans',
      parameters: {
        plan: 'string (professional, enterprise, custom)',
        customConfig: 'object (for custom plans)'
      },
      example: `{
  "plan": "enterprise"
}`,
      response: `{
  "success": true,
  "subscription": {
    "plan": "enterprise",
    "limits": {
      "requestsPerMonth": 50000,
      "requestsPerDay": 2000,
      "requestsPerHour": 500
    },
    "pricing": {
      "basePrice": 999,
      "perRequestPrice": 0.05,
      "overage": 0.15
    },
    "status": "active"
  }
}`
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  return (
    <div className="container mx-auto p-6 space-y-6">
      <div className="text-center space-y-4">
        <h1 className="text-4xl font-bold">FertiVision API Documentation</h1>
        <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
          Comprehensive AI-powered reproductive medicine APIs for clinical decision support and image analysis
        </p>
        <div className="flex justify-center space-x-4 flex-wrap gap-2">
          <Badge className="bg-green-100 text-green-800">
            <CheckCircle className="w-3 h-3 mr-1" />
            WHO 2021 Compliant
          </Badge>
          <Badge className="bg-blue-100 text-blue-800">
            <Shield className="w-3 h-3 mr-1" />
            HIPAA Secure
          </Badge>
          <Badge className="bg-purple-100 text-purple-800">
            <Zap className="w-3 h-3 mr-1" />
            Real-time Analysis
          </Badge>
          <Badge className="bg-red-100 text-red-800">
            <Shield className="w-3 h-3 mr-1" />
            Clinical Grade
          </Badge>
        </div>
      </div>

      {/* Quick Start */}
      <Card className="bg-gradient-to-r from-blue-50 to-purple-50">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Zap className="h-5 w-5" />
            Quick Start
          </CardTitle>
          <CardDescription>Get started with the FertiVision API in minutes</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="text-center p-4 bg-white rounded-lg">
              <Key className="h-8 w-8 mx-auto mb-2 text-blue-600" />
              <h3 className="font-semibold">1. Get API Key</h3>
              <p className="text-sm text-muted-foreground">Sign up and get your API key from the dashboard</p>
            </div>
            <div className="text-center p-4 bg-white rounded-lg">
              <Code className="h-8 w-8 mx-auto mb-2 text-green-600" />
              <h3 className="font-semibold">2. Make Request</h3>
              <p className="text-sm text-muted-foreground">Send images for AI analysis via REST API</p>
            </div>
            <div className="text-center p-4 bg-white rounded-lg">
              <Clock className="h-8 w-8 mx-auto mb-2 text-purple-600" />
              <h3 className="font-semibold">3. Get Results</h3>
              <p className="text-sm text-muted-foreground">Receive detailed analysis results in seconds</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* API Reference */}
      <Tabs defaultValue="endpoints" className="space-y-4">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="endpoints">API Endpoints</TabsTrigger>
          <TabsTrigger value="authentication">Authentication</TabsTrigger>
          <TabsTrigger value="examples">Code Examples</TabsTrigger>
          <TabsTrigger value="pricing">Pricing</TabsTrigger>
        </TabsList>

        <TabsContent value="endpoints" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Endpoint List */}
            <Card>
              <CardHeader>
                <CardTitle>Available Endpoints</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                {Object.entries(endpoints).map(([key, endpoint]) => (
                  <button
                    key={key}
                    onClick={() => setSelectedEndpoint(key)}
                    className={`w-full text-left p-3 rounded-lg border transition-colors ${
                      selectedEndpoint === key 
                        ? 'bg-blue-50 border-blue-200' 
                        : 'hover:bg-gray-50'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="font-medium">{endpoint.path}</span>
                      <Badge variant="outline">{endpoint.method}</Badge>
                    </div>
                    <p className="text-sm text-muted-foreground mt-1">
                      {endpoint.description}
                    </p>
                  </button>
                ))}
              </CardContent>
            </Card>

            {/* Endpoint Details */}
            <div className="lg:col-span-2 space-y-4">
              {selectedEndpoint && (
                <>
                  <Card>
                    <CardHeader>
                      <div className="flex items-center justify-between">
                        <CardTitle className="flex items-center gap-2">
                          <Badge>{endpoints[selectedEndpoint].method}</Badge>
                          {endpoints[selectedEndpoint].path}
                        </CardTitle>
                        <Button variant="outline" size="sm">
                          <ExternalLink className="h-4 w-4" />
                        </Button>
                      </div>
                      <CardDescription>
                        {endpoints[selectedEndpoint].description}
                      </CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                      <div>
                        <h4 className="font-semibold mb-2">Parameters</h4>
                        <div className="space-y-2">
                          {Object.entries(endpoints[selectedEndpoint].parameters).map(([param, type]) => (
                            <div key={param} className="flex items-center justify-between p-2 bg-gray-50 rounded">
                              <code className="text-sm font-mono">{param}</code>
                              <span className="text-sm text-muted-foreground">{type}</span>
                            </div>
                          ))}
                        </div>
                      </div>

                      <div>
                        <div className="flex items-center justify-between mb-2">
                          <h4 className="font-semibold">Request Example</h4>
                          <Button 
                            variant="outline" 
                            size="sm"
                            onClick={() => copyToClipboard(endpoints[selectedEndpoint].example)}
                          >
                            <Copy className="h-4 w-4" />
                          </Button>
                        </div>
                        <pre className="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto text-sm">
                          {endpoints[selectedEndpoint].example}
                        </pre>
                      </div>

                      <div>
                        <div className="flex items-center justify-between mb-2">
                          <h4 className="font-semibold">Response Example</h4>
                          <Button 
                            variant="outline" 
                            size="sm"
                            onClick={() => copyToClipboard(endpoints[selectedEndpoint].response)}
                          >
                            <Copy className="h-4 w-4" />
                          </Button>
                        </div>
                        <pre className="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto text-sm">
                          {endpoints[selectedEndpoint].response}
                        </pre>
                      </div>
                    </CardContent>
                  </Card>
                </>
              )}
            </div>
          </div>
        </TabsContent>

        <TabsContent value="authentication" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>API Authentication</CardTitle>
              <CardDescription>Secure your API requests with proper authentication</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <h3 className="font-semibold mb-2">Bearer Token Authentication</h3>
                <p className="text-muted-foreground mb-4">
                  All API requests must include your API key in the Authorization header.
                </p>
                <pre className="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto">
{`Authorization: Bearer YOUR_API_KEY

# Example with curl
curl -X POST https://api.fertivision.ai/v1/analyze \\
  -H "Authorization: Bearer fv_12345678_abcdefghijklmnop" \\
  -H "Content-Type: application/json" \\
  -d '{"image": "...", "analysisType": "sperm"}'`}
                </pre>
              </div>

              <div className="bg-yellow-50 p-4 rounded-lg border border-yellow-200">
                <h4 className="font-semibold text-yellow-800 mb-2">Security Best Practices</h4>
                <ul className="text-sm text-yellow-700 space-y-1">
                  <li>• Never expose your API key in client-side code</li>
                  <li>• Use environment variables to store API keys</li>
                  <li>• Rotate your API keys regularly</li>
                  <li>• Monitor your API usage for unusual activity</li>
                </ul>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="examples" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Python Example</CardTitle>
              </CardHeader>
              <CardContent>
                <pre className="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto text-sm">
{`import requests
import base64

# Read and encode image
with open('sperm_sample.jpg', 'rb') as f:
    image_data = base64.b64encode(f.read()).decode()

# API request
response = requests.post(
    'https://api.fertivision.ai/v1/analyze',
    headers={
        'Authorization': 'Bearer YOUR_API_KEY',
        'Content-Type': 'application/json'
    },
    json={
        'image': f'data:image/jpeg;base64,{image_data}',
        'analysisType': 'sperm',
        'options': {
            'includeVisualization': True
        }
    }
)

result = response.json()
print(f"Concentration: {result['result']['concentration']} M/ml")`}
                </pre>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>JavaScript Example</CardTitle>
              </CardHeader>
              <CardContent>
                <pre className="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto text-sm">
{`const analyzeImage = async (imageFile) => {
  // Convert file to base64
  const base64 = await fileToBase64(imageFile);
  
  const response = await fetch('/api/v1/analyze', {
    method: 'POST',
    headers: {
      'Authorization': 'Bearer YOUR_API_KEY',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      image: base64,
      analysisType: 'embryo',
      options: {
        detailedReport: true
      }
    })
  });
  
  const result = await response.json();
  console.log('Analysis result:', result);
};

const fileToBase64 = (file) => {
  return new Promise((resolve) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.readAsDataURL(file);
  });
};`}
                </pre>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="pricing" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Free Plan</CardTitle>
                <CardDescription>Perfect for testing and small projects</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="text-3xl font-bold">₹0<span className="text-lg font-normal">/month</span></div>
                <ul className="space-y-2 text-sm">
                  <li>• 100 API calls/month</li>
                  <li>• 10 calls/day limit</li>
                  <li>• Basic support</li>
                  <li>• Standard processing</li>
                </ul>
                <Button className="w-full">Get Started</Button>
              </CardContent>
            </Card>

            <Card className="border-blue-200 bg-blue-50">
              <CardHeader>
                <CardTitle>Professional</CardTitle>
                <CardDescription>For growing clinics and practices</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="text-3xl font-bold">₹299<span className="text-lg font-normal">/month</span></div>
                <ul className="space-y-2 text-sm">
                  <li>• 5,000 API calls/month</li>
                  <li>• ₹0.10 per additional call</li>
                  <li>• Priority support</li>
                  <li>• Advanced analytics</li>
                </ul>
                <Button className="w-full">Upgrade Now</Button>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Enterprise</CardTitle>
                <CardDescription>For large institutions and hospitals</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="text-3xl font-bold">₹999<span className="text-lg font-normal">/month</span></div>
                <ul className="space-y-2 text-sm">
                  <li>• 50,000 API calls/month</li>
                  <li>• ₹0.05 per additional call</li>
                  <li>• 24/7 dedicated support</li>
                  <li>• Custom integration</li>
                  <li>• SLA guarantee</li>
                </ul>
                <Button className="w-full">Contact Sales</Button>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}
