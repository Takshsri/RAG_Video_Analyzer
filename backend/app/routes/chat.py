
from fastapi import APIRouter
from pydantic import BaseModel
from groq import Groq
import os

from app.services.rag_service import search_transcripts

router = APIRouter()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

class ChatRequest(BaseModel):
    question: str
    metadata_a: dict = {}
    metadata_b: dict = {}

@router.post("/chat")
async def chat(data: ChatRequest):

    docs = search_transcripts(data.question)

    context = "\n\n".join([
        doc.page_content for doc in docs
    ])

    metadata_context = f"""
VIDEO A METADATA:
Views: {data.metadata_a.get("views")}
Likes: {data.metadata_a.get("likes")}
Comments: {data.metadata_a.get("comments")}
Creator: {data.metadata_a.get("creator")}
Engagement Rate: {data.metadata_a.get("engagement_rate")}

VIDEO B METADATA:
Views: {data.metadata_b.get("views")}
Likes: {data.metadata_b.get("likes")}
Comments: {data.metadata_b.get("comments")}
Creator: {data.metadata_b.get("creator")}
Engagement Rate: {data.metadata_b.get("engagement_rate")}
"""

    prompt = f"""
You are an advanced AI RAG video analysis assistant.

You must answer using:
1. Transcript chunks
2. Metadata
3. Engagement metrics

IMPORTANT:
- Compare both videos
- Mention exact views, likes, comments if available
- Explain which video performed better
- Keep answers short and intelligent
- Never say "cannot determine" if metadata exists

QUESTION:
{data.question}

METADATA:
{metadata_context}

TRANSCRIPT CONTEXT:
{context}

ANSWER:
"""

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.4
    )

    answer = completion.choices[0].message.content

    references = []

    for doc in docs:
        references.append({
            "video": doc.metadata.get("video_id"),
            "chunk": doc.metadata.get("chunk_id")
        })

    return {
        "answer": answer,
        "references": references
    }

