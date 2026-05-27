import { HttpClient } from "@/lib/http/httpClient";
import type { NextRequest } from "next/server";

class UserService extends HttpClient {
    async getCurrentUser(request: NextRequest): Promise<Response> {
        return this.sendRequestWithAuth(request, "/user/me")
    }
}

export const userService = new UserService()