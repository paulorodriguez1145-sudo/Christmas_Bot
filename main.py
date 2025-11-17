import os
from datetime import date
import tweepy
from openai import OpenAI
from dotenv import load_dotenv

# ----------------------------------------------------
# LOAD API KEYS FROM .env FILE
# ----------------------------------------------------
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

X_API_KEY = os.getenv("X_API_KEY")
X_API_SECRET = os.getenv("X_API_SECRET")
X_ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
X_ACCESS_TOKEN_SECRET = os.getenv("X_ACCESS_TOKEN_SECRET")

client = OpenAI(api_key=OPENAI_API_KEY)

# ----------------------------------------------------
# DATE LOGIC FOR COUNTDOWN TWEET
# ----------------------------------------------------
def days_until_christmas(today=None):
    today = today or date.today()
    this_year = today.year
    christmas = date(this_year, 12, 25)

    if today <= christmas:
        return (christmas - today).days
    else:
        next_christmas = date(this_year + 1, 12, 25)
        return (next_christmas - today).days


def make_countdown_tweet():
    today = date.today()
    d = days_until_christmas(today)

    # On Christmas Day
    if today.month == 12 and today.day == 25:
        return "🎄 Merry Christmas! 🎄"

    # Before Christmas
    this_year = today.year
    if today < date(this_year, 12, 25):
        if d == 1:
            return "1 day until Christmas 🎄"
        else:
            return f"{d} days until Christmas 🎄"

    # After Christmas
    if d == 1:
        return "Christmas is over… 1 day until next Christmas 🎄"
    else:
        return f"Christmas is over… {d} days until next Christmas 🎄"


# ----------------------------------------------------
# HOLIDAY CHARACTER TWEET USING OPENAI
# ----------------------------------------------------
def make_character_tweet():
    prompt = """
You are a Christmas Bot. Write a short tweet (max 220 characters)
in first person as a holiday-themed character (Santa, Rudolph, elf, snowman, etc.).
Make it cozy, playful, and family-friendly. No hashtags.
Return only the tweet text.
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a friendly Christmas Bot."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=80,
        temperature=0.9,
    )

    return response.choices[0].message.content.strip()

# ----------------------------------------------------
# TWITTER / X API POSTING FUNCTION (via tweepy)
# ----------------------------------------------------
import os
import requests
from requests_oauthlib import OAuth1

X_API_KEY = os.getenv("X_API_KEY")
X_API_SECRET = os.getenv("X_API_SECRET")
X_ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
X_ACCESS_TOKEN_SECRET = os.getenv("X_ACCESS_TOKEN_SECRET")

def post_to_x(text: str):
    url = "https://api.twitter.com/2/tweets"
    
    auth = OAuth1(
        X_API_KEY,
        client_secret=X_API_SECRET,
        resource_owner_key=X_ACCESS_TOKEN,
        resource_owner_secret=X_ACCESS_TOKEN_SECRET,
    )

    payload = {"text": text}

    r = requests.post(url, json=payload, auth=auth)
    print("Status:", r.status_code)
    print("Response:", r.text)


# ----------------------------------------------------
# MAIN DAILY EXECUTION
# ----------------------------------------------------
def main():
    # Tweet 1 — Countdown
    countdown_tweet = make_countdown_tweet()
    print("Posting countdown tweet:", countdown_tweet)
    post_to_x(countdown_tweet)

    # Tweet 2 — Holiday Character
    character_tweet = make_character_tweet()
    print("Posting character tweet:", character_tweet)
    post_to_x(character_tweet)


if __name__ == "__main__":
    main()
