"use client";

import React, { useState, useEffect } from "react";
import { X, Save, AlertCircle, Calendar, DollarSign, Package } from "lucide-react";

interface ProductFormModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
  product?: any | null; // If provided, edit mode
}

export default function ProductFormModal({
  isOpen,
  onClose,
  onSuccess,
  product,
}: ProductFormModalProps) {
  const isEdit = Boolean(product && product.id);

  const [formData, setFormData] = useState({
    productId: "",
    name: "",
    category: "Fresh Produce",
    quantity: 20,
    unit: "units",
    purchasePrice: 40,
    sellingPrice: 60,
    dailySalesRate: 2.5,
    expiryDate: new Date(Date.now() + 5 * 24 * 60 * 60 * 1000).toISOString().slice(0, 10),
    supplier: "Direct Farm Supply",
    storageCondition: "Ambient",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (product) {
      setFormData({
        productId: product.productId || "",
        name: product.name || "",
        category: product.category || "Fresh Produce",
        quantity: product.quantity ?? 20,
        unit: product.unit || "units",
        purchasePrice: product.purchasePrice ?? 0,
        sellingPrice: product.sellingPrice ?? 0,
        dailySalesRate: product.dailySalesRate ?? 1.0,
        expiryDate: product.expiryDate
          ? new Date(product.expiryDate).toISOString().slice(0, 10)
          : new Date().toISOString().slice(0, 10),
        supplier: product.supplier || "",
        storageCondition: product.storageCondition || "Ambient",
      });
    } else {
      setFormData({
        productId: `SKU-${Math.floor(1000 + Math.random() * 9000)}`,
        name: "",
        category: "Fresh Produce",
        quantity: 25,
        unit: "units",
        purchasePrice: 30,
        sellingPrice: 45,
        dailySalesRate: 3.0,
        expiryDate: new Date(Date.now() + 5 * 24 * 60 * 60 * 1000).toISOString().slice(0, 10),
        supplier: "Direct Farm Supply",
        storageCondition: "Ambient",
      });
    }
    setError(null);
  }, [product, isOpen]);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!formData.name.trim()) {
      setError("Product Name is required.");
      return;
    }
    if (formData.quantity < 0 || formData.sellingPrice < 0) {
      setError("Quantity and Selling Price must be non-negative.");
      return;
    }

    setLoading(true);
    try {
      const url = isEdit ? `/api/inventory/${product.id}` : "/api/inventory";
      const method = isEdit ? "PUT" : "POST";

      const res = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      const data = await res.json();
      if (!res.ok || !data.success) {
        throw new Error(data.error || "Failed to save product.");
      }

      onSuccess();
      onClose();
    } catch (err: any) {
      setError(err.message || "An unexpected error occurred.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div className="fixed inset-0 bg-black/50 backdrop-blur-xs" onClick={onClose} />
      <div className="relative w-full max-w-2xl rounded-2xl bg-white shadow-2xl border border-slate-200 overflow-hidden z-10 max-h-[90vh] flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-200 bg-slate-50">
          <div>
            <h3 className="text-lg font-bold text-slate-900">
              {isEdit ? "Edit Inventory Product" : "Add New Supermarket SKU"}
            </h3>
            <p className="text-xs text-slate-500">
              {isEdit
                ? "Update pricing, stock counts, and shelf-life metrics"
                : "Fill in product details to run real-time Random Forest expiry risk predictions"}
            </p>
          </div>
          <button
            onClick={onClose}
            className="rounded-lg p-2 text-slate-400 hover:bg-slate-200 hover:text-slate-700 transition-colors"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Form Body */}
        <form onSubmit={handleSubmit} className="flex-1 overflow-y-auto p-6 space-y-4">
          {error && (
            <div className="rounded-xl border border-red-200 bg-red-50 p-3 text-xs text-red-700 flex items-center gap-2">
              <AlertCircle className="h-4 w-4 shrink-0" />
              <span>{error}</span>
            </div>
          )}

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Product ID / SKU
              </label>
              <input
                type="text"
                disabled={isEdit}
                value={formData.productId}
                onChange={(e) => setFormData({ ...formData, productId: e.target.value })}
                className="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-800 disabled:bg-slate-100 disabled:text-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                required
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Category
              </label>
              <select
                value={formData.category}
                onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                className="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500"
              >
                <option value="Fresh Produce">Fresh Produce (Fruits & Veggies)</option>
                <option value="Dairy & Chilled">Dairy & Chilled Items</option>
                <option value="Bakery">Bakery & Fresh Breads</option>
                <option value="Meat & Seafood">Meat & Seafood</option>
                <option value="Grains & Pulses">Grains & Pulses (Rice, Dals, Atta)</option>
                <option value="Beverages">Beverages & Cold Pressed Juices</option>
                <option value="Snacks">Packaged Snacks & Confectionery</option>
                <option value="Plant-Based">Plant-Based / Specialty</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Product Name *
            </label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              placeholder="e.g. Robusta Bananas (1 Dozen)"
              className="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500"
              required
            />
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Quantity in Stock
              </label>
              <input
                type="number"
                min="0"
                step="any"
                value={formData.quantity}
                onChange={(e) => setFormData({ ...formData, quantity: parseFloat(e.target.value) || 0 })}
                className="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                required
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Unit of Measure
              </label>
              <input
                type="text"
                value={formData.unit}
                onChange={(e) => setFormData({ ...formData, unit: e.target.value })}
                placeholder="kg, packs, units"
                className="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Daily Sales Velocity
              </label>
              <input
                type="number"
                min="0.1"
                step="0.1"
                value={formData.dailySalesRate}
                onChange={(e) => setFormData({ ...formData, dailySalesRate: parseFloat(e.target.value) || 1.0 })}
                className="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                required
              />
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Purchase Cost (₹)
              </label>
              <input
                type="number"
                min="0"
                step="any"
                value={formData.purchasePrice}
                onChange={(e) => setFormData({ ...formData, purchasePrice: parseFloat(e.target.value) || 0 })}
                className="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Selling Price (₹) *
              </label>
              <input
                type="number"
                min="0"
                step="any"
                value={formData.sellingPrice}
                onChange={(e) => setFormData({ ...formData, sellingPrice: parseFloat(e.target.value) || 0 })}
                className="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                required
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Expiry Date *
              </label>
              <input
                type="date"
                value={formData.expiryDate}
                onChange={(e) => setFormData({ ...formData, expiryDate: e.target.value })}
                className="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                required
              />
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Supplier / Brand
              </label>
              <input
                type="text"
                value={formData.supplier}
                onChange={(e) => setFormData({ ...formData, supplier: e.target.value })}
                placeholder="e.g. Kisan Direct, Golden Mills"
                className="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Storage Conditions
              </label>
              <select
                value={formData.storageCondition}
                onChange={(e) => setFormData({ ...formData, storageCondition: e.target.value })}
                className="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-emerald-500"
              >
                <option value="Ambient">Ambient Room Temp (18-24°C)</option>
                <option value="Dry Ambient">Dry Ambient (Staples/Pulses/Rice)</option>
                <option value="Chilled (2-4°C)">Chilled (2-4°C) Dairy & Cuts</option>
                <option value="Chilled misted (4°C)">Chilled Misted (Leafy Greens)</option>
                <option value="Frozen (-18°C)">Frozen (-18°C)</option>
              </select>
            </div>
          </div>

          <div className="pt-4 border-t border-slate-200 flex justify-end gap-3">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-sm font-medium text-slate-600 hover:bg-slate-100 rounded-lg transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="flex items-center gap-2 px-5 py-2 text-sm font-medium text-white bg-emerald-800 hover:bg-emerald-700 rounded-lg shadow-sm transition-colors disabled:opacity-60"
            >
              <Save className="h-4 w-4" />
              <span>{loading ? "Saving..." : isEdit ? "Update SKU" : "Save Product"}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
