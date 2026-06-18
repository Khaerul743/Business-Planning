export interface WaSessionResponse {
    business_id: string;
    session_id: string;
    status: "pending_qr" | "authenticating" | "connected" | "disconnected" | "destroyed";
    qr_code: string | null;
    metadata: {
        phone_number?: string;
        display_name?: string;
    } | null;
}
