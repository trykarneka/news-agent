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


def fetch_news_by_category(api_key, category):
    url = "https://api.worldnewsapi.com/search-news"
    headers = {"x-api-key": api_key}
    params = {
        "source-countries": "in",
        "language": "en",
        "number": 5,
        "categories": category
    }

    resp = requests.get(url, headers=headers, params=params)
    print(f"DEBUG STATUS ({category}):", resp.status_code)
    try:
        data = resp.json()
        if "news" in data:
            return data["news"]
        elif "articles" in data:
            return data["articles"]
        else:
            print(f"⚠️ No articles found for category {category}")
            return []
    except Exception as e:
        print(f"❌ JSON parse failed for category {category}: {e}")
        return []

def format_news_html(api_key, categories):
    html_body = """
    <html>
      <body>
        <h2>📰 Your Morning India News Digest</h2>
    """

    for cat in categories.split(","):
        articles = fetch_news_by_category(api_key, cat.strip())
        html_body += f"<h3>{cat.capitalize()}</h3>"
        if not articles:
            html_body += "<p>⚠️ No articles found.</p>"
        else:
            html_body += "<ul>"
            for art in articles:
                title = art.get("title", "No Title")
                url = art.get("url", "#")
                html_body += f'<li><a href="{url}" target="_blank">{title}</a></li>'
            html_body += "</ul>"

    html_body += """
      </body>
    </html>
    """
    return html_body

def send_email(content_html):
    message = Mail(
        from_email=os.getenv("FROM_EMAIL"),
        to_emails=os.getenv("TO_EMAIL"),
        subject="Your Morning India News Digest 🌏",
        html_content=content_html
    )
    sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
    resp = sg.send(message)
    print(f"SendGrid response: {resp.status_code}")

if __name__ == "__main__":
    api_key = os.getenv("WORLDNEWS_API_KEY")
    categories = os.getenv("NEWS_CATEGORIES", "politics,business,technology,sports")
    print(api_key,"is the api key")
    html_content = format_news_html(api_key, categories)
    send_email(html_content)

