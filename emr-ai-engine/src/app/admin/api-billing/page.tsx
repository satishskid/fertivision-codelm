'use client';

import { useState, useEffect } from 'react';
import { useUser } from '@clerk/nextjs';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  DollarSign, 
  Users, 
  Activity, 
  TrendingUp,
  Settings,
  Plus,
  Edit,
  BarChart3,
  Clock,
  AlertCircle
} from 'lucide-react';

interface CustomerBilling {
  userId: string;
  email: string;
  name: string;
  plan: string;
  monthlyUsage: number;
  monthlyLimit: number;
  currentCost: number;
  customBilling?: {
    enabled: boolean;
    billingPeriod: string;
    customRate: number;
  };
  status: 'active' | 'suspended' | 'overdue';
  lastActivity: string;
}

export default function APIBillingDashboard() {
  const { user, isLoaded } = useUser();
  const [customers, setCustomers] = useState<CustomerBilling[]>([]);
  const [selectedCustomer, setSelectedCustomer] = useState<CustomerBilling | null>(null);
  const [showCustomBillingModal, setShowCustomBillingModal] = useState(false);

  // Check if user is admin
  const isAdmin = user?.emailAddresses[0]?.emailAddress === 'satish@skids.health';

  useEffect(() => {
    // Mock data - replace with actual API calls
    const mockCustomers: CustomerBilling[] = [
      {
        userId: '1',
        email: 'clinic@example.com',
        name: 'City Fertility Clinic',
        plan: 'enterprise',
        monthlyUsage: 15420,
        monthlyLimit: 50000,
        currentCost: 1245.50,
        status: 'active',
        lastActivity: '2024-01-21T10:30:00Z'
      },
      {
        userId: '2',
        email: 'dr.smith@hospital.com',
        name: 'Dr. Smith Medical Center',
        plan: 'professional',
        monthlyUsage: 3250,
        monthlyLimit: 5000,
        currentCost: 624.75,
        status: 'active',
        lastActivity: '2024-01-21T09:15:00Z'
      },
      {
        userId: '3',
        email: 'research@university.edu',
        name: 'University Research Lab',
        plan: 'custom',
        monthlyUsage: 8750,
        monthlyLimit: 10000,
        currentCost: 875.00,
        customBilling: {
          enabled: true,
          billingPeriod: 'monthly',
          customRate: 0.10
        },
        status: 'active',
        lastActivity: '2024-01-20T16:45:00Z'
      }
    ];
    setCustomers(mockCustomers);
  }, []);

  if (!isLoaded) {
    return <div className="flex items-center justify-center min-h-screen">Loading...</div>;
  }

  if (!isAdmin) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Card className="w-96">
          <CardHeader>
            <CardTitle className="text-red-600">Access Denied</CardTitle>
            <CardDescription>You don't have permission to access API billing management.</CardDescription>
          </CardHeader>
        </Card>
      </div>
    );
  }

  const totalRevenue = customers.reduce((sum, c) => sum + c.currentCost, 0);
  const totalUsage = customers.reduce((sum, c) => sum + c.monthlyUsage, 0);
  const averageUsage = totalUsage / customers.length;

  return (
    <div className="container mx-auto p-6 space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">API Billing Management</h1>
          <p className="text-muted-foreground">Manage customer subscriptions and custom billing</p>
        </div>
        <Button onClick={() => setShowCustomBillingModal(true)} className="flex items-center gap-2">
          <Plus className="h-4 w-4" />
          Create Custom Plan
        </Button>
      </div>

      {/* Overview Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Monthly Revenue</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">₹{totalRevenue.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">+12% from last month</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">API Customers</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{customers.length}</div>
            <p className="text-xs text-muted-foreground">Active subscribers</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total API Calls</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{totalUsage.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">This month</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Avg Usage</CardTitle>
            <BarChart3 className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{Math.round(averageUsage).toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">Calls per customer</p>
          </CardContent>
        </Card>
      </div>

      {/* Customer Management */}
      <Tabs defaultValue="customers" className="space-y-4">
        <TabsList>
          <TabsTrigger value="customers">Customer Management</TabsTrigger>
          <TabsTrigger value="billing">Custom Billing</TabsTrigger>
          <TabsTrigger value="analytics">Usage Analytics</TabsTrigger>
        </TabsList>

        <TabsContent value="customers" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>API Customers</CardTitle>
              <CardDescription>Manage customer subscriptions and billing</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {customers.map((customer) => (
                  <div key={customer.userId} className="flex items-center justify-between p-4 border rounded-lg">
                    <div className="flex items-center space-x-4">
                      <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white font-semibold">
                        {customer.name.charAt(0)}
                      </div>
                      <div>
                        <p className="font-semibold">{customer.name}</p>
                        <p className="text-sm text-muted-foreground">{customer.email}</p>
                        <div className="flex items-center space-x-2 mt-1">
                          <Badge variant={customer.plan === 'enterprise' ? 'default' : 'secondary'}>
                            {customer.plan}
                          </Badge>
                          <Badge variant={customer.status === 'active' ? 'default' : 'destructive'}>
                            {customer.status}
                          </Badge>
                        </div>
                      </div>
                    </div>
                    <div className="text-right space-y-1">
                      <p className="font-semibold">₹{customer.currentCost.toFixed(2)}</p>
                      <p className="text-sm text-muted-foreground">
                        {customer.monthlyUsage.toLocaleString()} / {customer.monthlyLimit.toLocaleString()} calls
                      </p>
                      <div className="w-32 bg-gray-200 rounded-full h-2">
                        <div 
                          className="bg-blue-600 h-2 rounded-full" 
                          style={{ width: `${(customer.monthlyUsage / customer.monthlyLimit) * 100}%` }}
                        ></div>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Button 
                        variant="outline" 
                        size="sm"
                        onClick={() => setSelectedCustomer(customer)}
                      >
                        <Edit className="h-4 w-4" />
                      </Button>
                      <Button variant="outline" size="sm">
                        <Settings className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="billing" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Custom Billing Plans</CardTitle>
              <CardDescription>Create and manage custom billing for enterprise customers</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <h3 className="text-lg font-semibold">Create Custom Plan</h3>
                  <div className="space-y-3">
                    <div>
                      <label className="text-sm font-medium">Customer Email</label>
                      <input 
                        type="email" 
                        className="w-full p-2 border rounded-md"
                        placeholder="customer@example.com"
                      />
                    </div>
                    <div>
                      <label className="text-sm font-medium">Billing Period</label>
                      <select className="w-full p-2 border rounded-md">
                        <option value="monthly">Monthly</option>
                        <option value="quarterly">Quarterly</option>
                        <option value="yearly">Yearly</option>
                        <option value="custom">Custom Period</option>
                      </select>
                    </div>
                    <div>
                      <label className="text-sm font-medium">API Call Limit</label>
                      <input 
                        type="number" 
                        className="w-full p-2 border rounded-md"
                        placeholder="10000"
                      />
                    </div>
                    <div>
                      <label className="text-sm font-medium">Base Price (₹)</label>
                      <input 
                        type="number" 
                        className="w-full p-2 border rounded-md"
                        placeholder="1500"
                      />
                    </div>
                    <div>
                      <label className="text-sm font-medium">Per-Call Rate (₹)</label>
                      <input 
                        type="number" 
                        step="0.01"
                        className="w-full p-2 border rounded-md"
                        placeholder="0.08"
                      />
                    </div>
                    <Button className="w-full">Create Custom Plan</Button>
                  </div>
                </div>

                <div className="space-y-4">
                  <h3 className="text-lg font-semibold">Active Custom Plans</h3>
                  {customers.filter(c => c.customBilling?.enabled).map((customer) => (
                    <div key={customer.userId} className="p-4 border rounded-lg">
                      <div className="flex justify-between items-start">
                        <div>
                          <p className="font-semibold">{customer.name}</p>
                          <p className="text-sm text-muted-foreground">{customer.email}</p>
                          <div className="mt-2 space-y-1">
                            <p className="text-sm">
                              <span className="font-medium">Period:</span> {customer.customBilling?.billingPeriod}
                            </p>
                            <p className="text-sm">
                              <span className="font-medium">Rate:</span> ₹{customer.customBilling?.customRate}/call
                            </p>
                            <p className="text-sm">
                              <span className="font-medium">Current Cost:</span> ₹{customer.currentCost}
                            </p>
                          </div>
                        </div>
                        <Button variant="outline" size="sm">
                          <Edit className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="analytics" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Usage Analytics</CardTitle>
              <CardDescription>Detailed API usage and billing analytics</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="space-y-3">
                  <h3 className="font-semibold text-green-600">Revenue Metrics</h3>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-sm">Monthly Revenue:</span>
                      <span className="font-medium">₹{totalRevenue.toFixed(2)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm">Average per Customer:</span>
                      <span className="font-medium">₹{(totalRevenue / customers.length).toFixed(2)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm">Growth Rate:</span>
                      <span className="font-medium text-green-600">+12%</span>
                    </div>
                  </div>
                </div>

                <div className="space-y-3">
                  <h3 className="font-semibold text-blue-600">Usage Metrics</h3>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-sm">Total API Calls:</span>
                      <span className="font-medium">{totalUsage.toLocaleString()}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm">Success Rate:</span>
                      <span className="font-medium text-green-600">99.2%</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm">Avg Response Time:</span>
                      <span className="font-medium">1.2s</span>
                    </div>
                  </div>
                </div>

                <div className="space-y-3">
                  <h3 className="font-semibold text-purple-600">Customer Metrics</h3>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-sm">Active Customers:</span>
                      <span className="font-medium">{customers.filter(c => c.status === 'active').length}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm">Enterprise Plans:</span>
                      <span className="font-medium">{customers.filter(c => c.plan === 'enterprise').length}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm">Custom Billing:</span>
                      <span className="font-medium">{customers.filter(c => c.customBilling?.enabled).length}</span>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
