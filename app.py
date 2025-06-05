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
    if not latest_box:
        return {"error": "최신 기사를 찾을 수 없습니다."}

    title_tag = latest_box.select_one("h4.title")
    desc_tag = latest_box.select_one("div.desc")
    link_tag = latest_box.select_one("a.link")

    if not title_tag or not desc_tag or not link_tag:
        return {"error": "기사 정보가 충분하지 않습니다."}

    article_url = "https://www.bntnews.co.kr" + link_tag['href']
    snippet = desc_tag.get_text(strip=True)

    # 본문 대신 snippet에서 정답 추출
    answers = re.findall(r"정답은\s*'([^']+)'", snippet)

    return {
        "title": title_tag.get_text(strip=True),
        "url": article_url,
        "answers": answers[:3]
    }

@app.route("/latest")
def latest():
    return jsonify(get_latest_solquiz())
