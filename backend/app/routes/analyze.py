from fastapi import APIRouter
from pydantic import BaseModel

from app.services.youtube_service import (
    get_youtube_transcript,
    get_youtube_metadata
)

from app.services.instagram_service import (
    get_instagram_transcript,
    get_instagram_metadata
)

from app.services.rag_service import (
    store_transcript
)

router = APIRouter()


class AnalyzeRequest(BaseModel):
    video_a: str
    video_b: str


def is_instagram_url(url: str):

    return "instagram.com" in url


@router.post("/analyze")
async def analyze_videos(data: AnalyzeRequest):

    # VIDEO A

    if is_instagram_url(data.video_a):

        transcript_a = get_instagram_transcript(
            data.video_a
        )

        metadata_a = get_instagram_metadata(
            data.video_a
        )

    else:

        transcript_a = get_youtube_transcript(
            data.video_a
        )

        metadata_a = get_youtube_metadata(
            data.video_a
        )

    # VIDEO B

    if is_instagram_url(data.video_b):

        transcript_b = get_instagram_transcript(
            data.video_b
        )

        metadata_b = get_instagram_metadata(
            data.video_b
        )

    else:

        transcript_b = get_youtube_transcript(
            data.video_b
        )

        metadata_b = get_youtube_metadata(
            data.video_b
        )

    # STORE TRANSCRIPTS

    if transcript_a != "Transcript unavailable":
        store_transcript(transcript_a, "A")

    if transcript_b != "Transcript unavailable":
        store_transcript(transcript_b, "B")

    # SAFE DEFAULTS

    metadata_a.setdefault("views", 0)
    metadata_a.setdefault("likes", 0)
    metadata_a.setdefault("comments", 0)

    metadata_b.setdefault("views", 0)
    metadata_b.setdefault("likes", 0)
    metadata_b.setdefault("comments", 0)

    # ENGAGEMENT

    engagement_a = 0
    engagement_b = 0

    if metadata_a["views"] > 0:

        engagement_a = (
            (
                metadata_a["likes"] +
                metadata_a["comments"]
            ) / metadata_a["views"]
        ) * 100

    if metadata_b["views"] > 0:

        engagement_b = (
            (
                metadata_b["likes"] +
                metadata_b["comments"]
            ) / metadata_b["views"]
        ) * 100

    metadata_a["engagement_rate"] = round(
        engagement_a,
        2
    )

    metadata_b["engagement_rate"] = round(
        engagement_b,
        2
    )

    return {

        "video_a": {

            "transcript_preview":
                transcript_a[:300],

            "transcript_length":
                len(transcript_a),

            "metadata":
                metadata_a,

            "engagement_rate":
                round(engagement_a, 2)
        },

        "video_b": {

            "transcript_preview":
                transcript_b[:300],

            "transcript_length":
                len(transcript_b),

            "metadata":
                metadata_b,

            "engagement_rate":
                round(engagement_b, 2)
        }
    }