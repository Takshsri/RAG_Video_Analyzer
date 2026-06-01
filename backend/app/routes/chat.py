from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    question: str

@router.post("/chat")
async def chat(data: ChatRequest):

    return {
        "answer": f"You asked: {data.question}"
    }