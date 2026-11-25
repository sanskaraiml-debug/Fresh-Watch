"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import {
  Package,
  AlertTriangle,
  Clock,
  ShieldCheck,
  TrendingDown,
  DollarSign,
  ArrowRight,
  UploadCloud,
  Sparkles,
  Download,
  SlidersHorizontal,
  ChevronRight,
  CheckCircle2,
  RefreshCw,
  Tag,
  ShoppingBag,
  Leaf,
  Layers,
} from "lucide-react";
import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Tooltip,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Legend,
  AreaChart,
  Area,
} from "recharts";
import KpiCard from "@/components/KpiCard";
import CsvUploadModal from "@/components/CsvUploadModal";
import ProductFormModal from "@/components/ProductFormModal";
import { formatCurrency } from "@/lib/utils";

export default function DashboardPage() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [isCsvModalOpen, setIsCsvModalOpen] = useState(false);
  const [isProductModalOpen, setIsProductModalOpen] = useState(false);
  const [isPredicting, setIsPredicting] = useState(false);
  const [predictionFeedback, setPredictionFeedback] = useState<string | null>(null);

  const fetchDashboardData = async () => {
    try {
      const res = await fetch("/api/analytics");
      if (res.ok) {
        const json = await res.json();
        setData(json);
      }
    } catch (e) {
      console.error("Dashboard fetch error:", e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const handleRunBatchPrediction = async () => {
    setIsPredicting(true);
    setPredictionFeedback("Running Random Forest inference across all inventory items...");
    try {
      const res = await fetch("/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ runAll: true }),
      });
      const result = await res.json();
      if (result.success) {
        setPredictionFeedback(
          `Predictions updated: ${result.summary?.highRisk} high risk, ${result.summary?.mediumRisk} medium risk, ${result.summary?.lowRisk} low risk items.`
        );
        fetchDashboardData();
      }
    } catch (err) {
      setPredictionFeedback("Failed to update predictions.");
    } finally {
      setIsPredicting(false);
      setTimeout(() => setPredictionFeedback(null), 4000);
    }
  };

  const handleResolveAlert = async (alertId: string) => {
    try {
      await fetch("/api/alerts", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: alertId }),
      });
      fetchDashboardData();
    } catch (err) {}
  };

  const kpis = data?.kpis || {};
  const charts = data?.charts || {};
  const alerts = data?.alerts || [];
  const recommendations = data?.recommendations || [];

  return (
    <div className="min-h-screen bg-slate-50/70 pb-16">
      {/* 1. Hero / Welcome Section */}
      <div className="relative overflow-hidden bg-gradient-to-r from-emerald-950 via-emerald-900 to-emerald-850 text-white border-b border-emerald-800">
        <div className="absolute inset-0 bg-[radial-gradient(#10b981_1px,transparent_1px)] [background-size:20px_20px] opacity-10" />
        
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 sm:py-12">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-6">
            <div className="max-w-2xl">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-800/80 border border-emerald-700/60 text-emerald-200 text-xs font-semibold mb-3">
                <Leaf className="h-3.5 w-3.5 text-emerald-400" />
                <span>Supermarket Inventory Intelligence</span>
              </div>
              <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-white">
                Inventory Analysis <span className="text-emerald-400 font-normal">🥬</span>
              </h1>
              <p className="mt-1 text-xl font-medium text-emerald-100">
                Predict. Prevent. Save.
              </p>
              <p className="mt-2 text-sm text-emerald-200/90 leading-relaxed max-w-xl">
                AI-powered expiry prediction to reduce food waste and maximize your profits. Proactively detect perishable inventory risks and execute dynamic pricing markdowns.
              </p>
            </div>

            {/* Quick Action Buttons */}
            <div className="flex flex-wrap items-center gap-3">
              <button
                onClick={() => setIsCsvModalOpen(true)}
                className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-white text-emerald-950 hover:bg-emerald-50 text-xs font-bold shadow-md transition-all active:scale-95"
              >
                <UploadCloud className="h-4 w-4 text-emerald-700" />
                <span>Upload CSV</span>
              </button>

              <button
                onClick={handleRunBatchPrediction}
                disabled={isPredicting}
                className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-emerald-700 text-white hover:bg-emerald-600 border border-emerald-500/50 text-xs font-bold shadow-md transition-all active:scale-95 disabled:opacity-60"
              >
                <Sparkles className={`h-4 w-4 ${isPredicting ? "animate-spin" : "text-emerald-300"}`} />
                <span>{isPredicting ? "Predicting..." : "Run Prediction"}</span>
              </button>

              <Link
                href="/api/export?format=csv"
                className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-emerald-900/80 text-emerald-100 hover:bg-emerald-800 border border-emerald-700/70 text-xs font-semibold shadow-xs transition-colors"
              >
                <Download className="h-4 w-4 text-emerald-300" />
                <span>Export Report</span>
              </Link>

              <Link
                href="/simulator"
                className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-emerald-900/80 text-emerald-100 hover:bg-emerald-800 border border-emerald-700/70 text-xs font-semibold shadow-xs transition-colors"
              >
                <SlidersHorizontal className="h-4 w-4 text-emerald-300" />
                <span>Open Simulator</span>
              </Link>
            </div>
          </div>

          {predictionFeedback && (
            <div className="mt-4 rounded-xl bg-emerald-800/90 border border-emerald-600 p-3 text-xs text-emerald-100 flex items-center gap-2">
              <CheckCircle2 className="h-4 w-4 text-emerald-300 shrink-0" />
              <span>{predictionFeedback}</span>
            </div>
          )}
        </div>
      </div>

      {/* Main Container */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-8 space-y-8">
        {/* 2. KPI Cards Section */}
        <div>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-sm font-bold uppercase tracking-wider text-slate-700 flex items-center gap-2">
              <Layers className="h-4 w-4 text-emerald-700" />
              Real-Time Inventory Metrics
            </h2>
            <button
              onClick={fetchDashboardData}
              className="text-xs text-slate-500 hover:text-emerald-800 flex items-center gap-1 font-medium transition-colors"
            >
              <RefreshCw className="h-3 w-3" /> Refresh
            </button>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
            <KpiCard
              title="Total Products"
              value={loading ? "..." : kpis.totalProducts ?? 0}
              subtext={`${kpis.totalStockUnits ?? 0} total units in stock`}
              icon={Package}
              bgColor="bg-slate-100"
              iconColor="text-slate-700"
            />
            <KpiCard
              title="At-Risk Items"
              value={loading ? "..." : kpis.atRiskItems ?? 0}
              subtext={`${kpis.atRiskPercent ?? 0}% of inventory catalog`}
              trend={`${kpis.atRiskItems ?? 0} Urgent`}
              trendType="negative"
              icon={AlertTriangle}
              bgColor="bg-red-50"
              iconColor="text-red-700"
            />
            <KpiCard
              title="Expiring Soon"
              value={loading ? "..." : kpis.expiringSoon ?? 0}
              subtext="Under 5 days of shelf life"
              trend="Shelf priority"
              trendType="warning"
              icon={Clock}
              bgColor="bg-amber-50"
              iconColor="text-amber-700"
            />
            <KpiCard
              title="Healthy Stock"
              value={loading ? "..." : kpis.healthyStock ?? 0}
              subtext={`${kpis.healthyPercent ?? 0}% stable sales velocity`}
              trend="Normal"
              trendType="positive"
              icon={ShieldCheck}
              bgColor="bg-emerald-50"
              iconColor="text-emerald-700"
            />
            <KpiCard
              title="Potential Savings"
              value={loading ? "..." : formatCurrency(kpis.potentialSavings ?? 0)}
              subtext={`From ${formatCurrency(kpis.potentialLoss ?? 0)} projected risk`}
              trend="Recoverable"
              trendType="positive"
              icon={DollarSign}
              bgColor="bg-emerald-50"
              iconColor="text-emerald-700"
            />
            <KpiCard
              title="Waste Reduction"
              value={loading ? "..." : `${kpis.foodWasteReduction ?? 76}%`}
              subtext="Food waste minimized with markdowns"
              trend="Target: 80%"
              trendType="positive"
              icon={TrendingDown}
              bgColor="bg-emerald-50"
              iconColor="text-emerald-700"
            />
          </div>
        </div>

        {/* 3. Analytics Charts Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Expiry Risk Breakdown (Pie Chart) */}
          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs flex flex-col">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100 mb-2">
              <div>
                <h3 className="text-sm font-bold text-slate-900">Expiry Risk Overview</h3>
                <p className="text-xs text-slate-500">Machine learning risk segmentation</p>
              </div>
              <span className="text-xs font-semibold px-2 py-0.5 rounded bg-emerald-50 text-emerald-700 border border-emerald-200">
                Random Forest
              </span>
            </div>

            <div className="h-64 w-full flex-1">
              {loading ? (
                <div className="h-full flex items-center justify-center text-xs text-slate-400">Loading charts...</div>
              ) : (
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={charts.riskDistribution || []}
                      cx="50%"
                      cy="50%"
                      innerRadius={55}
                      outerRadius={85}
                      paddingAngle={4}
                      dataKey="value"
                    >
                      {(charts.riskDistribution || []).map((entry: any, index: number) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip
                      formatter={(val: any, name: any) => [`${val} products`, name]}
                      contentStyle={{ backgroundColor: "#ffffff", borderRadius: "8px", border: "1px solid #e2e8f0" }}
                    />
                    <Legend verticalAlign="bottom" height={36} iconType="circle" />
                  </PieChart>
                </ResponsiveContainer>
              )}
            </div>

            <div className="mt-2 pt-3 border-t border-slate-100 grid grid-cols-3 text-center text-xs">
              <div>
                <span className="block font-bold text-emerald-700">{kpis.healthyStock ?? 0}</span>
                <span className="text-[11px] text-slate-500">Low Risk</span>
              </div>
              <div>
                <span className="block font-bold text-amber-600">{charts.riskDistribution?.[1]?.value ?? 0}</span>
                <span className="text-[11px] text-slate-500">Medium</span>
              </div>
              <div>
                <span className="block font-bold text-red-600">{kpis.atRiskItems ?? 0}</span>
                <span className="text-[11px] text-slate-500">High Risk</span>
              </div>
            </div>
          </div>

          {/* Weekly Stock & Velocity Trends (Area Chart) */}
          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs lg:col-span-2 flex flex-col">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100 mb-2">
              <div>
                <h3 className="text-sm font-bold text-slate-900">Weekly Stock & Wastage Velocity</h3>
                <p className="text-xs text-slate-500">Projected sales consumption vs expiring quantities</p>
              </div>
              <span className="text-xs text-slate-500 font-mono">7-Day Horizon</span>
            </div>

            <div className="h-64 w-full flex-1">
              {loading ? (
                <div className="h-full flex items-center justify-center text-xs text-slate-400">Loading trends...</div>
              ) : (
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={charts.weeklyTrends || []} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                    <defs>
                      <linearGradient id="colorSales" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#059669" stopOpacity={0.8} />
                        <stop offset="95%" stopColor="#059669" stopOpacity={0.0} />
                      </linearGradient>
                      <linearGradient id="colorRisk" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#ef4444" stopOpacity={0.8} />
                        <stop offset="95%" stopColor="#ef4444" stopOpacity={0.0} />
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                    <XAxis dataKey="day" stroke="#94a3b8" fontSize={12} tickLine={false} />
                    <YAxis stroke="#94a3b8" fontSize={12} tickLine={false} />
                    <Tooltip
                      contentStyle={{ backgroundColor: "#ffffff", borderRadius: "8px", border: "1px solid #e2e8f0" }}
                    />
                    <Legend verticalAlign="top" height={36} iconType="rect" />
                    <Area
                      type="monotone"
                      dataKey="projectedSales"
                      name="Projected Sales Velocity"
                      stroke="#059669"
                      fillOpacity={1}
                      fill="url(#colorSales)"
                    />
                    <Area
                      type="monotone"
                      dataKey="wasteRisk"
                      name="At-Risk Units"
                      stroke="#ef4444"
                      fillOpacity={1}
                      fill="url(#colorRisk)"
                    />
                  </AreaChart>
                </ResponsiveContainer>
              )}
            </div>

            <div className="mt-2 pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
              <span>Proactive markdowns prevent 85% of at-risk units from reaching dumpsters.</span>
              <Link href="/predictions" className="font-semibold text-emerald-800 hover:underline flex items-center gap-1">
                View All Predictions <ChevronRight className="h-3 w-3" />
              </Link>
            </div>
          </div>
        </div>

        {/* 4. Financial Loss Analysis by Category (Bar Chart) */}
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100 mb-4">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Financial Loss Analysis by Category</h3>
              <p className="text-xs text-slate-500">Calculated value of potential wastage if left unmanaged</p>
            </div>
            <span className="text-xs font-semibold text-emerald-800 bg-emerald-50 px-2.5 py-1 rounded-full border border-emerald-200">
              Total Risk: {formatCurrency(kpis.potentialLoss ?? 0)}
            </span>
          </div>

          <div className="h-64 w-full">
            {loading ? (
              <div className="h-full flex items-center justify-center text-xs text-slate-400">Loading financials...</div>
            ) : (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={charts.categoryFinancials || []} margin={{ top: 10, right: 10, left: 10, bottom: 25 }}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                  <XAxis
                    dataKey="category"
                    stroke="#64748b"
                    fontSize={11}
                    angle={-15}
                    textAnchor="end"
                    interval={0}
                  />
                  <YAxis stroke="#64748b" fontSize={11} tickFormatter={(v) => `₹${v}`} />
                  <Tooltip
                    formatter={(val: any) => [`₹${val}`, "Potential Financial Loss"]}
                    contentStyle={{ backgroundColor: "#ffffff", borderRadius: "8px", border: "1px solid #e2e8f0" }}
                  />
                  <Bar dataKey="potentialLoss" name="Potential Spoilage Loss (₹)" fill="#065f46" radius={[6, 6, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            )}
          </div>
        </div>

        {/* 5. Alerts & Top Recommendations Grid */}
        <div id="alerts-section" className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Recent Alerts */}
          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs flex flex-col">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100 mb-4">
              <div className="flex items-center gap-2">
                <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-red-100 text-red-700">
                  <AlertTriangle className="h-4 w-4" />
                </div>
                <div>
                  <h3 className="text-sm font-bold text-slate-900">Recent Spoilage Alerts</h3>
                  <p className="text-xs text-slate-500">Products approaching expiration deadline</p>
                </div>
              </div>
              <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-red-100 text-red-800">
                {alerts.length} Pending
              </span>
            </div>

            <div className="space-y-3 flex-1 overflow-y-auto max-h-96 pr-1">
              {alerts.length === 0 ? (
                <div className="p-8 text-center text-xs text-slate-500">
                  <CheckCircle2 className="h-8 w-8 text-emerald-500 mx-auto mb-2" />
                  All inventory stocks are within safe operational limits.
                </div>
              ) : (
                alerts.map((alert: any) => (
                  <div
                    key={alert.id}
                    className="p-3.5 rounded-xl border border-red-100 bg-red-50/40 hover:bg-red-50 transition-colors flex items-center justify-between gap-3"
                  >
                    <div className="min-w-0 flex-1">
                      <div className="flex items-center gap-2">
                        <span className="font-bold text-sm text-slate-900 truncate">{alert.name}</span>
                        <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-red-200 text-red-800 uppercase">
                          {alert.daysLeft}d left
                        </span>
                      </div>
                      <p className="text-xs text-slate-600 mt-1 line-clamp-1">
                        Stock: {alert.quantity} {alert.unit} • Selling at ₹{alert.price}
                      </p>
                      <p className="text-xs text-emerald-800 font-medium mt-1">
                        💡 Action: {alert.recommendedAction}
                      </p>
                    </div>

                    <button
                      onClick={() => handleResolveAlert(alert.id)}
                      className="shrink-0 text-xs font-semibold px-3 py-1.5 rounded-lg bg-white border border-slate-200 text-slate-700 hover:bg-emerald-50 hover:text-emerald-800 hover:border-emerald-300 transition-colors shadow-2xs"
                    >
                      Resolve
                    </button>
                  </div>
                ))
              )}
            </div>

            <div className="pt-3 border-t border-slate-100 mt-3 text-right">
              <Link href="/inventory?risk=High" className="text-xs font-semibold text-emerald-800 hover:underline">
                View all at-risk products →
              </Link>
            </div>
          </div>

          {/* Top Recommendations */}
          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-xs flex flex-col">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100 mb-4">
              <div className="flex items-center gap-2">
                <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-emerald-100 text-emerald-800">
                  <Tag className="h-4 w-4" />
                </div>
                <div>
                  <h3 className="text-sm font-bold text-slate-900">Top Pricing Recommendations</h3>
                  <p className="text-xs text-slate-500">Algorithmic markdowns & combos to clear inventory</p>
                </div>
              </div>
              <Link
                href="/pricing"
                className="text-xs font-semibold text-emerald-800 hover:underline"
              >
                Pricing Engine →
              </Link>
            </div>

            <div className="space-y-3 flex-1 overflow-y-auto max-h-96 pr-1">
              {recommendations.length === 0 ? (
                <div className="p-8 text-center text-xs text-slate-500">
                  <Sparkles className="h-8 w-8 text-emerald-500 mx-auto mb-2" />
                  No pending price markdowns required today.
                </div>
              ) : (
                recommendations.map((rec: any) => (
                  <div
                    key={rec.id}
                    className="p-3.5 rounded-xl border border-emerald-100 bg-emerald-50/40 hover:bg-emerald-50 transition-colors flex items-center justify-between gap-3"
                  >
                    <div className="min-w-0 flex-1">
                      <div className="flex items-center gap-2">
                        <span className="font-bold text-sm text-slate-900 truncate">{rec.productName}</span>
                        <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-emerald-200 text-emerald-900">
                          {rec.discountPct}% OFF
                        </span>
                      </div>
                      <div className="flex items-center gap-2 text-xs text-slate-600 mt-1">
                        <span className="line-through text-slate-400">₹{rec.originalPrice}</span>
                        <span className="font-bold text-emerald-800">₹{rec.suggestedPrice}</span>
                        <span>•</span>
                        <span className="text-emerald-700">Avoids ₹{rec.potentialLossAvoided} loss</span>
                      </div>
                      <p className="text-xs text-slate-500 mt-1 line-clamp-1">{rec.reason}</p>
                    </div>

                    <Link
                      href="/pricing"
                      className="shrink-0 text-xs font-semibold px-3 py-1.5 rounded-lg bg-emerald-800 text-white hover:bg-emerald-700 transition-colors shadow-2xs"
                    >
                      Apply
                    </Link>
                  </div>
                ))
              )}
            </div>

            <div className="pt-3 border-t border-slate-100 mt-3 text-right">
              <Link href="/pricing" className="text-xs font-semibold text-emerald-800 hover:underline">
                Open Dynamic Pricing Advisor →
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* CSV Upload Modal */}
      <CsvUploadModal
        isOpen={isCsvModalOpen}
        onClose={() => setIsCsvModalOpen(false)}
        onSuccess={() => {
          fetchDashboardData();
        }}
      />

      {/* Product Form Modal */}
      <ProductFormModal
        isOpen={isProductModalOpen}
        onClose={() => setIsProductModalOpen(false)}
        onSuccess={() => {
          fetchDashboardData();
        }}
      />
    </div>
  );
}
