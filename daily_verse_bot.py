"""
Daily Verse Bot

Sends one verse about Jesus Christ to a Discord channel each day,
using a Discord webhook. No bot application or login needed.

Setup:
1. In Discord, go to a server you control.
   Server Settings -> Integrations -> Webhooks -> New Webhook.
   Copy the Webhook URL.
2. Set it as an environment variable instead of pasting it in the code:
   On Mac/Linux:   export DISCORD_WEBHOOK_URL="your-url-here"
   On Windows:      setx DISCORD_WEBHOOK_URL "your-url-here"
3. Install the one library this script needs:
   pip install requests
4. Run it:
   python daily_verse_bot.py
"""

import json
import os
import random
from datetime import date

import requests

VERSES_FILE = "verses.json"


def load_verses():
    with open(VERSES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def pick_todays_verse(verses):
    # Uses today's date to pick a verse, so the same verse shows up
    # all day but a different one shows up tomorrow. This cycles
    # through the whole list in order, then starts over.
    day_number = date.today().toordinal()
    index = day_number % len(verses)
    return verses[index]


def send_to_discord(verse):
    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        raise RuntimeError(
            "No webhook URL found. Set the DISCORD_WEBHOOK_URL environment variable."
        )

    message = {
        "content": f"**{verse['ref']}**\n{verse['note']}"
    }

    response = requests.post(webhook_url, json=message)
    response.raise_for_status()


def main():
    verses = load_verses()
    verse = pick_todays_verse(verses)
    send_to_discord(verse)
    print(f"Sent: {verse['ref']}")


if __name__ == "__main__":
    main()
