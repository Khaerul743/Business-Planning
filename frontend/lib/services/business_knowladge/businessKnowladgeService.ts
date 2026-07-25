import { HttpClient } from "@/lib/http/httpClient";
import { NextRequest } from "next/server";
import { BaseBusinessKnowladge } from "./types";

class BusinessKnowladgeService extends HttpClient {
    async getAllBusinessKnowladges(request: NextRequest) {
        return this.sendRequestWithAuth(request, "/business_knowladge/me/all")
    }

    async postBusinessKnowladge(request: NextRequest, payload: BaseBusinessKnowladge) {
        return this.sendRequestWithAuth(request, "/business_knowladge/me", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) })
    }

    async updateBusinessKnowladge(request: NextRequest, businessKnowladgeId: string, payload: BaseBusinessKnowladge) {
        return this.sendRequestWithAuth(request, `/business_knowladge/me/${businessKnowladgeId}`, { method: "PUT", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) })
    }

    async delelteBusinessKnowladge(request: NextRequest, businessKnowladgeId: string) {
        return this.sendRequestWithAuth(request, `/business_knowladge/me/${businessKnowladgeId}`, { method: "DELETE" })
    }
}

export const businessKnowladgeService = new BusinessKnowladgeService()