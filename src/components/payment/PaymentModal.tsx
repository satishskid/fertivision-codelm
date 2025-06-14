'use client';

import { useState } from 'react';
import { useUser } from '@clerk/nextjs';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  QrCode, 
  CreditCard, 
  Check, 
  Star, 
  Zap,
  Shield,
  Users,
  Clock,
  Download
} from 'lucide-react';

interface PaymentModalProps {
  isOpen: boolean;
  onClose: () => void;
  selectedPlan?: 'professional' | 'enterprise';
}

interface PricingPlan {
  id: string;
  name: string;
  price: number;
  originalPrice?: number;
  description: string;
  features: string[];
  popular?: boolean;
  icon: React.ReactNode;
}

const pricingPlans: PricingPlan[] = [
  {
    id: 'professional',
    name: 'Professional',
    price: 299,
    originalPrice: 499,
    description: 'Perfect for individual practitioners and small clinics',
    icon: <Star className="h-5 w-5" />,
    features: [
      'Unlimited image analysis',
      'Advanced AI insights',
      'Export reports (PDF)',
      'Email support',
      'Mobile app access',
      'Basic analytics dashboard'
    ]
  },
  {
    id: 'enterprise',
    name: 'Enterprise',
    price: 999,
    originalPrice: 1499,
    description: 'Comprehensive solution for large clinics and hospitals',
    icon: <Shield className="h-5 w-5" />,
    popular: true,
    features: [
      'Everything in Professional',
      'Multi-user accounts',
      'API integration',
      'Custom branding',
      'Priority support',
      'Advanced analytics',
      'Data export/import',
      'Training sessions'
    ]
  }
];

