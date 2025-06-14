import { NextRequest, NextResponse } from 'next/server';
import { auth } from '@clerk/nextjs/server';
import { createCustomBilling, getUserSubscription, getUsageStats } from '@/lib/api-billing';

// Admin-only endpoint for managing customer billing
export async function POST(request: NextRequest) {
  try {
    const { userId } = await auth();
    if (!userId) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    // Check if user is admin (you can implement your own admin check)
    // For now, we'll use a simple email check
    const adminEmails = ['satish@skids.health'];
    // In a real app, you'd get the user's email from Clerk
    // const user = await clerkClient.users.getUser(userId);
    // if (!adminEmails.includes(user.emailAddresses[0]?.emailAddress)) {
    //   return NextResponse.json({ error: 'Admin access required' }, { status: 403 });
    // }

    const { action, customerId, billingConfig } = await request.json();

    switch (action) {
      case 'create_custom_plan':
        if (!customerId || !billingConfig) {
          return NextResponse.json({ 
            error: 'Missing customerId or billingConfig' 
          }, { status: 400 });
        }

        const customSubscription = await createCustomBilling(customerId, billingConfig);
        
        return NextResponse.json({
          success: true,
          subscription: customSubscription,
          message: 'Custom billing plan created successfully'
        });

      case 'get_customer_usage':
        if (!customerId) {
          return NextResponse.json({ 
            error: 'Missing customerId' 
          }, { status: 400 });
        }

        const [usage, subscription] = await Promise.all([
          getUsageStats(customerId, 'month'),
          getUserSubscription(customerId)
        ]);

        return NextResponse.json({
          customerId,
          usage,
          subscription,
          billing: {
            currentCost: usage.totalCost,
            projectedMonthlyCost: usage.totalCost,
            lastBillingDate: subscription.startDate,
            nextBillingDate: subscription.endDate
          }
        });

      case 'update_billing_config':
        if (!customerId || !billingConfig) {
          return NextResponse.json({ 
            error: 'Missing customerId or billingConfig' 
          }, { status: 400 });
        }

        const updatedSubscription = await createCustomBilling(customerId, billingConfig);
        
        return NextResponse.json({
          success: true,
          subscription: updatedSubscription,
          message: 'Billing configuration updated successfully'
        });

      default:
        return NextResponse.json({ 
          error: 'Invalid action. Supported: create_custom_plan, get_customer_usage, update_billing_config' 
        }, { status: 400 });
    }

  } catch (error) {
    console.error('Admin Billing API Error:', error);
    return NextResponse.json({ 
      error: 'Internal server error' 
    }, { status: 500 });
  }
}

// Get all customers and their billing information
export async function GET(request: NextRequest) {
  try {
    const { userId } = await auth();
    if (!userId) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    // Check admin access (simplified for demo)
    // In production, implement proper admin role checking

    // Mock customer data - in production, this would come from your database
    const customers = [
      {
        userId: 'user_1',
        email: 'clinic@example.com',
        name: 'City Fertility Clinic',
        subscription: await getUserSubscription('user_1'),
        usage: await getUsageStats('user_1', 'month'),
        billing: {
          totalRevenue: 1245.50,
          lastPayment: '2024-01-15',
          paymentMethod: 'razorpay',
          status: 'active'
        }
      },
      {
        userId: 'user_2',
        email: 'dr.smith@hospital.com',
        name: 'Dr. Smith Medical Center',
        subscription: await getUserSubscription('user_2'),
        usage: await getUsageStats('user_2', 'month'),
        billing: {
          totalRevenue: 624.75,
          lastPayment: '2024-01-10',
          paymentMethod: 'razorpay',
          status: 'active'
        }
      }
    ];

    const summary = {
      totalCustomers: customers.length,
      totalRevenue: customers.reduce((sum, c) => sum + c.billing.totalRevenue, 0),
      totalApiCalls: customers.reduce((sum, c) => sum + c.usage.totalRequests, 0),
      averageRevenuePerCustomer: customers.reduce((sum, c) => sum + c.billing.totalRevenue, 0) / customers.length
    };

    return NextResponse.json({
      customers,
      summary,
      billingPeriod: 'monthly',
      lastUpdated: new Date().toISOString()
    });

  } catch (error) {
    console.error('Admin Billing GET Error:', error);
    return NextResponse.json({ 
      error: 'Internal server error' 
    }, { status: 500 });
  }
}
