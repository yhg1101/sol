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
        return "<h1 style='color:black;'>❌ 최신 기사를 찾을 수 없습니다.</h1>"

    title_tag = latest_box.select_one("h4.title")
    desc_tag = latest_box.select_one("div.desc")
    link_tag = latest_box.select_one("a.link")

    if not title_tag or not desc_tag or not link_tag:
        return "<h1 style='color:black;'>❌ 기사 정보가 부족합니다.</h1>"

    title = title_tag.get_text(strip=True)
    snippet = desc_tag.get_text(strip=True)
    answers = re.findall(r"정답은\s*'([^']+)'", snippet)

    if not answers:
        return "<h1 style='color:black;'>❌ 정답을 찾을 수 없습니다.</h1>"

    return f"""
    <html>
        <body style="font-family: Arial; padding: 20px; color: black;">
            <h1>📰 {title}</h1>
            <h1>🎯 정답: {', '.join(answers[:3])}</h1>
        </body>
    </html>
    """

@app.route("/latest")
def latest():
    html_content = get_latest_solquiz()
    return Response(html_content, content_type="text/html; charset=utf-8")
