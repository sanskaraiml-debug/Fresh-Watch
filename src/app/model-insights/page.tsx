"use client";

import React, { useState, useEffect } from "react";
import {
  BrainCircuit,
  CheckCircle2,
  BarChart2,
  TrendingUp,
  Cpu,
  Layers,
  Sparkles,
  Info,
} from "lucide-react";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Cell,
} from "recharts";

export default function ModelInsightsPage() {
  const [modelInfo, setModelInfo] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchModelData() {
      try {
        const res = await fetch("/api/model-info");
        if (res.ok) {
          const data = await res.json();
          setModelInfo(data);
        }
      } catch (e) {
        console.error("Failed to load model info:", e);
      } finally {
        setLoading(false);
      }
    }
    fetchModelData();
  }, []);

  const featureData = [
    { name: "leftover", importance: 59.87, label: "Leftover Units" },
    { name: "expected_sales", importance: 23.23, label: "Expected Sales" },
    { name: "days_left", importance: 6.75, label: "Days Remaining" },
    { name: "stock", importance: 6.46, label: "Initial Stock" },
    { name: "daily_sales", importance: 3.70, label: "Daily Sales Velocity" },
  ];

  const comparisonData = modelInfo?.comparison || [
    { model: "Logistic Regression", accuracy: 0.955, precision: 0.9467, recall: 0.9444, f1: 0.9456 },
    { model: "Decision Tree", accuracy: 0.949, precision: 0.9481, recall: 0.9275, f1: 0.9377 },
    { model: "Random Forest", accuracy: 0.956, precision: 0.9469, recall: 0.9469, f1: 0.9469 },
  ];

  const confusionMatrix = modelInfo?.confusion_matrix || [
    [564, 22],
    [22, 392],
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Header */}
      <div className="pb-4 border-b border-slate-200">
        <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-emerald-100 text-emerald-800 text-[11px] font-semibold mb-1">
          <BrainCircuit className="h-3.5 w-3.5 text-emerald-700" />
          <span>Production Machine Learning Artifact</span>
        </div>
        <h1 className="text-2xl font-bold tracking-tight text-slate-900 flex items-center gap-2">
          <Cpu className="h-6 w-6 text-emerald-800" />
          Model Insights & Validation Metrics
        </h1>
        <p className="text-xs text-slate-500 mt-1">
          Evaluation benchmarks, feature importances, and confusion matrix for the trained Random Forest Classifier.
        </p>
      </div>

      {/* KPI Benchmarks */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="rounded-2xl border border-emerald-200 bg-white p-5 shadow-xs">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Accuracy</span>
          <div className="mt-2 text-3xl font-extrabold text-emerald-900">95.6%</div>
          <p className="mt-1 text-xs text-emerald-700">Test dataset evaluation</p>
        </div>

        <div className="rounded-2xl border border-emerald-200 bg-white p-5 shadow-xs">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Precision</span>
          <div className="mt-2 text-3xl font-extrabold text-emerald-900">94.7%</div>
          <p className="mt-1 text-xs text-emerald-700">Low false alarm rate</p>
        </div>

        <div className="rounded-2xl border border-emerald-200 bg-white p-5 shadow-xs">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Recall</span>
          <div className="mt-2 text-3xl font-extrabold text-emerald-900">94.7%</div>
          <p className="mt-1 text-xs text-emerald-700">Captures true spoilage risks</p>
        </div>

        <div className="rounded-2xl border border-emerald-200 bg-emerald-50/60 p-5 shadow-xs">
          <span className="text-xs font-semibold text-emerald-800 uppercase tracking-wider">F1-Score</span>
          <div className="mt-2 text-3xl font-extrabold text-emerald-900">0.9469</div>
          <p className="mt-1 text-xs text-emerald-700">Optimal balance</p>
        </div>
      </div>

      {/* Feature Importance & Confusion Matrix */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Feature Importance Bar Chart (7 cols) */}
        <div className="lg:col-span-7 rounded-2xl border border-slate-200 bg-white p-6 shadow-xs flex flex-col">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100 mb-4">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Feature Importance Breakdown</h3>
              <p className="text-xs text-slate-500">Relative weight assigned by the 100 decision trees</p>
            </div>
            <span className="text-xs font-semibold text-emerald-800 bg-emerald-50 px-2 py-0.5 rounded">
              Gini Impurity
            </span>
          </div>

          <div className="h-64 w-full flex-1">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={featureData} layout="vertical" margin={{ top: 5, right: 30, left: 40, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#f1f5f9" />
                <XAxis type="number" unit="%" stroke="#94a3b8" fontSize={11} />
                <YAxis dataKey="label" type="category" stroke="#64748b" fontSize={11} tickLine={false} />
                <Tooltip
                  formatter={(val: any) => [`${val}%`, "Importance"]}
                  contentStyle={{ backgroundColor: "#ffffff", borderRadius: "8px", border: "1px solid #e2e8f0" }}
                />
                <Bar dataKey="importance" fill="#065f46" radius={[0, 6, 6, 0]}>
                  {featureData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={index === 0 ? "#047857" : "#0f766e"} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>

          <p className="mt-3 text-xs text-slate-500 border-t border-slate-100 pt-3">
            <strong>Key insight:</strong> <code>leftover</code> (stock − daily_sales × days_left) drives ~60% of model prediction decisions, ensuring mathematical grounding without relying on arbitrary LLM generation.
          </p>
        </div>

        {/* 2x2 Confusion Matrix (5 cols) */}
        <div className="lg:col-span-5 rounded-2xl border border-slate-200 bg-white p-6 shadow-xs flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between pb-3 border-b border-slate-100 mb-4">
              <div>
                <h3 className="text-sm font-bold text-slate-900">Confusion Matrix</h3>
                <p className="text-xs text-slate-500">1,000 hold-out test samples</p>
              </div>
              <span className="text-xs font-mono text-slate-500">N = 1,000</span>
            </div>

            <div className="grid grid-cols-2 gap-3 text-center my-4">
              {/* True Negative */}
              <div className="p-4 rounded-xl bg-emerald-50 border border-emerald-200">
                <span className="text-[10px] font-bold text-emerald-800 uppercase block">
                  True Negative (Safe)
                </span>
                <span className="text-2xl font-extrabold text-emerald-900 mt-1 block">
                  {confusionMatrix[0][0]}
                </span>
                <span className="text-[10px] text-emerald-700">Correctly classified healthy stock</span>
              </div>

              {/* False Positive */}
              <div className="p-4 rounded-xl bg-slate-50 border border-slate-200">
                <span className="text-[10px] font-bold text-slate-500 uppercase block">
                  False Positive
                </span>
                <span className="text-2xl font-extrabold text-slate-700 mt-1 block">
                  {confusionMatrix[0][1]}
                </span>
                <span className="text-[10px] text-slate-400">False alarm markdowns</span>
              </div>

              {/* False Negative */}
              <div className="p-4 rounded-xl bg-slate-50 border border-slate-200">
                <span className="text-[10px] font-bold text-slate-500 uppercase block">
                  False Negative
                </span>
                <span className="text-2xl font-extrabold text-slate-700 mt-1 block">
                  {confusionMatrix[1][0]}
                </span>
                <span className="text-[10px] text-slate-400">Missed spoilage risk</span>
              </div>

              {/* True Positive */}
              <div className="p-4 rounded-xl bg-emerald-50 border border-emerald-200">
                <span className="text-[10px] font-bold text-emerald-800 uppercase block">
                  True Positive (Spoilage)
                </span>
                <span className="text-2xl font-extrabold text-emerald-900 mt-1 block">
                  {confusionMatrix[1][1]}
                </span>
                <span className="text-[10px] text-emerald-700">Correctly detected spoilage</span>
              </div>
            </div>
          </div>

          <div className="p-3 rounded-xl bg-slate-50 border border-slate-100 text-xs text-slate-600 flex items-start gap-2">
            <Info className="h-4 w-4 text-emerald-700 shrink-0 mt-0.5" />
            <span>
              Low false negative rate (2.2%) ensures that virtually no perishable stock approaches expiry unnoticed.
            </span>
          </div>
        </div>
      </div>

      {/* Model Benchmark Comparison Table */}
      <div className="rounded-2xl border border-slate-200 bg-white overflow-hidden shadow-xs">
        <div className="p-4 border-b border-slate-200 bg-slate-50/70">
          <h3 className="text-sm font-bold text-slate-900">Cross-Model Algorithm Comparison</h3>
          <p className="text-xs text-slate-500">Evaluated on identical 4,000 train / 1,000 test supermarket records</p>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse text-xs">
            <thead>
              <tr className="bg-slate-50 border-b border-slate-200 text-[11px] font-bold uppercase tracking-wider text-slate-500">
                <th className="p-3">Algorithm</th>
                <th className="p-3 text-right">Accuracy</th>
                <th className="p-3 text-right">Precision</th>
                <th className="p-3 text-right">Recall</th>
                <th className="p-3 text-right">F1 Score</th>
                <th className="p-3">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {comparisonData.map((row: any, i: number) => {
                const isSelected = row.model === "Random Forest";
                return (
                  <tr
                    key={i}
                    className={`transition-colors ${
                      isSelected ? "bg-emerald-50/60 font-semibold text-emerald-950" : "hover:bg-slate-50 text-slate-700"
                    }`}
                  >
                    <td className="p-3 flex items-center gap-2">
                      {isSelected && <CheckCircle2 className="h-4 w-4 text-emerald-700 shrink-0" />}
                      <span>{row.model}</span>
                    </td>
                    <td className="p-3 text-right">{(row.accuracy * 100).toFixed(1)}%</td>
                    <td className="p-3 text-right">{(row.precision * 100).toFixed(2)}%</td>
                    <td className="p-3 text-right">{(row.recall * 100).toFixed(2)}%</td>
                    <td className="p-3 text-right">{row.f1.toFixed(4)}</td>
                    <td className="p-3">
                      {isSelected ? (
                        <span className="px-2 py-0.5 rounded-full bg-emerald-200 text-emerald-900 text-[10px] font-bold">
                          Selected (Production)
                        </span>
                      ) : (
                        <span className="text-slate-400 text-[11px]">Benchmark</span>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
