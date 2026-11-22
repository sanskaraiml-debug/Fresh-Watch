import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { predictSingle } from "@/lib/ml-client";

export async function GET(
  req: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const product = await prisma.product.findUnique({
      where: { id: params.id },
      include: {
        predictions: { orderBy: { predictedAt: "desc" }, take: 5 },
        alerts: { orderBy: { createdAt: "desc" } },
        pricingRecommendations: { orderBy: { createdAt: "desc" } },
      },
    });

    if (!product) {
      return NextResponse.json({ success: false, error: "Product not found" }, { status: 404 });
    }

    return NextResponse.json({ success: true, product });
  } catch (error: any) {
    return NextResponse.json({ success: false, error: error.message }, { status: 500 });
  }
}

export async function PUT(
  req: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const body = await req.json();
    const {
      name,
      category,
      quantity,
      unit,
      purchasePrice,
      sellingPrice,
      dailySalesRate,
      expiryDate,
      supplier,
      storageCondition,
    } = body;

    const data: any = {};
    if (name) data.name = name;
    if (category) data.category = category;
    if (quantity !== undefined) data.quantity = Number(quantity);
    if (unit) data.unit = unit;
    if (purchasePrice !== undefined) data.purchasePrice = Number(purchasePrice);
    if (sellingPrice !== undefined) data.sellingPrice = Number(sellingPrice);
    if (dailySalesRate !== undefined) data.dailySalesRate = Number(dailySalesRate);
    if (expiryDate) data.expiryDate = new Date(expiryDate);
    if (supplier !== undefined) data.supplier = supplier;
    if (storageCondition !== undefined) data.storageCondition = storageCondition;

    const updated = await prisma.product.update({
      where: { id: params.id },
      data,
    });

    // Re-run prediction
    const now = new Date();
    const daysLeft = Math.max(0, Math.ceil((new Date(updated.expiryDate).getTime() - now.getTime()) / (1000 * 60 * 60 * 24)));
    const predResult = await predictSingle({
      product: updated.name,
      stock: updated.quantity,
      daily_sales: updated.dailySalesRate,
      days_left: daysLeft,
      price: updated.sellingPrice,
      category: updated.category,
    });

    await prisma.prediction.create({
      data: {
        productId: updated.id,
        daysLeft,
        expectedSales: predResult.expected_sales,
        leftover: predResult.unsold_quantity,
        wastageChance: predResult.wastage_chance,
        riskLevel: predResult.risk_level,
        potentialLoss: predResult.potential_loss,
        recommendedAction: predResult.recommended_action,
      },
    });

    return NextResponse.json({ success: true, product: updated });
  } catch (error: any) {
    return NextResponse.json({ success: false, error: error.message }, { status: 500 });
  }
}

export async function DELETE(
  req: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    await prisma.product.delete({
      where: { id: params.id },
    });
    return NextResponse.json({ success: true, message: "Product deleted successfully" });
  } catch (error: any) {
    return NextResponse.json({ success: false, error: error.message }, { status: 500 });
  }
}
