'use client';

import { useState } from 'react';
import { SignedIn, SignedOut, SignInButton, SignUpButton, UserButton, useUser } from '@clerk/nextjs';
import Link from 'next/link';
import { ArrowRightIcon, BeakerIcon, ChartBarIcon, CpuChipIcon, Cog6ToothIcon, CrownIcon } from '@heroicons/react/24/outline';
import PaymentModal from '@/components/payment/PaymentModal';

export default function Home() {
  const { user } = useUser();
  const [showPaymentModal, setShowPaymentModal] = useState(false);
  const [selectedPlan, setSelectedPlan] = useState<'professional' | 'enterprise'>('professional');

  // Check if user is admin for dashboard access
  const isAdmin = user?.emailAddresses[0]?.emailAddress === 'satish@skids.health';

  const handleUpgrade = (plan: 'professional' | 'enterprise') => {
    setSelectedPlan(plan);
    setShowPaymentModal(true);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      {/* Navigation */}
      <nav className="flex justify-between items-center p-6 max-w-7xl mx-auto">
        <div className="flex items-center space-x-2">
          <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center">
            <span className="text-white font-bold text-lg">F</span>
          </div>
          <h1 className="text-2xl font-bold text-indigo-900">FertiVision</h1>
        </div>
        <div className="flex items-center space-x-4">
          <SignedOut>
            <Link href="/demo" className="text-indigo-600 hover:text-indigo-800 font-medium">
              Demo
            </Link>
            <Link href="/pricing" className="text-indigo-600 hover:text-indigo-800 font-medium">
              Pricing
            </Link>
            <SignInButton mode="modal">
              <button className="text-indigo-600 hover:text-indigo-800 font-medium">
                Sign In
              </button>
            </SignInButton>
            <SignUpButton mode="modal">
              <button className="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700 transition-colors font-medium">
                Get Started
              </button>
            </SignUpButton>
          </SignedOut>
          <SignedIn>
            <Link href="/dashboard" className="text-indigo-600 hover:text-indigo-800 font-medium">
              Dashboard
            </Link>
            <Link href="/clinical-dashboard" className="text-indigo-600 hover:text-indigo-800 font-medium">
              Clinical APIs
            </Link>
            <Link href="/api-dashboard" className="text-indigo-600 hover:text-indigo-800 font-medium">
              API Usage
            </Link>
            <button
              onClick={() => handleUpgrade('professional')}
              className="text-indigo-600 hover:text-indigo-800 font-medium flex items-center space-x-1"
            >
              <CrownIcon className="w-4 h-4" />
              <span>Upgrade</span>
            </button>
            {isAdmin && (
              <>
                <Link href="/admin/dashboard" className="text-purple-600 hover:text-purple-800 font-medium">
                  Admin
                </Link>
                <Link href="/admin/api-billing" className="text-purple-600 hover:text-purple-800 font-medium">
                  API Billing
                </Link>
              </>
            )}
            <UserButton />
          </SignedIn>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-6 py-20">
        <div className="text-center">
          <h1 className="text-6xl font-bold text-gray-900 mb-6">
            AI-Enhanced
            <span className="text-indigo-600 block">Reproductive Medicine</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto leading-relaxed">
            Advanced AI analysis for sperm, oocyte, embryo, and follicle assessment.
            WHO 2021 and ESHRE compliant analysis with enterprise-grade accuracy for modern fertility clinics.
          </p>

          <div className="flex justify-center space-x-4 mb-12">
            <SignedOut>
              <SignUpButton mode="modal">
                <button className="bg-indigo-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-indigo-700 transition-colors flex items-center space-x-2">
                  <span>Start Free Trial</span>
                  <ArrowRightIcon className="w-5 h-5" />
                </button>
              </SignUpButton>
              <Link href="/demo" className="border border-indigo-600 text-indigo-600 px-8 py-4 rounded-lg text-lg font-semibold hover:bg-indigo-50 transition-colors">
                View Demo
              </Link>
            </SignedOut>
            <SignedIn>
              <Link href="/analysis" className="bg-indigo-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-indigo-700 transition-colors flex items-center space-x-2">
                <span>Start Analysis</span>
                <ArrowRightIcon className="w-5 h-5" />
              </Link>
              <Link href="/dashboard" className="border border-indigo-600 text-indigo-600 px-8 py-4 rounded-lg text-lg font-semibold hover:bg-indigo-50 transition-colors">
                Dashboard
              </Link>
            </SignedIn>
          </div>

          {/* Trust Indicators */}
          <div className="flex justify-center items-center space-x-8 text-sm text-gray-500 mb-16">
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-green-500 rounded-full"></div>
              <span>WHO 2021 Compliant</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-green-500 rounded-full"></div>
              <span>ESHRE Guidelines</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-green-500 rounded-full"></div>
              <span>HIPAA Compliant</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-green-500 rounded-full"></div>
              <span>Enterprise Ready</span>
            </div>
          </div>
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-3 gap-8 mb-20">
          <div className="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition-shadow">
            <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
              <BeakerIcon className="w-6 h-6 text-blue-600" />
            </div>
            <h3 className="text-xl font-semibold mb-4">🧬 Sperm Analysis</h3>
            <p className="text-gray-600 mb-4">WHO 2021 compliant semen analysis with automated parameter assessment including concentration, motility, and morphology.</p>
            <ul className="text-sm text-gray-500 space-y-1">
              <li>• Concentration analysis (×10⁶/ml)</li>
              <li>• Progressive motility assessment</li>
              <li>• Normal morphology evaluation</li>
              <li>• Automated classification</li>
            </ul>
          </div>

          <div className="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition-shadow">
            <div className="w-12 h-12 bg-pink-100 rounded-lg flex items-center justify-center mb-4">
              <ChartBarIcon className="w-6 h-6 text-pink-600" />
            </div>
            <h3 className="text-xl font-semibold mb-4">🥚 Oocyte Assessment</h3>
            <p className="text-gray-600 mb-4">ESHRE guidelines-based maturity evaluation and quality grading for optimal IVF/ICSI outcomes.</p>
            <ul className="text-sm text-gray-500 space-y-1">
              <li>• Maturity stage identification</li>
              <li>• Cytoplasm quality assessment</li>
              <li>• Zona pellucida evaluation</li>
              <li>• Polar body analysis</li>
            </ul>
          </div>

          <div className="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition-shadow">
            <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
              <CpuChipIcon className="w-6 h-6 text-green-600" />
            </div>
            <h3 className="text-xl font-semibold mb-4">👶 Embryo Grading</h3>
            <p className="text-gray-600 mb-4">Gardner grading system for Day 3-6 embryo development assessment with implantation potential prediction.</p>
            <ul className="text-sm text-gray-500 space-y-1">
              <li>• Cell count and symmetry</li>
              <li>• Fragmentation analysis</li>
              <li>• Blastocyst expansion grading</li>
              <li>• ICM and TE assessment</li>
            </ul>
          </div>
        </div>

        {/* Pricing Section */}
        <div className="bg-gradient-to-r from-indigo-600 to-purple-600 rounded-2xl p-12 text-white mb-20">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold mb-4">Choose Your Plan</h2>
            <p className="text-xl opacity-90">Unlock the full potential of AI-powered reproductive medicine</p>
          </div>

          <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            {/* Professional Plan */}
            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-8 border border-white/20">
              <div className="text-center mb-6">
                <h3 className="text-2xl font-bold mb-2">Professional</h3>
                <div className="flex items-baseline justify-center mb-2">
                  <span className="text-4xl font-bold">₹299</span>
                  <span className="text-lg opacity-75 line-through ml-2">₹499</span>
                  <span className="text-sm opacity-75 ml-2">/month</span>
                </div>
                <p className="opacity-90">Perfect for individual practitioners</p>
              </div>
              <ul className="space-y-3 mb-8">
                <li className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                  <span>Unlimited image analysis</span>
                </li>
                <li className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                  <span>Advanced AI insights</span>
                </li>
                <li className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                  <span>Export reports (PDF)</span>
                </li>
                <li className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                  <span>Email support</span>
                </li>
              </ul>
              <SignedIn>
                <button
                  onClick={() => handleUpgrade('professional')}
                  className="w-full bg-white text-indigo-600 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors"
                >
                  Upgrade to Professional
                </button>
              </SignedIn>
              <SignedOut>
                <SignUpButton mode="modal">
                  <button className="w-full bg-white text-indigo-600 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors">
                    Start Free Trial
                  </button>
                </SignUpButton>
              </SignedOut>
            </div>

            {/* Enterprise Plan */}
            <div className="bg-white/20 backdrop-blur-sm rounded-xl p-8 border-2 border-yellow-400 relative">
              <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                <span className="bg-yellow-400 text-black px-4 py-1 rounded-full text-sm font-semibold">
                  Most Popular
                </span>
              </div>
              <div className="text-center mb-6">
                <h3 className="text-2xl font-bold mb-2">Enterprise</h3>
                <div className="flex items-baseline justify-center mb-2">
                  <span className="text-4xl font-bold">₹999</span>
                  <span className="text-lg opacity-75 line-through ml-2">₹1499</span>
                  <span className="text-sm opacity-75 ml-2">/month</span>
                </div>
                <p className="opacity-90">For large clinics and hospitals</p>
              </div>
              <ul className="space-y-3 mb-8">
                <li className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                  <span>Everything in Professional</span>
                </li>
                <li className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                  <span>Multi-user accounts</span>
                </li>
                <li className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                  <span>API integration</span>
                </li>
                <li className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                  <span>Priority support</span>
                </li>
              </ul>
              <SignedIn>
                <button
                  onClick={() => handleUpgrade('enterprise')}
                  className="w-full bg-yellow-400 text-black py-3 rounded-lg font-semibold hover:bg-yellow-300 transition-colors"
                >
                  Upgrade to Enterprise
                </button>
              </SignedIn>
              <SignedOut>
                <SignUpButton mode="modal">
                  <button className="w-full bg-yellow-400 text-black py-3 rounded-lg font-semibold hover:bg-yellow-300 transition-colors">
                    Start Free Trial
                  </button>
                </SignUpButton>
              </SignedOut>
            </div>
          </div>
        </div>

        {/* CTA Section */}
        <div className="bg-indigo-600 rounded-2xl p-12 text-center text-white">
          <h2 className="text-3xl font-bold mb-4">Ready to Transform Your Practice?</h2>
          <p className="text-xl mb-8 opacity-90">Join leading fertility clinics using AI-powered analysis for better patient outcomes.</p>
          <SignedOut>
            <SignUpButton mode="modal">
              <button className="bg-white text-indigo-600 px-8 py-4 rounded-lg text-lg font-semibold hover:bg-gray-100 transition-colors">
                Start Free Trial
              </button>
            </SignUpButton>
          </SignedOut>
          <SignedIn>
            <Link href="/analysis" className="bg-white text-indigo-600 px-8 py-4 rounded-lg text-lg font-semibold hover:bg-gray-100 transition-colors inline-block">
              Start Analyzing
            </Link>
          </SignedIn>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-6">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-lg">F</span>
                </div>
                <span className="text-xl font-bold">FertiVision</span>
              </div>
              <p className="text-gray-400">AI-Enhanced Reproductive Medicine Analysis Platform</p>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Product</h4>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="/analysis" className="hover:text-white">AI Analysis</Link></li>
                <li><Link href="/pricing" className="hover:text-white">Pricing</Link></li>
                <li><Link href="/demo" className="hover:text-white">Demo</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Company</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="mailto:support@greybrain.ai" className="hover:text-white">Support</a></li>
                <li><a href="mailto:sales@greybrain.ai" className="hover:text-white">Sales</a></li>
                <li><Link href="/docs" className="hover:text-white">Documentation</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Legal</h4>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="/privacy" className="hover:text-white">Privacy Policy</Link></li>
                <li><Link href="/terms" className="hover:text-white">Terms of Service</Link></li>
                <li><Link href="/compliance" className="hover:text-white">Compliance</Link></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>© 2025 FertiVision powered by AI | Made by greybrain.ai</p>
          </div>
        </div>
      </footer>

      {/* Payment Modal */}
      <PaymentModal
        isOpen={showPaymentModal}
        onClose={() => setShowPaymentModal(false)}
        selectedPlan={selectedPlan}
      />
    </div>
  );
}
