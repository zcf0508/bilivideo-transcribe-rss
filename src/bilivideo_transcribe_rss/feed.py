import feedparser


def parse(user_id="1435696727") -> [str, list[str]]:
    rss = feedparser.parse(f"https://rsshub.huali.cafe/bilibili/user/video/{user_id}/0")
    return user_id, [item.link for item in rss.entries], rss
