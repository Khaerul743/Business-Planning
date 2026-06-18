import { HttpClient } from "@/lib/http/httpClient";
import { NextRequest } from "next/server";
import { UpdateAgent, CreateAgent } from "./types";

class AgentService extends HttpClient{
    async getAgent(request: NextRequest){
        return this.sendRequestWithAuth(request, "/agent/me")
    }
    async createAgent(request: NextRequest, payload: CreateAgent){
        return this.sendRequestWithAuth(request, "/agent", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        })
    }
    async updateAgent(request: NextRequest, payload: UpdateAgent){
        return this.sendRequestWithAuth(request,"/agent/me",{method: "PUT", body: JSON.stringify(payload)})
    }
    async invokeAgent(request: NextRequest, textMessage: string){
        return this.sendRequestWithAuth(request,"/agent/invoke/me", {method: "POST", body: JSON.stringify({"text_message": textMessage}), headers: {"Content-Type": "application/json"}})
    }   
}

export const agentService = new AgentService()