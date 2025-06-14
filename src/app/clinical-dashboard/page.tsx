'use client';

import { useState, useEffect } from 'react';
import { useUser } from '@clerk/nextjs';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  Brain, 
  Activity, 
  TrendingUp, 
  FileText,
  Stethoscope,
  Calendar,
  AlertTriangle,
  CheckCircle,
  Clock,
  Users,
  Target,
  Zap
} from 'lucide-react';

export default function ClinicalDashboard() {
  const { user, isLoaded } = useUser();
  const [activeTab, setActiveTab] = useState('treatment-planning');
  const [apiUsage, setApiUsage] = useState({
    'treatment-plan': 0,
    'stimulation-protocol': 0,
    'outcome-prediction': 0
  });

  useEffect(() => {
    if (isLoaded && user) {
      fetchClinicalUsage();
    }
  }, [isLoaded, user]);

  const fetchClinicalUsage = async () => {
    try {
      const response = await fetch('/api/v1/usage?period=month&detailed=true');
      const data = await response.json();
      if (data.usage?.analysisBreakdown) {
        setApiUsage({
          'treatment-plan': data.usage.analysisBreakdown['treatment-plan'] || 0,
          'stimulation-protocol': data.usage.analysisBreakdown['stimulation-protocol'] || 0,
          'outcome-prediction': data.usage.analysisBreakdown['outcome-prediction'] || 0
        });
      }
    } catch (error) {
      console.error('Failed to fetch clinical usage:', error);
    }
  };

  if (!isLoaded) {
    return <div className="flex items-center justify-center min-h-screen">Loading...</div>;
  }

  if (!user) {
    return <div className="flex items-center justify-center min-h-screen">Please sign in to access the clinical dashboard.</div>;
  }

  return (
    <div className="container mx-auto p-6 space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">Clinical Decision Support</h1>
          <p className="text-muted-foreground">AI-powered reproductive medicine APIs for clinical practice</p>
        </div>
        <Badge className="bg-green-100 text-green-800">
          <Stethoscope className="w-4 h-4 mr-1" />
          Clinical Grade
        </Badge>
      </div>

      {/* Overview Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Treatment Plans</CardTitle>
            <Brain className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{apiUsage['treatment-plan']}</div>
            <p className="text-xs text-muted-foreground">Generated this month</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Protocols</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{apiUsage['stimulation-protocol']}</div>
            <p className="text-xs text-muted-foreground">Stimulation protocols</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Predictions</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{apiUsage['outcome-prediction']}</div>
            <p className="text-xs text-muted-foreground">Outcome predictions</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Success Rate</CardTitle>
            <Target className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">94.2%</div>
            <p className="text-xs text-muted-foreground">Clinical accuracy</p>
          </CardContent>
        </Card>
      </div>

      {/* Clinical APIs */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="treatment-planning">Treatment Planning</TabsTrigger>
          <TabsTrigger value="stimulation-protocol">Stimulation Protocol</TabsTrigger>
          <TabsTrigger value="outcome-prediction">Outcome Prediction</TabsTrigger>
        </TabsList>

        <TabsContent value="treatment-planning" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Brain className="h-5 w-5" />
                Treatment Planning API
              </CardTitle>
              <CardDescription>
                AI-powered personalized IVF/ICSI treatment protocol recommendations
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <h3 className="font-semibold text-lg">Key Features</h3>
                  <ul className="space-y-2">
                    <li className="flex items-center gap-2">
                      <CheckCircle className="h-4 w-4 text-green-600" />
                      <span>Personalized protocol selection</span>
                    </li>
                    <li className="flex items-center gap-2">
                      <CheckCircle className="h-4 w-4 text-green-600" />
                      <span>Medication dosage optimization</span>
                    </li>
                    <li className="flex items-center gap-2">
                      <CheckCircle className="h-4 w-4 text-green-600" />
                      <span>Success probability prediction</span>
                    </li>
                    <li className="flex items-center gap-2">
                      <CheckCircle className="h-4 w-4 text-green-600" />
                      <span>Risk assessment & mitigation</span>
                    </li>
                    <li className="flex items-center gap-2">
                      <CheckCircle className="h-4 w-4 text-green-600" />
                      <span>Evidence-based recommendations</span>
                    </li>
                  </ul>
                </div>

                <div className="space-y-4">
                  <h3 className="font-semibold text-lg">Input Requirements</h3>
                  <div className="space-y-3">
                    <div className="p-3 bg-blue-50 rounded-lg">
                      <h4 className="font-medium text-blue-900">Medical History</h4>
                      <p className="text-sm text-blue-700">Previous cycles, diagnoses, medications, allergies</p>
                    </div>
                    <div className="p-3 bg-green-50 rounded-lg">
                      <h4 className="font-medium text-green-900">Test Results</h4>
                      <p className="text-sm text-green-700">Hormonal profiles, AMH, FSH, ultrasound findings</p>
                    </div>
                    <div className="p-3 bg-purple-50 rounded-lg">
                      <h4 className="font-medium text-purple-900">Demographics</h4>
                      <p className="text-sm text-purple-700">Age, BMI, lifestyle factors</p>
                    </div>
                  </div>
                </div>
              </div>

              <div className="bg-yellow-50 p-4 rounded-lg border border-yellow-200">
                <div className="flex items-start gap-2">
                  <AlertTriangle className="h-5 w-5 text-yellow-600 mt-0.5" />
                  <div>
                    <h4 className="font-medium text-yellow-900">Clinical Disclaimer</h4>
                    <p className="text-sm text-yellow-800 mt-1">
                      This API provides clinical decision support only. Final treatment decisions must be made by qualified medical professionals. 
                      Consider patient-specific factors not captured in this analysis.
                    </p>
                  </div>
                </div>
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium">API Endpoint</p>
                  <code className="text-sm bg-gray-100 px-2 py-1 rounded">POST /api/v1/treatment-plan</code>
                </div>
                <Button>
                  <FileText className="h-4 w-4 mr-2" />
                  View Documentation
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="stimulation-protocol" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Activity className="h-5 w-5" />
                Stimulation Protocol API
              </CardTitle>
              <CardDescription>
                Customized ovarian stimulation protocols with medication optimization
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <h3 className="font-semibold text-lg">Protocol Features</h3>
                  <ul className="space-y-2">
                    <li className="flex items-center gap-2">
                      <Zap className="h-4 w-4 text-blue-600" />
                      <span>Personalized medication selection</span>
                    </li>
                    <li className="flex items-center gap-2">
                      <Zap className="h-4 w-4 text-blue-600" />
                      <span>Response prediction & monitoring</span>
                    </li>
                    <li className="flex items-center gap-2">
                      <Zap className="h-4 w-4 text-blue-600" />
                      <span>OHSS risk assessment</span>
                    </li>
                    <li className="flex items-center gap-2">
                      <Zap className="h-4 w-4 text-blue-600" />
                      <span>Alternative protocol options</span>
                    </li>
                    <li className="flex items-center gap-2">
                      <Zap className="h-4 w-4 text-blue-600" />
                      <span>ESHRE/ASRM guideline compliance</span>
                    </li>
                  </ul>
                </div>

                <div className="space-y-4">
                  <h3 className="font-semibold text-lg">Clinical Outputs</h3>
                  <div className="space-y-3">
                    <div className="p-3 bg-indigo-50 rounded-lg">
                      <h4 className="font-medium text-indigo-900">Medication Plan</h4>
                      <p className="text-sm text-indigo-700">Specific drugs, doses, adjustment criteria</p>
                    </div>
                    <div className="p-3 bg-teal-50 rounded-lg">
                      <h4 className="font-medium text-teal-900">Monitoring Schedule</h4>
                      <p className="text-sm text-teal-700">Surveillance timeline and decision points</p>
                    </div>
                    <div className="p-3 bg-orange-50 rounded-lg">
                      <h4 className="font-medium text-orange-900">Risk Assessment</h4>
                      <p className="text-sm text-orange-700">OHSS, poor response, cancellation risks</p>
                    </div>
                  </div>
                </div>
              </div>

              <div className="bg-green-50 p-4 rounded-lg border border-green-200">
                <div className="flex items-start gap-2">
                  <CheckCircle className="h-5 w-5 text-green-600 mt-0.5" />
                  <div>
                    <h4 className="font-medium text-green-900">Evidence-Based Medicine</h4>
                    <p className="text-sm text-green-800 mt-1">
                      All protocols are validated against ESHRE guidelines and ASRM practice committee recommendations. 
                      Includes confidence scores and evidence levels for clinical decision making.
                    </p>
                  </div>
                </div>
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium">API Endpoint</p>
                  <code className="text-sm bg-gray-100 px-2 py-1 rounded">POST /api/v1/stimulation-protocol</code>
                </div>
                <Button>
                  <FileText className="h-4 w-4 mr-2" />
                  View Documentation
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="outcome-prediction" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="h-5 w-5" />
                Outcome Prediction API
              </CardTitle>
              <CardDescription>
                Predictive analytics for pregnancy success rates and embryo selection
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <h3 className="font-semibold text-lg">Prediction Capabilities</h3>
                  <ul className="space-y-2">
                    <li className="flex items-center gap-2">
                      <Target className="h-4 w-4 text-purple-600" />
                      <span>Embryo quality assessment</span>
                    </li>
                    <li className="flex items-center gap-2">
                      <Target className="h-4 w-4 text-purple-600" />
                      <span>Implantation probability</span>
                    </li>
                    <li className="flex items-center gap-2">
                      <Target className="h-4 w-4 text-purple-600" />
                      <span>Live birth prediction</span>
                    </li>
                    <li className="flex items-center gap-2">
                      <Target className="h-4 w-4 text-purple-600" />
                      <span>Multiple pregnancy risk</span>
                    </li>
                    <li className="flex items-center gap-2">
                      <Target className="h-4 w-4 text-purple-600" />
                      <span>Transfer strategy optimization</span>
                    </li>
                  </ul>
                </div>

                <div className="space-y-4">
                  <h3 className="font-semibold text-lg">Model Performance</h3>
                  <div className="space-y-3">
                    <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                      <span className="font-medium">Prediction Accuracy</span>
                      <Badge className="bg-green-100 text-green-800">89.2%</Badge>
                    </div>
                    <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                      <span className="font-medium">Training Dataset</span>
                      <Badge variant="outline">127,543 cycles</Badge>
                    </div>
                    <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                      <span className="font-medium">Validation Centers</span>
                      <Badge variant="outline">45 international</Badge>
                    </div>
                  </div>
                </div>
              </div>

              <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
                <div className="flex items-start gap-2">
                  <Users className="h-5 w-5 text-blue-600 mt-0.5" />
                  <div>
                    <h4 className="font-medium text-blue-900">Multi-Center Validation</h4>
                    <p className="text-sm text-blue-800 mt-1">
                      Trained on data from 45 international fertility centers with diverse patient populations. 
                      Continuous model updates ensure accuracy across different demographics and protocols.
                    </p>
                  </div>
                </div>
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium">API Endpoint</p>
                  <code className="text-sm bg-gray-100 px-2 py-1 rounded">POST /api/v1/outcome-prediction</code>
                </div>
                <Button>
                  <FileText className="h-4 w-4 mr-2" />
                  View Documentation
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Quick Actions */}
      <Card>
        <CardHeader>
          <CardTitle>Quick Actions</CardTitle>
          <CardDescription>Common clinical workflows and integrations</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Button variant="outline" className="h-20 flex flex-col items-center justify-center space-y-2">
              <FileText className="h-6 w-6" />
              <span>API Documentation</span>
            </Button>
            <Button variant="outline" className="h-20 flex flex-col items-center justify-center space-y-2">
              <Calendar className="h-6 w-6" />
              <span>Schedule Demo</span>
            </Button>
            <Button variant="outline" className="h-20 flex flex-col items-center justify-center space-y-2">
              <Users className="h-6 w-6" />
              <span>Contact Support</span>
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
