import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { predictSingle } from "@/lib/ml-client";

export async function GET(req: NextRequest) {
  try {
    const { searchParams } = new URL(req.url);
    const search = searchParams.get("search") || "";
    const category = searchParams.get("category") || "";
    const riskLevel = searchParams.get("risk") || "";
    const sortBy = searchParams.get("sortBy") || "createdAt";
    const sortOrder = searchParams.get("sortOrder") === "asc" ? "asc" : "desc";

    const where: any = {};

    if (search) {
      where.OR = [
        { name: { contains: search } },
        { productId: { contains: search } },
        { supplier: { contains: search } },
      ];
    }

    if (category && category !== "All") {
      where.category = category;
    }

    const products = await prisma.product.findMany({
      where,
      include: {
        predictions: {
          orderBy: { predictedAt: "desc" },
          take: 1,
        },
      },
      orderBy: { [sortBy]: sortOrder },
    });

    const now = new Date();
    let enriched = products.map((p) => {
      const diffDays = Math.max(0, Math.ceil((new Date(p.expiryDate).getTime() - now.getTime()) / (1000 * 60 * 60 * 24)));
      const pred = p.predictions[0];
      return {
        ...p,
        daysLeft: diffDays,
        riskLevel: pred?.riskLevel || (diffDays <= 3 ? "High Risk" : diffDays <= 7 ? "Medium Risk" : "Low Risk"),
        wastageChance: pred?.wastageChance ?? 0,
        expectedSales: pred?.expectedSales ?? Math.round(p.dailySalesRate * diffDays),
        leftover: pred?.leftover ?? Math.max(0, p.quantity - (p.dailySalesRate * diffDays)),
        potentialLoss: pred?.potentialLoss ?? (pred?.riskLevel === "High Risk" ? p.sellingPrice * p.quantity : 0),
        recommendedAction: pred?.recommendedAction || "Monitor inventory velocity",
      };
    });

    if (riskLevel && riskLevel !== "All") {
      enriched = enriched.filter((p) => p.riskLevel.toLowerCase().includes(riskLevel.toLowerCase()));
    }

    const categories = await prisma.product.findMany({
      select: { category: true },
      distinct: ["category"],
    });

    return NextResponse.json({
      success: true,
      count: enriched.length,
      categories: categories.map((c) => c.category),
      products: enriched,
    });
  } catch (error: any) {
    return NextResponse.json({ success: false, error: error.message }, { status: 500 });
  }
}

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();

    // Check if bulk CSV import
    if (body.bulk && Array.isArray(body.items)) {
      const createdItems = [];
      const now = new Date();

      for (const item of body.items) {
        if (!item.name || !item.quantity) continue;
        const daysLeft = Number(item.daysLeft || item.days_left || 7);
        const expiry = new Date(now);
        expiry.setDate(expiry.getDate() + daysLeft);

        const prodId = item.productId || `SKU-${Math.floor(1000 + Math.random() * 9000)}`;

        const product = await prisma.product.create({
          data: {
            productId: prodId,
            name: String(item.name).trim(),
            category: String(item.category || "General").trim(),
            quantity: Number(item.quantity || 0),
            unit: String(item.unit || "units"),
            purchasePrice: Number(item.purchasePrice || item.purchase_price || 0),
            sellingPrice: Number(item.price || item.sellingPrice || 0),
            dailySalesRate: Number(item.dailySalesRate || item.daily_sales || 1.0),
            expiryDate: expiry,
            supplier: item.supplier || "Direct Supply",
            storageCondition: item.storageCondition || "Ambient",
          },
        });

        // Generate prediction
        const predResult = await predictSingle({
          product: product.name,
          stock: product.quantity,
          daily_sales: product.dailySalesRate,
          days_left: daysLeft,
          price: product.sellingPrice,
          category: product.category,
        });

        await prisma.prediction.create({
          data: {
            productId: product.id,
            daysLeft: daysLeft,
            expectedSales: predResult.expected_sales,
            leftover: predResult.unsold_quantity,
            wastageChance: predResult.wastage_chance,
            riskLevel: predResult.risk_level,
            potentialLoss: predResult.potential_loss,
            recommendedAction: predResult.recommended_action,
          },
        });

        createdItems.push(product);
      }

      return NextResponse.json({
        success: true,
        message: `Successfully imported ${createdItems.length} products.`,
        importedCount: createdItems.length,
      });
    }

    // Single product creation
    const {
      productId,
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

    if (!name || quantity === undefined || sellingPrice === undefined || !expiryDate) {
      return NextResponse.json(
        { success: false, error: "Missing required fields (name, quantity, sellingPrice, expiryDate)" },
        { status: 400 }
      );
    }

    const prodId = productId || `SKU-${Math.floor(1000 + Math.random() * 9000)}`;
    const now = new Date();
    const expiry = new Date(expiryDate);
    const daysLeft = Math.max(0, Math.ceil((expiry.getTime() - now.getTime()) / (1000 * 60 * 60 * 24)));

    const product = await prisma.product.create({
      data: {
        productId: prodId,
        name,
        category: category || "General",
        quantity: Number(quantity),
        unit: unit || "units",
        purchasePrice: Number(purchasePrice || 0),
        sellingPrice: Number(sellingPrice),
        dailySalesRate: Number(dailySalesRate || 1.0),
        expiryDate: expiry,
        supplier: supplier || "Direct Supply",
        storageCondition: storageCondition || "Ambient",
      },
    });

    const predResult = await predictSingle({
      product: product.name,
      stock: product.quantity,
      daily_sales: product.dailySalesRate,
      days_left: daysLeft,
      price: product.sellingPrice,
      category: product.category,
    });

    const prediction = await prisma.prediction.create({
      data: {
        productId: product.id,
        daysLeft,
        expectedSales: predResult.expected_sales,
        leftover: predResult.unsold_quantity,
        wastageChance: predResult.wastage_chance,
        riskLevel: predResult.risk_level,
        potentialLoss: predResult.potential_loss,
        recommendedAction: predResult.recommended_action,
      },
    });

    return NextResponse.json({
      success: true,
      product: { ...product, prediction },
    });
  } catch (error: any) {
    return NextResponse.json({ success: false, error: error.message }, { status: 500 });
  }
}
