import { NextRequest, NextResponse } from 'next/server';
import { auth } from '@clerk/nextjs/server';
import { getUsageStats, getUserSubscription } from '@/lib/api-billing';

export async function GET(request: NextRequest) {
  try {
    const { userId } = await auth();
    if (!userId) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const { searchParams } = new URL(request.url);
    const period = searchParams.get('period') as 'hour' | 'day' | 'month' | 'year' || 'month';
    const detailed = searchParams.get('detailed') === 'true';

    const [usage, subscription] = await Promise.all([
      getUsageStats(userId, period),
      getUserSubscription(userId)
    ]);

    const response = {
      usage,
      subscription: {
        plan: subscription.plan,
        limits: subscription.limits,
        pricing: subscription.pricing,
        status: subscription.status,
        endDate: subscription.endDate
      },
      billing: {
        currentPeriodCost: usage.totalCost,
        estimatedMonthlyCost: period === 'month' ? usage.totalCost : usage.totalCost * (30 / getDaysInPeriod(period)),
        nextBillingDate: subscription.endDate
      }
    };

    if (detailed) {
      // Add more detailed analytics for enterprise users
      return NextResponse.json({
        ...response,
        analytics: {
          successRate: usage.totalRequests > 0 ? (usage.successfulRequests / usage.totalRequests) * 100 : 0,
          averageRequestSize: 0, // Would calculate from actual data
          peakUsageHours: [], // Would analyze hourly patterns
          costTrends: [], // Would show cost trends over time
          apiPerformance: {
            averageResponseTime: usage.averageProcessingTime,
            errorRate: usage.totalRequests > 0 ? (usage.failedRequests / usage.totalRequests) * 100 : 0
          }
        }
      });
    }

    return NextResponse.json(response);

  } catch (error) {
    console.error('Usage API Error:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

function getDaysInPeriod(period: string): number {
  switch (period) {
    case 'hour': return 1/24;
    case 'day': return 1;
    case 'month': return 30;
    case 'year': return 365;
    default: return 30;
  }
}
