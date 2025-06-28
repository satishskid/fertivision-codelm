import Link from 'next/link';
import { ArrowRightIcon, BeakerIcon, ChartBarIcon, CpuChipIcon } from '@heroicons/react/24/outline';

export default function DemoPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      {/* Navigation */}
      <nav className="flex justify-between items-center p-6 max-w-7xl mx-auto">
        <div className="flex items-center space-x-2">
          <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center">
            <span className="text-white font-bold text-lg">F</span>
          </div>
          <h1 className="text-2xl font-bold text-indigo-900">FertiVision</h1>
          <span className="bg-yellow-100 text-yellow-800 px-2 py-1 rounded-full text-xs font-medium ml-2">
            DEMO MODE
          </span>
        </div>
        <div className="flex items-center space-x-4">
          <Link href="/demo/analysis" className="text-indigo-600 hover:text-indigo-800 font-medium">
            Try Analysis
          </Link>
          <Link href="/demo/pricing" className="text-indigo-600 hover:text-indigo-800 font-medium">
            Pricing
          </Link>
          <Link href="/" className="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700 transition-colors font-medium">
            Full Version
          </Link>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-6 py-20">
        <div className="text-center">
          <div className="bg-yellow-100 border border-yellow-300 rounded-lg p-4 mb-8 max-w-2xl mx-auto">
            <h2 className="text-lg font-semibold text-yellow-800 mb-2">🚀 Demo Mode Active</h2>
            <p className="text-yellow-700">
              This is a demonstration version of FertiVision Cloud SaaS. 
              All features are functional but using simulated data for testing purposes.
            </p>
          </div>

          <h1 className="text-6xl font-bold text-gray-900 mb-6">
            AI-Enhanced
            <span className="text-indigo-600 block">Reproductive Medicine</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto leading-relaxed">
            Advanced AI analysis for sperm, oocyte, embryo, and follicle assessment. 
            WHO 2021 and ESHRE compliant analysis with enterprise-grade accuracy for modern fertility clinics.
          </p>
          
          <div className="flex justify-center space-x-4 mb-12">
            <Link href="/demo/analysis" className="bg-indigo-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-indigo-700 transition-colors flex items-center space-x-2">
              <span>Try Demo Analysis</span>
              <ArrowRightIcon className="w-5 h-5" />
            </Link>
            <Link href="/demo/pricing" className="border border-indigo-600 text-indigo-600 px-8 py-4 rounded-lg text-lg font-semibold hover:bg-indigo-50 transition-colors">
              View Pricing
            </Link>
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

        {/* Additional Features */}
        <div className="grid md:grid-cols-2 gap-8 mb-20">
          <div className="bg-white p-8 rounded-xl shadow-lg">
            <h3 className="text-xl font-semibold mb-4">🔬 Follicle Counting</h3>
            <p className="text-gray-600 mb-4">Automated antral follicle count (AFC) for ovarian reserve assessment and PCOS screening.</p>
            <ul className="text-sm text-gray-500 space-y-1">
              <li>• Automated follicle detection</li>
              <li>• Size distribution analysis</li>
              <li>• Ovarian reserve classification</li>
              <li>• PCOS indicators</li>
            </ul>
          </div>
          
          <div className="bg-white p-8 rounded-xl shadow-lg">
            <h3 className="text-xl font-semibold mb-4">🏥 Hysteroscopy Analysis</h3>
            <p className="text-gray-600 mb-4">Endometrial morphology and pathology analysis for fertility treatment planning and optimization.</p>
            <ul className="text-sm text-gray-500 space-y-1">
              <li>• Endometrial thickness measurement</li>
              <li>• Pattern recognition</li>
              <li>• Pathology detection</li>
              <li>• Receptivity assessment</li>
            </ul>
          </div>
        </div>

        {/* Demo Features */}
        <div className="bg-indigo-600 rounded-2xl p-12 text-center text-white mb-20">
          <h2 className="text-3xl font-bold mb-4">Try the Demo Features</h2>
          <p className="text-xl mb-8 opacity-90">Experience the full FertiVision platform with simulated data and real AI processing.</p>
          <div className="grid md:grid-cols-3 gap-6">
            <Link href="/demo/analysis" className="bg-white text-indigo-600 p-6 rounded-lg hover:bg-gray-100 transition-colors">
              <h3 className="font-semibold mb-2">🔬 AI Analysis Demo</h3>
              <p className="text-sm">Upload sample images and see real AI analysis results</p>
            </Link>
            <Link href="/demo/pricing" className="bg-white text-indigo-600 p-6 rounded-lg hover:bg-gray-100 transition-colors">
              <h3 className="font-semibold mb-2">💳 Pricing Demo</h3>
              <p className="text-sm">Explore subscription plans and payment flow</p>
            </Link>
            <Link href="/demo/dashboard" className="bg-white text-indigo-600 p-6 rounded-lg hover:bg-gray-100 transition-colors">
              <h3 className="font-semibold mb-2">📊 Dashboard Demo</h3>
              <p className="text-sm">See user analytics and usage tracking</p>
            </Link>
          </div>
        </div>

        {/* Setup Instructions */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-8">
          <h3 className="text-xl font-semibold text-blue-900 mb-4">🚀 Ready for Production?</h3>
          <div className="text-blue-800 space-y-3">
            <p><strong>Step 1:</strong> Get your Clerk API keys from <a href="https://clerk.com" className="underline">clerk.com</a></p>
            <p><strong>Step 2:</strong> Get your Razorpay keys from <a href="https://razorpay.com" className="underline">razorpay.com</a></p>
            <p><strong>Step 3:</strong> Get AI provider keys from <a href="https://console.groq.com" className="underline">Groq</a> and <a href="https://openrouter.ai" className="underline">OpenRouter</a></p>
            <p><strong>Step 4:</strong> Update your <code className="bg-blue-100 px-2 py-1 rounded">.env.local</code> file with real credentials</p>
            <p><strong>Step 5:</strong> Deploy to Vercel with <code className="bg-blue-100 px-2 py-1 rounded">vercel --prod</code></p>
          </div>
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
              <h4 className="font-semibold mb-4">Demo</h4>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="/demo/analysis" className="hover:text-white">Try Analysis</Link></li>
                <li><Link href="/demo/pricing" className="hover:text-white">Pricing</Link></li>
                <li><Link href="/demo/dashboard" className="hover:text-white">Dashboard</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Production</h4>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="/" className="hover:text-white">Full Version</Link></li>
                <li><Link href="/admin" className="hover:text-white">Admin Panel</Link></li>
                <li><a href="https://clerk.com" className="hover:text-white">Get Clerk Keys</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Support</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="mailto:support@greybrain.ai" className="hover:text-white">Contact Support</a></li>
                <li><a href="mailto:sales@greybrain.ai" className="hover:text-white">Sales Inquiry</a></li>
                <li><Link href="/docs" className="hover:text-white">Documentation</Link></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>© 2025 FertiVision powered by AI | Made by greybrain.ai</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
