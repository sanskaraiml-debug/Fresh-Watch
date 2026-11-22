import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";

export async function GET() {
  try {
    let settings = await prisma.storeSetting.findFirst();

    if (!settings) {
      settings = await prisma.storeSetting.create({
        data: {
          storeName: "FreshWatch Supermarket",
          currency: "₹",
          highRiskThreshold: 75.0,
          mediumRiskThreshold: 45.0,
          autoDiscountEnabled: true,
          defaultDiscountPct: 20.0,
        },
      });
    }

    // Check ML service status
    const ML_SERVICE_URL = process.env.ML_SERVICE_URL || "http://127.0.0.1:8000";
    let mlStatus = "offline";
    try {
      const res = await fetch(`${ML_SERVICE_URL}/health`, { signal: AbortSignal.timeout(1000) });
      if (res.ok) mlStatus = "online";
    } catch {}

    const groqConfigured = Boolean(
      process.env.GROQ_API_KEY &&
      process.env.GROQ_API_KEY !== "gsk_placeholder_replace_with_your_key"
    );

    return NextResponse.json({
      success: true,
      settings,
      systemStatus: {
        database: "connected",
        mlService: mlStatus,
        groqConfigured,
        nodeVersion: process.version,
      },
    });
  } catch (error: any) {
    return NextResponse.json({ success: false, error: error.message }, { status: 500 });
  }
}

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const {
      storeName,
      currency,
      highRiskThreshold,
      mediumRiskThreshold,
      autoDiscountEnabled,
      defaultDiscountPct,
    } = body;

    let settings = await prisma.storeSetting.findFirst();

    if (settings) {
      settings = await prisma.storeSetting.update({
        where: { id: settings.id },
        data: {
          ...(storeName && { storeName }),
          ...(currency && { currency }),
          ...(highRiskThreshold !== undefined && { highRiskThreshold: Number(highRiskThreshold) }),
          ...(mediumRiskThreshold !== undefined && { mediumRiskThreshold: Number(mediumRiskThreshold) }),
          ...(autoDiscountEnabled !== undefined && { autoDiscountEnabled: Boolean(autoDiscountEnabled) }),
          ...(defaultDiscountPct !== undefined && { defaultDiscountPct: Number(defaultDiscountPct) }),
        },
      });
    }

    return NextResponse.json({ success: true, settings });
  } catch (error: any) {
    return NextResponse.json({ success: false, error: error.message }, { status: 500 });
  }
}
