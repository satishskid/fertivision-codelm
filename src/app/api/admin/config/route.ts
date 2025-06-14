import { auth, currentUser } from '@clerk/nextjs';
import { NextRequest, NextResponse } from 'next/server';
import { getAppConfig, setAppConfig } from '@/lib/db';

// Check if user is admin
async function isAdmin(userId: string): Promise<boolean> {
  const user = await currentUser();
  if (!user) return false;
  
  // Check against environment variables
  const adminEmail = process.env.ADMIN_EMAIL;
  const adminUserId = process.env.ADMIN_CLERK_USER_ID;
  
  return user.emailAddresses[0]?.emailAddress === adminEmail || 
         userId === adminUserId;
}

// Get all configurations
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

    // Define all configurable keys
    const configKeys = [
      { key: 'groq_api_key', description: 'Groq API Key for AI analysis', type: 'password' },
      { key: 'openrouter_api_key', description: 'OpenRouter API Key for AI analysis', type: 'password' },
      { key: 'razorpay_key_id', description: 'Razorpay Key ID for payments', type: 'text' },
      { key: 'razorpay_key_secret', description: 'Razorpay Key Secret for payments', type: 'password' },
      { key: 'razorpay_webhook_secret', description: 'Razorpay Webhook Secret', type: 'password' },
      { key: 'support_email', description: 'Support email address', type: 'text' },
      { key: 'admin_email', description: 'Admin email address', type: 'text' },
      { key: 'app_name', description: 'Application name', type: 'text' },
      { key: 'smtp_host', description: 'SMTP host for email notifications', type: 'text' },
      { key: 'smtp_port', description: 'SMTP port', type: 'text' },
      { key: 'smtp_user', description: 'SMTP username', type: 'text' },
      { key: 'smtp_pass', description: 'SMTP password', type: 'password' }
    ];

    // Get current values for all keys
    const configs = await Promise.all(
      configKeys.map(async (config) => ({
        ...config,
        value: await getAppConfig(config.key) || ''
      }))
    );

    return NextResponse.json({
      success: true,
      configs
    });

  } catch (error) {
    console.error('Get config error:', error);
    return NextResponse.json({
      success: false,
      error: 'Internal server error'
    }, { status: 500 });
  }
}

// Set configuration
export async function POST(request: NextRequest) {
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

    const { key, value } = await request.json();

    if (!key) {
      return NextResponse.json({ 
        success: false, 
        error: 'Configuration key is required' 
      }, { status: 400 });
    }

    // Validate key
    const allowedKeys = [
      'groq_api_key',
      'openrouter_api_key', 
      'razorpay_key_id',
      'razorpay_key_secret',
      'razorpay_webhook_secret',
      'support_email',
      'admin_email',
      'app_name',
      'smtp_host',
      'smtp_port',
      'smtp_user',
      'smtp_pass'
    ];

    if (!allowedKeys.includes(key)) {
      return NextResponse.json({ 
        success: false, 
        error: 'Invalid configuration key' 
      }, { status: 400 });
    }

    // Save configuration
    const success = await setAppConfig(key, value || '', `Updated by admin ${userId}`);

    if (!success) {
      return NextResponse.json({ 
        success: false, 
        error: 'Failed to save configuration' 
      }, { status: 500 });
    }

    // Also update environment variables for immediate effect
    process.env[key.toUpperCase()] = value;

    return NextResponse.json({
      success: true,
      message: 'Configuration saved successfully'
    });

  } catch (error) {
    console.error('Set config error:', error);
    return NextResponse.json({
      success: false,
      error: 'Internal server error'
    }, { status: 500 });
  }
}
