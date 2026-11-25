import { NextRequest, NextResponse } from "next/server";
import { askInventoryAnalysisAssistant } from "@/lib/groq";
import { prisma } from "@/lib/prisma";

export async function POST(req: NextRequest) {
  try {
    const { prompt, history } = await req.json();

    if (!prompt || typeof prompt !== "string" || !prompt.trim()) {
      return NextResponse.json({ success: false, error: "Prompt is required" }, { status: 400 });
    }

    // Save user message to database
    await prisma.chatMessage.create({
      data: {
        role: "user",
        content: prompt.trim(),
      },
    });

    // Query Groq with grounded inventory
    const response = await askInventoryAnalysisAssistant(prompt.trim(), history || []);

    // Save assistant response to database
    await prisma.chatMessage.create({
      data: {
        role: "assistant",
        content: response,
      },
    });

    return NextResponse.json({
      success: true,
      response,
    });
  } catch (error: any) {
    return NextResponse.json({ success: false, error: error.message }, { status: 500 });
  }
}

export async function GET() {
  try {
    const messages = await prisma.chatMessage.findMany({
      orderBy: { createdAt: "desc" },
      take: 20,
    });

    return NextResponse.json({
      success: true,
      messages: messages.reverse(),
    });
  } catch (error: any) {
    return NextResponse.json({ success: false, error: error.message }, { status: 500 });
  }
}
