from flask import Flask, Response
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
        return "❌ 최신 기사를 찾을 수 없습니다."

    desc_tag = latest_box.select_one("div.desc")
    link_tag = latest_box.select_one("a.link")

    if not desc_tag or not link_tag:
        return "❌ 기사 정보가 충분하지 않습니다."

    snippet = desc_tag.get_text(strip=True)
    answers = re.findall(r"정답은\s*'([^']+)'", snippet)

    if not answers:
        return "❌ 정답을 찾을 수 없습니다."

    return f"🎯 정답: {', '.join(answers[:3])}"

@app.route("/latest")
def latest():
    result = get_latest_solquiz()
    return Response(result, content_type="text/plain; charset=utf-8")
