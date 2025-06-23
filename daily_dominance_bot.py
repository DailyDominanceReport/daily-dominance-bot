import requests
import os
import random
from datetime import datetime
from dotenv import load_dotenv
import tweepy

# Load secrets from .env
load_dotenv()

BEARER_TOKEN = os.getenv("BEARER_TOKEN")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

# Twitter client setup
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# CoinGecko endpoints
MD_ID = "market-dominance"
COINGECKO_API = "https://api.coingecko.com/api/v3"
LAST_FILE = "last_dominance.txt"

# Phrases
phrases = [
    "Jarvis prepare the cuck chair.",
    "Studied Economics",
    "Never Submit",
    "There is no safe word",
    "Gonna cry, piss your pants?",
    "Hash from MD 🙏",
    "Cock Torture (Online)",
    "Penetration - yes please",
    "Total Market Domination",
    "My massive fucking titties?"
]

def get_fdv_dominance():
    md_data = requests.get(f"{COINGECKO_API}/coins/{MD_ID}").json()
    fdv = md_data["market_data"]["fully_diluted_valuation"]["usd"]
    global_data = requests.get(f"{COINGECKO_API}/global").json()
    total_marketcap = global_data["data"]["total_market_cap"]["usd"]
    return (fdv / total_marketcap) * 100, total_marketcap

def get_last_dominance():
    if os.path.exists(LAST_FILE):
        with open(LAST_FILE, "r") as f:
            return float(f.read().strip())
    return None

def save_current_dominance(current):
    with open(LAST_FILE, "w") as f:
        f.write(str(current))

def create_tweet(dominance_percent, marketcap, last_dominance):
    # Determine direction and change
    change_line = ""
    if last_dominance is not None:
        change = dominance_percent - last_dominance
        direction = "⬆️" if change > 0 else "⬇️"
        percent_change = abs((change / last_dominance) * 100)
        change_line = f" ({direction} {percent_change:.2f}%)"

    # Build tweet
    phrase = random.choice(phrases)
    tweet = (
        f"🔮 Daily Dominance Report.\n\n"
        f"😈 Dominance (FDV): {dominance_percent:.8f}%{change_line}\n"
        f"🌐 Total Market Cap: ${marketcap:,.2f}\n\n"
        f"{phrase}\n"
        "$MD"
    )
    return tweet

def pick_random_image():
    replicant_dir = "replicants_jpg"
    images = [f for f in os.listdir(replicant_dir) if f.lower().endswith(".jpg")]
    if not images:
        return None
    return os.path.join(replicant_dir, random.choice(images))

def main():
    try:
        # Get current dominance + market cap
        dominance, marketcap = get_fdv_dominance()

        # Read and update last dominance % file
        last_dominance = get_last_dominance()
        save_current_dominance(dominance)

        # Build tweet
        tweet = create_tweet(dominance, marketcap, last_dominance)
        print("Tweet content:\n", tweet)

        # Pick and upload image
        image_path = pick_random_image()
        if image_path:
            media = api.media_upload(image_path)
            api.update_status(status=tweet, media_ids=[media.media_id])
        else:
            api.update_status(status=tweet)

        print("Tweet sent!")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