export default function PaymentModal({ isOpen, onClose, selectedPlan }: PaymentModalProps) {
  const { user } = useUser();
  const [currentPlan, setCurrentPlan] = useState(selectedPlan || 'professional');
  const [paymentMethod, setPaymentMethod] = useState<'qr' | 'card'>('qr');
  const [paymentStatus, setPaymentStatus] = useState<'pending' | 'processing' | 'success' | 'failed'>('pending');

  const plan = pricingPlans.find(p => p.id === currentPlan);

  const handlePaymentConfirmation = () => {
    setPaymentStatus('processing');
    
    // Simulate payment processing
    setTimeout(() => {
      setPaymentStatus('success');
      
      // Auto-close after success
      setTimeout(() => {
        onClose();
        setPaymentStatus('pending');
      }, 3000);
    }, 2000);
  };

  const renderPaymentSuccess = () => (
    <div className="text-center space-y-4 py-8">
      <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto">
        <Check className="h-8 w-8 text-green-600" />
      </div>
      <div>
        <h3 className="text-xl font-semibold text-green-600">Payment Successful!</h3>
        <p className="text-muted-foreground">
          Welcome to FertiVision {plan?.name} plan
        </p>
      </div>
      <div className="bg-green-50 p-4 rounded-lg">
        <p className="text-sm text-green-800">
          Your account has been upgraded. You now have access to all {plan?.name} features.
        </p>
      </div>
    </div>
  );

  const renderQRPayment = () => (
    <div className="space-y-6">
      <div className="text-center">
        <h3 className="text-lg font-semibold mb-2">Scan QR Code to Pay</h3>
        <p className="text-muted-foreground text-sm">
          Use any UPI app to scan and pay ₹{plan?.price}
        </p>
      </div>

      <Card className="bg-gradient-to-br from-blue-50 to-purple-50">
        <CardContent className="p-6">
          <div className="flex flex-col items-center space-y-4">
            {/* QR Code - Your Razorpay QR Code */}
            <div className="bg-white p-4 rounded-lg shadow-lg border">
              <img
                src="/razorpay-qr.svg"
                alt="Razorpay QR Code for Payment"
                className="w-48 h-48"
              />
            </div>
            
            <div className="text-center space-y-2">
              <div className="flex items-center justify-center space-x-2">
                <span className="text-sm font-medium">Powered by</span>
                <span className="font-bold text-blue-600">Razorpay</span>
              </div>
              <p className="text-xs text-muted-foreground">
                SKIDS TECHNOLOGY PRIVATE LIMITED
              </p>
            </div>

            <div className="flex items-center space-x-4 text-sm text-muted-foreground">
              <div className="flex items-center space-x-1">
                <img src="/api/placeholder/24/24" alt="GPay" className="w-6 h-6" />
                <span>GPay</span>
              </div>
              <div className="flex items-center space-x-1">
                <img src="/api/placeholder/24/24" alt="PhonePe" className="w-6 h-6" />
                <span>PhonePe</span>
              </div>
              <div className="flex items-center space-x-1">
                <img src="/api/placeholder/24/24" alt="Paytm" className="w-6 h-6" />
                <span>Paytm</span>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      <div className="bg-yellow-50 p-4 rounded-lg border border-yellow-200">
        <div className="flex items-start space-x-2">
          <Clock className="h-4 w-4 text-yellow-600 mt-0.5" />
          <div className="text-sm">
            <p className="font-medium text-yellow-800">Payment Instructions:</p>
            <ol className="list-decimal list-inside text-yellow-700 mt-1 space-y-1">
              <li>Open any UPI app (GPay, PhonePe, Paytm)</li>
              <li>Scan the QR code above</li>
              <li>Verify amount: ₹{plan?.price}</li>
              <li>Complete the payment</li>
              <li>Click "I've Paid" button below</li>
            </ol>
          </div>
        </div>
      </div>

      <Button 
        onClick={handlePaymentConfirmation} 
        className="w-full"
        size="lg"
      >
        I've Completed the Payment
      </Button>
    </div>
  );

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            {plan?.icon}
            Upgrade to {plan?.name}
          </DialogTitle>
          <DialogDescription>
            Choose your payment method and complete the subscription
          </DialogDescription>
        </DialogHeader>

        {paymentStatus === 'success' ? (
          renderPaymentSuccess()
        ) : (
          <div className="space-y-6">
            {/* Plan Selection */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {pricingPlans.map((planOption) => (
                <Card 
                  key={planOption.id}
                  className={`cursor-pointer transition-all ${
                    currentPlan === planOption.id 
                      ? 'ring-2 ring-blue-500 bg-blue-50' 
                      : 'hover:shadow-md'
                  } ${planOption.popular ? 'border-purple-200' : ''}`}
                  onClick={() => setCurrentPlan(planOption.id)}
                >
                  <CardHeader className="pb-3">
                    <div className="flex items-center justify-between">
                      <CardTitle className="flex items-center gap-2 text-lg">
                        {planOption.icon}
                        {planOption.name}
                      </CardTitle>
                      {planOption.popular && (
                        <Badge className="bg-purple-100 text-purple-800">Popular</Badge>
                      )}
                    </div>
                    <div className="flex items-baseline gap-2">
                      <span className="text-2xl font-bold">₹{planOption.price}</span>
                      {planOption.originalPrice && (
                        <span className="text-sm text-muted-foreground line-through">
                          ₹{planOption.originalPrice}
                        </span>
                      )}
                      <span className="text-sm text-muted-foreground">/month</span>
                    </div>
                    <CardDescription>{planOption.description}</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <ul className="space-y-2">
                      {planOption.features.slice(0, 4).map((feature, index) => (
                        <li key={index} className="flex items-center gap-2 text-sm">
                          <Check className="h-3 w-3 text-green-600" />
                          {feature}
                        </li>
                      ))}
                      {planOption.features.length > 4 && (
                        <li className="text-sm text-muted-foreground">
                          +{planOption.features.length - 4} more features
                        </li>
                      )}
                    </ul>
                  </CardContent>
                </Card>
              ))}
            </div>

            {/* Payment Method Selection */}
            <Tabs value={paymentMethod} onValueChange={(value) => setPaymentMethod(value as 'qr' | 'card')}>
              <TabsList className="grid w-full grid-cols-2">
                <TabsTrigger value="qr" className="flex items-center gap-2">
                  <QrCode className="h-4 w-4" />
                  UPI/QR Code
                </TabsTrigger>
                <TabsTrigger value="card" className="flex items-center gap-2">
                  <CreditCard className="h-4 w-4" />
                  Card Payment
                </TabsTrigger>
              </TabsList>

              <TabsContent value="qr" className="mt-6">
                {paymentStatus === 'processing' ? (
                  <div className="text-center py-8">
                    <div className="animate-spin w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full mx-auto mb-4"></div>
                    <p className="text-muted-foreground">Verifying your payment...</p>
                  </div>
                ) : (
                  renderQRPayment()
                )}
              </TabsContent>

              <TabsContent value="card" className="mt-6">
                <div className="text-center py-8">
                  <CreditCard className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                  <p className="text-muted-foreground">
                    Card payment integration coming soon!
                  </p>
                  <p className="text-sm text-muted-foreground mt-2">
                    Please use UPI/QR code payment for now.
                  </p>
                </div>
              </TabsContent>
            </Tabs>

            {/* Order Summary */}
            <Card className="bg-gray-50">
              <CardHeader className="pb-3">
                <CardTitle className="text-lg">Order Summary</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex justify-between">
                  <span>FertiVision {plan?.name}</span>
                  <span>₹{plan?.price}</span>
                </div>
                {plan?.originalPrice && (
                  <div className="flex justify-between text-green-600">
                    <span>Discount</span>
                    <span>-₹{plan.originalPrice - plan.price}</span>
                  </div>
                )}
                <div className="border-t pt-3 flex justify-between font-semibold">
                  <span>Total</span>
                  <span>₹{plan?.price}</span>
                </div>
                <p className="text-xs text-muted-foreground">
                  * All prices are in Indian Rupees (INR)
                </p>
              </CardContent>
            </Card>
          </div>
        )}
      </DialogContent>
    </Dialog>
  );
}
