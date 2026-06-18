import { HttpClient } from "@/lib/http/httpClient";
import { NextRequest } from "next/server";

export interface AddBusinessPayload {
    name: string;
    owner_name?: string;
    phone_number: string;
    description: string;
    address: string;
}

class BusinessService extends HttpClient {
    async getCustomers(request: NextRequest): Promise<Response> {
        return this.sendRequestWithAuth(request, "/business/customers/me");
    }

    async getCurrentBusiness(request: NextRequest): Promise<Response> {
        return this.sendRequestWithAuth(request, "/business/me");
    }

    async createBusiness(request: NextRequest, payload: AddBusinessPayload): Promise<Response> {
        return this.sendRequestWithAuth(request, "/business", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });
    }
}

export const businessService = new BusinessService();
