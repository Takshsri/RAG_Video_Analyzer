import instaloader

L = instaloader.Instaloader()

# OPTIONAL LOGIN
# Replace with your Instagram username/password
# Better results after login

try:
    L.login("YOUR_INSTAGRAM_USERNAME", "YOUR_INSTAGRAM_PASSWORD")
except Exception as e:
    print("Instagram Login Failed:", e)


def get_instagram_transcript(url: str):

    return "Instagram transcript unavailable"


def get_instagram_metadata(url: str):

    try:

        shortcode = url.split("/reel/")[1].split("/")[0]

        post = instaloader.Post.from_shortcode(
            L.context,
            shortcode
        )

        views = getattr(post, "video_view_count", None)

        if views is None:
            views = 0

        likes = getattr(post, "likes", 0)
        comments = getattr(post, "comments", 0)

        creator = "Unknown"

        if post.owner_username:
            creator = post.owner_username
        print("Instagram shortcode:", shortcode)
        print("Views:", views)
        print("Likes:", likes)
        print("Comments:", comments)
        return {
            "views": views,
            "likes": likes,
            "comments": comments,
            "creator": creator
        }

    except Exception as e:

        print("Instagram Error:", str(e))

        return {
            "views": 0,
            "likes": 0,
            "comments": 0,
            "creator": "Unavailable"
        }