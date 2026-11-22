import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";

export async function GET(req: NextRequest) {
  try {
    const { searchParams } = new URL(req.url);
    const format = searchParams.get("format") || "csv";

    const products = await prisma.product.findMany({
      include: {
        predictions: {
          orderBy: { predictedAt: "desc" },
          take: 1,
        },
      },
    });

    const now = new Date();
    const rows = products.map((p) => {
      const diffDays = Math.max(0, Math.ceil((new Date(p.expiryDate).getTime() - now.getTime()) / (1000 * 60 * 60 * 24)));
      const pred = p.predictions[0];
      return {
        productId: p.productId,
        name: p.name,
        category: p.category,
        quantity: p.quantity,
        unit: p.unit,
        purchasePrice: p.purchasePrice,
        sellingPrice: p.sellingPrice,
        dailySalesRate: p.dailySalesRate,
        daysLeft: diffDays,
        riskLevel: pred?.riskLevel || (diffDays <= 3 ? "High Risk" : "Low Risk"),
        wastageChance: `${pred?.wastageChance ?? 0}%`,
        expectedLeftover: pred?.leftover ?? 0,
        potentialLoss: `₹${pred?.potentialLoss ?? 0}`,
        recommendedAction: pred?.recommendedAction || "Normal retail velocity",
        storageCondition: p.storageCondition,
        supplier: p.supplier || "N/A",
      };
    });

    if (format === "json") {
      return NextResponse.json({ success: true, count: rows.length, data: rows });
    }

    // CSV format
    const headers = [
      "Product ID",
      "Product Name",
      "Category",
      "Quantity",
      "Unit",
      "Purchase Price",
      "Selling Price",
      "Daily Sales Rate",
      "Days Left",
      "Risk Level",
      "Wastage Chance",
      "Expected Leftover",
      "Potential Loss",
      "Recommended Action",
      "Storage Condition",
      "Supplier",
    ];

    const csvLines = [headers.join(",")];
    for (const r of rows) {
      const line = [
        `"${r.productId}"`,
        `"${r.name.replace(/"/g, '""')}"`,
        `"${r.category}"`,
        r.quantity,
        `"${r.unit}"`,
        r.purchasePrice,
        r.sellingPrice,
        r.dailySalesRate,
        r.daysLeft,
        `"${r.riskLevel}"`,
        `"${r.wastageChance}"`,
        r.expectedLeftover,
        `"${r.potentialLoss}"`,
        `"${r.recommendedAction.replace(/"/g, '""')}"`,
        `"${r.storageCondition}"`,
        `"${r.supplier}"`,
      ].join(",");
      csvLines.push(line);
    }

    const csvContent = csvLines.join("\n");

    return new NextResponse(csvContent, {
      status: 200,
      headers: {
        "Content-Type": "text/csv; charset=utf-8",
        "Content-Disposition": `attachment; filename="FreshWatch_Inventory_Report_${new Date().toISOString().slice(0, 10)}.csv"`,
      },
    });
  } catch (error: any) {
    return NextResponse.json({ success: false, error: error.message }, { status: 500 });
  }
}
