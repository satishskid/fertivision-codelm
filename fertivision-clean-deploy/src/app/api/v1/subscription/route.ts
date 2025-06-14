import { NextRequest, NextResponse } from 'next/server';
import { auth } from '@clerk/nextjs/server';
import { getUserSubscription, updateUserSubscription, createCustomBilling } from '@/lib/api-billing';

export async function GET(request: NextRequest) {
  try {
    const { userId } = await auth();
    if (!userId) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const subscription = await getUserSubscription(userId);
    
    return NextResponse.json({
      subscription,
      availablePlans: {
        free: {
          name: 'Free',
          price: 0,
          requests: 100,
          features: ['Basic AI Analysis', 'Standard Support']
        },
        professional: {
          name: 'Professional',
          price: 299,
          requests: 5000,
          features: ['Advanced AI Analysis', 'Priority Support', 'Usage Analytics']
        },
        enterprise: {
          name: 'Enterprise',
          price: 999,
          requests: 50000,
          features: ['Premium AI Analysis', '24/7 Support', 'Custom Integration']
        },
        custom: {
          name: 'Custom',
          price: 'Variable',
          requests: 'Custom',
          features: ['Everything in Enterprise', 'Custom Billing', 'Dedicated Support']
        }
      }
    });

  } catch (error) {
    console.error('Subscription API Error:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

export async function POST(request: NextRequest) {
  try {
    const { userId } = await auth();
    if (!userId) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const { plan, customConfig } = await request.json();
    
    if (!plan || !['professional', 'enterprise', 'custom'].includes(plan)) {
      return NextResponse.json({ 
        error: 'Invalid plan. Must be: professional, enterprise, or custom' 
      }, { status: 400 });
    }

    let subscription;
    
    if (plan === 'custom') {
      if (!customConfig) {
        return NextResponse.json({ 
          error: 'Custom configuration required for custom plan' 
        }, { status: 400 });
      }
      
      subscription = await createCustomBilling(userId, customConfig);
    } else {
      subscription = await updateUserSubscription(userId, plan);
    }

    return NextResponse.json({
      success: true,
      subscription,
      message: `Successfully upgraded to ${plan} plan`
    });

  } catch (error) {
    console.error('Subscription Update Error:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
