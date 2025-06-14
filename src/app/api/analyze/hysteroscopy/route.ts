import { auth } from '@clerk/nextjs';
import { NextRequest, NextResponse } from 'next/server';
import { getUserByClerkId, saveAnalysis, incrementUserUsage } from '@/lib/db';
import { analyzeImage } from '@/lib/analysis-engine';
import { canPerformAnalysis } from '@/lib/razorpay';

export async function POST(request: NextRequest) {
  try {
    const { userId } = auth();
    if (!userId) {
      return NextResponse.json({ success: false, error: 'Authentication required' }, { status: 401 });
    }

    const user = await getUserByClerkId(userId);
    if (!user) {
      return NextResponse.json({ success: false, error: 'User not found' }, { status: 404 });
    }

    if (!canPerformAnalysis(user.subscription_plan, user.analyses_used, user.analyses_limit)) {
      return NextResponse.json({ success: false, error: 'Usage limit exceeded. Please upgrade your plan.' }, { status: 403 });
    }

    const formData = await request.formData();
    const image = formData.get('image') as File;
    const patientId = formData.get('patient_id') as string;
    const caseId = formData.get('case_id') as string;
    const additionalNotes = formData.get('additional_notes') as string;

    if (!image || !image.type.startsWith('image/')) {
      return NextResponse.json({ success: false, error: 'Valid image file required' }, { status: 400 });
    }

    const analysisResult = await analyzeImage(image, 'hysteroscopy', patientId, caseId, additionalNotes);

    if (!analysisResult.success) {
      return NextResponse.json({ success: false, error: analysisResult.error || 'Analysis failed' }, { status: 500 });
    }

    const savedAnalysis = await saveAnalysis(
      user.id, 'hysteroscopy', {
        classification: analysisResult.classification,
        confidence: analysisResult.confidence,
        parameters: analysisResult.parameters,
        technical_details: analysisResult.technical_details,
        clinical_recommendations: analysisResult.clinical_recommendations
      }, undefined, image.name, patientId, caseId, analysisResult.confidence, analysisResult.processing_time
    );

    await incrementUserUsage(user.id);

    return NextResponse.json({
      success: true,
      analysis_id: savedAnalysis?.id.toString() || `temp_${Date.now()}`,
      analysis_type: 'hysteroscopy',
      classification: analysisResult.classification,
      confidence: analysisResult.confidence,
      parameters: analysisResult.parameters,
      technical_details: analysisResult.technical_details,
      clinical_recommendations: analysisResult.clinical_recommendations,
      timestamp: new Date().toISOString(),
      processing_time: analysisResult.processing_time,
      patient_id: patientId,
      case_id: caseId
    });

  } catch (error) {
    console.error('Hysteroscopy analysis error:', error);
    return NextResponse.json({ success: false, error: 'Internal server error' }, { status: 500 });
  }
}

export async function GET() {
  return NextResponse.json({
    success: true,
    endpoint: 'hysteroscopy_analysis',
    status: 'operational',
    timestamp: new Date().toISOString()
  });
}
