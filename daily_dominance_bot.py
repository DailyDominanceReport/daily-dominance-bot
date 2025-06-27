import os
import requests
import random
import tweepy
from datetime import datetime
from decimal import Decimal

# === Load secrets from environment variables or GitHub secrets ===
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

# === Initialize Twitter client ===
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# === Random phrases ===
def pick_random_phrase():
    phrases = [
        "Cock Torture (Online)",
        "$MD",
        "Dominance Supremacy",
        "Peak Replicant Activity",
        "Engage Protocol",
        "Initiating Cycle",
        "Daily Scan Complete",
        "☑ Market Status: Active",
    ]
    return random.choice(phrases)

# === Format number cleanly ===
def format_number(num, decimals=2):
    return f"{num:,.{decimals}f}"

# === Get market dominance data ===
def fetch_dominance_data():
    url = "https://api.coingecko.com/api/v3/coins/market_dominance"
    response = requests.get(url)
    data = response.json()

    # Replace 'market_dominance' and 'market_cap' with the actual keys in your API
    dominance = Decimal(data["market_dominance"])
    market_cap = Decimal(data["total_market_cap"])
    return dominance, market_cap

# === Load last dominance value to compute change ===
def load_last_dominance():
    try:
        with open("last_dominance.txt", "r") as f:
            return Decimal(f.read().strip())
    except FileNotFoundError:
        return None

def save_dominance(value):
    with open("last_dominance.txt", "w") as f:
        f.write(str(value))

# === Create tweet text ===
def create_tweet(dominance, market_cap, last_dominance):
    change = dominance - last_dominance if last_dominance else Decimal(0)
    arrow = "🔺" if change > 0 else "🔻" if change < 0 else "⏺"
    percent_change = f"{arrow} {abs(change):.2f}%"

    lines = [
        "🧵 Daily Dominance Report.",
        f"🧬 Dominance (FDV): {dominance:.8%} ({percent_change})",
        f"🧪 Total Market Cap: ${format_number(market_cap, 2)}",
        "",
        pick_random_phrase(),
    ]

    return "\n".join(lines)

# === Main bot function ===
def main():
    try:
        dominance, market_cap = fetch_dominance_data()
        last_dominance = load_last_dominance()

        tweet = create_tweet(dominance, market_cap, last_dominance)
        print("Tweet content:\n", tweet)

        # Send tweet (text only)
        api.update_status(status=tweet)

        save_dominance(dominance)

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
