import xml.etree.ElementTree as ET
from typing import Dict, List

import feedparser

from .constant import RSSHUB_HOST


def parse(user_id="1435696727") -> [str, list[str]]:
    rss = feedparser.parse(f"https://{RSSHUB_HOST}/bilibili/user/video/{user_id}/0")
    return user_id, [item.link for item in rss.entries], rss


def gen(rss: feedparser.FeedParserDict, status: List[Dict[str, str]]):
    # 把 text 字段替换 describe
    for item in rss.entries:
        for i in status:
            if i["url"] == item.link:
                item.description = i["text"]
                break

    # 创建根元素
    root = ET.Element("rss")
    root.set("version", "2.0")

    # 创建子元素
    channel = ET.SubElement(root, "channel")
    title = ET.SubElement(channel, "title")
    title.text = rss.feed.title
    link = ET.SubElement(channel, "link")
    link.text = rss.feed.link
    description = ET.SubElement(channel, "description")
    description.text = rss.feed.description

    # 添加条目
    for item in rss.entries:
        entry = ET.SubElement(channel, "item")
        title = ET.SubElement(entry, "title")
        title.text = item.title
        link = ET.SubElement(entry, "link")
        link.text = item.link
        description = ET.SubElement(entry, "description")
        description.text = item.description

    # 将树写入字符串并返回
    return ET.tostring(root, encoding="unicode")
