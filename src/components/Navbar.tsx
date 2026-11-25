"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import {
  Menu,
  Search,
  Leaf,
  Bell,
  Sparkles,
  Bot,
  User,
  CheckCircle2,
  AlertCircle,
  HelpCircle,
} from "lucide-react";

interface NavbarProps {
  onOpenDrawer: () => void;
}

export default function Navbar({ onOpenDrawer }: NavbarProps) {
  const router = useRouter();
  const [searchQuery, setSearchQuery] = useState("");
  const [activeAlertsCount, setActiveAlertsCount] = useState(0);
  const [systemOnline, setSystemOnline] = useState(true);

  useEffect(() => {
    // Fetch live alert count & status
    async function checkStatus() {
      try {
        const res = await fetch("/api/alerts");
        if (res.ok) {
          const data = await res.json();
          setActiveAlertsCount(data.alerts?.length || 0);
        }
      } catch (e) {
        // quiet
      }
    }
    checkStatus();
  }, []);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      router.push(`/inventory?search=${encodeURIComponent(searchQuery.trim())}`);
    }
  };

  return (
    <header className="sticky top-0 z-40 w-full border-b border-slate-200 bg-white/95 backdrop-blur supports-[backdrop-filter]:bg-white/80">
      <div className="flex h-16 items-center justify-between px-4 sm:px-6 lg:px-8">
        {/* Left: Hamburger Button (CRITICAL: ☰ icon) & Brand */}
        <div className="flex items-center gap-3">
          <button
            onClick={onOpenDrawer}
            className="flex h-10 w-10 items-center justify-center rounded-lg border border-slate-200 bg-white text-slate-700 shadow-xs hover:bg-emerald-50 hover:text-emerald-800 hover:border-emerald-300 transition-colors focus:outline-none focus:ring-2 focus:ring-emerald-500"
            title="Open navigation menu (☰)"
            aria-label="Open Navigation Drawer"
          >
            <Menu className="h-5 w-5" />
          </button>

          <Link href="/" className="flex items-center gap-2.5 group">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-emerald-800 text-white shadow-xs group-hover:bg-emerald-700 transition-colors">
              <Leaf className="h-5 w-5 text-emerald-300" />
            </div>
            <div className="hidden sm:block">
              <div className="flex items-center gap-1.5">
                <span className="font-bold text-lg text-slate-900 tracking-tight">Inventory Analysis</span>
                <span className="text-[11px] font-medium text-emerald-800 bg-emerald-100 px-1.5 py-0.2 rounded-full border border-emerald-200">
                  AI Retail
                </span>
              </div>
            </div>
          </Link>
        </div>

        {/* Center: Search Inventory Input */}
        <div className="flex-1 max-w-md mx-4 hidden md:block">
          <form onSubmit={handleSearchSubmit} className="relative">
            <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search products, SKUs, or pulses..."
              className="w-full rounded-full border border-slate-200 bg-slate-50/80 py-2 pl-10 pr-4 text-sm text-slate-800 placeholder-slate-400 transition-all focus:border-emerald-500 focus:bg-white focus:outline-none focus:ring-2 focus:ring-emerald-500/20"
            />
          </form>
        </div>

        {/* Right: Actions, Status & User Menu */}
        <div className="flex items-center gap-2 sm:gap-3">
          {/* System Status Pill */}
          <div className="hidden lg:flex items-center gap-2 px-3 py-1.5 rounded-full border border-slate-200 bg-slate-50 text-xs font-medium text-slate-700">
            <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
            <span>RF ML & Database Active</span>
          </div>

          {/* Quick Voice / Chat Assistant button */}
          <Link
            href="/chat"
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-emerald-200 bg-emerald-50 text-emerald-800 text-xs font-semibold hover:bg-emerald-100 transition-colors shadow-2xs"
            title="Groq AI Assistant"
          >
            <Bot className="h-4 w-4 text-emerald-600" />
            <span className="hidden sm:inline">AI Assistant</span>
          </Link>

          {/* Alert Notification Bell */}
          <Link
            href="/#alerts-section"
            className="relative flex h-9 w-9 items-center justify-center rounded-lg border border-slate-200 bg-white text-slate-600 hover:bg-slate-100 hover:text-slate-900 transition-colors"
            title={`${activeAlertsCount} active alerts`}
          >
            <Bell className="h-4 w-4" />
            {activeAlertsCount > 0 && (
              <span className="absolute -top-1 -right-1 flex h-4 w-4 items-center justify-center rounded-full bg-red-500 text-[10px] font-bold text-white shadow-xs">
                {activeAlertsCount}
              </span>
            )}
          </Link>

          {/* User Profile avatar */}
          <div className="flex items-center gap-2 pl-2 border-l border-slate-200">
            <div className="flex h-9 w-9 items-center justify-center rounded-full bg-slate-800 text-white font-semibold text-xs shadow-xs">
              SM
            </div>
            <div className="hidden xl:block text-left">
              <span className="block text-xs font-semibold text-slate-900 leading-tight">Store Manager</span>
              <span className="block text-[11px] text-slate-500 leading-tight">Supermarket HQ</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
