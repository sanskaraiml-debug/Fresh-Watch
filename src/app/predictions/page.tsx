"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import {
  Sparkles,
  AlertTriangle,
  ShieldCheck,
  TrendingDown,
  RefreshCw,
  SlidersHorizontal,
  Tag,
  ArrowRight,
  CheckCircle2,
  BrainCircuit,
  DollarSign,
} from "lucide-react";
import { formatCurrency, getRiskBadgeClasses } from "@/lib/utils";

export default function PredictionsPage() {
  const [predictions, setPredictions] = useState<any[]>([]);
  const [summary, setSummary] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [isPredicting, setIsPredicting] = useState(false);
  const [filterRisk, setFilterRisk] = useState("All");

  const runPredictions = async () => {
    setIsPredicting(true);
    try {
      const res = await fetch("/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ runAll: true }),
      });
      if (res.ok) {
        const data = await res.json();
        setPredictions(data.predictions || []);
        setSummary(data.summary || null);
      }
    } catch (e) {
      console.error("Batch prediction failed:", e);
    } finally {
      setIsPredicting(false);
      setLoading(false);
    }
  };

  useEffect(() => {
    runPredictions();
  }, []);

  const filteredItems = predictions.filter((p) => {
    if (filterRisk === "All") return true;
    return p.risk_level.toLowerCase().includes(filterRisk.toLowerCase());
  });

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 pb-4 border-b border-slate-200">
        <div>
          <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-emerald-100 text-emerald-800 text-[11px] font-semibold mb-1">
            <BrainCircuit className="h-3.5 w-3.5 text-emerald-700" />
            <span>Random Forest Model • 95.6% F1 Accuracy</span>
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900 flex items-center gap-2">
            <Sparkles className="h-6 w-6 text-emerald-800" />
            AI Expiry & Wastage Prediction Engine
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Evaluating stock, sales rates, days remaining, expected sales velocity, and projected leftover quantities.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={runPredictions}
            disabled={isPredicting}
            className="flex items-center gap-2 px-4 py-2 rounded-xl bg-emerald-800 text-white text-xs font-semibold hover:bg-emerald-700 shadow-sm transition-all disabled:opacity-60"
          >
            <RefreshCw className={`h-4 w-4 ${isPredicting ? "animate-spin" : ""}`} />
            <span>{isPredicting ? "Running Inference..." : "Re-run Batch Inference"}</span>
          </button>

          <Link
            href="/simulator"
            className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-white border border-slate-200 text-slate-700 text-xs font-semibold hover:bg-slate-50 shadow-2xs transition-all"
          >
            <SlidersHorizontal className="h-4 w-4 text-emerald-700" />
            <span>Single Item Simulator</span>
          </Link>
        </div>
      </div>

      {/* Summary Cards */}
      {summary && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
              Total Inferred Items
            </span>
            <div className="mt-2 text-2xl font-bold text-slate-900">{summary.total}</div>
            <p className="mt-1 text-xs text-slate-500">Full supermarket catalog</p>
          </div>

          <div className="rounded-2xl border border-red-200 bg-red-50/60 p-5 shadow-xs">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-red-800 uppercase tracking-wider">
                High Wastage Risk
              </span>
              <AlertTriangle className="h-4 w-4 text-red-600" />
            </div>
            <div className="mt-2 text-2xl font-bold text-red-700">{summary.highRisk} Items</div>
            <p className="mt-1 text-xs text-red-600">Immediate discounting required</p>
          </div>

          <div className="rounded-2xl border border-amber-200 bg-amber-50/60 p-5 shadow-xs">
            <span className="text-xs font-semibold text-amber-800 uppercase tracking-wider">
              Medium Risk (Watchlist)
            </span>
            <div className="mt-2 text-2xl font-bold text-amber-700">{summary.mediumRisk} Items</div>
            <p className="mt-1 text-xs text-amber-600">Approaching buffer threshold</p>
          </div>

          <div className="rounded-2xl border border-emerald-200 bg-emerald-50/60 p-5 shadow-xs">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-emerald-800 uppercase tracking-wider">
                Total At-Risk Value
              </span>
              <DollarSign className="h-4 w-4 text-emerald-700" />
            </div>
            <div className="mt-2 text-2xl font-bold text-emerald-900">
              {formatCurrency(summary.totalPotentialLoss)}
            </div>
            <p className="mt-1 text-xs text-emerald-700">Preventable with dynamic markdowns</p>
          </div>
        </div>
      )}

      {/* Filter Tabs */}
      <div className="flex items-center gap-2 border-b border-slate-200 pb-2 text-xs font-semibold">
        {["All", "High Risk", "Medium Risk", "Low Risk"].map((risk) => (
          <button
            key={risk}
            onClick={() => setFilterRisk(risk)}
            className={`px-3 py-1.5 rounded-lg transition-colors ${
              filterRisk === risk
                ? "bg-emerald-800 text-white shadow-2xs"
                : "text-slate-600 hover:bg-slate-100"
            }`}
          >
            {risk}
          </button>
        ))}
      </div>

      {/* Prediction Results Table */}
      <div className="rounded-2xl border border-slate-200 bg-white overflow-hidden shadow-xs">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-50/80 border-b border-slate-200 text-[11px] font-bold uppercase tracking-wider text-slate-500">
                <th className="p-3">Product Name</th>
                <th className="p-3">Category</th>
                <th className="p-3 text-right">Stock</th>
                <th className="p-3 text-right">Velocity</th>
                <th className="p-3 text-right">Days Left</th>
                <th className="p-3 text-right">Expected Leftover</th>
                <th className="p-3 text-center">Wastage %</th>
                <th className="p-3">Risk Level</th>
                <th className="p-3 text-right">Potential Loss</th>
                <th className="p-3">Prescribed Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-xs">
              {loading ? (
                <tr>
                  <td colSpan={10} className="p-8 text-center text-slate-400">
                    Running model inference on inventory...
                  </td>
                </tr>
              ) : filteredItems.length === 0 ? (
                <tr>
                  <td colSpan={10} className="p-8 text-center text-slate-400">
                    No items found matching the selected filter.
                  </td>
                </tr>
              ) : (
                filteredItems.map((item, idx) => {
                  const badge = getRiskBadgeClasses(item.risk_level);
                  return (
                    <tr key={idx} className="hover:bg-slate-50 transition-colors">
                      <td className="p-3 font-bold text-slate-900">{item.product}</td>
                      <td className="p-3 text-slate-500">{item.category}</td>
                      <td className="p-3 text-right font-semibold text-slate-800">{item.stock}</td>
                      <td className="p-3 text-right text-slate-600">{item.daily_sales}/day</td>
                      <td className="p-3 text-right font-medium text-slate-700">{item.days_left}d</td>
                      <td className="p-3 text-right font-bold text-slate-800">
                        {item.unsold_quantity} units
                      </td>
                      <td className="p-3 text-center">
                        <span className="font-bold text-slate-900">{item.wastage_chance}%</span>
                      </td>
                      <td className="p-3">
                        <span
                          className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-semibold border ${badge.bg}`}
                        >
                          <span className={`h-1.5 w-1.5 rounded-full ${badge.dot}`} />
                          {item.risk_level}
                        </span>
                      </td>
                      <td className="p-3 text-right font-bold text-red-600">
                        ₹{item.potential_loss}
                      </td>
                      <td className="p-3 text-emerald-800 font-medium">
                        {item.recommended_action}
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>

        <div className="p-4 border-t border-slate-100 bg-slate-50/60 flex items-center justify-between text-xs text-slate-500">
          <span>Inference generated using Random Forest Classifier (wastage_model.pkl)</span>
          <Link href="/pricing" className="font-semibold text-emerald-800 hover:underline flex items-center gap-1">
            Apply Dynamic Markdowns <Tag className="h-3.5 w-3.5" />
          </Link>
        </div>
      </div>
    </div>
  );
}
