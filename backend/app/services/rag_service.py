from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from dotenv import load_dotenv
load_dotenv()
from app.utils.chunking import chunk_text

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector_store = Chroma(
    persist_directory="chroma_db",
    embedding_function=embedding_model
)

def store_transcript(transcript: str, video_id: str):

    chunks = chunk_text(transcript)

    documents = []

    for index, chunk in enumerate(chunks):

        documents.append(
            Document(
                page_content=chunk,
                metadata={
                    "video_id": video_id,
                    "chunk_id": index
                }
            )
        )

    vector_store.add_documents(documents)

def search_transcripts(query: str):

    results = vector_store.similarity_search(
        query,
        k=4
    )

    return results