from fastapi import APIRouter
from pydantic import BaseModel

from app.services.youtube_service import (
    get_youtube_transcript
)

from app.services.rag_service import (
    store_transcript
)

router = APIRouter()

class AnalyzeRequest(BaseModel):
    video_a: str
    video_b: str


@router.post("/analyze")
async def analyze_videos(data: AnalyzeRequest):

    transcript_a = get_youtube_transcript(data.video_a)

    transcript_b = get_youtube_transcript(data.video_b)

    store_transcript(transcript_a, "A")
    store_transcript(transcript_b, "B")

    return {
        "video_a": {
            "transcript_preview": transcript_a[:300],
            "transcript_length": len(transcript_a)
        },
        "video_b": {
            "transcript_preview": transcript_b[:300],
            "transcript_length": len(transcript_b)
        }
    }