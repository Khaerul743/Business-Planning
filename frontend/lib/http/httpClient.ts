import { config } from "dotenv";
import { cookies } from "next/headers";
import type { NextRequest } from "next/server";
import { NextResponse } from "next/server";
import { ExternalServiceError, InternalServerError } from "../errors/appError";

config()
export class HttpClient {
  protected baseUrl: string;

  constructor() {
    // Isi dulu baru validasi
    const url = process.env.BACKEND_SERVICE_URL;
    if (!url) {
      console.error("BACKEND_SERVICE_URL not found inside .env");
      throw new InternalServerError();
    }
    this.baseUrl = url;
  }

  protected async sendRequest<T>(endpoint: string, option?: RequestInit): Promise<T> {
    const res = await fetch(`${this.baseUrl}/api${endpoint}`, {
      ...option,
      headers: {
        "Content-Type": "application/json",
        ...option?.headers,
      },
    });

    if (res.status >= 500) {
      throw new ExternalServiceError(res.status);
    }

    return res.json();
  }

  protected async sendRequestWithAuth<T>(request: NextRequest, endpoint: string, option?: RequestInit): Promise<Response> {
    const access_token = request.cookies.get("access_token")?.value
    const refresh_token = request.cookies.get("refresh_token")?.value
    if (!access_token && !refresh_token) {
      return new Response(
        JSON.stringify({ status: "error", message: "Unauthorized", code: "UNAUTHORIZED" }),
        { status: 401 }
      );
    }

    let res = await fetch(`${this.baseUrl}/api${endpoint}`, {
      ...option,
      headers: {
        Cookie: `access_token=${access_token}; refresh_token=${refresh_token}`,
        ...option?.headers,
      },
    });

    if (res.status === 401 && refresh_token) {
      const refreshRes = await fetch(`${this.baseUrl}/api/auth/refresh`, {
        method: "POST",
        headers: {
          Cookie: `refresh_token=${refresh_token}`,
        },
      });

      if (!refreshRes.ok) {
        console.log(await refreshRes.json())
        return NextResponse.json(
          { status: "error", message: "Session expired", code: "SESSION_EXPIRED" },
          { status: 401 }
        );
      }

      const refreshData = await refreshRes.json();

      // Langsung set cookie HTTP-only menggunakan next/headers
      const cookieStore = await cookies();

      // Jika Backend mengembalikan access_token di root (refreshData.access_token)
      // Sesuaikan jika ternyata Backend mengembalikan refreshData.data.access_token
      const newAccessToken = refreshData.access_token || refreshData.data?.access_token;

      if (newAccessToken) {
        cookieStore.set("access_token", newAccessToken, {
          httpOnly: true,
          path: "/",
          maxAge: 60 * 60, // 1 jam
        });
      }
      // retry request pakai token baru
      const retryRes = await fetch(`${this.baseUrl}/api${endpoint}`, {
        ...option,
        headers: {
          Cookie: `access_token=${newAccessToken}; refresh_token=${refresh_token}`,
          ...option?.headers,
        },
      });

      // Kembalikan langsung Response dari Backend, API Routes (route.ts) akan menghandlenya
      return retryRes;
    }

    return res
  }
}