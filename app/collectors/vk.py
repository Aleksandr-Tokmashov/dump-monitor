import requests
from app.db import SessionLocal
from app.models import PostRaw
import os
from datetime import datetime, timedelta
import time 

# TODO: расширить парсинг:
# - пагинация wall.get (offset)
# - динамический count по активности группы
# - исторический сбор (last_seen_post_id)
# - приоритет групп по сигналам
# - добавить групп


VK_TOKEN = os.getenv("VK_TOKEN")
VK_VERSION = "5.131"

SOURCES = [
    {"id": -211335662, "type": "posts"},
    {"id": -38981315, "type": "comments"},
]


def fetch_vk():
    db = SessionLocal()

    for source in SOURCES:
        group_id = source["id"]
        source_type = source["type"]

        # --- ПОСТЫ ---
        if source_type == "posts":
            posts = get_posts(group_id)

            for post in posts:
                save_post(db, group_id, post)

        # --- КОММЕНТАРИИ ---
        elif source_type == "comments":
            posts = get_posts(group_id)

            for post in posts:
                comments = get_comments(group_id, post["id"])

                for comment in comments:
                    save_comment(db, group_id, post["id"], comment)

    db.commit()
    db.close()

def get_posts(group_id, count=100, max_posts=1000):
    url = "https://api.vk.com/method/wall.get"

    all_posts = []
    offset = 0

    while len(all_posts) < max_posts:
        time.sleep(0.3)

        params = {
            "owner_id": group_id,
            "count": count,
            "offset": offset,
            "access_token": VK_TOKEN,
            "v": VK_VERSION
        }

        data = requests.get(url, params=params).json()

        if "error" in data:
            print("VK ERROR:", data["error"])
            break

        items = data["response"]["items"]

        if not items:
            break

        all_posts.extend(items)
        offset += count

    return all_posts

def get_comments(group_id, post_id):
    url = "https://api.vk.com/method/wall.getComments"

    params = {
        "owner_id": group_id,
        "post_id": post_id,
        "count": 10,
        "access_token": VK_TOKEN,
        "v": VK_VERSION
    }

    data = requests.get(url, params=params).json()

    if "error" in data:
        print("VK ERROR:", data["error"])
        return []

    print("COMMENTS RESPONSE:", data)
    
    return data["response"]["items"]

def save_post(db, group_id, post):
    text = post.get("text", "")
    attachments = post.get("attachments", [])

    six_months_ago = datetime.now() - timedelta(days=180)
    post_date = datetime.fromtimestamp(post["date"])

    if post_date < six_months_ago:
        return
    
    if not text and not attachments:
        return

    url = f"https://vk.com/wall{group_id}_{post['id']}"
    
    existing = db.query(PostRaw).filter(PostRaw.url == url).first()
    if existing:
        return

    if not text:
        return
    
    db.add(PostRaw(
        source="vk_post",
        text=text,
        url=url
    ))


def save_comment(db, group_id, post_id, comment):
    text = comment.get("text", "")
    if not text:
        return

    url = f"https://vk.com/wall{group_id}_{post_id}?reply={comment['id']}"

    db.add(PostRaw(
        source="vk_comment",
        text=text,
        url=url
    ))