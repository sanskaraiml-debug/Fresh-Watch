"use client";

import React, { useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  Boxes,
  Sparkles,
  Tag,
  SlidersHorizontal,
  BarChart3,
  Bot,
  BrainCircuit,
  Settings,
  X,
  Leaf,
  ChevronRight,
  TrendingUp,
} from "lucide-react";

interface NavigationDrawerProps {
  isOpen: boolean;
  onClose: () => void;
}

export const NAV_ITEMS = [
  {
    name: "Dashboard",
    href: "/",
    icon: LayoutDashboard,
    badge: null,
    desc: "Overview & Real-time KPIs",
  },
  {
    name: "Inventory Management",
    href: "/inventory",
    icon: Boxes,
    badge: "40 SKUs",
    desc: "Track & manage stock items",
  },
  {
    name: "AI Expiry Prediction",
    href: "/predictions",
    icon: Sparkles,
    badge: "ML Powered",
    desc: "Random Forest wastage forecast",
  },
  {
    name: "Dynamic Pricing Advisor",
    href: "/pricing",
    icon: Tag,
    badge: "Smart Markdowns",
    desc: "Intelligent discount engine",
  },
  {
    name: "Single Item Simulator",
    href: "/simulator",
    icon: SlidersHorizontal,
    badge: "What-If",
    desc: "Interactive scenario sandbox",
  },
  {
    name: "Analytics & Reports",
    href: "/reports",
    icon: BarChart3,
    badge: "CSV / Print",
    desc: "Audits & financial summaries",
  },
  {
    name: "Groq AI Assistant",
    href: "/chat",
    icon: Bot,
    badge: "Multilingual",
    desc: "Conversational & calling intelligence",
  },
  {
    name: "Model Insights",
    href: "/model-insights",
    icon: BrainCircuit,
    badge: "95.6% Acc",
    desc: "Feature importance & metrics",
  },
  {
    name: "Settings",
    href: "/settings",
    icon: Settings,
    badge: null,
    desc: "Store config & thresholds",
  },
];

export default function NavigationDrawer({ isOpen, onClose }: NavigationDrawerProps) {
  const pathname = usePathname();

  // Close on Escape key
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape" && isOpen) {
        onClose();
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [isOpen, onClose]);

  // Prevent background scroll when drawer is open
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "unset";
    }
    return () => {
      document.body.style.overflow = "unset";
    };
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex">
      {/* Backdrop overlay */}
      <div
        className="fixed inset-0 bg-black/50 backdrop-blur-sm transition-opacity duration-300 ease-out"
        onClick={onClose}
        aria-hidden="true"
      />

      {/* Slide-out drawer - hidden by default, slides in smoothly from left */}
      <div
        className="relative z-50 flex h-full w-full max-w-xs flex-col bg-white shadow-2xl border-r border-slate-200 transition-transform duration-300 ease-out animate-slide-in-left"
        role="dialog"
        aria-modal="true"
        aria-label="FreshWatch Navigation Menu"
      >
        {/* Drawer Header */}
        <div className="flex items-center justify-between px-6 py-5 border-b border-emerald-100 bg-emerald-900 text-white">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-800 text-emerald-300 border border-emerald-700/60 shadow-inner">
              <Leaf className="h-6 w-6 text-emerald-400" />
            </div>
            <div>
              <div className="flex items-center gap-1.5">
                <span className="font-bold text-lg tracking-tight text-white">FreshWatch</span>
                <span className="text-xs px-1.5 py-0.5 rounded bg-emerald-700/80 text-emerald-200 font-mono">v2.0</span>
              </div>
              <p className="text-xs text-emerald-200/80 font-normal">Supermarket Intelligence</p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="rounded-lg p-2 text-emerald-200 hover:bg-emerald-800 hover:text-white transition-colors"
            title="Close navigation (Esc)"
            aria-label="Close menu"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Navigation Items List */}
        <div className="flex-1 overflow-y-auto px-4 py-4 space-y-1 scrollbar-thin">
          <div className="px-2 pb-2 text-[11px] font-semibold uppercase tracking-wider text-slate-500">
            System Modules
          </div>

          {NAV_ITEMS.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href;

            return (
              <Link
                key={item.href}
                href={item.href}
                onClick={onClose}
                className={`group flex items-center justify-between px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all ${
                  isActive
                    ? "bg-emerald-50 text-emerald-900 border border-emerald-200/80 shadow-sm"
                    : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
                }`}
              >
                <div className="flex items-center gap-3 min-w-0">
                  <div
                    className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-lg transition-colors ${
                      isActive
                        ? "bg-emerald-600 text-white shadow-sm"
                        : "bg-slate-100 text-slate-500 group-hover:bg-slate-200 group-hover:text-slate-700"
                    }`}
                  >
                    <Icon className="h-4 w-4" />
                  </div>
                  <div className="truncate text-left">
                    <span className="block truncate">{item.name}</span>
                    <span className="block text-[11px] font-normal text-slate-500 truncate">
                      {item.desc}
                    </span>
                  </div>
                </div>

                {item.badge ? (
                  <span
                    className={`ml-2 text-[10px] font-semibold px-2 py-0.5 rounded-full shrink-0 ${
                      isActive
                        ? "bg-emerald-200 text-emerald-800"
                        : "bg-slate-200 text-slate-600 group-hover:bg-slate-300"
                    }`}
                  >
                    {item.badge}
                  </span>
                ) : (
                  <ChevronRight
                    className={`h-4 w-4 text-slate-400 opacity-0 group-hover:opacity-100 transition-opacity ${
                      isActive ? "opacity-100 text-emerald-600" : ""
                    }`}
                  />
                )}
              </Link>
            );
          })}
        </div>

        {/* Drawer Footer with Quick ML Health Badge */}
        <div className="border-t border-slate-200 p-4 bg-slate-50/80">
          <div className="rounded-xl border border-emerald-200/80 bg-white p-3 shadow-xs">
            <div className="flex items-center justify-between mb-1">
              <span className="text-xs font-semibold text-slate-700 flex items-center gap-1.5">
                <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
                Random Forest ML
              </span>
              <span className="text-[11px] font-semibold text-emerald-700 bg-emerald-100 px-1.5 py-0.5 rounded">
                95.6% F1
              </span>
            </div>
            <p className="text-[11px] text-slate-500">
              Active model predicting spoilage & dynamic markdowns.
            </p>
          </div>
          <div className="mt-3 text-center text-[11px] text-slate-500">
            FreshWatch SaaS Platform © 2026
          </div>
        </div>
      </div>
    </div>
  );
}
