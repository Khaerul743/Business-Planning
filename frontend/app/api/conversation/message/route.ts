import { conversationService } from "@/lib/services/conversation/conversationService";
import { ConversationMessageResponse } from "@/lib/services/conversation/types";
import { ErrorResponse, SuccessResponse } from "@/lib/services/responseType";
import { NextRequest, NextResponse } from "next/server";

export async function GET(request: NextRequest) {
  try {
    const id = request.nextUrl.searchParams.get("id");
    if (!id) {
      return NextResponse.json<ErrorResponse>(
        { status: "error", code: "BAD_REQUEST", message: "ID is required" },
        { status: 400 }
      );
    }

    const results = await Promise.allSettled([
      conversationService.getConversationMessages(request, id),
      conversationService.getConversationStatusAgent(request, id)
    ]);

    const [messagesResult, convStatusAgentResult] = results;

    // 🔴 1. Cek jika ada 401 Unauthorized
    for (const result of results) {
      if (result.status === "fulfilled" && result.value.status === 401) {
        const data = await result.value.json().catch(() => ({}));
        return NextResponse.json<ErrorResponse>(
          {
            status: data.status || "error",
            code: data.code || "UNAUTHORIZED",
            message: data.message || "Unauthorized"
          },
          { status: 401 }
        );
      }
    }

    // 🟢 2. Parse data normal (graceful)
    let messages = [];
    let convStatusAgent = true;

    if (messagesResult.status === "fulfilled" && messagesResult.value.ok) {
      const data = await messagesResult.value.json();
      messages = data.data || [];
    }

    if (convStatusAgentResult.status === "fulfilled" && convStatusAgentResult.value.ok) {
      const data = await convStatusAgentResult.value.json();
      convStatusAgent = data.data?.customer_status_agent ?? true;
    }

    return NextResponse.json<SuccessResponse<ConversationMessageResponse>>({
      status: "success",
      message: "Get messages is successfully",
      data: {
        messages,
        convStatusAgent
      }
    });
  } catch (error: any) {
    return NextResponse.json<ErrorResponse>(
      {
        status: "error",
        message: error.message || "Internal server error",
        code: "INTERNAL_SERVER_ERROR"
      },
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest) {
  try {
    const id = request.nextUrl.searchParams.get("id");
    if (!id) {
      return NextResponse.json<ErrorResponse>(
        { status: "error", code: "BAD_REQUEST", message: "ID is required" },
        { status: 400 }
      );
    }
    const body = await request.json();
    const { text_message } = body;
    const res = await conversationService.postHumanMessage(request, id, text_message);
    const data = await res.json();
    if (!res.ok) {
      return NextResponse.json<ErrorResponse>(data, { status: res.status });
    }
    return NextResponse.json(data, { status: res.status });
  } catch (error: any) {
    return NextResponse.json<ErrorResponse>(
      {
        status: "error",
        message: error.message || "Internal server error",
        code: "INTERNAL_SERVER_ERROR"
      },
      { status: 500 }
    );
  }
}