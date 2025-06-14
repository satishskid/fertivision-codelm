import type { Metadata } from "next";
import { ClerkProvider } from '@clerk/nextjs';
import { Inter } from 'next/font/google';
import { Toaster } from 'react-hot-toast';
import "./globals.css";

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: "FertiVision - AI-Enhanced Reproductive Medicine",
  description: "Advanced AI analysis for reproductive medicine with WHO 2021 and ESHRE compliance",
  keywords: "fertility, IVF, AI, sperm analysis, embryo grading, reproductive medicine",
  authors: [{ name: "greybrain.ai" }],
  openGraph: {
    title: "FertiVision - AI-Enhanced Reproductive Medicine",
    description: "Advanced AI analysis for reproductive medicine",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <ClerkProvider>
      <html lang="en">
        <head>
          <script src="https://checkout.razorpay.com/v1/checkout.js" async></script>
        </head>
        <body className={`${inter.className} antialiased`}>
          {children}
          <Toaster
            position="top-right"
            toastOptions={{
              duration: 4000,
              style: {
                background: '#363636',
                color: '#fff',
              },
            }}
          />
        </body>
      </html>
    </ClerkProvider>
  );
}
