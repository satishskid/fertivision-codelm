import { auth, currentUser } from '@clerk/nextjs';
import { NextRequest, NextResponse } from 'next/server';
import { checkAIProviders } from '@/lib/analysis-engine';

// Check if user is admin
async function isAdmin(userId: string): Promise<boolean> {
  const user = await currentUser();
  if (!user) return false;
  
  const adminEmail = process.env.ADMIN_EMAIL;
  const adminUserId = process.env.ADMIN_CLERK_USER_ID;
  
  return user.emailAddresses[0]?.emailAddress === adminEmail || 
         userId === adminUserId;
}

export async function GET(request: NextRequest) {
  try {
    const { userId } = auth();
    if (!userId) {
      return NextResponse.json({ 
        success: false, 
        error: 'Authentication required' 
      }, { status: 401 });
    }

    if (!(await isAdmin(userId))) {
      return NextResponse.json({ 
        success: false, 
        error: 'Admin access required' 
      }, { status: 403 });
    }

    // Test AI providers
    const status = await checkAIProviders();

    return NextResponse.json({
      success: true,
      status,
      message: `Groq: ${status.groq ? 'Connected' : 'Failed'}, OpenRouter: ${status.openrouter ? 'Connected' : 'Failed'}`
    });

  } catch (error) {
    console.error('AI test error:', error);
    return NextResponse.json({
      success: false,
      error: 'Failed to test AI providers'
    }, { status: 500 });
  }
}
