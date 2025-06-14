import { auth } from '@clerk/nextjs';
import { NextRequest, NextResponse } from 'next/server';
import { getUserByClerkId, saveAnalysis, incrementUserUsage } from '@/lib/db';
import { analyzeImage } from '@/lib/analysis-engine';
import { canPerformAnalysis } from '@/lib/razorpay';

export async function POST(request: NextRequest) {
  try {
    // Check authentication
    const { userId } = auth();
    if (!userId) {
      return NextResponse.json({ 
        success: false, 
        error: 'Authentication required' 
      }, { status: 401 });
    }

    // Get user from database
    const user = await getUserByClerkId(userId);
    if (!user) {
      return NextResponse.json({ 
        success: false, 
        error: 'User not found' 
      }, { status: 404 });
    }

    // Check usage limits
    if (!canPerformAnalysis(user.subscription_plan, user.analyses_used, user.analyses_limit)) {
      return NextResponse.json({ 
        success: false, 
        error: 'Usage limit exceeded. Please upgrade your plan to continue.' 
      }, { status: 403 });
    }

    // Parse form data
    const formData = await request.formData();
    const image = formData.get('image') as File;
    const patientId = formData.get('patient_id') as string;
    const caseId = formData.get('case_id') as string;
    const additionalNotes = formData.get('additional_notes') as string;

    if (!image) {
      return NextResponse.json({ 
        success: false, 
        error: 'No image file provided' 
      }, { status: 400 });
    }

    // Validate image file
    if (!image.type.startsWith('image/')) {
      return NextResponse.json({ 
        success: false, 
        error: 'Invalid file type. Please upload an image file.' 
      }, { status: 400 });
    }

    if (image.size > 50 * 1024 * 1024) { // 50MB limit
      return NextResponse.json({ 
        success: false, 
        error: 'File too large. Maximum size is 50MB.' 
      }, { status: 400 });
    }

    // Perform AI analysis
    const analysisResult = await analyzeImage(
      image,
      'sperm',
      patientId,
      caseId,
      additionalNotes
    );

    if (!analysisResult.success) {
      return NextResponse.json({
        success: false,
        error: analysisResult.error || 'Analysis failed'
      }, { status: 500 });
    }

    // Save analysis to database
    const savedAnalysis = await saveAnalysis(
      user.id,
      'sperm',
      {
        classification: analysisResult.classification,
        confidence: analysisResult.confidence,
        parameters: analysisResult.parameters,
        technical_details: analysisResult.technical_details,
        clinical_recommendations: analysisResult.clinical_recommendations
      },
      undefined, // image_url - we're not storing images for privacy
      image.name,
      patientId,
      caseId,
      analysisResult.confidence,
      analysisResult.processing_time
    );

    if (!savedAnalysis) {
      console.error('Failed to save analysis to database');
      // Continue anyway, don't fail the request
    }

    // Increment user usage count
    await incrementUserUsage(user.id);

    // Return successful analysis result
    return NextResponse.json({
      success: true,
      analysis_id: savedAnalysis?.id.toString() || `temp_${Date.now()}`,
      analysis_type: 'sperm',
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
    console.error('Sperm analysis API error:', error);
    
    return NextResponse.json({
      success: false,
      error: error instanceof Error ? error.message : 'Internal server error'
    }, { status: 500 });
  }
}

// Health check endpoint
export async function GET() {
  return NextResponse.json({
    success: true,
    endpoint: 'sperm_analysis',
    status: 'operational',
    timestamp: new Date().toISOString()
  });
}
