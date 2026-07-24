import { NextRequest, NextResponse } from "next/server";
import { businessService, UpdateBusinessPayload } from "@/lib/services/business/businessService";

export async function GET(request: NextRequest) {
    try {
        const res = await businessService.getCurrentBusiness(request);
        const data = await res.json();
        return NextResponse.json(data, { status: res.status });
    } catch (e: any) {
        return NextResponse.json({ status: "error", message: e.message }, { status: 500 });
    }
}

export async function PUT(request: NextRequest) {
    try {
        const payload: UpdateBusinessPayload = await request.json();
        const res = await businessService.updateBusiness(request, payload);
        const data = await res.json();
        return NextResponse.json(data, { status: res.status });
    } catch (e: any) {
        return NextResponse.json({ status: "error", message: e.message }, { status: 500 });
    }
}
