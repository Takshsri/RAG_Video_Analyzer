from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from app.utils.chunking import chunk_text


embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector_store = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embedding_model
)


def store_transcript(transcript: str, video_id: str):

    chunks = chunk_text(transcript)

    documents = []

    metadatas = []

    ids = []

    for i, chunk in enumerate(chunks):

        documents.append(chunk)

        metadatas.append({
            "video_id": video_id,
            "chunk_id": i
        })

        ids.append(f"{video_id}_{i}")

    vector_store.add_texts(
        texts=documents,
        metadatas=metadatas,
        ids=ids
    )


def search_chunks(query: str):

    results = vector_store.similarity_search(
        query,
        k=4
    )

    return results