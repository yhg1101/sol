# app.py
from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

def get_latest_solquiz():
    url = "https://www.bntnews.co.kr/article/search?searchText=쏠퀴즈"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    latest_box = soup.select_one("div.text_box")
    link_tag = latest_box.select_one("a.link") if latest_box else None
    if not link_tag or not link_tag.get('href'):
        return {"error": "기사 링크를 찾지 못함"}

    article_url = "https://www.bntnews.co.kr" + link_tag['href']
    article_res = requests.get(article_url, headers=headers)
    article_soup = BeautifulSoup(article_res.text, "html.parser")
    content_tag = article_soup.select_one(".article-body")
    if not content_tag:
        return {"error": "본문을 찾지 못함"}

    full_text = content_tag.get_text(separator=' ', strip=True)
    answers = re.findall(r"정답은\\s*'([^']+)'", full_text)

    return {
        "title": latest_box.select_one("h4.title").get_text(strip=True),
        "url": article_url,
        "answers": answers[:3]
    }

@app.route("/latest")
def latest():
    return jsonify(get_latest_solquiz())

if __name__ == "__main__":
    app.run()
