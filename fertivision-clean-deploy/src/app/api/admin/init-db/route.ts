import { auth, currentUser } from '@clerk/nextjs';
import { NextRequest, NextResponse } from 'next/server';
import { initializeDatabase } from '@/lib/db';

// Check if user is admin
async function isAdmin(userId: string): Promise<boolean> {
  const user = await currentUser();
  if (!user) return false;
  
  const adminEmail = process.env.ADMIN_EMAIL;
  const adminUserId = process.env.ADMIN_CLERK_USER_ID;
  
  return user.emailAddresses[0]?.emailAddress === adminEmail || 
         userId === adminUserId;
}

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

    // Initialize database
    const success = await initializeDatabase();

    if (success) {
      return NextResponse.json({
        success: true,
        message: 'Database initialized successfully'
      });
    } else {
      return NextResponse.json({
        success: false,
        error: 'Failed to initialize database'
      }, { status: 500 });
    }

  } catch (error) {
    console.error('Database initialization error:', error);
    return NextResponse.json({
      success: false,
      error: 'Failed to initialize database'
    }, { status: 500 });
  }
}
