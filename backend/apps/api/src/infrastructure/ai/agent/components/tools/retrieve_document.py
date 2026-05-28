from src.infrastructure.vectorstore.chroma_db import RAGSystem


class RetrieveDocumentTool:
    def __init__(self, chromadb_path: str, collection_name: str):
        self.chromadb_path: str = chromadb_path
        self.collection_name = collection_name
        self.rag = RAGSystem(self.chromadb_path)
        self.rag.initial_collection(collection_name)

    def read_document(self, query: str):
        """Gunakan tool untuk mencari informasi dokumen yang telah diberikan oleh pengguna. Pastikan kamu memasukan keyword yang sesuai dan sesuai konteks yang diminta oleh pengguna"""
        try:
            # get_document = self.rag.ask(query)
            get_document = None
            if not get_document:
                get_document = self.rag.similarity_search(query)
                if get_document == "":
                    get_document = "Tidak ada informasi relevan yang ditemukan."

            return get_document
        except Exception as e:
            print(f"Terjadi kesalahan di tool get_document: {e}")
            return f"Terjadi kesalahan saat query ke document {e}"
