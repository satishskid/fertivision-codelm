import { auth, currentUser } from '@clerk/nextjs';
import { redirect } from 'next/navigation';
import Link from 'next/link';
import { UserButton } from '@clerk/nextjs';
import { 
  ChartBarIcon, 
  BeakerIcon, 
  CreditCardIcon, 
  DocumentTextIcon,
  ClockIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline';
import { getUserByClerkId, createUser, getUserAnalyses } from '@/lib/db';
import { SUBSCRIPTION_PLANS, getDaysUntilRenewal } from '@/lib/razorpay';

export default async function Dashboard() {
  const { userId } = auth();
  
  if (!userId) {
    redirect('/sign-in');
  }

  // Get current user from Clerk
  const clerkUser = await currentUser();
  
  if (!clerkUser) {
    redirect('/sign-in');
  }

  // Get or create user in our database
  let user = await getUserByClerkId(userId);
  
  if (!user) {
    user = await createUser(
      userId,
      clerkUser.emailAddresses[0]?.emailAddress || '',
      clerkUser.firstName && clerkUser.lastName 
        ? `${clerkUser.firstName} ${clerkUser.lastName}` 
        : clerkUser.firstName || ''
    );
  }

  if (!user) {
    return <div>Error loading user data</div>;
  }

  // Get user's recent analyses
  const recentAnalyses = await getUserAnalyses(user.id, 10);
  
  // Get subscription plan details
  const currentPlan = SUBSCRIPTION_PLANS[user.subscription_plan as keyof typeof SUBSCRIPTION_PLANS];
  
  // Calculate usage percentage
  const usagePercentage = user.analyses_limit === -1 
    ? 0 
    : Math.min((user.analyses_used / user.analyses_limit) * 100, 100);

  // Mock subscription end date for demo (replace with real data)
  const subscriptionEndDate = Math.floor(Date.now() / 1000) + (30 * 24 * 60 * 60); // 30 days from now
  const daysUntilRenewal = getDaysUntilRenewal(subscriptionEndDate);

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
              <h1 className="text-xl font-semibold text-gray-900">Dashboard</h1>
            </div>
            <div className="flex items-center space-x-4">
              <Link href="/analysis" className="text-indigo-600 hover:text-indigo-800 font-medium">
                New Analysis
              </Link>
              <Link href="/pricing" className="text-indigo-600 hover:text-indigo-800 font-medium">
                Pricing
              </Link>
              <UserButton />
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Welcome back, {clerkUser.firstName || 'User'}!
          </h1>
          <p className="text-gray-600">
            Here's an overview of your FertiVision account and recent activity.
          </p>
        </div>

        {/* Stats Cards */}
        <div className="grid md:grid-cols-4 gap-6 mb-8">
          {/* Usage Card */}
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                <ChartBarIcon className="w-6 h-6 text-blue-600" />
              </div>
              <span className="text-sm text-gray-500">This Month</span>
            </div>
            <div className="mb-2">
              <div className="text-2xl font-bold text-gray-900">
                {user.analyses_used}
                {user.analyses_limit !== -1 && (
                  <span className="text-lg text-gray-500">/{user.analyses_limit}</span>
                )}
              </div>
              <div className="text-sm text-gray-600">
                {user.analyses_limit === -1 ? 'Unlimited analyses' : 'Analyses used'}
              </div>
            </div>
            {user.analyses_limit !== -1 && (
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className={`h-2 rounded-full ${
                    usagePercentage > 90 ? 'bg-red-500' : 
                    usagePercentage > 70 ? 'bg-yellow-500' : 'bg-blue-500'
                  }`}
                  style={{ width: `${usagePercentage}%` }}
                ></div>
              </div>
            )}
          </div>

          {/* Subscription Card */}
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-indigo-100 rounded-lg flex items-center justify-center">
                <CreditCardIcon className="w-6 h-6 text-indigo-600" />
              </div>
              <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                user.subscription_plan === 'enterprise' ? 'bg-purple-100 text-purple-800' :
                user.subscription_plan === 'professional' ? 'bg-blue-100 text-blue-800' :
                'bg-gray-100 text-gray-800'
              }`}>
                {currentPlan?.name || 'Free'}
              </span>
            </div>
            <div className="mb-2">
              <div className="text-2xl font-bold text-gray-900">
                {currentPlan?.price === 0 ? 'Free' : `₹${(currentPlan?.price || 0) / 100}`}
              </div>
              <div className="text-sm text-gray-600">Current plan</div>
            </div>
            {user.subscription_plan !== 'free' && (
              <div className="text-xs text-gray-500">
                Renews in {daysUntilRenewal} days
              </div>
            )}
          </div>

          {/* Recent Analyses */}
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                <BeakerIcon className="w-6 h-6 text-green-600" />
              </div>
              <span className="text-sm text-gray-500">Last 7 days</span>
            </div>
            <div className="mb-2">
              <div className="text-2xl font-bold text-gray-900">
                {recentAnalyses.filter(a => {
                  const weekAgo = new Date();
                  weekAgo.setDate(weekAgo.getDate() - 7);
                  return new Date(a.created_at) > weekAgo;
                }).length}
              </div>
              <div className="text-sm text-gray-600">Recent analyses</div>
            </div>
          </div>

          {/* Success Rate */}
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-emerald-100 rounded-lg flex items-center justify-center">
                <CheckCircleIcon className="w-6 h-6 text-emerald-600" />
              </div>
              <span className="text-sm text-gray-500">All time</span>
            </div>
            <div className="mb-2">
              <div className="text-2xl font-bold text-gray-900">
                {recentAnalyses.length > 0 ? '98.5%' : '0%'}
              </div>
              <div className="text-sm text-gray-600">Success rate</div>
            </div>
          </div>
        </div>

        {/* Usage Warning */}
        {user.analyses_limit !== -1 && usagePercentage > 80 && (
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-8">
            <div className="flex items-center">
              <ExclamationTriangleIcon className="w-5 h-5 text-yellow-600 mr-3" />
              <div>
                <h3 className="text-sm font-medium text-yellow-800">
                  Usage Limit Warning
                </h3>
                <p className="text-sm text-yellow-700 mt-1">
                  You've used {user.analyses_used} of {user.analyses_limit} analyses this month. 
                  {usagePercentage > 95 ? (
                    <span> Consider upgrading your plan to continue analyzing.</span>
                  ) : (
                    <span> Consider upgrading to avoid interruptions.</span>
                  )}
                </p>
              </div>
              <Link 
                href="/pricing" 
                className="ml-auto bg-yellow-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-yellow-700 transition-colors"
              >
                Upgrade Plan
              </Link>
            </div>
          </div>
        )}

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Quick Actions */}
          <div className="lg:col-span-2">
            <h2 className="text-xl font-semibold text-gray-900 mb-6">Quick Actions</h2>
            <div className="grid md:grid-cols-2 gap-6">
              <Link href="/analysis" className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition-shadow group">
                <div className="w-12 h-12 bg-indigo-100 rounded-lg flex items-center justify-center mb-4 group-hover:bg-indigo-200 transition-colors">
                  <BeakerIcon className="w-6 h-6 text-indigo-600" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">New Analysis</h3>
                <p className="text-gray-600 mb-4">Upload medical images for AI-powered analysis</p>
                <div className="text-indigo-600 font-medium group-hover:text-indigo-700">
                  Start analyzing →
                </div>
              </Link>

              <Link href="/reports" className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition-shadow group">
                <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4 group-hover:bg-green-200 transition-colors">
                  <DocumentTextIcon className="w-6 h-6 text-green-600" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">View Reports</h3>
                <p className="text-gray-600 mb-4">Access your analysis history and reports</p>
                <div className="text-green-600 font-medium group-hover:text-green-700">
                  View reports →
                </div>
              </Link>

              <Link href="/pricing" className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition-shadow group">
                <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4 group-hover:bg-purple-200 transition-colors">
                  <CreditCardIcon className="w-6 h-6 text-purple-600" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Manage Subscription</h3>
                <p className="text-gray-600 mb-4">Upgrade your plan or manage billing</p>
                <div className="text-purple-600 font-medium group-hover:text-purple-700">
                  Manage plan →
                </div>
              </Link>

              <Link href="/admin" className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition-shadow group">
                <div className="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center mb-4 group-hover:bg-gray-200 transition-colors">
                  <ClockIcon className="w-6 h-6 text-gray-600" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Admin Settings</h3>
                <p className="text-gray-600 mb-4">Configure API keys and system settings</p>
                <div className="text-gray-600 font-medium group-hover:text-gray-700">
                  Open settings →
                </div>
              </Link>
            </div>
          </div>

          {/* Recent Activity */}
          <div>
            <h2 className="text-xl font-semibold text-gray-900 mb-6">Recent Activity</h2>
            <div className="bg-white rounded-lg shadow">
              {recentAnalyses.length > 0 ? (
                <div className="divide-y divide-gray-200">
                  {recentAnalyses.slice(0, 5).map((analysis) => (
                    <div key={analysis.id} className="p-4">
                      <div className="flex items-center justify-between">
                        <div>
                          <div className="text-sm font-medium text-gray-900 capitalize">
                            {analysis.analysis_type} Analysis
                          </div>
                          <div className="text-sm text-gray-500">
                            {analysis.patient_id && `Patient: ${analysis.patient_id}`}
                          </div>
                          <div className="text-xs text-gray-400">
                            {new Date(analysis.created_at).toLocaleDateString()}
                          </div>
                        </div>
                        <div className="text-right">
                          <div className="text-sm font-medium text-green-600">
                            {analysis.confidence ? `${analysis.confidence}%` : 'Completed'}
                          </div>
                          <div className="text-xs text-gray-500">
                            {analysis.processing_time ? `${analysis.processing_time}s` : ''}
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="p-8 text-center">
                  <BeakerIcon className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-lg font-medium text-gray-900 mb-2">No analyses yet</h3>
                  <p className="text-gray-600 mb-4">Start your first analysis to see activity here</p>
                  <Link 
                    href="/analysis" 
                    className="bg-indigo-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-indigo-700 transition-colors"
                  >
                    Start Analysis
                  </Link>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
