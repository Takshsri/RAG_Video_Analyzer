from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url: str):

    try:

        if "youtu.be/" in url:
            return url.split("youtu.be/")[1].split("?")[0]

        if "watch?v=" in url:
            return url.split("watch?v=")[1].split("&")[0]

        return None

    except Exception as e:

        print("Video ID Error:", e)

        return None


def get_youtube_transcript(video_url: str):

    try:

        video_id = extract_video_id(video_url)

        ytt_api = YouTubeTranscriptApi()

        transcript = ytt_api.fetch(video_id)

        full_text = " ".join(
            [chunk.text for chunk in transcript]
        )

        return full_text

    except Exception as e:

        print("Transcript Error:", e)

        return "Transcript unavailable"