from flask import Flask, render_template, request, jsonify
import requests
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Env variables
X_BEARER_TOKEN = os.getenv("X_BEARER_TOKEN")
INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")
THREADS_ACCESS_TOKEN = os.getenv("THREADS_ACCESS_TOKEN")
INSTAGRAM_USER_ID = os.getenv("INSTAGRAM_USER_ID")
X_USER_ID = os.getenv("X_USER_ID")

# Sentiment model
MODEL = "cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)
labels = ['Negative', 'Neutral', 'Positive']

def analyze_sentiment(text):
    encoded = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    scores = softmax(model(**encoded).logits.detach().numpy()[0])
    return labels[scores.argmax()]

def match_date(timestamp, target_date):
    post_date = timestamp.split('T')[0]
    return post_date == target_date

# Instagram
def get_instagram_posts():
    url = f"https://graph.facebook.com/v18.0/{INSTAGRAM_USER_ID}/media?fields=id,caption,timestamp&access_token={INSTAGRAM_ACCESS_TOKEN}"
    res = requests.get(url).json()
    posts = res.get("data", [])
    return [{"id": p["id"], "caption": p.get("caption", ""), "timestamp": p["timestamp"]} for p in posts]

def get_instagram_comments(post_id):
    url = f"https://graph.facebook.com/v18.0/{post_id}/comments?fields=text,from&access_token={INSTAGRAM_ACCESS_TOKEN}"
    res = requests.get(url).json()
    return [{"text": c.get("text", ""), "username": c.get("from", {}).get("username", "Unknown")} for c in res.get("data", [])]

# Threads
def get_threads_posts():
    url = f"https://graph.threads.net/v1.0/me/threads?fields=id,text,timestamp&access_token={THREADS_ACCESS_TOKEN}"
    res = requests.get(url).json()
    threads = res.get("data", [])
    return [{"id": t["id"], "text": t.get("text", ""), "timestamp": t.get("timestamp", "")} for t in threads]

def get_threads_comments(thread_id):
    url = f"https://graph.threads.net/v1.0/{thread_id}?fields=replies{{text,username}}&access_token={THREADS_ACCESS_TOKEN}"
    res = requests.get(url).json()
    replies = res.get("replies", {}).get("data", [])
    return [{"text": r.get("text", ""), "username": r.get("username", "Unknown")} for r in replies]

# X (Twitter)
def get_x_posts():
    url = f"https://api.twitter.com/2/users/{X_USER_ID}/tweets?tweet.fields=created_at,text"
    headers = {"Authorization": f"Bearer {X_BEARER_TOKEN}"}
    res = requests.get(url, headers=headers).json()
    print(res)
    return res.get("data", [])

def get_x_replies(convo_id):
    url = (
        f"https://api.twitter.com/2/tweets/search/recent"
        f"?query=conversation_id:{convo_id}"
        f"&tweet.fields=text,author_id"
        f"&expansions=author_id"
        f"&user.fields=username"
    )
    headers = {"Authorization": f"Bearer {X_BEARER_TOKEN}"}
    res = requests.get(url, headers=headers).json()
    users = {u["id"]: u["username"] for u in res.get("includes", {}).get("users", [])}
    replies = res.get("data", [])
    print(res)
    return [{"text": r["text"], "username": users.get(r["author_id"], "Unknown")} for r in replies]

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/platform/<platform>')
def platform_page(platform):
    posts = []
    if platform == "Instagram":
        posts = get_instagram_posts()
    elif platform == "Threads":
        posts = get_threads_posts()
    elif platform == "X":
        posts = get_x_posts()
    return render_template('platform_page.html', platform=platform, posts=posts)

# (same imports and initial code...)

@app.route('/api/insights', methods=['POST'])
def get_insights():
    data = request.get_json()
    platforms = data.get('platforms', [])
    platform = data.get('platform')
    caption_id = data.get('caption')
    thread_id = data.get('thread')
    status_id = data.get('status_id')
    date_filter = data.get('date')

    results = []

    if platforms:
        for p in platforms:
            if p == 'Instagram':
                posts = get_instagram_posts()
                for post in posts:
                    comments = get_instagram_comments(post["id"])
                    for comment in comments:
                        sentiment = analyze_sentiment(comment["text"])
                        results.append({
                            "platform": "Instagram",
                            "comment": comment["text"],
                            "username": comment["username"],
                            "sentiment": sentiment
                        })
            elif p == 'Threads':
                threads = get_threads_posts()
                for thread in threads:
                    comments = get_threads_comments(thread["id"])
                    for comment in comments:
                        sentiment = analyze_sentiment(comment["text"])
                        results.append({
                            "platform": "Threads",
                            "comment": comment["text"],
                            "username": comment["username"],
                            "sentiment": sentiment
                        })
            elif p == 'X':
                tweets = get_x_posts()
                for tweet in tweets:
                    replies = get_x_replies(tweet["id"])
                    for reply in replies:
                        sentiment = analyze_sentiment(reply["text"])
                        results.append({
                            "platform": "X",
                            "comment": reply["text"],
                            "username": reply["username"],
                            "sentiment": sentiment
                        })

    elif platform == "Instagram":
        posts = get_instagram_posts()
        if caption_id:
            comments = get_instagram_comments(caption_id)
            for comment in comments:
                sentiment = analyze_sentiment(comment["text"])
                results.append({
                    "platform": "Instagram",
                    "comment": comment["text"],
                    "username": comment["username"],
                    "sentiment": sentiment
                })
        elif date_filter:
            for post in posts:
                if match_date(post["timestamp"], date_filter):
                    comments = get_instagram_comments(post["id"])
                    for comment in comments:
                        sentiment = analyze_sentiment(comment["text"])
                        results.append({
                            "platform": "Instagram",
                            "comment": comment["text"],
                            "username": comment["username"],
                            "sentiment": sentiment
                        })

    elif platform == "Threads":
        threads = get_threads_posts()
        if thread_id:
            comments = get_threads_comments(thread_id)
            for comment in comments:
                sentiment = analyze_sentiment(comment["text"])
                results.append({
                    "platform": "Threads",
                    "comment": comment["text"],
                    "username": comment["username"],
                    "sentiment": sentiment
                })
        elif date_filter:
            for thread in threads:
                if match_date(thread["timestamp"], date_filter):
                    comments = get_threads_comments(thread["id"])
                    for comment in comments:
                        sentiment = analyze_sentiment(comment["text"])
                        results.append({
                            "platform": "Threads",
                            "comment": comment["text"],
                            "username": comment["username"],
                            "sentiment": sentiment
                        })

    elif platform == "X":
        if status_id:
            replies = get_x_replies(status_id)
            for reply in replies:
                sentiment = analyze_sentiment(reply["text"])
                results.append({
                    "platform": "X",
                    "comment": reply["text"],
                    "username": reply["username"],
                    "sentiment": sentiment
                })

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
