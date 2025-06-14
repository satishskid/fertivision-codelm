'use client';

import { useState, useEffect } from 'react';
import { useUser } from '@clerk/nextjs';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  Activity, 
  DollarSign, 
  Clock, 
  TrendingUp,
  Key,
  Code,
  BarChart3,
  AlertTriangle,
  CheckCircle,
  Copy
} from 'lucide-react';

interface APIUsageData {
  totalRequests: number;
  successfulRequests: number;
  failedRequests: number;
  totalCost: number;
  averageProcessingTime: number;
  analysisBreakdown: {
    sperm: number;
    oocyte: number;
    embryo: number;
    follicle: number;
  };
  period: string;
}

interface SubscriptionData {
  plan: string;
  limits: {
    requestsPerMonth: number;
    requestsPerDay: number;
    requestsPerHour: number;
  };
  pricing: {
    basePrice: number;
    perRequestPrice: number;
    overage: number;
  };
  status: string;
  endDate: string;
}

export default function APIDashboard() {
  const { user, isLoaded } = useUser();
  const [usage, setUsage] = useState<APIUsageData | null>(null);
  const [subscription, setSubscription] = useState<SubscriptionData | null>(null);
  const [apiKey, setApiKey] = useState<string>('');
  const [showApiKey, setShowApiKey] = useState(false);

  useEffect(() => {
    if (isLoaded && user) {
      fetchUsageData();
      fetchSubscriptionData();
      generateApiKey();
    }
  }, [isLoaded, user]);

  const fetchUsageData = async () => {
    try {
      const response = await fetch('/api/v1/usage?period=month&detailed=true');
      const data = await response.json();
      setUsage(data.usage);
    } catch (error) {
      console.error('Failed to fetch usage data:', error);
      // Mock data for demo
      setUsage({
        totalRequests: 1250,
        successfulRequests: 1238,
        failedRequests: 12,
        totalCost: 125.50,
        averageProcessingTime: 1.2,
        analysisBreakdown: {
          sperm: 450,
          oocyte: 320,
          embryo: 280,
          follicle: 200
        },
        period: 'month'
      });
    }
  };

  const fetchSubscriptionData = async () => {
    try {
      const response = await fetch('/api/v1/subscription');
      const data = await response.json();
      setSubscription(data.subscription);
    } catch (error) {
      console.error('Failed to fetch subscription data:', error);
      // Mock data for demo
      setSubscription({
        plan: 'professional',
        limits: {
          requestsPerMonth: 5000,
          requestsPerDay: 200,
          requestsPerHour: 50
        },
        pricing: {
          basePrice: 299,
          perRequestPrice: 0.10,
          overage: 0.25
        },
        status: 'active',
        endDate: '2024-02-21T00:00:00Z'
      });
    }
  };

  const generateApiKey = () => {
    // Generate a demo API key
    const key = `fv_${user?.id?.slice(0, 8)}_${Math.random().toString(36).substr(2, 16)}`;
    setApiKey(key);
  };

  const copyApiKey = () => {
    navigator.clipboard.writeText(apiKey);
    // You could add a toast notification here
  };

  if (!isLoaded) {
    return <div className="flex items-center justify-center min-h-screen">Loading...</div>;
  }

  if (!user) {
    return <div className="flex items-center justify-center min-h-screen">Please sign in to access the API dashboard.</div>;
  }

  const usagePercentage = subscription ? (usage?.totalRequests || 0) / subscription.limits.requestsPerMonth * 100 : 0;
  const remainingRequests = subscription ? subscription.limits.requestsPerMonth - (usage?.totalRequests || 0) : 0;

  return (
    <div className="container mx-auto p-6 space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">API Dashboard</h1>
          <p className="text-muted-foreground">Monitor your FertiVision API usage and manage your subscription</p>
        </div>
        <Badge variant={subscription?.status === 'active' ? 'default' : 'destructive'}>
          {subscription?.plan} Plan
        </Badge>
      </div>

      {/* Overview Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">API Calls This Month</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{usage?.totalRequests.toLocaleString() || 0}</div>
            <p className="text-xs text-muted-foreground">
              {remainingRequests.toLocaleString()} remaining
            </p>
            <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
              <div 
                className="bg-blue-600 h-2 rounded-full" 
                style={{ width: `${Math.min(usagePercentage, 100)}%` }}
              ></div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Success Rate</CardTitle>
            <CheckCircle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {usage ? ((usage.successfulRequests / usage.totalRequests) * 100).toFixed(1) : 0}%
            </div>
            <p className="text-xs text-muted-foreground">
              {usage?.failedRequests || 0} failed requests
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Current Cost</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">₹{usage?.totalCost.toFixed(2) || '0.00'}</div>
            <p className="text-xs text-muted-foreground">
              Base: ₹{subscription?.pricing.basePrice || 0}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Avg Response Time</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{usage?.averageProcessingTime.toFixed(1) || 0}s</div>
            <p className="text-xs text-muted-foreground">
              Processing time
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Detailed Dashboard */}
      <Tabs defaultValue="usage" className="space-y-4">
        <TabsList>
          <TabsTrigger value="usage">Usage Analytics</TabsTrigger>
          <TabsTrigger value="api-keys">API Keys</TabsTrigger>
          <TabsTrigger value="billing">Billing & Plans</TabsTrigger>
          <TabsTrigger value="documentation">Documentation</TabsTrigger>
        </TabsList>

        <TabsContent value="usage" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Analysis Type Breakdown</CardTitle>
                <CardDescription>Distribution of API calls by analysis type</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {usage && Object.entries(usage.analysisBreakdown).map(([type, count]) => (
                    <div key={type} className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <div className="w-3 h-3 bg-blue-600 rounded-full"></div>
                        <span className="capitalize">{type} Analysis</span>
                      </div>
                      <div className="text-right">
                        <span className="font-medium">{count}</span>
                        <span className="text-sm text-muted-foreground ml-2">
                          ({((count / usage.totalRequests) * 100).toFixed(1)}%)
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Usage Limits</CardTitle>
                <CardDescription>Current usage against your plan limits</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span>Monthly Limit</span>
                      <span>{usage?.totalRequests || 0} / {subscription?.limits.requestsPerMonth || 0}</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div 
                        className={`h-2 rounded-full ${usagePercentage > 90 ? 'bg-red-600' : usagePercentage > 70 ? 'bg-yellow-600' : 'bg-green-600'}`}
                        style={{ width: `${Math.min(usagePercentage, 100)}%` }}
                      ></div>
                    </div>
                  </div>
                  
                  {usagePercentage > 80 && (
                    <div className="flex items-center space-x-2 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
                      <AlertTriangle className="h-4 w-4 text-yellow-600" />
                      <span className="text-sm text-yellow-800">
                        You're approaching your monthly limit. Consider upgrading your plan.
                      </span>
                    </div>
                  )}

                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <span className="text-muted-foreground">Daily Limit:</span>
                      <p className="font-medium">{subscription?.limits.requestsPerDay || 0}</p>
                    </div>
                    <div>
                      <span className="text-muted-foreground">Hourly Limit:</span>
                      <p className="font-medium">{subscription?.limits.requestsPerHour || 0}</p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="api-keys" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>API Authentication</CardTitle>
              <CardDescription>Manage your API keys for accessing FertiVision services</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <label className="text-sm font-medium">Your API Key</label>
                <div className="flex items-center space-x-2 mt-1">
                  <input 
                    type={showApiKey ? 'text' : 'password'}
                    value={apiKey}
                    readOnly
                    className="flex-1 p-2 border rounded-md bg-gray-50"
                  />
                  <Button 
                    variant="outline" 
                    size="sm"
                    onClick={() => setShowApiKey(!showApiKey)}
                  >
                    {showApiKey ? 'Hide' : 'Show'}
                  </Button>
                  <Button 
                    variant="outline" 
                    size="sm"
                    onClick={copyApiKey}
                  >
                    <Copy className="h-4 w-4" />
                  </Button>
                </div>
                <p className="text-xs text-muted-foreground mt-1">
                  Keep your API key secure. Don't share it in publicly accessible areas.
                </p>
              </div>

              <div className="bg-blue-50 p-4 rounded-lg">
                <h3 className="font-medium text-blue-900 mb-2">Quick Start</h3>
                <pre className="text-xs bg-white p-3 rounded border overflow-x-auto">
{`curl -X POST https://api.fertivision.ai/v1/analyze \\
  -H "Authorization: Bearer ${apiKey}" \\
  -H "Content-Type: application/json" \\
  -d '{
    "image": "base64_encoded_image",
    "analysisType": "sperm",
    "options": {}
  }'`}
                </pre>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="billing" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Current Plan</CardTitle>
                <CardDescription>Your subscription details and pricing</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="font-medium">Plan:</span>
                  <Badge>{subscription?.plan}</Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span className="font-medium">Monthly Base:</span>
                  <span>₹{subscription?.pricing.basePrice}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="font-medium">Per Request:</span>
                  <span>₹{subscription?.pricing.perRequestPrice}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="font-medium">Overage Rate:</span>
                  <span>₹{subscription?.pricing.overage}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="font-medium">Next Billing:</span>
                  <span>{subscription ? new Date(subscription.endDate).toLocaleDateString() : 'N/A'}</span>
                </div>
                <Button className="w-full">Upgrade Plan</Button>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Billing History</CardTitle>
                <CardDescription>Your recent billing and usage history</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex items-center justify-between p-3 border rounded">
                    <div>
                      <p className="font-medium">January 2024</p>
                      <p className="text-sm text-muted-foreground">1,250 API calls</p>
                    </div>
                    <span className="font-medium">₹125.50</span>
                  </div>
                  <div className="flex items-center justify-between p-3 border rounded">
                    <div>
                      <p className="font-medium">December 2023</p>
                      <p className="text-sm text-muted-foreground">980 API calls</p>
                    </div>
                    <span className="font-medium">₹98.00</span>
                  </div>
                  <div className="flex items-center justify-between p-3 border rounded">
                    <div>
                      <p className="font-medium">November 2023</p>
                      <p className="text-sm text-muted-foreground">1,450 API calls</p>
                    </div>
                    <span className="font-medium">₹145.00</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="documentation" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>API Documentation</CardTitle>
              <CardDescription>Learn how to integrate FertiVision AI into your applications</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="p-4 border rounded-lg">
                  <h3 className="font-medium mb-2">🧬 Sperm Analysis</h3>
                  <p className="text-sm text-muted-foreground mb-3">
                    WHO 2021 compliant semen analysis with automated parameter assessment.
                  </p>
                  <Button variant="outline" size="sm">View Docs</Button>
                </div>
                <div className="p-4 border rounded-lg">
                  <h3 className="font-medium mb-2">🥚 Oocyte Assessment</h3>
                  <p className="text-sm text-muted-foreground mb-3">
                    ESHRE guidelines-based maturity evaluation and quality grading.
                  </p>
                  <Button variant="outline" size="sm">View Docs</Button>
                </div>
                <div className="p-4 border rounded-lg">
                  <h3 className="font-medium mb-2">👶 Embryo Grading</h3>
                  <p className="text-sm text-muted-foreground mb-3">
                    Gardner grading system for embryo development assessment.
                  </p>
                  <Button variant="outline" size="sm">View Docs</Button>
                </div>
                <div className="p-4 border rounded-lg">
                  <h3 className="font-medium mb-2">🔬 Follicle Analysis</h3>
                  <p className="text-sm text-muted-foreground mb-3">
                    Automated follicle counting and size distribution analysis.
                  </p>
                  <Button variant="outline" size="sm">View Docs</Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
