import { agentService } from "@/lib/services/agent/agentService";
import { AgentResponse } from "@/lib/services/agent/types";
import { SuccessResponse, type ErrorResponse } from "@/lib/services/responseType";
import { NextRequest, NextResponse } from "next/server";

export async function GET(request: NextRequest) {
    try {
        const res = await agentService.getAgent(request)
        const data = await res.json()
        if (!res.ok) {
            return NextResponse.json<ErrorResponse>({ code: data.code, message: data.message, status: data.status }, { status: res.status })
        }

        return NextResponse.json<SuccessResponse<AgentResponse>>(data, { status: res.status })
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



export async function PUT(request: NextRequest) {
    try {
        const body = await request.json();
        // Destructure only the fields we want to update (exclude enable_ai/status)
        const {
            name,
            fallback_email,
            base_prompt,
            llm_model,
            llm_provider,
            tone,
            temperature
        } = body;

        const payload = {
            name,
            fallback_email,
            base_prompt,
            llm_model,
            llm_provider,
            tone,
            temperature
        };

        const res = await agentService.updateAgent(request, payload as any);
        const data = await res.json();

        if (!res.ok) {
            return NextResponse.json<ErrorResponse>({ code: data.code, message: data.message, status: data.status }, { status: res.status })
        }

        return NextResponse.json<SuccessResponse<AgentResponse>>(data, { status: res.status })
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
        const body = await request.json();
        const res = await agentService.createAgent(request, body);
        const data = await res.json();
        
        if (!res.ok) {
            return NextResponse.json<ErrorResponse>({ code: data.code, message: data.message, status: data.status }, { status: res.status });
        }

        return NextResponse.json<SuccessResponse<AgentResponse>>(data, { status: res.status });
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