import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url: str):

    if "watch?v=" in url:
        return url.split("watch?v=")[1].split("&")[0]

    if "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]

    return None


def get_youtube_transcript(url: str):

    try:
        video_id = extract_video_id(url)

        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        full_text = " ".join([
            item["text"] for item in transcript
        ])

        return full_text

    except Exception:
        return "Transcript unavailable"


def get_youtube_metadata(url: str):

    try:
        ydl_opts = {
            "quiet": True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(url, download=False)

            views = info.get("view_count", 0)
            likes = info.get("like_count", 0)
            comments = info.get("comment_count", 0)

            engagement_rate = 0

            if views > 0:
                engagement_rate = (
                    (likes + comments) / views
                ) * 100

            return {
                "title": info.get("title"),
                "channel": info.get("uploader"),
                "views": views,
                "likes": likes,
                "comments": comments,
                "duration": info.get("duration"),
                "engagement_rate": round(
                    engagement_rate,
                    2
                )
            }

    except Exception as e:

        return {
            "error": str(e)
        }