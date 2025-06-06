from flask import Flask, render_template, request
import requests

app = Flask(__name__)

NEWS_API_KEY = "e811420d5dec41aea5fea3d22f2e2373"

def get_news(country='us', category=None, query=None):
    query = query.strip() if query else None

    if query:
        # Search all news with query (no country/category filter)
        url = f"https://newsapi.org/v2/everything?q={query}&language=en&sortBy=publishedAt"
    else:
        # Get top headlines by country and optional category
        url = f"https://newsapi.org/v2/top-headlines?country={country}"
        if category:
            url += f"&category={category}"

    url += f"&apiKey={NEWS_API_KEY}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        print(f"[DEBUG] URL: {url}")
        print(f"[DEBUG] Articles count: {len(data.get('articles', []))}")

        return data.get('articles', [])
    except Exception as e:
        print("Error fetching news:", e)
        return []

@app.route('/')
def home():
    country = request.args.get('country') or 'us'  # Default to US
    category = request.args.get('category', '')
    query = request.args.get('q', '')
    articles = get_news(country=country, category=category, query=query)
    return render_template('index.html', articles=articles, country=country, category=category, query=query)

if __name__ == "__main__":
    app.run(debug=True)
