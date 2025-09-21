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
'''
def send_email(news_content):
    subject = f"Your Morning India News Digest - {date.today()}"
    message = Mail(
        from_email=From(FROM_EMAIL),
        to_emails=To(TO_EMAIL),
        subject=subject,
        html_content=news_content
    )
    sg = SendGridAPIClient(SENDGRID_API_KEY)
    resp = sg.send(message)
    print(f"SendGrid response: {resp.status_code}")
import os
import requests
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
'''
def fetch_world_news(api_key, categories=None):
    base_url = "https://api.worldnewsapi.com/search-news"
    params = {
        "source-country": "in",   # ✅ India-specific
        "language": "en",
        "number": 5               # how many articles per category
    }
    all_articles = []

    if categories:
        for cat in categories.split(","):
            params["categories"] = cat.strip()
            print(f"Fetching category: {cat}")
            resp = requests.get(base_url, headers={"x-api-key": api_key}, params=params)
            data = resp.json()
            articles = data.get("news", [])
            all_articles.extend(articles)
    else:
        resp = requests.get(base_url, headers={"x-api-key": api_key}, params=params)
        data = resp.json()
        all_articles = data.get("news", [])

    return all_articles

def format_news(articles):
    if not articles:
        return "⚠️ No news articles found today."

    body = ""
    for art in articles:
        body += f"- {art.get('title')} ({art.get('url')})\n"
    return body

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
    categories = os.getenv("NEWS_CATEGORIES", "politics,business,technology")

    articles = fetch_world_news(api_key, categories)
    email_body = format_news(articles)
    send_email(email_body)

