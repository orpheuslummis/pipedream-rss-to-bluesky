from atproto import Client, client_utils
import os
from typing import Dict, Any
import re


class BlueskyPoster:
    def __init__(self, handle: str, password: str):
        self.client = Client()
        self.handle = handle
        self.password = password

    def login(self) -> bool:
        """Login to Bluesky."""
        try:
            self.client.login(self.handle, self.password)
            return True
        except Exception as e:
            print(f"Login failed: {str(e)}")
            return False

    def create_post_text(self, title: str) -> client_utils.TextBuilder:
        """Create simple text for Bluesky post."""
        return client_utils.TextBuilder().text(title)

    def post(
        self, text: client_utils.TextBuilder, title: str, description: str, link: str
    ) -> Dict[str, Any]:
        """Post content to Bluesky with rich link preview."""
        try:
            # Clean up the description
            clean_description = re.sub(r"<[^>]+>", "", description)
            clean_description = " ".join(clean_description.split())
            if len(clean_description) > 300:
                clean_description = clean_description[:297] + "..."

            # Create external link embed with full metadata
            embed = {
                "$type": "app.bsky.embed.external",
                "external": {
                    "uri": link,
                    "title": title,
                    "description": clean_description,
                },
            }

            # Send post with embedded link
            result = self.client.send_post(text, embed=embed)

            return {"success": True, "uri": result.uri, "cid": result.cid}
        except Exception as e:
            return {"success": False, "error": str(e)}


def handler(pd: "pipedream"):
    """
    Pipedream handler for processing RSS entries and posting to Bluesky.
    """
    # Get Bluesky credentials
    handle = os.getenv("BSKY_HANDLE")
    password = os.getenv("BSKY_APP_PASSWORD")

    if not handle or not password:
        return {"success": False, "error": "Missing Bluesky credentials"}

    # Extract RSS entry data from trigger
    event = pd.steps["trigger"]["event"]
    title = event.get("title", "")
    description = event.get("description", "")
    link = event.get("link", "")

    # Initialize Bluesky poster
    poster = BlueskyPoster(handle, password)

    # Attempt login
    if not poster.login():
        return {"success": False, "error": "Failed to login to Bluesky"}

    # Create post text (just the title)
    text = poster.create_post_text(title)

    # Post to Bluesky with rich preview
    result = poster.post(text, title, description, link)

    # Return results for next step
    return {
        "success": result.get("success", False),
        "post_uri": result.get("uri"),
        "post_cid": result.get("cid"),
        "error": result.get("error"),
        "metadata": {
            "source": "rss",
            "original_guid": event.get("guid", ""),
            "author": event.get("author", ""),
            "pubdate": event.get("pubdate", ""),
        },
    }
