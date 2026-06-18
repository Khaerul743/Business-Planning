import { HttpClient } from "@/lib/http/httpClient";
import { NextRequest } from "next/server";

class WaService extends HttpClient {
    async getSessionStatus(request: NextRequest, business_id: string): Promise<Response> {
        return this.sendRequestWithAuth(request, `/whatsapp/session/${business_id}`);
    }

    async createSession(request: NextRequest, business_id: string): Promise<Response> {
        return this.sendRequestWithAuth(request, `/whatsapp/session`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ business_id })
        });
    }

    async deleteSession(request: NextRequest, business_id: string): Promise<Response> {
        return this.sendRequestWithAuth(request, `/whatsapp/session/${business_id}`, {
            method: "DELETE"
        });
    }

    async reconnectSession(request: NextRequest, business_id: string): Promise<Response> {
        return this.sendRequestWithAuth(request, `/whatsapp/session/reconnect/${business_id}`, {
            method: "POST"
        });
    }
}

export const waService = new WaService();
