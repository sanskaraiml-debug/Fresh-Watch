"use client";

import React, { useState, useEffect } from "react";
import {
  Settings,
  Save,
  CheckCircle2,
  AlertCircle,
  Database,
  Cpu,
  Bot,
  ShieldAlert,
  Server,
  Layers,
} from "lucide-react";

export default function SettingsPage() {
  const [formData, setFormData] = useState({
    storeName: "FreshWatch Supermarket",
    currency: "₹",
    highRiskThreshold: 75,
    mediumRiskThreshold: 45,
    autoDiscountEnabled: true,
    defaultDiscountPct: 20,
  });

  const [systemStatus, setSystemStatus] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [statusMessage, setStatusMessage] = useState<string | null>(null);

  useEffect(() => {
    async function loadSettings() {
      try {
        const res = await fetch("/api/settings");
        if (res.ok) {
          const data = await res.json();
          if (data.settings) {
            setFormData({
              storeName: data.settings.storeName,
              currency: data.settings.currency,
              highRiskThreshold: data.settings.highRiskThreshold,
              mediumRiskThreshold: data.settings.mediumRiskThreshold,
              autoDiscountEnabled: data.settings.autoDiscountEnabled,
              defaultDiscountPct: data.settings.defaultDiscountPct,
            });
          }
          if (data.systemStatus) {
            setSystemStatus(data.systemStatus);
          }
        }
      } catch (e) {
        console.error("Failed to load settings:", e);
      } finally {
        setLoading(false);
      }
    }
    loadSettings();
  }, []);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setStatusMessage(null);
    try {
      const res = await fetch("/api/settings", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      const data = await res.json();
      if (res.ok && data.success) {
        setStatusMessage("Settings updated successfully.");
        setTimeout(() => setStatusMessage(null), 3000);
      } else {
        throw new Error(data.error || "Failed to update settings");
      }
    } catch (err: any) {
      alert(err.message || "Error saving settings");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 py-8 space-y-8">
      {/* Header */}
      <div className="pb-4 border-b border-slate-200">
        <h1 className="text-2xl font-bold tracking-tight text-slate-900 flex items-center gap-2">
          <Settings className="h-6 w-6 text-emerald-800" />
          Store Preferences & System Settings
        </h1>
        <p className="text-xs text-slate-500 mt-1">
          Configure risk thresholds, local currency, automation preferences, and inspect microservice health.
        </p>
      </div>

      {statusMessage && (
        <div className="rounded-xl border border-emerald-200 bg-emerald-50 p-3 text-xs text-emerald-800 flex items-center gap-2">
          <CheckCircle2 className="h-4 w-4 text-emerald-600 shrink-0" />
          <span>{statusMessage}</span>
        </div>
      )}

      {/* System Health Status Cards */}
      <div>
        <h2 className="text-sm font-bold uppercase tracking-wider text-slate-700 mb-3 flex items-center gap-2">
          <Server className="h-4 w-4 text-emerald-700" />
          System Integration Health
        </h2>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="p-4 rounded-2xl border border-slate-200 bg-white shadow-xs">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-semibold text-slate-600 flex items-center gap-1.5">
                <Database className="h-4 w-4 text-emerald-700" />
                Prisma Database
              </span>
              <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
            </div>
            <div className="text-sm font-bold text-slate-900">Connected (SQLite)</div>
            <p className="text-[11px] text-slate-400 mt-1">Syncing inventory & predictions</p>
          </div>

          <div className="p-4 rounded-2xl border border-slate-200 bg-white shadow-xs">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-semibold text-slate-600 flex items-center gap-1.5">
                <Cpu className="h-4 w-4 text-emerald-700" />
                ML Microservice
              </span>
              <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
            </div>
            <div className="text-sm font-bold text-slate-900">
              {systemStatus?.mlService === "online" ? "Online (FastAPI :8000)" : "Active (Direct Model)"}
            </div>
            <p className="text-[11px] text-slate-400 mt-1">Random Forest 100 Estimators</p>
          </div>

          <div className="p-4 rounded-2xl border border-slate-200 bg-white shadow-xs">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-semibold text-slate-600 flex items-center gap-1.5">
                <Bot className="h-4 w-4 text-emerald-700" />
                AI Assistant Engine
              </span>
              <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
            </div>
            <div className="text-sm font-bold text-slate-900">
              {systemStatus?.groqConfigured ? "Groq API Connected" : "Grounded Engine Active"}
            </div>
            <p className="text-[11px] text-slate-400 mt-1">Multilingual Voice & Text</p>
          </div>
        </div>
      </div>

      {/* Main Settings Form */}
      <form onSubmit={handleSave} className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs space-y-6">
        <h2 className="text-sm font-bold uppercase tracking-wider text-slate-700 pb-2 border-b border-slate-100">
          Store Configuration
        </h2>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Store Name
            </label>
            <input
              type="text"
              value={formData.storeName}
              onChange={(e) => setFormData({ ...formData, storeName: e.target.value })}
              className="w-full rounded-lg border border-slate-200 px-3 py-2 text-xs text-slate-800 focus:outline-none focus:ring-1 focus:ring-emerald-500"
              required
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Currency Symbol
            </label>
            <input
              type="text"
              value={formData.currency}
              onChange={(e) => setFormData({ ...formData, currency: e.target.value })}
              className="w-full rounded-lg border border-slate-200 px-3 py-2 text-xs text-slate-800 focus:outline-none focus:ring-1 focus:ring-emerald-500"
              required
            />
          </div>
        </div>

        <div className="pt-4 border-t border-slate-100">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700 mb-3">
            Expiry Risk Thresholds
          </h3>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                High Risk Threshold (%)
              </label>
              <input
                type="number"
                min="50"
                max="95"
                value={formData.highRiskThreshold}
                onChange={(e) => setFormData({ ...formData, highRiskThreshold: parseInt(e.target.value) })}
                className="w-full rounded-lg border border-slate-200 px-3 py-2 text-xs text-slate-800 focus:outline-none focus:ring-1 focus:ring-emerald-500"
                required
              />
              <p className="text-[10px] text-slate-400 mt-1">
                Items with wastage probability ≥ this threshold generate urgent alerts.
              </p>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Medium Risk Threshold (%)
              </label>
              <input
                type="number"
                min="20"
                max="70"
                value={formData.mediumRiskThreshold}
                onChange={(e) => setFormData({ ...formData, mediumRiskThreshold: parseInt(e.target.value) })}
                className="w-full rounded-lg border border-slate-200 px-3 py-2 text-xs text-slate-800 focus:outline-none focus:ring-1 focus:ring-emerald-500"
                required
              />
              <p className="text-[10px] text-slate-400 mt-1">
                Items entering this range are marked for weekly specials.
              </p>
            </div>
          </div>
        </div>

        <div className="pt-4 border-t border-slate-100">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700 mb-3">
            Markdown Automation
          </h3>

          <div className="space-y-4">
            <label className="flex items-center gap-3 cursor-pointer">
              <input
                type="checkbox"
                checked={formData.autoDiscountEnabled}
                onChange={(e) => setFormData({ ...formData, autoDiscountEnabled: e.target.checked })}
                className="h-4 w-4 rounded border-slate-300 text-emerald-800 focus:ring-emerald-500"
              />
              <div>
                <span className="text-xs font-semibold text-slate-800 block">
                  Enable Proactive Pricing Recommendations
                </span>
                <span className="text-[11px] text-slate-400 block">
                  Automatically prescribe discount percentages when products breach the high-risk mark.
                </span>
              </div>
            </label>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Default Recommended Markdown (%)
              </label>
              <input
                type="number"
                min="5"
                max="50"
                value={formData.defaultDiscountPct}
                onChange={(e) => setFormData({ ...formData, defaultDiscountPct: parseInt(e.target.value) })}
                className="w-full max-w-xs rounded-lg border border-slate-200 px-3 py-2 text-xs text-slate-800 focus:outline-none focus:ring-1 focus:ring-emerald-500"
              />
            </div>
          </div>
        </div>

        <div className="pt-4 border-t border-slate-100 flex justify-end">
          <button
            type="submit"
            disabled={saving}
            className="flex items-center gap-2 px-6 py-2.5 rounded-xl bg-emerald-800 text-white text-xs font-semibold hover:bg-emerald-700 shadow-sm transition-all disabled:opacity-60"
          >
            <Save className="h-4 w-4" />
            <span>{saving ? "Saving Changes..." : "Save Preferences"}</span>
          </button>
        </div>
      </form>
    </div>
  );
}
