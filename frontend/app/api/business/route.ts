import { NextRequest, NextResponse } from "next/server";
import { businessService } from "@/lib/services/business/businessService";

export async function POST(request: NextRequest) {
    try {
        const body = await request.json();
        const res = await businessService.createBusiness(request, body);
        const data = await res.json();
        return NextResponse.json(data, { status: res.status });
    } catch (e: any) {
        return NextResponse.json({ status: "error", message: e.message }, { status: 500 });
    }
}
