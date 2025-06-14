'use client';

import { useState, useEffect } from 'react';
import { useUser } from '@clerk/nextjs';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  Users, 
  CreditCard, 
  TrendingUp, 
  DollarSign,
  QrCode,
  Eye,
  Download,
  Calendar,
  Activity
} from 'lucide-react';

interface UserData {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  createdAt: string;
  lastSignIn: string;
  paymentStatus: 'free' | 'paid' | 'premium';
  subscriptionPlan: string;
  totalPayments: number;
  lastPayment: string;
}

interface PaymentStats {
  totalRevenue: number;
  totalUsers: number;
  paidUsers: number;
  freeUsers: number;
  monthlyRevenue: number;
  conversionRate: number;
}

export default function AdminDashboard() {
  const { user, isLoaded } = useUser();
  const [users, setUsers] = useState<UserData[]>([]);
  const [stats, setStats] = useState<PaymentStats>({
    totalRevenue: 0,
    totalUsers: 0,
    paidUsers: 0,
    freeUsers: 0,
    monthlyRevenue: 0,
    conversionRate: 0
  });
  const [showQRCode, setShowQRCode] = useState(false);

  // Mock data - In production, this would come from your database
  useEffect(() => {
    const mockUsers: UserData[] = [
      {
        id: '1',
        email: 'user1@example.com',
        firstName: 'John',
        lastName: 'Doe',
        createdAt: '2024-01-15',
        lastSignIn: '2024-01-20',
        paymentStatus: 'paid',
        subscriptionPlan: 'Professional',
        totalPayments: 2999,
        lastPayment: '2024-01-20'
      },
      {
        id: '2',
        email: 'user2@example.com',
        firstName: 'Jane',
        lastName: 'Smith',
        createdAt: '2024-01-10',
        lastSignIn: '2024-01-19',
        paymentStatus: 'free',
        subscriptionPlan: 'Free',
        totalPayments: 0,
        lastPayment: 'Never'
      },
      {
        id: '3',
        email: 'user3@example.com',
        firstName: 'Dr. Sarah',
        lastName: 'Johnson',
        createdAt: '2024-01-05',
        lastSignIn: '2024-01-21',
        paymentStatus: 'premium',
        subscriptionPlan: 'Enterprise',
        totalPayments: 9999,
        lastPayment: '2024-01-21'
      }
    ];

    setUsers(mockUsers);
    
    // Calculate stats
    const totalUsers = mockUsers.length;
    const paidUsers = mockUsers.filter(u => u.paymentStatus !== 'free').length;
    const freeUsers = totalUsers - paidUsers;
    const totalRevenue = mockUsers.reduce((sum, u) => sum + u.totalPayments, 0);
    const conversionRate = totalUsers > 0 ? (paidUsers / totalUsers) * 100 : 0;

    setStats({
      totalRevenue,
      totalUsers,
      paidUsers,
      freeUsers,
      monthlyRevenue: totalRevenue * 0.3, // Mock monthly revenue
      conversionRate
    });
  }, []);

  if (!isLoaded) {
    return <div className="flex items-center justify-center min-h-screen">Loading...</div>;
  }

  // Check if user is admin (you can implement your own admin check logic)
  const isAdmin = user?.emailAddresses[0]?.emailAddress === 'satish@skids.health';

  if (!isAdmin) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Card className="w-96">
          <CardHeader>
            <CardTitle className="text-red-600">Access Denied</CardTitle>
            <CardDescription>You don't have permission to access this dashboard.</CardDescription>
          </CardHeader>
        </Card>
      </div>
    );
  }

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'paid':
        return <Badge className="bg-green-100 text-green-800">Paid</Badge>;
      case 'premium':
        return <Badge className="bg-purple-100 text-purple-800">Premium</Badge>;
      default:
        return <Badge variant="secondary">Free</Badge>;
    }
  };

  return (
    <div className="container mx-auto p-6 space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">Admin Dashboard</h1>
          <p className="text-muted-foreground">FertiVision Cloud Platform Analytics</p>
        </div>
        <Button onClick={() => setShowQRCode(!showQRCode)} className="flex items-center gap-2">
          <QrCode className="h-4 w-4" />
          {showQRCode ? 'Hide' : 'Show'} Payment QR
        </Button>
      </div>

      {/* QR Code Display */}
      {showQRCode && (
        <Card className="bg-gradient-to-r from-blue-50 to-purple-50">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <QrCode className="h-5 w-5" />
              Razorpay Payment QR Code
            </CardTitle>
            <CardDescription>
              SKIDS TECHNOLOGY PRIVATE LIMITED - UPI Payment Gateway
            </CardDescription>
          </CardHeader>
          <CardContent className="flex flex-col items-center space-y-4">
            <div className="bg-white p-4 rounded-lg shadow-lg">
              <img
                src="/razorpay-qr.svg"
                alt="Razorpay QR Code"
                className="w-64 h-64"
              />
            </div>
            <div className="text-center">
              <p className="font-semibold">SCAN & PAY WITH ANY UPI APP</p>
              <div className="flex items-center gap-4 mt-2">
                <span className="text-sm text-muted-foreground">Powered by</span>
                <span className="font-bold text-blue-600">Razorpay</span>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Revenue</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">₹{(stats.totalRevenue / 100).toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">
              +12% from last month
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Users</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.totalUsers}</div>
            <p className="text-xs text-muted-foreground">
              {stats.paidUsers} paid, {stats.freeUsers} free
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Conversion Rate</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.conversionRate.toFixed(1)}%</div>
            <p className="text-xs text-muted-foreground">
              Free to paid conversion
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Monthly Revenue</CardTitle>
            <CreditCard className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">₹{(stats.monthlyRevenue / 100).toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">
              This month's earnings
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Detailed Analytics */}
      <Tabs defaultValue="users" className="space-y-4">
        <TabsList>
          <TabsTrigger value="users">User Management</TabsTrigger>
          <TabsTrigger value="payments">Payment Analytics</TabsTrigger>
          <TabsTrigger value="activity">Activity Log</TabsTrigger>
        </TabsList>

        <TabsContent value="users" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Registered Users</CardTitle>
              <CardDescription>
                All users registered on the platform with their payment status
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {users.map((user) => (
                  <div key={user.id} className="flex items-center justify-between p-4 border rounded-lg">
                    <div className="flex items-center space-x-4">
                      <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white font-semibold">
                        {user.firstName[0]}{user.lastName[0]}
                      </div>
                      <div>
                        <p className="font-semibold">{user.firstName} {user.lastName}</p>
                        <p className="text-sm text-muted-foreground">{user.email}</p>
                        <p className="text-xs text-muted-foreground">
                          Joined: {new Date(user.createdAt).toLocaleDateString()}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-4">
                      <div className="text-right">
                        <p className="font-semibold">{user.subscriptionPlan}</p>
                        <p className="text-sm text-muted-foreground">
                          ₹{(user.totalPayments / 100).toLocaleString()} total
                        </p>
                      </div>
                      {getStatusBadge(user.paymentStatus)}
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="payments" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Payment Analytics</CardTitle>
              <CardDescription>
                Detailed payment and subscription analytics
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="p-4 border rounded-lg">
                  <h3 className="font-semibold text-green-600">Successful Payments</h3>
                  <p className="text-2xl font-bold">{stats.paidUsers}</p>
                  <p className="text-sm text-muted-foreground">Total paid subscriptions</p>
                </div>
                <div className="p-4 border rounded-lg">
                  <h3 className="font-semibold text-blue-600">Average Revenue Per User</h3>
                  <p className="text-2xl font-bold">
                    ₹{stats.totalUsers > 0 ? ((stats.totalRevenue / stats.totalUsers) / 100).toFixed(0) : 0}
                  </p>
                  <p className="text-sm text-muted-foreground">ARPU calculation</p>
                </div>
                <div className="p-4 border rounded-lg">
                  <h3 className="font-semibold text-purple-600">Premium Users</h3>
                  <p className="text-2xl font-bold">
                    {users.filter(u => u.paymentStatus === 'premium').length}
                  </p>
                  <p className="text-sm text-muted-foreground">Enterprise subscriptions</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="activity" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Recent Activity</CardTitle>
              <CardDescription>
                Latest user activities and system events
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex items-center space-x-3 p-3 bg-green-50 rounded-lg">
                  <Activity className="h-4 w-4 text-green-600" />
                  <div>
                    <p className="text-sm font-medium">New payment received</p>
                    <p className="text-xs text-muted-foreground">Dr. Sarah Johnson upgraded to Enterprise - ₹999</p>
                  </div>
                  <span className="text-xs text-muted-foreground ml-auto">2 hours ago</span>
                </div>
                <div className="flex items-center space-x-3 p-3 bg-blue-50 rounded-lg">
                  <Users className="h-4 w-4 text-blue-600" />
                  <div>
                    <p className="text-sm font-medium">New user registration</p>
                    <p className="text-xs text-muted-foreground">Jane Smith signed up for free trial</p>
                  </div>
                  <span className="text-xs text-muted-foreground ml-auto">5 hours ago</span>
                </div>
                <div className="flex items-center space-x-3 p-3 bg-purple-50 rounded-lg">
                  <CreditCard className="h-4 w-4 text-purple-600" />
                  <div>
                    <p className="text-sm font-medium">Subscription renewal</p>
                    <p className="text-xs text-muted-foreground">John Doe renewed Professional plan - ₹299</p>
                  </div>
                  <span className="text-xs text-muted-foreground ml-auto">1 day ago</span>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
