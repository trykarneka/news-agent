import os
import requests
from datetime import date
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, To, From

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL")
TO_EMAIL = os.getenv("TO_EMAIL")
NEWS_CATEGORIES = os.getenv("NEWS_CATEGORIES", "general").split(",")  # e.g. "technology,business"

print(NEWS_CATEGORIES,"are the categories")
def fetch_news(category):
    url = f"https://newsapi.org/v2/top-headlines?country=us&category={category}&apiKey={NEWS_API_KEY}"
    response = requests.get(url).json()
    articles = response.get("articles", [])[:5]
    news_html = f"<h2>{category.capitalize()} News</h2>"
    if not articles:
        news_html += "<p>No articles found.</p>"
    for a in articles:
        news_html += f"<p><b>{a['title']}</b><br>{a.get('description','')}<br><a href='{a['url']}'>Read more</a></p>"
    return news_html


def fetch_top_news(api_key):
    url = "https://api.worldnewsapi.com/search-news"
    headers = {
        "x-api-key": api_key   # same as curl
    }
    params = {
        "source-countries": "in",
        "language": "en",
        "number": 5
    }

    resp = requests.get(url, headers=headers, params=params)
    print("DEBUG STATUS:", resp.status_code)
    print("DEBUG RAW:", resp.text[:300])  # log first 300 chars for debugging

    try:
        data = resp.json()
        if "news" in data:
            return data["news"]
        elif "articles" in data:
            return data["articles"]
        else:
            print("⚠️ Unexpected response keys:", list(data.keys()))
            return []
    except Exception as e:
        print("❌ JSON parse failed:", e)
        return []

def format_news(api_key):
    articles = fetch_top_news(api_key)
    email_body = "📰 **Your Morning India News Digest (Top 5)**\n\n"

    if not articles:
        email_body += "⚠️ No articles found.\n"
    else:
        for art in articles:
            title = art.get("title", "No Title")
            url = art.get("url", "#")
            email_body += f"- {title} ({url})\n"

    return email_body

def send_email(content):
    message = Mail(
        from_email=os.getenv("FROM_EMAIL"),
        to_emails=os.getenv("TO_EMAIL"),
        subject="Your Morning India News Digest 🌏",
        plain_text_content=content
    )
    sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
    resp = sg.send(message)
    print(f"SendGrid response: {resp.status_code}")

if __name__ == "__main__":
    api_key = os.getenv("WORLDNEWS_API_KEY")
    print(api_key,"is the api key")
    email_body = format_news(api_key)
    send_email(email_body)

