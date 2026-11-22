"use client";

import React, { useState, useEffect } from "react";
import {
  SlidersHorizontal,
  Sparkles,
  TrendingUp,
  AlertTriangle,
  ShieldCheck,
  Tag,
  DollarSign,
  Package,
  Layers,
  ArrowRight,
} from "lucide-react";
import { formatCurrency, getRiskBadgeClasses } from "@/lib/utils";

export default function SimulatorPage() {
  const [productName, setProductName] = useState("Robusta Bananas (1 Dozen)");
  const [category, setCategory] = useState("Fresh Produce");
  const [stock, setStock] = useState(45);
  const [dailySales, setDailySales] = useState(5.5);
  const [daysLeft, setDaysLeft] = useState(3);
  const [price, setPrice] = useState(55);

  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  // Run prediction on slider change (debounced)
  useEffect(() => {
    let active = true;
    const compute = async () => {
      setLoading(true);
      try {
        const res = await fetch("/api/predict", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            product: productName,
            stock,
            daily_sales: dailySales,
            days_left: daysLeft,
            price,
            category,
          }),
        });
        if (res.ok) {
          const data = await res.json();
          if (active) setResult(data.result);
        }
      } catch (e) {
      } finally {
        if (active) setLoading(false);
      }
    };

    const timeout = setTimeout(compute, 150);
    return () => {
      active = false;
      clearTimeout(timeout);
    };
  }, [productName, stock, dailySales, daysLeft, price, category]);

  const presetScenarios = [
    {
      label: "Bananas (High Spoilage)",
      name: "Robusta Bananas (1 Dozen)",
      stock: 45,
      sales: 5.5,
      days: 3,
      price: 55,
      category: "Fresh Produce",
    },
    {
      label: "Fresh Cow Milk (3 Days Left)",
      name: "Fresh Cow Milk (1L)",
      stock: 24,
      sales: 3.0,
      days: 3,
      price: 32,
      category: "Dairy & Chilled",
    },
    {
      label: "Basmati Rice (Safe Staple)",
      name: "Royal Basmati Rice (5kg)",
      stock: 45,
      sales: 2.5,
      days: 60,
      price: 420,
      category: "Grains & Pulses",
    },
    {
      label: "Sweet Strawberries (Urgent 2d)",
      name: "Sweet Strawberries Box (250g)",
      stock: 18,
      sales: 1.2,
      days: 2,
      price: 120,
      category: "Fresh Produce",
    },
  ];

  const badge = getRiskBadgeClasses(result?.risk_level || "Low Risk");

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Header */}
      <div className="pb-4 border-b border-slate-200">
        <h1 className="text-2xl font-bold tracking-tight text-slate-900 flex items-center gap-2">
          <SlidersHorizontal className="h-6 w-6 text-emerald-800" />
          Single Item What-If Simulator
        </h1>
        <p className="text-xs text-slate-500 mt-1">
          Adjust stock quantities, velocity rates, shelf-life buffers, and prices in real time to simulate Random Forest predictions.
        </p>
      </div>

      {/* Preset Scenarios */}
      <div>
        <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider block mb-2">
          Quick Preset Scenarios
        </span>
        <div className="flex flex-wrap gap-2">
          {presetScenarios.map((sc, i) => (
            <button
              key={i}
              onClick={() => {
                setProductName(sc.name);
                setStock(sc.stock);
                setDailySales(sc.sales);
                setDaysLeft(sc.days);
                setPrice(sc.price);
                setCategory(sc.category);
              }}
              className="px-3 py-1.5 rounded-lg border border-slate-200 bg-white hover:bg-emerald-50 hover:border-emerald-300 text-xs font-medium text-slate-700 hover:text-emerald-900 transition-colors shadow-2xs"
            >
              {sc.label}
            </button>
          ))}
        </div>
      </div>

      {/* Main Grid: Controls vs Live Output */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left: Interactive Controls (5 cols) */}
        <div className="lg:col-span-5 rounded-2xl border border-slate-200 bg-white p-6 shadow-xs space-y-5">
          <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider pb-2 border-b border-slate-100 flex items-center justify-between">
            <span>Simulation Parameters</span>
            <span className="text-[11px] text-emerald-800 font-normal">Real-Time</span>
          </h2>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Product Name
            </label>
            <input
              type="text"
              value={productName}
              onChange={(e) => setProductName(e.target.value)}
              className="w-full rounded-lg border border-slate-200 px-3 py-2 text-xs text-slate-800 focus:outline-none focus:ring-1 focus:ring-emerald-500"
            />
          </div>

          {/* Stock Slider */}
          <div>
            <div className="flex items-center justify-between text-xs mb-1">
              <span className="font-semibold text-slate-700">Stock on Shelf</span>
              <span className="font-bold text-emerald-800 text-sm">{stock} units</span>
            </div>
            <input
              type="range"
              min="1"
              max="150"
              value={stock}
              onChange={(e) => setStock(parseInt(e.target.value))}
              className="w-full accent-emerald-700 cursor-pointer"
            />
            <div className="flex justify-between text-[10px] text-slate-400 mt-0.5">
              <span>1 unit</span>
              <span>150 units</span>
            </div>
          </div>

          {/* Daily Sales Slider */}
          <div>
            <div className="flex items-center justify-between text-xs mb-1">
              <span className="font-semibold text-slate-700">Daily Sales Velocity</span>
              <span className="font-bold text-emerald-800 text-sm">{dailySales} units/day</span>
            </div>
            <input
              type="range"
              min="0.2"
              max="20"
              step="0.1"
              value={dailySales}
              onChange={(e) => setDailySales(parseFloat(e.target.value))}
              className="w-full accent-emerald-700 cursor-pointer"
            />
            <div className="flex justify-between text-[10px] text-slate-400 mt-0.5">
              <span>0.2 /day</span>
              <span>20 /day</span>
            </div>
          </div>

          {/* Days Left Slider */}
          <div>
            <div className="flex items-center justify-between text-xs mb-1">
              <span className="font-semibold text-slate-700">Days Until Expiry</span>
              <span className="font-bold text-emerald-800 text-sm">{daysLeft} days</span>
            </div>
            <input
              type="range"
              min="1"
              max="90"
              value={daysLeft}
              onChange={(e) => setDaysLeft(parseInt(e.target.value))}
              className="w-full accent-emerald-700 cursor-pointer"
            />
            <div className="flex justify-between text-[10px] text-slate-400 mt-0.5">
              <span>1 day</span>
              <span>90 days</span>
            </div>
          </div>

          {/* Price Slider */}
          <div>
            <div className="flex items-center justify-between text-xs mb-1">
              <span className="font-semibold text-slate-700">Retail Selling Price</span>
              <span className="font-bold text-emerald-800 text-sm">₹{price}</span>
            </div>
            <input
              type="range"
              min="10"
              max="1000"
              step="5"
              value={price}
              onChange={(e) => setPrice(parseInt(e.target.value))}
              className="w-full accent-emerald-700 cursor-pointer"
            />
            <div className="flex justify-between text-[10px] text-slate-400 mt-0.5">
              <span>₹10</span>
              <span>₹1,000</span>
            </div>
          </div>
        </div>

        {/* Right: Simulated Prediction Results (7 cols) */}
        <div className="lg:col-span-7 space-y-6">
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs space-y-5">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <div>
                <span className="text-xs text-slate-500 uppercase tracking-wider block">
                  Model Prediction Output
                </span>
                <h3 className="text-lg font-bold text-slate-900">{productName}</h3>
              </div>

              {result && (
                <span
                  className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold border ${badge.bg}`}
                >
                  <span className={`h-2 w-2 rounded-full ${badge.dot}`} />
                  {result.risk_level}
                </span>
              )}
            </div>

            {/* Metrics Grid */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-100">
                <span className="text-[11px] font-semibold text-slate-500 uppercase block">
                  Expected Sales
                </span>
                <span className="text-xl font-extrabold text-slate-800 mt-1 block">
                  {result?.expected_sales ?? 0} units
                </span>
                <span className="text-[10px] text-slate-400">At current velocity</span>
              </div>

              <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-100">
                <span className="text-[11px] font-semibold text-slate-500 uppercase block">
                  Unsold Leftover
                </span>
                <span className={`text-xl font-extrabold mt-1 block ${result?.unsold_quantity > 0 ? "text-red-600" : "text-emerald-700"}`}>
                  {result?.unsold_quantity ?? 0} units
                </span>
                <span className="text-[10px] text-slate-400">Projected wastage</span>
              </div>

              <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-100">
                <span className="text-[11px] font-semibold text-slate-500 uppercase block">
                  Wastage Chance
                </span>
                <span className="text-xl font-extrabold text-slate-900 mt-1 block">
                  {result?.wastage_chance ?? 0}%
                </span>
                <span className="text-[10px] text-slate-400">Random Forest prob</span>
              </div>

              <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-100">
                <span className="text-[11px] font-semibold text-slate-500 uppercase block">
                  Potential Loss
                </span>
                <span className="text-xl font-extrabold text-red-600 mt-1 block">
                  ₹{result?.potential_loss ?? 0}
                </span>
                <span className="text-[10px] text-slate-400">Unrecovered inventory</span>
              </div>
            </div>

            {/* Markdown Prescription Box */}
            <div className="rounded-xl border border-emerald-200 bg-emerald-50/70 p-5 space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold uppercase tracking-wider text-emerald-900 flex items-center gap-1.5">
                  <Tag className="h-4 w-4 text-emerald-700" />
                  Prescribed Pricing Intervention
                </span>
                {result?.discount_pct > 0 && (
                  <span className="text-xs font-bold px-2 py-0.5 rounded-full bg-emerald-200 text-emerald-900">
                    -{result.discount_pct}% Markdown
                  </span>
                )}
              </div>

              <p className="text-xs text-emerald-950 font-medium leading-relaxed">
                {result?.recommended_action}
              </p>

              {result?.discount_pct > 0 && (
                <div className="pt-2 border-t border-emerald-200 flex items-center justify-between text-xs">
                  <div>
                    <span className="text-slate-500 mr-2">New Target Price:</span>
                    <span className="font-extrabold text-emerald-900 text-sm">
                      ₹{result?.suggested_price}
                    </span>
                  </div>
                  <span className="text-emerald-800 font-semibold">
                    Expected to clear ~80% of leftover stock
                  </span>
                </div>
              )}
            </div>

            {/* Visual Stock vs Leftover Bar */}
            <div className="space-y-1.5">
              <div className="flex items-center justify-between text-xs text-slate-600">
                <span>Stock Allocation Breakdown</span>
                <span>
                  {result?.expected_sales} sold / {result?.unsold_quantity} leftover
                </span>
              </div>
              <div className="h-4 w-full bg-slate-100 rounded-full overflow-hidden flex">
                <div
                  className="bg-emerald-600 h-full transition-all duration-300"
                  style={{
                    width: `${Math.min(100, ((result?.expected_sales || 0) / Math.max(stock, 1)) * 100)}%`,
                  }}
                  title="Expected Sales"
                />
                <div
                  className="bg-red-500 h-full transition-all duration-300"
                  style={{
                    width: `${Math.min(100, ((result?.unsold_quantity || 0) / Math.max(stock, 1)) * 100)}%`,
                  }}
                  title="Projected Leftover Wastage"
                />
              </div>
              <div className="flex items-center justify-between text-[11px] text-slate-400">
                <span className="flex items-center gap-1">
                  <span className="h-2 w-2 rounded-full bg-emerald-600" /> Expected Sold
                </span>
                <span className="flex items-center gap-1">
                  <span className="h-2 w-2 rounded-full bg-red-500" /> Spoilage Wastage
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
