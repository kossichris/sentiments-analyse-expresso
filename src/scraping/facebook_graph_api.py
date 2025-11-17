"""
Scraping Facebook posts using the official Graph API.
Requires: requests, pandas

Usage:
    python src/scraping/facebook_graph_api.py
"""
import requests
import pandas as pd
from datetime import datetime

# === CONFIGURATION ===
ACCESS_TOKEN = "EAALFRNhFpEkBP3xwnSIaZAjDkNZAF2ZCEA1mAI177sr9kx6Y8WZB9UEQsq1ZCnSHsIxtZAhOTZA3FzFLn2Q0vf4xXu7C9GgL6rBHFqiZCyJwR1BwiPxH69csJihJlNJQuXzr39t4CyB4au8JbZAlcL6WALZBk9fmBmgM4CMoYQOxpyczTKMV6KwX81N6IWwbTrqX7v0AKaMpRuTeUZBkHdFoJCcqLKYRVwLpL3QKRtlmSNVZAvV9If9z"  # <-- Replace with your token
PAGE_ID = "Expresso221"  # Or the numeric page ID
POST_LIMIT = 50  # Number of posts to fetch
OUTPUT_FILE = "data/facebook_expresso_graph.csv"


def get_facebook_posts(page_id, access_token, limit=50):
    """
    Fetch public posts from a Facebook page using Graph API.
    """
    url = f"https://graph.facebook.com/v19.0/{page_id}/posts"
    params = {
        "access_token": access_token,
        "fields": "id,message,created_time,permalink_url,shares,likes.summary(true),comments.summary(true)",
        "limit": limit
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("data", [])


def parse_posts(posts):
    """
    Convert raw API data to DataFrame rows.
    """
    rows = []
    for post in posts:
        rows.append({
            "platform": "facebook",
            "brand": "Expresso",
            "post_id": post.get("id"),
            "post_url": post.get("permalink_url"),
            "post_date": post.get("created_time"),
            "content": post.get("message"),
            "like_count": post.get("likes", {}).get("summary", {}).get("total_count", 0),
            "comment_count": post.get("comments", {}).get("summary", {}).get("total_count", 0),
            "share_count": post.get("shares", {}).get("count", 0),
            "reactions_json": None
        })
    return rows


def main():
    print(f"🔑 Using Facebook Graph API for page: {PAGE_ID}")
    posts = get_facebook_posts(PAGE_ID, ACCESS_TOKEN, POST_LIMIT)
    print(f"✅ {len(posts)} posts récupérés")
    rows = parse_posts(posts)
    df = pd.DataFrame(rows)
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
    print(f"💾 Données enregistrées dans {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
