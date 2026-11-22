"use client";

import React, { useState } from "react";
import "./globals.css";
import Navbar from "@/components/Navbar";
import NavigationDrawer from "@/components/NavigationDrawer";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const [drawerOpen, setDrawerOpen] = useState(false);

  return (
    <html lang="en">
      <head>
        <title>FreshWatch — Supermarket Expiry & Wastage Prediction System</title>
        <meta
          name="description"
          content="Enterprise AI-powered supermarket inventory management platform to predict expiry risk, dynamic markdowns, and food wastage reduction."
        />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </head>
      <body className="min-h-screen bg-slate-50 text-slate-800 antialiased selection:bg-emerald-100 selection:text-emerald-900">
        {/* Collapsible Navigation Drawer (Hidden by default, opened via Hamburger ☰) */}
        <NavigationDrawer isOpen={drawerOpen} onClose={() => setDrawerOpen(false)} />

        <div className="flex min-h-screen flex-col w-full">
          {/* Main Top Header */}
          <Navbar onOpenDrawer={() => setDrawerOpen(true)} />

          {/* Full-width content area - No permanent sidebar! */}
          <main className="flex-1 w-full">{children}</main>

          {/* Footer */}
          <footer className="border-t border-slate-200 bg-white py-6 text-center text-xs text-slate-500">
            <div className="mx-auto max-w-7xl px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
              <div className="flex items-center gap-2">
                <span className="font-semibold text-slate-800">FreshWatch</span>
                <span>— Predict. Prevent. Save.</span>
              </div>
              <div className="flex items-center gap-4 text-slate-600">
                <span>Random Forest Classifier (95.6% F1)</span>
                <span>•</span>
                <span>Groq AI Integration</span>
                <span>•</span>
                <span>Next.js & Prisma</span>
              </div>
            </div>
          </footer>
        </div>
      </body>
    </html>
  );
}
