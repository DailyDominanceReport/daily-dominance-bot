import os
import requests
import random
import tweepy
from decimal import Decimal
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# === Load secrets from environment variables ===
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

# === Twitter Auth ===
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# === CoinGecko API Constants ===
MD_ID = "market-dominance"
COINGECKO_API = "https://api.coingecko.com/api/v3"

# === Get FDV Dominance ===
def get_fdv_dominance():
    md_data = requests.get(f"{COINGECKO_API}/coins/{MD_ID}").json()
    fdv = Decimal(md_data["market_data"]["fully_diluted_valuation"]["usd"])

    global_data = requests.get(f"{COINGECKO_API}/global").json()
    total_marketcap = Decimal(global_data["data"]["total_market_cap"]["usd"])

    dominance_percent = (fdv / total_marketcap) * 100
    return dominance_percent, total_marketcap

# === Random phrase picker ===
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

# === Format number with commas ===
def format_number(num, decimals=2):
    return f"{num:,.{decimals}f}"

# === File helpers ===
def load_last_dominance():
    try:
        with open("last_dominance.txt", "r") as f:
            return Decimal(f.read().strip())
    except FileNotFoundError:
        return None

def save_dominance(value):
    with open("last_dominance.txt", "w") as f:
        f.write(str(value))

# === Build Tweet ===
def create_tweet(dominance, market_cap, last_dominance):
    change = dominance - last_dominance if last_dominance else Decimal(0)
    arrow = "🔺" if change > 0 else "🔻" if change < 0 else "⏺"
    percent_change = f"{arrow} {abs(change):.2f}%"

    lines = [
        "🧵 Daily Dominance Report.",
        f"🧬 Dominance (FDV): {dominance:.8%} ({percent_change})",
        f"🧪 Total Market Cap: ${format_number(market_cap)}",
        "",
        pick_random_phrase(),
    ]
    return "\n".join(lines)

# === Main ===
def main():
    try:
        dominance, market_cap = get_fdv_dominance()
        last_dominance = load_last_dominance()

        tweet = create_tweet(dominance / 100, market_cap, last_dominance)
        print("Tweet content:\n", tweet)

        # Send tweet
        api.update_status(status=tweet)

        save_dominance(dominance / 100)

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
