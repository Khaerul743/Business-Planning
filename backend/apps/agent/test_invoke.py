import asyncio
from langgraph_sdk import get_client
from uuid import UUID
from langsmith import uuid7

async def main():
    # Inisialisasi client yang mengarah ke local server
    client = get_client(url="http://127.0.0.1:2024")

    # Membuat thread baru (thread digunakan untuk menyimpan conversation history / state)
    custom_thread_id = str(uuid7())
    thread = await client.threads.create(thread_id=custom_thread_id)

    # Input state awal, sesuai dengan BaseAgentStateModel dan tipe input yang dibutuhkan
    inputs = {"messages": [], "user_message": "metode pembayarannya apa?"}

    # Runtime context / config
    # Berisi parameter yang dibutuhkan oleh `get_context` node (ContextAgent)
    # Pastikan menggunakan format string UUID yang valid untuk database
    config = {
        "configurable": {
            "business_id": "06a8a34c-12f8-42c6-bf09-33f2e3a08171",  # Ganti dengan UUID business
            "agent_id": "a04b8eb2-3b32-44e2-9a6a-bbca2c23ab58",  # Ganti dengan UUID agent
        }
    }

    print("Menjalankan graph...")

    # Kita menggunakan runs.stream untuk melihat step-by-step update dari setiap node
    # assistant_id adalah nama graph yang didefinisikan di langgraph.json ("agent")
    # async for chunk in client.runs.stream(
    #     thread_id=thread["thread_id"],
    #     assistant_id="agent",
    #     input=inputs,
    #     config=config,
    #     stream_mode="updates",
    # ):
    #     if chunk.event == "updates":
    #         print(f"\nUpdate dari Node:")
    #         for node_name, state_update in chunk.data.items():
    #             print(f"[{node_name}] -> {state_update}")
    raw_data = [{'ai_response': 'Maaf, sepertinya saya belum ada informasi terkait dengan yang ada tanyakan', 'user_message': 'apakah restoran ini menjual narkoba?', 'category': 'produk', 'is_business_related': True, 'knowledge_gap_detected': True}]
    result =await client.runs.wait(
        thread_id=thread["thread_id"],
        assistant_id="gap_analysis_agent",
        input={"messages": [], "user_message": "", "raw_data": raw_data, "business_description": "Ayam Bakar Naufal adalah usaha kuliner rumahan yang menyajikan berbagai menu ayam bakar dengan bumbu khas nusantara. Selain ayam bakar, tersedia juga beberapa pilihan lauk pendamping seperti ayam goreng, ikan bakar, dan aneka sambal. "},
        config=config
    )

    print(result)
    # while True:
    #     input_message = input("User: ")
    #     inputs = {"messages": [], "user_message": input_message}
    #     if input_message.lower() == "exit":
    #         print("\n" + "="*50)
    #         print("📜 MENGAMBIL HISTORY STATE MESSAGES 📜")
    #         print("="*50)
    #         try:
    #             # state = await client.threads.get_state(thread["thread_id"])
                
    #             # Handling jika state berupa dictionary atau object
    #             state_values = state.get("values", {}) if isinstance(state, dict) else getattr(state, "values", {})
    #             messages = state_values.get("messages", [])
                
    #             for msg in messages:
    #                 # Message biasanya dictionary di sdk response
    #                 if isinstance(msg, dict):
    #                     msg_type = msg.get("type", "")
    #                     content = msg.get("content", "")
    #                     tool_calls = msg.get("tool_calls", [])
    #                     name = msg.get("name", "")
    #                 else:
    #                     msg_type = getattr(msg, "type", "")
    #                     content = getattr(msg, "content", "")
    #                     tool_calls = getattr(msg, "tool_calls", [])
    #                     name = getattr(msg, "name", "")
                    
    #                 if not content and not tool_calls:
    #                     continue
                        
    #                 if msg_type == "human":
    #                     print(f"👤 Human: {content}\n")
    #                 elif msg_type == "ai":
    #                     tool_str = ""
    #                     if tool_calls:
    #                         tool_names = ", ".join([tc.get("name", "") if isinstance(tc, dict) else getattr(tc, "name", "") for tc in tool_calls])
    #                         tool_str = f" [🛠️ Menggunakan tool: {tool_names}]"
    #                     print(f"🤖 AI{tool_str}: {content}\n")
    #                 elif msg_type == "tool":
    #                     print(f"   🔧 Tool Message ({name}): {content}\n")
    #                 elif msg_type == "system":
    #                     # Mengabaikan system message agar terminal tidak terlalu penuh
    #                     pass
    #                 else:
    #                     print(f"📝 {msg_type.capitalize()}: {content}\n")
    #         except Exception as e:
    #             print(f"Gagal mengambil history state: {e}")
            
    #         print("="*50)
    #         print("👋 Program dihentikan.")
    #         break

    #     result =await client.runs.wait(
    #         thread_id=thread["thread_id"],
    #         assistant_id="customer_service_agent",
    #         input=inputs,
    #         config=config
    #     )
    #     print(f"AI: {result["response"]}")
    #     print(f"Sentiment: {result["sentiment"]}")
    #     print(f"category: {result["category"]}")
    #     print(f"business_related: {result["is_business_related"]}")
    #     print(f"gap detected: {result["knowledge_gap_detected"]}")
    #     print(f"Fallback_Human: {result["fallback_human"]}")
    #     print(f"Token Usage: {result["token_usage"]}")


if __name__ == "__main__":
    asyncio.run(main())
