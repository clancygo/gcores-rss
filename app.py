import os
import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator

def fetch_gcores_articles():
    url = "https://www.gcores.com/articles"
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(resp.text, "html.parser")
    articles = []
    for a in soup.select("a.story_title"):
        title = a.get_text(strip=True)
        link = "https://www.gcores.com" + a["href"]
        articles.append((title, link))
    return articles[:20]

def build_feed():
    fg = FeedGenerator()
    fg.title("机核网最新文章")
    fg.link(href="https://www.gcores.com/articles", rel="alternate")
    fg.description("自动生成的机核网RSS源")
    for title, link in fetch_gcores_articles():
        fe = fg.add_entry()
        fe.title(title)
        fe.link(href=link)
    os.makedirs("output", exist_ok=True)
    fg.rss_file("output/feed.xml", pretty=True)
    print("✅ RSS 生成成功：output/feed.xml")

if __name__ == "__main__":
    build_feed()
