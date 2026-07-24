import { analyticService } from "@/lib/services/analytic/analyticService";
import { SentimentAnalysisResponse } from "@/lib/services/analytic/types";
import { ErrorResponse, SuccessResponse } from "@/lib/services/responseType";
import { NextRequest, NextResponse } from "next/server";

export async function GET(request: NextRequest) {
    try {
        const res = await analyticService.getSentimentAnalysis(request);
        const data = await res.json();

        if (!res.ok) {
            return NextResponse.json<ErrorResponse>(
                { code: data.code, message: data.message, status: data.status },
                { status: res.status }
            );
        }

        return NextResponse.json<SuccessResponse<SentimentAnalysisResponse>>(data, { status: res.status });
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
