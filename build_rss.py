#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, time, requests
from datetime import datetime
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from dateutil import parser as dateparser

BASE_URL = "https://www.gcores.com"
LIST_URL = "https://www.gcores.com/articles"
OUTPUT = "rss.xml"
HEADERS = {"User-Agent": "gcores-rss-bot/1.0 (+https://github.com/yourname/gcores-rss)"}

def fetch(url):
    r = requests.get(url, headers=HEADERS, timeout=15)
    r.raise_for_status()
    return r.text

def parse_list(html):
    soup = BeautifulSoup(html, "html.parser")
    items = []
    for h4 in soup.select("h4.title a"):
        href, title = h4.get("href"), h4.get_text(strip=True)
        if href and title:
            items.append({"title": title, "link": urljoin(BASE_URL, href)})
    return items

def extract_meta(html):
    soup = BeautifulSoup(html, "html.parser")
    desc = (soup.select_one("div.am-article-content p") or {}).get_text(strip=True) if soup.select_one("div.am-article-content p") else ""
    pub = soup.find("meta", {"property": "article:published_time"})
    pubdate = dateparser.parse(pub.get("content")) if pub and pub.get("content") else datetime.utcnow()
    return desc, pubdate

def rfc2822(dt): return dt.strftime("%a, %d %b %Y %H:%M:%S +0000")

def main():
    html = fetch(LIST_URL)
    items = parse_list(html)
    out = []
    for i, it in enumerate(items[:40]):
        try:
            art_html = fetch(it["link"])
            desc, pub = extract_meta(art_html)
        except Exception as e:
            desc, pub = "", datetime.utcnow()
        out.append(f"<item><title><![CDATA[{it['title']}]]></title><link>{it['link']}</link><guid>{it['link']}</guid><description><![CDATA[{desc}]]></description><pubDate>{rfc2822(pub)}</pubDate></item>")
        time.sleep(1)
    rss = f"<?xml version='1.0' encoding='utf-8'?><rss version='2.0'><channel><title>机核 RSS</title><link>{LIST_URL}</link><lastBuildDate>{rfc2822(datetime.utcnow())}</lastBuildDate>{''.join(out)}</channel></rss>"
    with open(OUTPUT, 'w', encoding='utf-8') as f: f.write(rss)

if __name__ == '__main__': main()
