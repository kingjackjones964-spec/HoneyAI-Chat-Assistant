# Ultimate2026App.py
# All-in-One Python Starter Code (2026 Trending Needs)

import random
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import requests
from bs4 import BeautifulSoup

# =========================
# Hashtag + Caption Generator
# =========================
def generate_hashtags(topic):
    trending_tags = ["#viral", "#trending", "#explore", "#foryou", "#fun", "#2026", "#musttry"]
    topic_tag = "#" + topic.replace(" ", "")
    hashtags = [topic_tag] + random.sample(trending_tags, 4)
    return " ".join(hashtags)

def generate_caption(topic):
    captions = [
        f"Check this out! {topic} is amazing!",
        f"Top tips about {topic} you must see!",
        f"Don't miss this {topic} trend!",
        f"{topic} is trending now! #2026",
    ]
    return random.choice(captions)

# =========================
# Quotes / Shayari Generator
# =========================
def generate_quote(category):
    shayari = {
        "motivational": [
            "Keep going, the best is yet to come!",
            "Dream big, work hard, stay focused!",
            "Every day is a new chance to shine!",
        ],
        "love": [
            "Love is not what you say, love is what you do.",
            "Every heart deserves a little happiness.",
            "True love waits and always finds its way.",
        ],
        "fun": [
            "Smile, it confuses people!",
            "Life is short, eat dessert first!",
            "Dance like nobody's watching!",
        ]
    }
    if category not in shayari:
        category = "motivational"
    return random.choice(shayari[category])

# =========================
# Basic Thumbnail Creator
# =========================
def create_thumbnail(text, filename="thumbnail.png"):
    img = Image.new('RGB', (720, 1280), color = (73, 109, 137))
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 70)
    except:
        font = ImageFont.load_default()
    d.text((50,600), text, fill=(255,255,0), font=font)
    img.save(filename)
    print(f"Thumbnail saved as {filename}")

# =========================
# Internship Scraper (Sample city-wise)
# =========================
def get_internships(city="Delhi"):
    url = f"https://internshala.com/internships/{city.lower()}-internship"
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")
        # Sample: find all <a> tags with internships
        internships = [a.get_text().strip() for a in soup.find_all("a")[:5]]  # top 5
        if not internships:
            internships = ["No internships found - demo mode"]
    except:
        internships = ["Could not fetch internships - demo mode"]
    return internships

# =========================
# Viral Topic Analyzer (Dummy)
# =========================
def viral_topics():
    topics = ["AI Tools", "Short Videos", "Crypto 2026", "Motivational Quotes", "Health Hacks", "Shayari"]
    trending = random.sample(topics, 3)
    return trending

# =========================
# Main Program
# =========================
def main():
    while True:
        print("\n=== Ultimate 2026 All-in-One Tool ===")
        print("1. Generate Hashtag & Caption")
        print("2. Generate Quote / Shayari")
        print("3. Create Thumbnail")
        print("4. Get Internship List (Sample)")
        print("5. Show Trending Topics")
        print("0. Exit")

        choice = input("Enter option: ")

        if choice == "1":
            topic = input("Enter topic: ")
            print("\nCaption: ", generate_caption(topic))
            print("Hashtags: ", generate_hashtags(topic))
        elif choice == "2":
            category = input("Enter category (motivational/love/fun): ")
            print("\nQuote/Shayari: ", generate_quote(category))
        elif choice == "3":
            text = input("Enter text for thumbnail: ")
            create_thumbnail(text)
        elif choice == "4":
            city = input("Enter city (default Delhi): ") or "Delhi"
            internships = get_internships(city)
            print("\nTop Internships:")
            for i, intern in enumerate(internships, 1):
                print(f"{i}. {intern}")
        elif choice == "5":
            print("\nTrending Topics 2026:", viral_topics())
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid option! Try again.")

if __name__ == "__main__":
    main()
