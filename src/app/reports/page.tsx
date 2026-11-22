"use client";

import React, { useState, useEffect } from "react";
import {
  BarChart3,
  Download,
  Printer,
  FileSpreadsheet,
  FileText,
  Clock,
  DollarSign,
  AlertTriangle,
  CheckCircle2,
  Calendar,
} from "lucide-react";
import { formatCurrency, formatDate } from "@/lib/utils";

export default function ReportsPage() {
  const [data, setData] = useState<any>(null);
  const [products, setProducts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const [anRes, invRes] = await Promise.all([
          fetch("/api/analytics"),
          fetch("/api/inventory"),
        ]);
        if (anRes.ok) setData(await anRes.json());
        if (invRes.ok) {
          const inv = await invRes.json();
          setProducts(inv.products || []);
        }
      } catch (e) {
        console.error("Report fetch error:", e);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  const handlePrint = () => {
    window.print();
  };

  const kpis = data?.kpis || {};
  const highRiskItems = products.filter((p) => p.riskLevel === "High Risk");
  const expiringSoon = products.filter((p) => p.daysLeft <= 5);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 print:p-0 print:m-0">
      {/* Top Header - Hidden in Print */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 pb-4 border-b border-slate-200 print:hidden">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900 flex items-center gap-2">
            <BarChart3 className="h-6 w-6 text-emerald-800" />
            Inventory Audit & Wastage Reports
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Formal audit logs, shelf-life risk summaries, and downloadable export formats.
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <a
            href="/api/export?format=csv"
            className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-emerald-800 text-white text-xs font-semibold hover:bg-emerald-700 shadow-sm transition-all"
          >
            <FileSpreadsheet className="h-4 w-4" />
            <span>Download CSV Audit</span>
          </a>

          <a
            href="/api/export?format=json"
            target="_blank"
            className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-white border border-slate-200 text-slate-700 text-xs font-semibold hover:bg-slate-50 shadow-2xs transition-all"
          >
            <FileText className="h-4 w-4 text-emerald-700" />
            <span>JSON Feed</span>
          </a>

          <button
            onClick={handlePrint}
            className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-white border border-slate-200 text-slate-700 text-xs font-semibold hover:bg-slate-50 shadow-2xs transition-all"
          >
            <Printer className="h-4 w-4 text-emerald-700" />
            <span>Print Report</span>
          </button>
        </div>
      </div>

      {/* Printable Report Header */}
      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between pb-4 border-b border-slate-200 gap-2">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xl font-bold text-slate-900">FreshWatch Supermarket</span>
              <span className="text-xs font-semibold px-2 py-0.5 rounded bg-emerald-100 text-emerald-800">
                Official Audit Report
              </span>
            </div>
            <p className="text-xs text-slate-500 mt-1">
              Generated on {new Date().toLocaleDateString("en-US", { dateStyle: "full" })} at{" "}
              {new Date().toLocaleTimeString()}
            </p>
          </div>

          <div className="text-right text-xs text-slate-500">
            <span className="block font-semibold text-slate-800">Location: Main Retail Store</span>
            <span>Total Catalog Tracked: {kpis.totalProducts ?? 0} SKUs</span>
          </div>
        </div>

        {/* Executive Summary Metrics */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <div className="p-4 rounded-xl bg-slate-50 border border-slate-100">
            <span className="text-xs font-semibold text-slate-500 uppercase block">
              Inventory Valuation
            </span>
            <span className="text-xl font-extrabold text-slate-900 mt-1 block">
              {formatCurrency(kpis.totalInventoryValue ?? 0)}
            </span>
            <span className="text-[11px] text-slate-400">Total current shelf stock</span>
          </div>

          <div className="p-4 rounded-xl bg-red-50 border border-red-100">
            <span className="text-xs font-semibold text-red-800 uppercase block">
              Spoilage Exposure
            </span>
            <span className="text-xl font-extrabold text-red-700 mt-1 block">
              {formatCurrency(kpis.potentialLoss ?? 0)}
            </span>
            <span className="text-[11px] text-red-600">{highRiskItems.length} SKUs at high risk</span>
          </div>

          <div className="p-4 rounded-xl bg-emerald-50 border border-emerald-100">
            <span className="text-xs font-semibold text-emerald-800 uppercase block">
              Proactive Recovery
            </span>
            <span className="text-xl font-extrabold text-emerald-900 mt-1 block">
              {formatCurrency(kpis.potentialSavings ?? 0)}
            </span>
            <span className="text-[11px] text-emerald-700">72% recovery with markdowns</span>
          </div>

          <div className="p-4 rounded-xl bg-slate-50 border border-slate-100">
            <span className="text-xs font-semibold text-slate-500 uppercase block">
              Expiring ≤ 5 Days
            </span>
            <span className="text-xl font-extrabold text-amber-700 mt-1 block">
              {expiringSoon.length} Products
            </span>
            <span className="text-[11px] text-slate-400">Immediate shelf priority</span>
          </div>
        </div>

        {/* High Risk Table */}
        <div>
          <h2 className="text-sm font-bold uppercase tracking-wider text-slate-800 mb-3 flex items-center gap-2">
            <AlertTriangle className="h-4 w-4 text-red-600" />
            Urgent Attention: High Expiry Risk Items
          </h2>

          <div className="rounded-xl border border-slate-200 overflow-hidden text-xs">
            <table className="w-full text-left">
              <thead className="bg-slate-50 border-b border-slate-200 font-semibold text-slate-700">
                <tr>
                  <th className="p-2.5">SKU / Product</th>
                  <th className="p-2.5">Category</th>
                  <th className="p-2.5 text-right">Stock</th>
                  <th className="p-2.5 text-right">Daily Velocity</th>
                  <th className="p-2.5 text-right">Days Left</th>
                  <th className="p-2.5 text-right">Projected Leftover</th>
                  <th className="p-2.5 text-right">At-Risk Loss</th>
                  <th className="p-2.5">Recommended Intervention</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 bg-white">
                {highRiskItems.length === 0 ? (
                  <tr>
                    <td colSpan={8} className="p-6 text-center text-slate-400">
                      No high-risk items found in inventory.
                    </td>
                  </tr>
                ) : (
                  highRiskItems.map((item, i) => (
                    <tr key={i} className="hover:bg-slate-50">
                      <td className="p-2.5 font-bold text-slate-900">
                        {item.name}
                        <div className="text-[10px] text-slate-400 font-mono">{item.productId}</div>
                      </td>
                      <td className="p-2.5 text-slate-600">{item.category}</td>
                      <td className="p-2.5 text-right font-semibold text-slate-800">
                        {item.quantity} {item.unit}
                      </td>
                      <td className="p-2.5 text-right text-slate-600">{item.dailySalesRate}/day</td>
                      <td className="p-2.5 text-right font-bold text-red-600">{item.daysLeft}d</td>
                      <td className="p-2.5 text-right font-bold text-slate-800">{item.leftover} units</td>
                      <td className="p-2.5 text-right font-bold text-red-600">₹{item.potentialLoss}</td>
                      <td className="p-2.5 text-emerald-800 font-medium">
                        {item.recommendedAction}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Audit Sign-off section for print */}
        <div className="pt-6 border-t border-slate-200 grid grid-cols-2 gap-8 text-xs text-slate-600">
          <div>
            <span className="block font-semibold text-slate-800">Inventory Officer Signature</span>
            <div className="mt-8 border-b border-slate-300 w-48" />
            <span className="text-[11px] text-slate-400 mt-1 block">Date: ________________________</span>
          </div>
          <div>
            <span className="block font-semibold text-slate-800">Store Manager Approval</span>
            <div className="mt-8 border-b border-slate-300 w-48" />
            <span className="text-[11px] text-slate-400 mt-1 block">Date: ________________________</span>
          </div>
        </div>
      </div>
    </div>
  );
}
