"use client";

import React, { useState } from "react";
import { X, UploadCloud, FileText, CheckCircle2, AlertTriangle, AlertCircle } from "lucide-react";

interface CsvUploadModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

export default function CsvUploadModal({ isOpen, onClose, onSuccess }: CsvUploadModalProps) {
  const [file, setFile] = useState<File | null>(null);
  const [previewRows, setPreviewRows] = useState<any[]>([]);
  const [validationErrors, setValidationErrors] = useState<string[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<string | null>(null);

  if (!isOpen) return null;

  const parseCsvText = (text: string) => {
    const lines = text.split(/\r?\n/).filter((l) => l.trim().length > 0);
    if (lines.length < 2) {
      setValidationErrors(["CSV file is empty or lacks data rows."]);
      return;
    }

    const headers = lines[0].split(",").map((h) => h.trim().toLowerCase().replace(/"/g, ""));
    const requiredCols = ["product", "stock", "daily_sales", "days_left"];
    const missing = requiredCols.filter((col) => !headers.includes(col) && !headers.includes(col.replace("_", "")));

    if (missing.length > 0) {
      setValidationErrors([
        `Missing required columns: ${missing.join(", ")}.`,
        `Expected headers: product, stock, daily_sales, days_left (or daysLeft), price (optional).`,
      ]);
      return;
    }

    const parsed: any[] = [];
    const errors: string[] = [];

    for (let i = 1; i < lines.length; i++) {
      const rowVals = lines[i].split(",").map((v) => v.trim().replace(/"/g, ""));
      if (rowVals.length !== headers.length) {
        errors.push(`Row ${i + 1}: Expected ${headers.length} columns, found ${rowVals.length}.`);
        continue;
      }

      const item: any = {};
      headers.forEach((h, idx) => {
        item[h] = rowVals[idx];
      });

      const productName = item.product || item.name || item.product_name;
      const stock = parseFloat(item.stock);
      const dailySales = parseFloat(item.daily_sales || item.dailySales || item.sales_rate || "1.0");
      const daysLeft = parseInt(item.days_left || item.daysleft || item.days || "7");
      const price = parseFloat(item.price || item.selling_price || item.sellingprice || "50");

      if (!productName) {
        errors.push(`Row ${i + 1}: Missing product name.`);
      } else if (isNaN(stock) || stock < 0) {
        errors.push(`Row ${i + 1} (${productName}): Invalid stock value '${item.stock}'. Must be a positive number.`);
      } else if (isNaN(dailySales) || dailySales < 0) {
        errors.push(`Row ${i + 1} (${productName}): Invalid daily sales rate.`);
      } else {
        parsed.push({
          name: productName,
          stock,
          daily_sales: dailySales,
          days_left: daysLeft,
          price: isNaN(price) ? 50 : price,
          category: item.category || "General",
        });
      }
    }

    setValidationErrors(errors.slice(0, 5));
    setPreviewRows(parsed);
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selected = e.target.files?.[0];
    if (!selected) return;
    setFile(selected);
    setValidationErrors([]);
    setUploadStatus(null);

    const reader = new FileReader();
    reader.onload = (event) => {
      const text = event.target?.result as string;
      parseCsvText(text);
    };
    reader.readAsText(selected);
  };

  const handleConfirmImport = async () => {
    if (previewRows.length === 0) return;
    setIsProcessing(true);
    setUploadStatus("Importing products and executing Random Forest predictions...");

    try {
      const res = await fetch("/api/inventory", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          bulk: true,
          items: previewRows.map((r) => ({
            name: r.name,
            quantity: r.stock,
            dailySalesRate: r.daily_sales,
            daysLeft: r.days_left,
            price: r.price,
            category: r.category,
          })),
        }),
      });

      const data = await res.json();
      if (!res.ok || !data.success) {
        throw new Error(data.error || "Failed to import items.");
      }

      setUploadStatus(`Success! Imported ${data.importedCount} products into Inventory Analysis.`);
      setTimeout(() => {
        onSuccess();
        onClose();
      }, 1200);
    } catch (err: any) {
      setValidationErrors([err.message || "Upload failed."]);
      setUploadStatus(null);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div className="fixed inset-0 bg-black/50 backdrop-blur-xs" onClick={onClose} />
      <div className="relative w-full max-w-2xl rounded-2xl bg-white shadow-2xl border border-slate-200 overflow-hidden z-10 max-h-[90vh] flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-200 bg-slate-50">
          <div>
            <h3 className="text-lg font-bold text-slate-900">Upload Inventory CSV</h3>
            <p className="text-xs text-slate-500">
              Bulk import supermarket inventory with automated schema validation
            </p>
          </div>
          <button
            onClick={onClose}
            className="rounded-lg p-2 text-slate-400 hover:bg-slate-200 hover:text-slate-700 transition-colors"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Body */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {/* Dropzone */}
          <label className="flex flex-col items-center justify-center border-2 border-dashed border-emerald-300 rounded-xl p-6 bg-emerald-50/50 hover:bg-emerald-50 cursor-pointer transition-colors">
            <UploadCloud className="h-10 w-10 text-emerald-600 mb-2" />
            <span className="text-sm font-semibold text-slate-700">
              Click to select a CSV file or drag and drop
            </span>
            <span className="text-xs text-slate-500 mt-1">
              Supports CSV with headers: <code>product, stock, daily_sales, days_left, price</code>
            </span>
            <input
              type="file"
              accept=".csv"
              onChange={handleFileChange}
              className="hidden"
            />
          </label>

          {/* Validation Warnings / Errors */}
          {validationErrors.length > 0 && (
            <div className="rounded-xl border border-amber-200 bg-amber-50 p-4 space-y-1">
              <div className="flex items-center gap-2 text-xs font-bold text-amber-800">
                <AlertTriangle className="h-4 w-4 shrink-0 text-amber-600" />
                <span>Validation Issues Detected:</span>
              </div>
              <ul className="list-disc pl-5 text-xs text-amber-700 space-y-0.5">
                {validationErrors.map((err, i) => (
                  <li key={i}>{err}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Status notification */}
          {uploadStatus && (
            <div className="rounded-xl border border-emerald-200 bg-emerald-50 p-3 text-xs font-medium text-emerald-800 flex items-center gap-2">
              <CheckCircle2 className="h-4 w-4 text-emerald-600" />
              <span>{uploadStatus}</span>
            </div>
          )}

          {/* Preview Table */}
          {previewRows.length > 0 && (
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-bold uppercase tracking-wider text-slate-700">
                  Ready to Import ({previewRows.length} valid rows)
                </span>
                <span className="text-xs text-slate-500">Showing first 5 preview items</span>
              </div>

              <div className="rounded-xl border border-slate-200 overflow-hidden text-xs">
                <table className="w-full text-left">
                  <thead className="bg-slate-100 text-slate-700 font-semibold border-b border-slate-200">
                    <tr>
                      <th className="p-2.5">Product Name</th>
                      <th className="p-2.5">Stock</th>
                      <th className="p-2.5">Daily Sales</th>
                      <th className="p-2.5">Days Left</th>
                      <th className="p-2.5">Price</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100 bg-white">
                    {previewRows.slice(0, 5).map((row, i) => (
                      <tr key={i}>
                        <td className="p-2.5 font-medium text-slate-900">{row.name}</td>
                        <td className="p-2.5 text-slate-600">{row.stock}</td>
                        <td className="p-2.5 text-slate-600">{row.daily_sales}/day</td>
                        <td className="p-2.5 text-slate-600">{row.days_left}d</td>
                        <td className="p-2.5 text-slate-600">₹{row.price}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-slate-200 bg-slate-50 flex justify-end gap-3">
          <button
            type="button"
            onClick={onClose}
            className="px-4 py-2 text-sm font-medium text-slate-600 hover:bg-slate-200 rounded-lg transition-colors"
          >
            Cancel
          </button>
          <button
            type="button"
            disabled={previewRows.length === 0 || isProcessing}
            onClick={handleConfirmImport}
            className="flex items-center gap-2 px-5 py-2 text-sm font-medium text-white bg-emerald-800 hover:bg-emerald-700 rounded-lg shadow-sm transition-colors disabled:opacity-60"
          >
            <CheckCircle2 className="h-4 w-4" />
            <span>{isProcessing ? "Processing..." : `Import ${previewRows.length} Items`}</span>
          </button>
        </div>
      </div>
    </div>
  );
}
