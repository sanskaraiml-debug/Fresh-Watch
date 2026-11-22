import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";

export async function GET() {
  try {
    const recommendations = await prisma.pricingRecommendation.findMany({
      include: {
        product: true,
      },
      orderBy: { createdAt: "desc" },
    });

    return NextResponse.json({
      success: true,
      recommendations,
    });
  } catch (error: any) {
    return NextResponse.json({ success: false, error: error.message }, { status: 500 });
  }
}

export async function POST(req: NextRequest) {
  try {
    const { id, action } = await req.json();

    if (!id || !action) {
      return NextResponse.json({ success: false, error: "Missing recommendation ID or action" }, { status: 400 });
    }

    const rec = await prisma.pricingRecommendation.findUnique({
      where: { id },
      include: { product: true },
    });

    if (!rec) {
      return NextResponse.json({ success: false, error: "Recommendation not found" }, { status: 404 });
    }

    if (action === "apply") {
      // Update product's sellingPrice to suggestedPrice and mark recommendation Applied
      await prisma.$transaction([
        prisma.product.update({
          where: { id: rec.productId },
          data: { sellingPrice: rec.suggestedPrice },
        }),
        prisma.pricingRecommendation.update({
          where: { id },
          data: { status: "Applied" },
        }),
      ]);

      return NextResponse.json({
        success: true,
        message: `Applied ${rec.discountPct}% discount on ${rec.product.name}. New selling price is ₹${rec.suggestedPrice}.`,
      });
    }

    if (action === "dismiss") {
      await prisma.pricingRecommendation.update({
        where: { id },
        data: { status: "Dismissed" },
      });

      return NextResponse.json({
        success: true,
        message: "Recommendation dismissed.",
      });
    }

    return NextResponse.json({ success: false, error: "Invalid action" }, { status: 400 });
  } catch (error: any) {
    return NextResponse.json({ success: false, error: error.message }, { status: 500 });
  }
}
