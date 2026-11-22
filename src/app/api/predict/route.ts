import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { predictBatch, predictSingle } from "@/lib/ml-client";

export async function POST(req: NextRequest) {
  try {
    const body = await req.json().catch(() => ({}));
    const runAll = body.runAll === true;

    if (runAll) {
      // Run batch prediction across all database products
      const products = await prisma.product.findMany();
      const now = new Date();

      const items = products.map((p) => {
        const daysLeft = Math.max(0, Math.ceil((new Date(p.expiryDate).getTime() - now.getTime()) / (1000 * 60 * 60 * 24)));
        return {
          product: p.name,
          stock: p.quantity,
          daily_sales: p.dailySalesRate,
          days_left: daysLeft,
          price: p.sellingPrice,
          category: p.category,
          id: p.id,
        };
      });

      const batchResult = await predictBatch(items);

      // Save predictions to database
      for (let i = 0; i < items.length; i++) {
        const pred = batchResult.predictions[i];
        const item = items[i];

        await prisma.prediction.create({
          data: {
            productId: item.id,
            daysLeft: item.days_left,
            expectedSales: pred.expected_sales,
            leftover: pred.unsold_quantity,
            wastageChance: pred.wastage_chance,
            riskLevel: pred.risk_level,
            potentialLoss: pred.potential_loss,
            recommendedAction: pred.recommended_action,
          },
        });

        // If high risk, create alert if not already active
        if (pred.risk_level === "High Risk") {
          const existingAlert = await prisma.alert.findFirst({
            where: { productId: item.id, resolved: false },
          });

          if (!existingAlert) {
            await prisma.alert.create({
              data: {
                productId: item.id,
                title: `Expiry Risk: ${item.product}`,
                message: `${item.product} is at ${pred.wastage_chance}% risk of wastage with ${item.days_left} days left.`,
                riskLevel: "High",
              },
            });
          }
        }
      }

      return NextResponse.json({
        success: true,
        summary: {
          total: batchResult.total_items,
          highRisk: batchResult.high_risk_count,
          mediumRisk: batchResult.medium_risk_count,
          lowRisk: batchResult.low_risk_count,
          totalPotentialLoss: batchResult.total_potential_loss,
        },
        predictions: batchResult.predictions,
      });
    }

    // Single item simulation
    const { product, stock, daily_sales, days_left, price, category } = body;
    if (stock === undefined || daily_sales === undefined || days_left === undefined) {
      return NextResponse.json({ success: false, error: "Missing required fields" }, { status: 400 });
    }

    const result = await predictSingle({
      product: product || "Simulated Product",
      stock: Number(stock),
      daily_sales: Number(daily_sales),
      days_left: Number(days_left),
      price: Number(price || 0),
      category: category || "General",
    });

    return NextResponse.json({ success: true, result });
  } catch (error: any) {
    return NextResponse.json({ success: false, error: error.message }, { status: 500 });
  }
}
