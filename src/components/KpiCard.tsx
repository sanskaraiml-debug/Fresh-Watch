import React from "react";
import { LucideIcon } from "lucide-react";

interface KpiCardProps {
  title: string;
  value: string | number;
  subtext?: string;
  trend?: string;
  trendType?: "positive" | "negative" | "neutral" | "warning";
  icon: LucideIcon;
  iconColor?: string;
  bgColor?: string;
}

export default function KpiCard({
  title,
  value,
  subtext,
  trend,
  trendType = "neutral",
  icon: Icon,
  iconColor = "text-emerald-700",
  bgColor = "bg-emerald-50",
}: KpiCardProps) {
  const getTrendColor = () => {
    switch (trendType) {
      case "positive":
        return "text-emerald-700 bg-emerald-50 border-emerald-200";
      case "warning":
        return "text-amber-700 bg-amber-50 border-amber-200";
      case "negative":
        return "text-red-700 bg-red-50 border-red-200";
      default:
        return "text-slate-600 bg-slate-50 border-slate-200";
    }
  };

  return (
    <div className="rounded-xl border border-slate-200/90 bg-white p-5 shadow-xs hover:shadow-md transition-shadow">
      <div className="flex items-center justify-between">
        <span className="text-xs font-semibold uppercase tracking-wider text-slate-500">
          {title}
        </span>
        <div className={`flex h-10 w-10 items-center justify-center rounded-xl ${bgColor} ${iconColor} border border-black/5`}>
          <Icon className="h-5 w-5" />
        </div>
      </div>

      <div className="mt-3 flex items-baseline gap-2">
        <span className="text-2xl font-bold tracking-tight text-slate-900">
          {value}
        </span>
        {trend && (
          <span
            className={`inline-flex items-center rounded-full border px-2 py-0.5 text-[11px] font-semibold ${getTrendColor()}`}
          >
            {trend}
          </span>
        )}
      </div>

      {subtext && (
        <p className="mt-2 text-xs text-slate-500 line-clamp-1">
          {subtext}
        </p>
      )}
    </div>
  );
}
