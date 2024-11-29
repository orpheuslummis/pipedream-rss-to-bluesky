# pipedream-rss-to-bluesky

A Pipedream workflow component that automatically posts RSS feed entries to
Bluesky, complete with rich link previews and metadata.

## Features

- Automatically posts RSS feed entries to Bluesky
- Includes rich link previews with title and description
- Cleans up HTML from descriptions
- Handles authentication with Bluesky
- Preserves metadata from RSS feeds
- Truncates long descriptions appropriately

## Prerequisites

- A Bluesky account
- A Bluesky App Password
- A Pipedream account
- An RSS feed source configured in Pipedream

## Environment Variables

The following environment variables need to be set in your Pipedream workflow:

- `BSKY_HANDLE`: Your Bluesky handle (e.g., `username.bsky.social`)
- `BSKY_APP_PASSWORD`: Your Bluesky App Password

## Usage

1. Create a new Pipedream workflow
2. Add an RSS trigger source
3. Add a Python step and include this script
4. Configure the environment variables
5. Deploy and activate the workflow

## How It Works

The script processes RSS feed entries through the following steps:

1. Receives RSS entry data from the Pipedream trigger
2. Authenticates with Bluesky using provided credentials
3. Creates a post with the entry title
4. Adds a rich preview with the link, title, and cleaned description
5. Posts the content to Bluesky
6. Returns success/failure status and post metadata

## Response Format

The handler returns a JSON object containing:

```json
{
    "success": true/false,
    "post_uri": "at://...",
    "post_cid": "bafyre...",
    "error": "error message if any",
    "metadata": {
        "source": "rss",
        "original_guid": "original entry guid",
        "author": "entry author",
        "pubdate": "publication date"
    }
}
```
