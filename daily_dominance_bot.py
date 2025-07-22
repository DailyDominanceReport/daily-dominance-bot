import os
import requests
import random
import tweepy
from decimal import Decimal
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# === Load secrets from environment variables ===
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

# === Twitter Auth using Tweepy Client (v2) ===
client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET
)

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
        "Hash from $MD",
        "Gonna cry, piss your pants?",
        "GMD",
        "Dominate the trenches",
        "Jarvis, prepare the cuck chair",
        "Purple up",
        "Wew predicted this",
        "Studied economics",
        "Dominate your reality",
        "Mr Penis"
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
        "🧵 Dominance Report.\n",
        f"🧬 Dominance (TMD): {dominance:.8%} ({percent_change})",
        f"🧪 Total Market Cap: ${format_number(market_cap)}",
        "",
        pick_random_phrase(),
        "$MD"
    ]
    return "\n".join(lines)

# === Main ===
def main():
    try:
        dominance, market_cap = get_fdv_dominance()
        last_dominance = load_last_dominance()

        tweet = create_tweet(dominance / 100, market_cap, last_dominance)
        print("Tweet content:\n", tweet)

        # Send tweet using Twitter API v2
        client.create_tweet(text=tweet)

        save_dominance(dominance / 100)

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
