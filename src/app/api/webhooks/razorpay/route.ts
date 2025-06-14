import { NextRequest, NextResponse } from 'next/server';
import { verifyWebhookSignature, webhookHandlers, getPlanById } from '@/lib/razorpay';
import { updateUserSubscription, updateSubscriptionStatus } from '@/lib/db';
import { sql } from '@vercel/postgres';

export async function POST(request: NextRequest) {
  try {
    // Get the raw body and signature
    const body = await request.text();
    const signature = request.headers.get('x-razorpay-signature');

    if (!signature) {
      console.error('Missing Razorpay signature');
      return NextResponse.json({ error: 'Missing signature' }, { status: 400 });
    }

    // Verify webhook signature
    const isValid = verifyWebhookSignature(body, signature);
    if (!isValid) {
      console.error('Invalid Razorpay webhook signature');
      return NextResponse.json({ error: 'Invalid signature' }, { status: 400 });
    }

    // Parse the webhook payload
    const event = JSON.parse(body);
    const eventType = event.event;
    const payload = event.payload;

    console.log(`Received Razorpay webhook: ${eventType}`);

    // Handle different webhook events
    switch (eventType) {
      case 'subscription.activated':
        await handleSubscriptionActivated(payload);
        break;
        
      case 'subscription.charged':
        await handleSubscriptionCharged(payload);
        break;
        
      case 'subscription.cancelled':
        await handleSubscriptionCancelled(payload);
        break;
        
      case 'subscription.paused':
        await handleSubscriptionPaused(payload);
        break;
        
      case 'subscription.resumed':
        await handleSubscriptionResumed(payload);
        break;
        
      case 'payment.failed':
        await handlePaymentFailed(payload);
        break;
        
      default:
        console.log(`Unhandled webhook event: ${eventType}`);
    }

    return NextResponse.json({ success: true });

  } catch (error) {
    console.error('Webhook processing error:', error);
    return NextResponse.json({ 
      error: 'Webhook processing failed' 
    }, { status: 500 });
  }
}

async function handleSubscriptionActivated(payload: any) {
  try {
    const subscription = payload.subscription.entity;
    const planId = subscription.notes?.plan_type;
    
    if (!planId) {
      console.error('No plan_type in subscription notes');
      return;
    }

    const plan = getPlanById(planId);
    if (!plan) {
      console.error(`Invalid plan ID: ${planId}`);
      return;
    }

    // Find user by subscription ID
    const result = await sql`
      SELECT u.id, u.clerk_user_id 
      FROM users u 
      JOIN subscriptions s ON u.id = s.user_id 
      WHERE s.razorpay_subscription_id = ${subscription.id}
    `;

    if (result.rows.length === 0) {
      console.error(`User not found for subscription: ${subscription.id}`);
      return;
    }

    const user = result.rows[0];

    // Update user subscription
    await updateUserSubscription(
      user.id,
      planId as 'free' | 'professional' | 'enterprise',
      plan.analyses_limit
    );

    // Update subscription status
    await updateSubscriptionStatus(
      user.id,
      'active',
      new Date(subscription.current_start * 1000),
      new Date(subscription.current_end * 1000)
    );

    console.log(`Subscription activated for user ${user.clerk_user_id}: ${planId}`);

  } catch (error) {
    console.error('Error handling subscription activation:', error);
  }
}

async function handleSubscriptionCharged(payload: any) {
  try {
    const payment = payload.payment.entity;
    const subscription = payload.subscription.entity;

    console.log(`Payment charged: ${payment.id} for subscription: ${subscription.id}`);

    // Update subscription period if needed
    if (subscription.current_start && subscription.current_end) {
      const result = await sql`
        SELECT s.id 
        FROM subscriptions s 
        WHERE s.razorpay_subscription_id = ${subscription.id}
      `;

      if (result.rows.length > 0) {
        await updateSubscriptionStatus(
          result.rows[0].id,
          'active',
          new Date(subscription.current_start * 1000),
          new Date(subscription.current_end * 1000)
        );
      }
    }

    // Reset usage count for the new period
    await sql`
      UPDATE users 
      SET analyses_used = 0, updated_at = NOW()
      WHERE id IN (
        SELECT user_id FROM subscriptions 
        WHERE razorpay_subscription_id = ${subscription.id}
      )
    `;

  } catch (error) {
    console.error('Error handling subscription charge:', error);
  }
}

async function handleSubscriptionCancelled(payload: any) {
  try {
    const subscription = payload.subscription.entity;

    // Find user and update to free plan
    const result = await sql`
      SELECT u.id, u.clerk_user_id 
      FROM users u 
      JOIN subscriptions s ON u.id = s.user_id 
      WHERE s.razorpay_subscription_id = ${subscription.id}
    `;

    if (result.rows.length > 0) {
      const user = result.rows[0];

      // Update to free plan
      await updateUserSubscription(user.id, 'free', 10);

      // Update subscription status
      const subscriptionResult = await sql`
        SELECT id FROM subscriptions 
        WHERE razorpay_subscription_id = ${subscription.id}
      `;

      if (subscriptionResult.rows.length > 0) {
        await updateSubscriptionStatus(
          subscriptionResult.rows[0].id,
          'cancelled'
        );
      }

      console.log(`Subscription cancelled for user ${user.clerk_user_id}`);
    }

  } catch (error) {
    console.error('Error handling subscription cancellation:', error);
  }
}

async function handleSubscriptionPaused(payload: any) {
  try {
    const subscription = payload.subscription.entity;

    const result = await sql`
      SELECT id FROM subscriptions 
      WHERE razorpay_subscription_id = ${subscription.id}
    `;

    if (result.rows.length > 0) {
      await updateSubscriptionStatus(
        result.rows[0].id,
        'paused'
      );
    }

    console.log(`Subscription paused: ${subscription.id}`);

  } catch (error) {
    console.error('Error handling subscription pause:', error);
  }
}

async function handleSubscriptionResumed(payload: any) {
  try {
    const subscription = payload.subscription.entity;

    const result = await sql`
      SELECT id FROM subscriptions 
      WHERE razorpay_subscription_id = ${subscription.id}
    `;

    if (result.rows.length > 0) {
      await updateSubscriptionStatus(
        result.rows[0].id,
        'active',
        new Date(subscription.current_start * 1000),
        new Date(subscription.current_end * 1000)
      );
    }

    console.log(`Subscription resumed: ${subscription.id}`);

  } catch (error) {
    console.error('Error handling subscription resume:', error);
  }
}

async function handlePaymentFailed(payload: any) {
  try {
    const payment = payload.payment.entity;
    
    console.log(`Payment failed: ${payment.id}`);
    
    // You might want to send notification emails here
    // or implement retry logic

  } catch (error) {
    console.error('Error handling payment failure:', error);
  }
}

// Health check
export async function GET() {
  return NextResponse.json({
    success: true,
    endpoint: 'razorpay_webhook',
    status: 'operational',
    timestamp: new Date().toISOString()
  });
}
