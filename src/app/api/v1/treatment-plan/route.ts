import { NextRequest, NextResponse } from 'next/server';
import { auth } from '@clerk/nextjs/server';
import { trackAPIUsage, checkAPILimits, getUserSubscription } from '@/lib/api-billing';
import { ClinicalAI, PatientMedicalHistory, CurrentTestResults, PatientDemographics } from '@/lib/clinical-ai';

export async function POST(request: NextRequest) {
  try {
    // Authentication and billing check
    const { userId } = await auth();
    if (!userId) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const subscription = await getUserSubscription(userId);
    const canUseAPI = await checkAPILimits(userId, subscription);
    
    if (!canUseAPI.allowed) {
      return NextResponse.json({ 
        error: 'API limit exceeded', 
        message: canUseAPI.message,
        usage: canUseAPI.usage 
      }, { status: 429 });
    }

    // Parse and validate input data
    const { medicalHistory, testResults, demographics, options } = await request.json();
    
    // Validate required fields
    const validation = validateTreatmentPlanInput(medicalHistory, testResults, demographics);
    if (!validation.valid) {
      return NextResponse.json({ 
        error: 'Invalid input data', 
        details: validation.errors 
      }, { status: 400 });
    }

    // HIPAA compliance check
    if (!options?.consentGiven) {
      return NextResponse.json({ 
        error: 'Patient consent required for clinical decision support' 
      }, { status: 400 });
    }

    // Track API usage
    await trackAPIUsage(userId, 'treatment-plan', {
      timestamp: new Date(),
      requestSize: JSON.stringify({ medicalHistory, testResults, demographics }).length,
      userAgent: request.headers.get('user-agent') || 'unknown'
    });

    // Generate AI-powered treatment recommendation
    const startTime = Date.now();
    const treatmentPlan = await ClinicalAI.generateTreatmentPlan(
      medicalHistory as PatientMedicalHistory,
      testResults as CurrentTestResults,
      demographics as PatientDemographics
    );
    const processingTime = (Date.now() - startTime) / 1000;

    // Add clinical warnings and disclaimers
    const response = {
      success: true,
      treatmentPlan,
      clinicalWarnings: [
        'This recommendation is for clinical decision support only',
        'Final treatment decisions must be made by qualified medical professionals',
        'Consider patient-specific factors not captured in this analysis',
        'Regular monitoring and adjustment may be required'
      ],
      disclaimer: 'This AI-generated recommendation should be used in conjunction with clinical judgment and is not a substitute for professional medical advice.',
      processingTime,
      timestamp: new Date().toISOString(),
      usage: {
        remaining: canUseAPI.remaining - 1,
        resetDate: canUseAPI.resetDate
      }
    };

    return NextResponse.json(response);

  } catch (error) {
    console.error('Treatment Plan API Error:', error);
    return NextResponse.json({ 
      error: 'Internal server error',
      message: 'Unable to generate treatment plan. Please try again.'
    }, { status: 500 });
  }
}

export async function GET(request: NextRequest) {
  return NextResponse.json({
    service: 'Treatment Planning API',
    version: '1.0.0',
    description: 'AI-powered personalized IVF/ICSI treatment protocol recommendations',
    capabilities: [
      'Personalized protocol selection',
      'Medication dosage optimization',
      'Success probability prediction',
      'Risk assessment and mitigation',
      'Evidence-based recommendations'
    ],
    inputRequirements: {
      medicalHistory: {
        previousCycles: 'Array of previous IVF/ICSI cycles with outcomes',
        diagnoses: 'Primary and secondary fertility diagnoses',
        medications: 'Previous medication responses and allergies',
        surgicalHistory: 'Relevant surgical procedures'
      },
      testResults: {
        hormones: 'AMH, FSH, LH, E2, TSH, Prolactin levels',
        ultrasound: 'AFC, ovarian volume, endometrial assessment',
        genetics: 'Optional genetic testing results'
      },
      demographics: {
        age: 'Patient age in years',
        BMI: 'Body mass index',
        lifestyle: 'Smoking, alcohol, exercise, stress factors'
      }
    },
    outputProvides: {
      protocol: 'Recommended stimulation protocol with rationale',
      medications: 'Specific drug types, dosages, and timing',
      monitoring: 'Surveillance schedule and adjustment criteria',
      predictions: 'Success rates and expected outcomes',
      alternatives: 'Alternative treatment options',
      warnings: 'Clinical alerts and contraindications'
    },
    compliance: [
      'HIPAA compliant data handling',
      'Evidence-based recommendations',
      'Clinical decision support standards',
      'Medical device software guidelines'
    ],
    pricing: {
      professional: '₹25 per analysis',
      enterprise: '₹15 per analysis',
      custom: 'Volume-based pricing available'
    }
  });
}

function validateTreatmentPlanInput(medicalHistory: any, testResults: any, demographics: any) {
  const errors: string[] = [];

  // Validate demographics
  if (!demographics) {
    errors.push('Demographics data is required');
  } else {
    if (!demographics.age || demographics.age < 18 || demographics.age > 55) {
      errors.push('Valid patient age (18-55) is required');
    }
    if (!demographics.BMI || demographics.BMI < 15 || demographics.BMI > 50) {
      errors.push('Valid BMI (15-50) is required');
    }
  }

  // Validate test results
  if (!testResults) {
    errors.push('Test results are required');
  } else {
    if (!testResults.hormones) {
      errors.push('Hormonal test results are required');
    } else {
      if (!testResults.hormones.AMH || testResults.hormones.AMH < 0) {
        errors.push('Valid AMH level is required');
      }
      if (!testResults.hormones.FSH || testResults.hormones.FSH < 0) {
        errors.push('Valid FSH level is required');
      }
    }
    
    if (!testResults.ultrasound) {
      errors.push('Ultrasound findings are required');
    } else {
      if (!testResults.ultrasound.antrallFollicleCount || testResults.ultrasound.antrallFollicleCount < 0) {
        errors.push('Valid antral follicle count is required');
      }
    }
  }

  // Validate medical history
  if (!medicalHistory) {
    errors.push('Medical history is required');
  } else {
    if (!medicalHistory.diagnoses || !medicalHistory.diagnoses.primary) {
      errors.push('Primary fertility diagnosis is required');
    }
    if (!Array.isArray(medicalHistory.previousCycles)) {
      errors.push('Previous cycles must be an array (can be empty)');
    }
    if (!Array.isArray(medicalHistory.allergies)) {
      errors.push('Allergies must be an array (can be empty)');
    }
  }

  return {
    valid: errors.length === 0,
    errors
  };
}
