"use client";

import React, { useState, useEffect } from "react";
import {
  Tag,
  CheckCircle2,
  AlertTriangle,
  Sparkles,
  ShoppingBag,
  TrendingUp,
  Percent,
  Layers,
  Check,
  X,
  RotateCcw,
} from "lucide-react";
import { formatCurrency } from "@/lib/utils";

export default function PricingAdvisorPage() {
  const [recommendations, setRecommendations] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [actionFeedback, setActionFeedback] = useState<string | null>(null);

  const fetchRecommendations = async () => {
    try {
      const res = await fetch("/api/pricing");
      if (res.ok) {
        const data = await res.json();
        setRecommendations(data.recommendations || []);
      }
    } catch (e) {
      console.error("Failed to load recommendations:", e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRecommendations();
  }, []);

  const handleAction = async (id: string, action: "apply" | "dismiss") => {
    try {
      const res = await fetch("/api/pricing", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id, action }),
      });
      const data = await res.json();
      if (res.ok && data.success) {
        setActionFeedback(data.message);
        fetchRecommendations();
        setTimeout(() => setActionFeedback(null), 3500);
      }
    } catch (e) {
      alert("Failed to update pricing recommendation.");
    }
  };

  // Pre-configured curated combo offers for supermarkets
  const combos = [
    {
      title: "Breakfast Essentials Bundle",
      items: ["Fresh Cow Milk (1L)", "Whole Wheat Bread (400g)"],
      originalTotal: 77,
      comboPrice: 62,
      discount: "20% OFF",
      reason: "Milk expires in 3 days; pairing with high-turnover daily bread doubles velocity.",
    },
    {
      title: "Tea-Time Refresh Combo",
      items: ["Garlic Herb Toast Slices", "Digestive Wheat Biscuits (200g)"],
      originalTotal: 80,
      comboPrice: 65,
      discount: "18% OFF",
      reason: "Clears bakery toast approaching 12-day window with staple biscuits.",
    },
    {
      title: "Fresh Morning Vitamin Pack",
      items: ["Robusta Bananas (1 Dozen)", "Sweet Strawberries Box (250g)"],
      originalTotal: 175,
      comboPrice: 125,
      discount: "28% OFF",
      reason: "Both fruits have ≤ 3 days remaining. Liquidate together to avoid spoilage.",
    },
  ];

  const pendingRecs = recommendations.filter((r) => r.status === "Pending");
  const appliedRecs = recommendations.filter((r) => r.status === "Applied");

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Header */}
      <div className="pb-4 border-b border-slate-200">
        <h1 className="text-2xl font-bold tracking-tight text-slate-900 flex items-center gap-2">
          <Tag className="h-6 w-6 text-emerald-800" />
          Dynamic Pricing Advisor & Markdown Engine
        </h1>
        <p className="text-xs text-slate-500 mt-1">
          Algorithmic discount suggestions to clear inventory before spoilage, maximize revenue, and minimize food wastage.
        </p>
      </div>

      {actionFeedback && (
        <div className="rounded-xl border border-emerald-200 bg-emerald-50 p-3 text-xs text-emerald-800 flex items-center gap-2">
          <CheckCircle2 className="h-4 w-4 text-emerald-600 shrink-0" />
          <span>{actionFeedback}</span>
        </div>
      )}

      {/* KPI Overview of Pricing Impact */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
            Pending Recommendations
          </span>
          <div className="mt-2 text-2xl font-bold text-slate-900">{pendingRecs.length} SKUs</div>
          <p className="mt-1 text-xs text-slate-500">Require manager confirmation</p>
        </div>

        <div className="rounded-2xl border border-emerald-200 bg-emerald-50/60 p-5 shadow-xs">
          <span className="text-xs font-semibold text-emerald-800 uppercase tracking-wider">
            Active Markdowns Applied
          </span>
          <div className="mt-2 text-2xl font-bold text-emerald-900">{appliedRecs.length} Products</div>
          <p className="mt-1 text-xs text-emerald-700">Currently updated on shelf & register</p>
        </div>

        <div className="rounded-2xl border border-emerald-200 bg-emerald-50/60 p-5 shadow-xs">
          <span className="text-xs font-semibold text-emerald-800 uppercase tracking-wider">
            Loss Avoidance Potential
          </span>
          <div className="mt-2 text-2xl font-bold text-emerald-900">
            {formatCurrency(
              pendingRecs.reduce((acc, r) => acc + (r.potentialLossAvoided || 0), 0)
            )}
          </div>
          <p className="mt-1 text-xs text-emerald-700">Estimated revenue saved through price elasticity</p>
        </div>
      </div>

      {/* Dynamic Markdown Cards */}
      <div>
        <h2 className="text-sm font-bold uppercase tracking-wider text-slate-700 mb-4 flex items-center gap-2">
          <Sparkles className="h-4 w-4 text-emerald-700" />
          Prescribed Single-Item Markdowns
        </h2>

        {loading ? (
          <div className="rounded-2xl border border-slate-200 bg-white p-8 text-center text-xs text-slate-400">
            Loading pricing models...
          </div>
        ) : pendingRecs.length === 0 ? (
          <div className="rounded-2xl border border-slate-200 bg-white p-8 text-center text-xs text-slate-500">
            <CheckCircle2 className="h-8 w-8 text-emerald-500 mx-auto mb-2" />
            No pending price reductions required right now. All products are priced optimally.
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {pendingRecs.map((rec) => (
              <div
                key={rec.id}
                className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs hover:border-emerald-300 transition-all space-y-4"
              >
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-slate-100 text-slate-600">
                      {rec.product?.category || "General"}
                    </span>
                    <h3 className="text-base font-bold text-slate-900 mt-1">
                      {rec.product?.name}
                    </h3>
                    <p className="text-xs text-slate-500 font-mono">
                      Current Stock: {rec.product?.quantity} {rec.product?.unit}
                    </p>
                  </div>

                  <span className="text-sm font-extrabold px-3 py-1 rounded-xl bg-emerald-100 text-emerald-800 border border-emerald-200">
                    -{rec.discountPct}%
                  </span>
                </div>

                <div className="grid grid-cols-3 gap-2 p-3 rounded-xl bg-slate-50 border border-slate-100 text-center">
                  <div>
                    <span className="block text-[11px] text-slate-400">Original Price</span>
                    <span className="block text-sm font-bold text-slate-500 line-through">
                      ₹{rec.originalPrice}
                    </span>
                  </div>
                  <div>
                    <span className="block text-[11px] text-emerald-700 font-medium">Suggested Price</span>
                    <span className="block text-base font-extrabold text-emerald-800">
                      ₹{rec.suggestedPrice}
                    </span>
                  </div>
                  <div>
                    <span className="block text-[11px] text-slate-400">Loss Avoided</span>
                    <span className="block text-sm font-bold text-emerald-700">
                      ₹{rec.potentialLossAvoided}
                    </span>
                  </div>
                </div>

                <p className="text-xs text-slate-600 leading-relaxed bg-emerald-50/50 p-2.5 rounded-lg border border-emerald-100">
                  <strong>Rationale:</strong> {rec.reason}
                </p>

                <div className="flex items-center justify-end gap-2 pt-2 border-t border-slate-100">
                  <button
                    onClick={() => handleAction(rec.id, "dismiss")}
                    className="flex items-center gap-1 px-3 py-1.5 text-xs font-semibold text-slate-500 hover:text-slate-800 hover:bg-slate-100 rounded-lg transition-colors"
                  >
                    <X className="h-3.5 w-3.5" /> Dismiss
                  </button>
                  <button
                    onClick={() => handleAction(rec.id, "apply")}
                    className="flex items-center gap-1.5 px-4 py-1.5 text-xs font-semibold text-white bg-emerald-800 hover:bg-emerald-700 rounded-lg shadow-sm transition-colors"
                  >
                    <Check className="h-3.5 w-3.5" /> Apply Discount to Shelf
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Suggested Combo Offers */}
      <div className="pt-4 border-t border-slate-200">
        <h2 className="text-sm font-bold uppercase tracking-wider text-slate-700 mb-4 flex items-center gap-2">
          <ShoppingBag className="h-4 w-4 text-emerald-700" />
          Cross-Category Combo Offer Recommendations
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {combos.map((combo, i) => (
            <div
              key={i}
              className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between">
                  <h3 className="font-bold text-slate-900 text-sm">{combo.title}</h3>
                  <span className="text-[11px] font-bold px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800">
                    {combo.discount}
                  </span>
                </div>

                <ul className="mt-3 space-y-1 text-xs text-slate-700">
                  {combo.items.map((item, idx) => (
                    <li key={idx} className="flex items-center gap-1.5">
                      <span className="h-1.5 w-1.5 rounded-full bg-emerald-600" />
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>

                <p className="mt-3 text-xs text-slate-500 italic">"{combo.reason}"</p>
              </div>

              <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between">
                <div>
                  <span className="text-xs text-slate-400 line-through mr-2">₹{combo.originalTotal}</span>
                  <span className="text-base font-bold text-emerald-800">₹{combo.comboPrice}</span>
                </div>
                <button
                  onClick={() => alert(`Combo bundle '${combo.title}' configured for POS terminals!`)}
                  className="px-3 py-1.5 rounded-lg bg-emerald-50 text-emerald-800 border border-emerald-200 hover:bg-emerald-100 text-xs font-semibold transition-colors"
                >
                  Activate Combo
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
