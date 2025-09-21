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

def fetch_world_news(api_key, category=None):
    base_url = "https://api.worldnewsapi.com/search-news"
    
    # 1️⃣ same as your curl
    headers = {"x-api-key": api_key}
    
    params = {
        "source-countries": "in",
        "language": "en",
        "number": 5
    }
    if category:
        params["categories"] = category.strip()

    resp = requests.get(base_url, headers=headers, params=params)

    if resp.status_code == 401:
        print("⚠️ Got 401 with x-api-key header, retrying with Authorization header...")
        
        # 2️⃣ Retry with Authorization header
        headers = {"Authorization": f"ApiKey {api_key}"}
        resp = requests.get(base_url, headers=headers, params=params)

    if resp.status_code == 401:
        print("⚠️ Still unauthorized, trying as query param...")
        
        # 3️⃣ Retry with api-key in query
        params["api-key"] = api_key
        headers = {}  # clear headers
        resp = requests.get(base_url, headers=headers, params=params)

    print("DEBUG STATUS:", resp.status_code)
    print("DEBUG RESPONSE:", resp.text[:500])  # only first 500 chars

    try:
        data = resp.json()
        if "news" in data:
            return data["news"]
        elif "articles" in data:
            return data["articles"]
        else:
            return []
    except Exception as e:
        print("Error parsing JSON:", e)
        return []

def format_news_grouped(api_key, categories):
    email_body = "📰 **Your Morning India News Digest**\n\n"

    for cat in categories.split(","):
        articles = fetch_world_news(api_key, cat)
        email_body += f"\n=== {cat.capitalize()} ===\n"
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
    categories = os.getenv("NEWS_CATEGORIES", "politics,business,technology,sports")

    email_body = format_news_grouped(api_key, categories)
    send_email(email_body)
