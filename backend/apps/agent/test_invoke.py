import asyncio
from langgraph_sdk import get_client

async def main():
    # Inisialisasi client yang mengarah ke local server
    client = get_client(url="http://127.0.0.1:2024")
    
    # Membuat thread baru (thread digunakan untuk menyimpan conversation history / state)
    thread = await client.threads.create()
    print(f"Created thread: {thread['thread_id']}")
    
    # Input state awal, sesuai dengan BaseAgentStateModel dan tipe input yang dibutuhkan
    inputs = {
        "messages": [
            {
                "role": "user", 
                "content": "Halo, saya ingin bertanya tentang produk Anda."
            }
        ],
        "user_message": "Halo, saya ingin bertanya tentang produk Anda."
    }
    
    # Runtime context / config
    # Berisi parameter yang dibutuhkan oleh `get_context` node (ContextAgent)
    # Pastikan menggunakan format string UUID yang valid untuk database
    config = {
        "configurable": {
            "business_id": "06a8a34c-12f8-42c6-bf09-33f2e3a08171", # Ganti dengan UUID business
            "agent_id": "a04b8eb2-3b32-44e2-9a6a-bbca2c23ab58"    # Ganti dengan UUID agent
        }
    }
    
    print("Menjalankan graph...")
    
    # Kita menggunakan runs.stream untuk melihat step-by-step update dari setiap node
    # assistant_id adalah nama graph yang didefinisikan di langgraph.json ("agent")
    async for chunk in client.runs.stream(
        thread_id=thread["thread_id"],
        assistant_id="agent",
        input=inputs,
        config=config,
        stream_mode="updates"
    ):
        if chunk.event == "updates":
            print(f"\nUpdate dari Node:")
            for node_name, state_update in chunk.data.items():
                print(f"[{node_name}] -> {state_update}")

if __name__ == "__main__":
    asyncio.run(main())
