from fastapi import APIRouter
from pydantic import BaseModel

from app.services.rag_service import search_chunks

router = APIRouter()

chat_history = []


class ChatRequest(BaseModel):
    question: str


@router.post("/chat")
async def chat(request: ChatRequest):

    question = request.question

    results = search_chunks(question)

    context = []

    references = []

    for item in results:

        context.append(item.page_content)

        references.append({
            "video": item.metadata.get("video_id"),
            "chunk": item.metadata.get("chunk_id")
        })

    answer = "\n\n".join(context[:2])

    chat_history.append({
        "question": question,
        "answer": answer
    })

    return {
        "answer": answer,
        "references": references,
        "history_length": len(chat_history)
    }