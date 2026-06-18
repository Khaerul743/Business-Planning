from fastapi import WebSocket
from collections import defaultdict


class ConnectionManager:
    def __init__(self):
        self.active_connections = defaultdict(list)

    async def connect(self, business_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[business_id].append(websocket)

    def disconnect(self, business_id: str, websocket: WebSocket):
        if websocket in self.active_connections[business_id]:
            self.active_connections[business_id].remove(websocket)

        if not self.active_connections[business_id]:
            del self.active_connections[business_id]

    async def send_to_business(self, business_id: str, data: dict):
        if business_id not in self.active_connections:
            return

        dead_connections = []

        for ws in self.active_connections[business_id]:
            try:
                await ws.send_json(data)
            except:
                dead_connections.append(ws)

        for ws in dead_connections:
            self.disconnect(business_id, ws)


manager = ConnectionManager()