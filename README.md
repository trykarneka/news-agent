# 📰 News Agent (Daily Email Digest via SendGrid with Categories)

This project fetches the latest news from specific categories and emails it to you every morning at **7 AM IST** using GitHub Actions and SendGrid.

---

## ⚙️ Setup

1. **Fork or clone this repo** into your GitHub account.

2. **Create a SendGrid account** at [https://sendgrid.com](https://sendgrid.com).
   - Verify your sender email under "Sender Authentication".
   - Generate an **API Key** (with Mail Send permission).

3. **Add Secrets** in your repo:
   - `NEWS_API_KEY` → Your [NewsAPI.org](https://newsapi.org/) API key  
   - `SENDGRID_API_KEY` → Your SendGrid API key  
   - `FROM_EMAIL` → Verified sender email in SendGrid  
   - `TO_EMAIL` → Recipient email  
   - `NEWS_CATEGORIES` → Comma-separated list of categories (e.g., `technology,business,sports`)  

   👉 Available categories: `business`, `entertainment`, `general`, `health`, `science`, `sports`, `technology`

4. Push changes to GitHub.  
   The workflow will run automatically every day at **7 AM IST**.

---

## 🔍 Run Manually
You can also run the workflow manually in GitHub Actions tab (thanks to `workflow_dispatch`).

---

✅ Done! You’ll now get a personalized news digest daily 🎉
