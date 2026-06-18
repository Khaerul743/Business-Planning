import { NextRequest, NextResponse } from "next/server";
import { businessService } from "@/lib/services/business/businessService";
import { waService } from "@/lib/services/wa/waService";

export async function GET(request: NextRequest) {
    try {
        const bRes = await businessService.getCurrentBusiness(request);
        const bData = await bRes.json();
        if (!bRes.ok) return NextResponse.json(bData, { status: bRes.status });
        const business_id = bData.data?.id;

        if (!business_id) throw new Error("Business ID not found");

        const res = await waService.getSessionStatus(request, business_id);
        const data = await res.json();
        return NextResponse.json(data, { status: res.status });
    } catch (e: any) {
        return NextResponse.json({ status: "error", message: e.message }, { status: 500 });
    }
}

export async function POST(request: NextRequest) {
    try {
        const bRes = await businessService.getCurrentBusiness(request);
        const bData = await bRes.json();
        if (!bRes.ok) return NextResponse.json(bData, { status: bRes.status });
        const business_id = bData.data?.id;

        if (!business_id) throw new Error("Business ID not found");

        const res = await waService.createSession(request, business_id);
        const data = await res.json();
        return NextResponse.json(data, { status: res.status });
    } catch (e: any) {
        return NextResponse.json({ status: "error", message: e.message }, { status: 500 });
    }
}

export async function DELETE(request: NextRequest) {
    try {
        const bRes = await businessService.getCurrentBusiness(request);
        const bData = await bRes.json();
        if (!bRes.ok) return NextResponse.json(bData, { status: bRes.status });
        const business_id = bData.data?.id;

        if (!business_id) throw new Error("Business ID not found");

        const res = await waService.deleteSession(request, business_id);
        const data = await res.json();
        return NextResponse.json(data, { status: res.status });
    } catch (e: any) {
        return NextResponse.json({ status: "error", message: e.message }, { status: 500 });
    }
}
