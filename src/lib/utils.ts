import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatCurrency(amount: number, currency: string = "₹"): string {
  return `${currency}${Number(amount || 0).toLocaleString("en-IN", {
    minimumFractionDigits: 0,
    maximumFractionDigits: 2,
  })}`;
}

export function formatDate(date: string | Date | null | undefined): string {
  if (!date) return "-";
  const d = new Date(date);
  return d.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
}

export function getDaysLeft(expiryDate: string | Date): number {
  const now = new Date();
  const target = new Date(expiryDate);
  const diffTime = target.getTime() - now.getTime();
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  return Math.max(0, diffDays);
}

export function getRiskBadgeClasses(risk: string) {
  const lower = (risk || "").toLowerCase();
  if (lower.includes("high")) {
    return {
      bg: "bg-red-50 text-red-700 border-red-200",
      dot: "bg-red-500",
      badge: "text-red-700 bg-red-100",
    };
  }
  if (lower.includes("medium")) {
    return {
      bg: "bg-amber-50 text-amber-700 border-amber-200",
      dot: "bg-amber-500",
      badge: "text-amber-700 bg-amber-100",
    };
  }
  return {
    bg: "bg-emerald-50 text-emerald-700 border-emerald-200",
    dot: "bg-emerald-500",
    badge: "text-emerald-700 bg-emerald-100",
  };
}
