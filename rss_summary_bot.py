import feedparser
import openai
import os
import requests

openai.api_key = os.getenv("OPENAI_API_KEY")
slack_webhook = os.getenv("SLACK_WEBHOOK_URL")

feed = feedparser.parse("https://rss.nytimes.com/services/xml/rss/nyt/Politics.xml")

for entry in feed.entries[:3]:
    title = entry.title
    link = entry.link
    prompt = f"Summarize this article: {title} - {link}"

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    summary = response.choices[0].message["content"]
    print(f"Title: {title}\nSummary: {summary}\n")

    if slack_webhook:
        slack_message = f"*{title}*\n{link}\n\n{summary}"
        requests.post(slack_webhook, json={"text": slack_message})
