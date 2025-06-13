import requests
import os
from dotenv import load_dotenv
import tweepy
import random

# Load .env keys
load_dotenv()

BEARER_TOKEN = os.getenv("BEARER_TOKEN")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

# Auth using v2 client
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET
)

# CoinGecko data
MD_ID = "market-dominance"
COINGECKO_API = "https://api.coingecko.com/api/v3"

def get_fdv_dominance():
    md_data = requests.get(f"{COINGECKO_API}/coins/{MD_ID}").json()
    fdv = md_data["market_data"]["fully_diluted_valuation"]["usd"]

    global_data = requests.get(f"{COINGECKO_API}/global").json()
    total_marketcap = global_data["data"]["total_market_cap"]["usd"]

    dominance_percent = (fdv / total_marketcap) * 100
    return dominance_percent

from datetime import datetime

from datetime import datetime

def create_tweet(dominance_percent, fdv, marketcap):
    now = datetime.utcnow()
    
    # Add your spicy endings here
    endings = [
        "Jarvis prepare the cuck chair.",
        "Studied Economics",
        "Never Submit",
        "There is no safe word",
        "Gonna cry, piss your pants?"
    ]
    
    ending = random.choice(endings)

    return (
        f"📊 Daily Dominance Report\n\n"
        f"🔹 Dominance (FDV): {dominance_percent:.8f}%\n"
        f"💰 Token FDV: ${fdv:,.2f}\n"
        f"🌐 Total Market Cap: ${marketcap:,.2f}\n"
        f"🕒 Last Updated: {now.strftime('%B %d, %Y @ %H:%M')} UTC\n\n"
        f"{ending}\n"
        "$MD"
    )

def main():
    try:
        dominance = get_fdv_dominance()
        
        # Fetch values again to format them into tweet
        md_data = requests.get(f"{COINGECKO_API}/coins/{MD_ID}").json()
        fdv = md_data["market_data"]["fully_diluted_valuation"]["usd"]
        
        global_data = requests.get(f"{COINGECKO_API}/global").json()
        total_marketcap = global_data["data"]["total_market_cap"]["usd"]

        tweet = create_tweet(dominance, fdv, total_marketcap)
        client.create_tweet(text=tweet)
        print("Tweet sent!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()