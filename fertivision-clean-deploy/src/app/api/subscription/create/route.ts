import { auth } from '@clerk/nextjs';
import { NextRequest, NextResponse } from 'next/server';
import { getUserByClerkId, createSubscription, updateUserSubscription } from '@/lib/db';
import { 
  createCustomer, 
  createSubscription as createRazorpaySubscription, 
  SUBSCRIPTION_PLANS,
  getPlanById 
} from '@/lib/razorpay';

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

    // Get request data
    const { planId, customerEmail, customerName } = await request.json();

    if (!planId) {
      return NextResponse.json({ 
        success: false, 
        error: 'Plan ID is required' 
      }, { status: 400 });
    }

    // Validate plan
    const plan = getPlanById(planId);
    if (!plan) {
      return NextResponse.json({ 
        success: false, 
        error: 'Invalid plan ID' 
      }, { status: 400 });
    }

    // Get user from database
    const user = await getUserByClerkId(userId);
    if (!user) {
      return NextResponse.json({ 
        success: false, 
        error: 'User not found' 
      }, { status: 404 });
    }

    // Handle free plan
    if (planId === 'free') {
      // Update user subscription to free
      await updateUserSubscription(user.id, 'free', 10);
      
      return NextResponse.json({
        success: true,
        message: 'Successfully switched to free plan',
        subscription: {
          id: 'free_plan',
          plan_id: 'free',
          status: 'active'
        }
      });
    }

    try {
      // Create Razorpay customer
      const customer = await createCustomer(
        customerEmail || user.email,
        customerName || user.full_name || 'User'
      );

      // Create Razorpay subscription
      const subscription = await createRazorpaySubscription(
        planId,
        customer.id
      );

      // Save subscription to database
      const savedSubscription = await createSubscription(
        user.id,
        planId,
        subscription.id
      );

      if (!savedSubscription) {
        console.error('Failed to save subscription to database');
        // Continue anyway, don't fail the request
      }

      return NextResponse.json({
        success: true,
        subscription: {
          id: subscription.id,
          plan_id: planId,
          status: subscription.status,
          customer_id: customer.id,
          short_url: subscription.short_url
        },
        customer: {
          id: customer.id,
          email: customer.email,
          name: customer.name
        }
      });

    } catch (razorpayError) {
      console.error('Razorpay error:', razorpayError);
      
      return NextResponse.json({
        success: false,
        error: 'Failed to create subscription. Please try again or contact support.'
      }, { status: 500 });
    }

  } catch (error) {
    console.error('Subscription creation error:', error);
    
    return NextResponse.json({
      success: false,
      error: error instanceof Error ? error.message : 'Internal server error'
    }, { status: 500 });
  }
}

// Get user's current subscription
export async function GET(request: NextRequest) {
  try {
    const { userId } = auth();
    if (!userId) {
      return NextResponse.json({ 
        success: false, 
        error: 'Authentication required' 
      }, { status: 401 });
    }

    const user = await getUserByClerkId(userId);
    if (!user) {
      return NextResponse.json({ 
        success: false, 
        error: 'User not found' 
      }, { status: 404 });
    }

    const currentPlan = getPlanById(user.subscription_plan);

    return NextResponse.json({
      success: true,
      subscription: {
        plan_id: user.subscription_plan,
        plan_name: currentPlan?.name || 'Unknown',
        analyses_used: user.analyses_used,
        analyses_limit: user.analyses_limit,
        price: currentPlan?.price || 0
      }
    });

  } catch (error) {
    console.error('Get subscription error:', error);
    
    return NextResponse.json({
      success: false,
      error: 'Internal server error'
    }, { status: 500 });
  }
}
