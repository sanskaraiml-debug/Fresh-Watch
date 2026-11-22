import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";

export async function GET() {
  try {
    const alerts = await prisma.alert.findMany({
      where: { resolved: false },
      include: {
        product: true,
      },
      orderBy: { createdAt: "desc" },
    });

    return NextResponse.json({ success: true, alerts });
  } catch (error: any) {
    return NextResponse.json({ success: false, error: error.message }, { status: 500 });
  }
}

export async function POST(req: NextRequest) {
  try {
    const { id, actionTaken } = await req.json();

    if (!id) {
      return NextResponse.json({ success: false, error: "Missing alert ID" }, { status: 400 });
    }

    const updated = await prisma.alert.update({
      where: { id },
      data: {
        resolved: true,
        actionTaken: actionTaken || "Acknowledged and resolved by manager",
      },
    });

    return NextResponse.json({ success: true, alert: updated });
  } catch (error: any) {
    return NextResponse.json({ success: false, error: error.message }, { status: 500 });
  }
}
