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

def fetch_news(category):
    url = f"https://newsapi.org/v2/top-headlines?country=in&category={category}&apiKey={NEWS_API_KEY}"
    response = requests.get(url).json()
    articles = response.get("articles", [])[:5]
    news_html = f"<h2>{category.capitalize()} News</h2>"
    if not articles:
        news_html += "<p>No articles found.</p>"
    for a in articles:
        news_html += f"<p><b>{a['title']}</b><br>{a.get('description','')}<br><a href='{a['url']}'>Read more</a></p>"
    return news_html

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

if __name__ == "__main__":
    combined_news = ""
    for cat in NEWS_CATEGORIES:
        combined_news += fetch_news(cat.strip())
    send_email(combined_news)
    print("✅ News sent via SendGrid with categories!")
