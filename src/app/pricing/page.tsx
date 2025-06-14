'use client';

import { useState } from 'react';
import { useAuth, useUser } from '@clerk/nextjs';
import Link from 'next/link';
import { CheckIcon, XMarkIcon } from '@heroicons/react/24/outline';
import { SUBSCRIPTION_PLANS, formatCurrency } from '@/lib/razorpay';
import toast from 'react-hot-toast';

declare global {
  interface Window {
    Razorpay: any;
  }
}

export default function Pricing() {
  const { isSignedIn } = useAuth();
  const { user } = useUser();
  const [isProcessing, setIsProcessing] = useState<string | null>(null);

  const handleSubscribe = async (planId: string) => {
    if (!isSignedIn) {
      toast.error('Please sign in to subscribe');
      return;
    }

    if (planId === 'free') {
      toast.success('You are already on the free plan!');
      return;
    }

    setIsProcessing(planId);

    try {
      // Create subscription
      const response = await fetch('/api/subscription/create', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          planId,
          customerEmail: user?.emailAddresses[0]?.emailAddress,
          customerName: user?.fullName || user?.firstName || 'User'
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to create subscription');
      }

      // Initialize Razorpay checkout
      const options = {
        subscription_id: data.subscription.id,
        name: 'FertiVision',
        description: `${SUBSCRIPTION_PLANS[planId as keyof typeof SUBSCRIPTION_PLANS].name} Plan`,
        image: '/logo.png',
        handler: function (response: any) {
          toast.success('Subscription activated successfully!');
          // Redirect to dashboard
          window.location.href = '/dashboard';
        },
        prefill: {
          email: user?.emailAddresses[0]?.emailAddress,
          name: user?.fullName || user?.firstName || 'User'
        },
        notes: {
          plan_name: SUBSCRIPTION_PLANS[planId as keyof typeof SUBSCRIPTION_PLANS].name,
          user_id: user?.id
        },
        theme: {
          color: '#4F46E5'
        },
        modal: {
          ondismiss: function() {
            setIsProcessing(null);
            toast.error('Payment cancelled');
          }
        }
      };

      const rzp = new window.Razorpay(options);
      rzp.open();

    } catch (error) {
      console.error('Subscription error:', error);
      toast.error(error instanceof Error ? error.message : 'Failed to process subscription');
      setIsProcessing(null);
    }
  };

  const plans = [
    {
      ...SUBSCRIPTION_PLANS.free,
      popular: false,
      buttonText: 'Current Plan',
      buttonAction: () => handleSubscribe('free')
    },
    {
      ...SUBSCRIPTION_PLANS.professional,
      popular: true,
      buttonText: 'Subscribe Now',
      buttonAction: () => handleSubscribe('professional')
    },
    {
      ...SUBSCRIPTION_PLANS.enterprise,
      popular: false,
      buttonText: 'Subscribe Now',
      buttonAction: () => handleSubscribe('enterprise')
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex justify-between items-center">
            <Link href="/" className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-lg">F</span>
              </div>
              <span className="text-2xl font-bold text-indigo-900">FertiVision</span>
            </Link>
            <div className="flex items-center space-x-4">
              {isSignedIn ? (
                <>
                  <Link href="/dashboard" className="text-indigo-600 hover:text-indigo-800 font-medium">
                    Dashboard
                  </Link>
                  <Link href="/analysis" className="text-indigo-600 hover:text-indigo-800 font-medium">
                    Analysis
                  </Link>
                </>
              ) : (
                <Link href="/" className="text-indigo-600 hover:text-indigo-800 font-medium">
                  Home
                </Link>
              )}
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-6 py-16">
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Choose Your Plan
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Scale your reproductive medicine practice with AI-powered analysis. 
            All plans include WHO 2021 and ESHRE compliant analysis with enterprise-grade security.
          </p>
        </div>

        {/* Pricing Cards */}
        <div className="grid lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {plans.map((plan) => (
            <div
              key={plan.id}
              className={`relative bg-white rounded-2xl shadow-lg ${
                plan.popular ? 'ring-2 ring-indigo-500 scale-105' : ''
              }`}
            >
              {plan.popular && (
                <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                  <span className="bg-indigo-500 text-white px-4 py-2 rounded-full text-sm font-medium">
                    Most Popular
                  </span>
                </div>
              )}

              <div className="p-8">
                <div className="text-center mb-8">
                  <h3 className="text-2xl font-bold text-gray-900 mb-2">
                    {plan.name}
                  </h3>
                  <div className="mb-4">
                    <span className="text-5xl font-bold text-gray-900">
                      {plan.price === 0 ? 'Free' : formatCurrency(plan.price)}
                    </span>
                    {plan.price > 0 && (
                      <span className="text-gray-600 ml-2">/month</span>
                    )}
                  </div>
                  <p className="text-gray-600">
                    {plan.analyses_limit === -1 
                      ? 'Unlimited analyses' 
                      : `${plan.analyses_limit} analyses per month`
                    }
                  </p>
                </div>

                <ul className="space-y-4 mb-8">
                  {plan.features.map((feature, index) => (
                    <li key={index} className="flex items-start">
                      <CheckIcon className="w-5 h-5 text-green-500 mt-0.5 mr-3 flex-shrink-0" />
                      <span className="text-gray-700">{feature}</span>
                    </li>
                  ))}
                </ul>

                <button
                  onClick={plan.buttonAction}
                  disabled={isProcessing === plan.id}
                  className={`w-full py-3 px-6 rounded-lg font-semibold transition-colors ${
                    plan.popular
                      ? 'bg-indigo-600 text-white hover:bg-indigo-700'
                      : plan.id === 'free'
                      ? 'bg-gray-100 text-gray-600 cursor-default'
                      : 'bg-gray-900 text-white hover:bg-gray-800'
                  } ${
                    isProcessing === plan.id ? 'opacity-50 cursor-not-allowed' : ''
                  }`}
                >
                  {isProcessing === plan.id ? 'Processing...' : plan.buttonText}
                </button>
              </div>
            </div>
          ))}
        </div>

        {/* Features Comparison */}
        <div className="mt-20">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
            Feature Comparison
          </h2>
          
          <div className="bg-white rounded-lg shadow overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-4 text-left text-sm font-medium text-gray-900">
                      Features
                    </th>
                    <th className="px-6 py-4 text-center text-sm font-medium text-gray-900">
                      Free
                    </th>
                    <th className="px-6 py-4 text-center text-sm font-medium text-gray-900">
                      Professional
                    </th>
                    <th className="px-6 py-4 text-center text-sm font-medium text-gray-900">
                      Enterprise
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  <tr>
                    <td className="px-6 py-4 text-sm text-gray-900">Monthly Analyses</td>
                    <td className="px-6 py-4 text-center text-sm text-gray-600">10</td>
                    <td className="px-6 py-4 text-center text-sm text-gray-600">500</td>
                    <td className="px-6 py-4 text-center text-sm text-gray-600">Unlimited</td>
                  </tr>
                  <tr>
                    <td className="px-6 py-4 text-sm text-gray-900">AI Analysis Types</td>
                    <td className="px-6 py-4 text-center">
                      <CheckIcon className="w-5 h-5 text-green-500 mx-auto" />
                    </td>
                    <td className="px-6 py-4 text-center">
                      <CheckIcon className="w-5 h-5 text-green-500 mx-auto" />
                    </td>
                    <td className="px-6 py-4 text-center">
                      <CheckIcon className="w-5 h-5 text-green-500 mx-auto" />
                    </td>
                  </tr>
                  <tr>
                    <td className="px-6 py-4 text-sm text-gray-900">WHO 2021 Compliance</td>
                    <td className="px-6 py-4 text-center">
                      <CheckIcon className="w-5 h-5 text-green-500 mx-auto" />
                    </td>
                    <td className="px-6 py-4 text-center">
                      <CheckIcon className="w-5 h-5 text-green-500 mx-auto" />
                    </td>
                    <td className="px-6 py-4 text-center">
                      <CheckIcon className="w-5 h-5 text-green-500 mx-auto" />
                    </td>
                  </tr>
                  <tr>
                    <td className="px-6 py-4 text-sm text-gray-900">API Access</td>
                    <td className="px-6 py-4 text-center">
                      <XMarkIcon className="w-5 h-5 text-red-500 mx-auto" />
                    </td>
                    <td className="px-6 py-4 text-center">
                      <CheckIcon className="w-5 h-5 text-green-500 mx-auto" />
                    </td>
                    <td className="px-6 py-4 text-center">
                      <CheckIcon className="w-5 h-5 text-green-500 mx-auto" />
                    </td>
                  </tr>
                  <tr>
                    <td className="px-6 py-4 text-sm text-gray-900">Priority Support</td>
                    <td className="px-6 py-4 text-center">
                      <XMarkIcon className="w-5 h-5 text-red-500 mx-auto" />
                    </td>
                    <td className="px-6 py-4 text-center">
                      <CheckIcon className="w-5 h-5 text-green-500 mx-auto" />
                    </td>
                    <td className="px-6 py-4 text-center">
                      <CheckIcon className="w-5 h-5 text-green-500 mx-auto" />
                    </td>
                  </tr>
                  <tr>
                    <td className="px-6 py-4 text-sm text-gray-900">Custom Integrations</td>
                    <td className="px-6 py-4 text-center">
                      <XMarkIcon className="w-5 h-5 text-red-500 mx-auto" />
                    </td>
                    <td className="px-6 py-4 text-center">
                      <CheckIcon className="w-5 h-5 text-green-500 mx-auto" />
                    </td>
                    <td className="px-6 py-4 text-center">
                      <CheckIcon className="w-5 h-5 text-green-500 mx-auto" />
                    </td>
                  </tr>
                  <tr>
                    <td className="px-6 py-4 text-sm text-gray-900">White-label Options</td>
                    <td className="px-6 py-4 text-center">
                      <XMarkIcon className="w-5 h-5 text-red-500 mx-auto" />
                    </td>
                    <td className="px-6 py-4 text-center">
                      <XMarkIcon className="w-5 h-5 text-red-500 mx-auto" />
                    </td>
                    <td className="px-6 py-4 text-center">
                      <CheckIcon className="w-5 h-5 text-green-500 mx-auto" />
                    </td>
                  </tr>
                  <tr>
                    <td className="px-6 py-4 text-sm text-gray-900">24/7 Support</td>
                    <td className="px-6 py-4 text-center">
                      <XMarkIcon className="w-5 h-5 text-red-500 mx-auto" />
                    </td>
                    <td className="px-6 py-4 text-center">
                      <XMarkIcon className="w-5 h-5 text-red-500 mx-auto" />
                    </td>
                    <td className="px-6 py-4 text-center">
                      <CheckIcon className="w-5 h-5 text-green-500 mx-auto" />
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* FAQ Section */}
        <div className="mt-20">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
            Frequently Asked Questions
          </h2>
          
          <div className="max-w-3xl mx-auto space-y-8">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Can I change my plan anytime?
              </h3>
              <p className="text-gray-600">
                Yes, you can upgrade or downgrade your plan at any time. Changes will be reflected in your next billing cycle.
              </p>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Is my data secure and compliant?
              </h3>
              <p className="text-gray-600">
                Absolutely. We follow HIPAA compliance standards and use enterprise-grade security. Your medical images are processed securely and not stored permanently.
              </p>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Do you offer custom enterprise solutions?
              </h3>
              <p className="text-gray-600">
                Yes, we offer custom enterprise solutions including on-premise deployment, custom AI models, and dedicated support. Contact us for more information.
              </p>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                What payment methods do you accept?
              </h3>
              <p className="text-gray-600">
                We accept all major credit cards, debit cards, UPI, and net banking through our secure Razorpay integration.
              </p>
            </div>
          </div>
        </div>

        {/* CTA Section */}
        <div className="mt-20 bg-indigo-600 rounded-2xl p-12 text-center text-white">
          <h2 className="text-3xl font-bold mb-4">Ready to Get Started?</h2>
          <p className="text-xl mb-8 opacity-90">
            Join leading fertility clinics using AI-powered analysis for better patient outcomes.
          </p>
          {!isSignedIn ? (
            <Link 
              href="/"
              className="bg-white text-indigo-600 px-8 py-4 rounded-lg text-lg font-semibold hover:bg-gray-100 transition-colors inline-block"
            >
              Sign Up for Free
            </Link>
          ) : (
            <Link 
              href="/analysis"
              className="bg-white text-indigo-600 px-8 py-4 rounded-lg text-lg font-semibold hover:bg-gray-100 transition-colors inline-block"
            >
              Start Analyzing
            </Link>
          )}
        </div>
      </div>
    </div>
  );
}
