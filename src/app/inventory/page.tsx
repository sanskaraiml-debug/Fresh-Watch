"use client";

import React, { useState, useEffect } from "react";
import {
  Boxes,
  Plus,
  UploadCloud,
  Download,
  Search,
  Filter,
  Trash2,
  Edit,
  ArrowUpDown,
  AlertTriangle,
  CheckCircle2,
  Clock,
  Layers,
  Sparkles,
} from "lucide-react";
import ProductFormModal from "@/components/ProductFormModal";
import CsvUploadModal from "@/components/CsvUploadModal";
import { formatCurrency, formatDate, getRiskBadgeClasses } from "@/lib/utils";

export default function InventoryPage() {
  const [products, setProducts] = useState<any[]>([]);
  const [categories, setCategories] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);

  // Filters & Search
  const [search, setSearch] = useState("");
  const [categoryFilter, setCategoryFilter] = useState("All");
  const [riskFilter, setRiskFilter] = useState("All");
  const [sortBy, setSortBy] = useState("expiryDate");
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("asc");

  // Selection
  const [selectedIds, setSelectedIds] = useState<string[]>([]);

  // Modals
  const [isProductModalOpen, setIsProductModalOpen] = useState(false);
  const [editingProduct, setEditingProduct] = useState<any | null>(null);
  const [isCsvModalOpen, setIsCsvModalOpen] = useState(false);
  const [actionMessage, setActionMessage] = useState<string | null>(null);

  const fetchInventory = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (search) params.set("search", search);
      if (categoryFilter !== "All") params.set("category", categoryFilter);
      if (riskFilter !== "All") params.set("risk", riskFilter);
      params.set("sortBy", sortBy);
      params.set("sortOrder", sortOrder);

      const res = await fetch(`/api/inventory?${params.toString()}`);
      if (res.ok) {
        const data = await res.json();
        setProducts(data.products || []);
        if (data.categories) {
          setCategories(data.categories);
        }
      }
    } catch (e) {
      console.error("Failed to load inventory:", e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchInventory();
  }, [categoryFilter, riskFilter, sortBy, sortOrder]);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    fetchInventory();
  };

  const handleDelete = async (id: string, name: string) => {
    if (!confirm(`Are you sure you want to delete ${name}?`)) return;
    try {
      const res = await fetch(`/api/inventory/${id}`, { method: "DELETE" });
      if (res.ok) {
        setActionMessage(`Deleted ${name} from inventory.`);
        fetchInventory();
        setTimeout(() => setActionMessage(null), 3000);
      }
    } catch (e) {
      alert("Failed to delete product.");
    }
  };

  const handleBulkDelete = async () => {
    if (selectedIds.length === 0) return;
    if (!confirm(`Delete ${selectedIds.length} selected products?`)) return;
    try {
      for (const id of selectedIds) {
        await fetch(`/api/inventory/${id}`, { method: "DELETE" });
      }
      setSelectedIds([]);
      setActionMessage(`Deleted ${selectedIds.length} products.`);
      fetchInventory();
      setTimeout(() => setActionMessage(null), 3000);
    } catch (e) {
      alert("Failed to delete some items.");
    }
  };

  const handleSelectAll = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.checked) {
      setSelectedIds(products.map((p) => p.id));
    } else {
      setSelectedIds([]);
    }
  };

  const toggleSelectOne = (id: string) => {
    if (selectedIds.includes(id)) {
      setSelectedIds(selectedIds.filter((i) => i !== id));
    } else {
      setSelectedIds([...selectedIds, id]);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 pb-4 border-b border-slate-200">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900 flex items-center gap-2">
            <Boxes className="h-6 w-6 text-emerald-800" />
            Supermarket Inventory Management
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Real-time catalog monitoring, sales velocity, expiry milestones, and bulk CSV operations.
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <button
            onClick={() => {
              setEditingProduct(null);
              setIsProductModalOpen(true);
            }}
            className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-emerald-800 text-white text-xs font-semibold hover:bg-emerald-700 shadow-sm transition-all"
          >
            <Plus className="h-4 w-4" />
            <span>Add Product</span>
          </button>

          <button
            onClick={() => setIsCsvModalOpen(true)}
            className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-white border border-slate-200 text-slate-700 text-xs font-semibold hover:bg-slate-50 shadow-2xs transition-all"
          >
            <UploadCloud className="h-4 w-4 text-emerald-700" />
            <span>Upload CSV</span>
          </button>

          <a
            href="/api/export?format=csv"
            className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-white border border-slate-200 text-slate-700 text-xs font-semibold hover:bg-slate-50 shadow-2xs transition-all"
          >
            <Download className="h-4 w-4 text-emerald-700" />
            <span>Export CSV</span>
          </a>
        </div>
      </div>

      {actionMessage && (
        <div className="rounded-xl border border-emerald-200 bg-emerald-50 p-3 text-xs text-emerald-800 flex items-center gap-2">
          <CheckCircle2 className="h-4 w-4 text-emerald-600 shrink-0" />
          <span>{actionMessage}</span>
        </div>
      )}

      {/* Filters & Search Toolbar */}
      <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-xs space-y-3">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-3">
          {/* Search form */}
          <form onSubmit={handleSearchSubmit} className="relative flex-1 max-w-md">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Filter by product name, SKU, or supplier..."
              className="w-full rounded-xl border border-slate-200 bg-slate-50/70 py-2 pl-9 pr-3 text-xs text-slate-800 placeholder-slate-400 focus:border-emerald-500 focus:bg-white focus:outline-none focus:ring-1 focus:ring-emerald-500"
            />
          </form>

          {/* Filters & Sorters */}
          <div className="flex flex-wrap items-center gap-2 text-xs">
            {/* Category Filter */}
            <select
              value={categoryFilter}
              onChange={(e) => setCategoryFilter(e.target.value)}
              className="rounded-xl border border-slate-200 bg-slate-50/70 py-2 px-3 text-slate-700 focus:outline-none focus:border-emerald-500"
            >
              <option value="All">All Categories</option>
              {categories.map((c) => (
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
            </select>

            {/* Risk Filter */}
            <select
              value={riskFilter}
              onChange={(e) => setRiskFilter(e.target.value)}
              className="rounded-xl border border-slate-200 bg-slate-50/70 py-2 px-3 text-slate-700 focus:outline-none focus:border-emerald-500"
            >
              <option value="All">All Risk Levels</option>
              <option value="High Risk">High Risk Only</option>
              <option value="Medium Risk">Medium Risk</option>
              <option value="Low Risk">Low Risk (Healthy)</option>
            </select>

            {/* Sort Field */}
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="rounded-xl border border-slate-200 bg-slate-50/70 py-2 px-3 text-slate-700 focus:outline-none focus:border-emerald-500"
            >
              <option value="expiryDate">Sort by Expiry Date</option>
              <option value="quantity">Sort by Quantity</option>
              <option value="sellingPrice">Sort by Price</option>
              <option value="dailySalesRate">Sort by Sales Velocity</option>
              <option value="name">Sort by Name</option>
            </select>

            {/* Sort Order Toggle */}
            <button
              onClick={() => setSortOrder(sortOrder === "asc" ? "desc" : "asc")}
              className="p-2 rounded-xl border border-slate-200 bg-slate-50 text-slate-700 hover:bg-slate-100 transition-colors"
              title={`Switch to ${sortOrder === "asc" ? "Descending" : "Ascending"}`}
            >
              <ArrowUpDown className="h-4 w-4" />
            </button>
          </div>
        </div>

        {/* Selected row counter & batch delete */}
        {selectedIds.length > 0 && (
          <div className="flex items-center justify-between p-2 rounded-lg bg-emerald-50 border border-emerald-200 text-xs text-emerald-900">
            <span>
              <strong>{selectedIds.length}</strong> items selected
            </span>
            <button
              onClick={handleBulkDelete}
              className="flex items-center gap-1 font-semibold text-red-600 hover:text-red-700"
            >
              <Trash2 className="h-3.5 w-3.5" />
              <span>Delete Selected</span>
            </button>
          </div>
        )}
      </div>

      {/* Main Inventory Table */}
      <div className="rounded-2xl border border-slate-200 bg-white overflow-hidden shadow-xs">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-50/80 border-b border-slate-200 text-[11px] font-bold uppercase tracking-wider text-slate-500">
                <th className="p-3 w-8">
                  <input
                    type="checkbox"
                    onChange={handleSelectAll}
                    checked={products.length > 0 && selectedIds.length === products.length}
                    className="rounded border-slate-300 text-emerald-800 focus:ring-emerald-500"
                  />
                </th>
                <th className="p-3">Product Name & SKU</th>
                <th className="p-3">Category</th>
                <th className="p-3 text-right">In Stock</th>
                <th className="p-3 text-right">Selling Price</th>
                <th className="p-3 text-right">Daily Sales</th>
                <th className="p-3">Days Left</th>
                <th className="p-3">ML Risk Status</th>
                <th className="p-3">Storage</th>
                <th className="p-3 text-center">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-xs">
              {loading ? (
                <tr>
                  <td colSpan={10} className="p-8 text-center text-slate-400">
                    Loading inventory catalog...
                  </td>
                </tr>
              ) : products.length === 0 ? (
                <tr>
                  <td colSpan={10} className="p-8 text-center text-slate-400">
                    No products matched your search or filters.
                  </td>
                </tr>
              ) : (
                products.map((p) => {
                  const badge = getRiskBadgeClasses(p.riskLevel);
                  const isExpiringUrgent = p.daysLeft <= 3;

                  return (
                    <tr
                      key={p.id}
                      className="hover:bg-slate-50/80 transition-colors group"
                    >
                      <td className="p-3">
                        <input
                          type="checkbox"
                          checked={selectedIds.includes(p.id)}
                          onChange={() => toggleSelectOne(p.id)}
                          className="rounded border-slate-300 text-emerald-800 focus:ring-emerald-500"
                        />
                      </td>

                      <td className="p-3">
                        <div className="font-bold text-slate-900 group-hover:text-emerald-800 transition-colors">
                          {p.name}
                        </div>
                        <div className="text-[11px] text-slate-400 font-mono">
                          {p.productId} {p.supplier ? `• ${p.supplier}` : ""}
                        </div>
                      </td>

                      <td className="p-3">
                        <span className="inline-block px-2 py-0.5 rounded-full bg-slate-100 text-slate-700 text-[11px] font-medium">
                          {p.category}
                        </span>
                      </td>

                      <td className="p-3 text-right font-semibold text-slate-800">
                        {p.quantity} <span className="text-[11px] font-normal text-slate-400">{p.unit}</span>
                      </td>

                      <td className="p-3 text-right">
                        <span className="font-semibold text-slate-900">₹{p.sellingPrice}</span>
                        {p.purchasePrice > 0 && (
                          <div className="text-[10px] text-slate-400">Cost: ₹{p.purchasePrice}</div>
                        )}
                      </td>

                      <td className="p-3 text-right font-medium text-slate-700">
                        {p.dailySalesRate} <span className="text-[11px] text-slate-400">/day</span>
                      </td>

                      <td className="p-3">
                        <div className={`inline-flex items-center gap-1 font-bold ${isExpiringUrgent ? "text-red-600" : "text-slate-700"}`}>
                          <Clock className="h-3.5 w-3.5" />
                          <span>{p.daysLeft}d left</span>
                        </div>
                        <div className="text-[10px] text-slate-400">Exp: {formatDate(p.expiryDate)}</div>
                      </td>

                      <td className="p-3">
                        <span
                          className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-semibold border ${badge.bg}`}
                        >
                          <span className={`h-1.5 w-1.5 rounded-full ${badge.dot}`} />
                          {p.riskLevel}
                        </span>
                        {p.potentialLoss > 0 && (
                          <div className="text-[10px] text-red-600 font-medium mt-0.5">
                            Risk: ₹{p.potentialLoss}
                          </div>
                        )}
                      </td>

                      <td className="p-3 text-slate-500 text-[11px]">
                        {p.storageCondition}
                      </td>

                      <td className="p-3 text-center">
                        <div className="flex items-center justify-center gap-1">
                          <button
                            onClick={() => {
                              setEditingProduct(p);
                              setIsProductModalOpen(true);
                            }}
                            className="p-1.5 rounded-lg text-slate-500 hover:text-emerald-800 hover:bg-emerald-50 transition-colors"
                            title="Edit product"
                          >
                            <Edit className="h-3.5 w-3.5" />
                          </button>
                          <button
                            onClick={() => handleDelete(p.id, p.name)}
                            className="p-1.5 rounded-lg text-slate-500 hover:text-red-700 hover:bg-red-50 transition-colors"
                            title="Delete product"
                          >
                            <Trash2 className="h-3.5 w-3.5" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>

        {/* Footer info */}
        <div className="px-4 py-3 border-t border-slate-100 bg-slate-50/50 flex items-center justify-between text-xs text-slate-500">
          <span>Showing {products.length} products in supermarket catalog</span>
          <span>Predictions synced with Random Forest service</span>
        </div>
      </div>

      {/* Edit / Add Modal */}
      <ProductFormModal
        isOpen={isProductModalOpen}
        onClose={() => setIsProductModalOpen(false)}
        onSuccess={fetchInventory}
        product={editingProduct}
      />

      {/* CSV Modal */}
      <CsvUploadModal
        isOpen={isCsvModalOpen}
        onClose={() => setIsCsvModalOpen(false)}
        onSuccess={fetchInventory}
      />
    </div>
  );
}
