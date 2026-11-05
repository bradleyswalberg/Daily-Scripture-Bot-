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
    day_number = date.today().toordinal()
    index = day_number % len(verses)
    return verses[index]


def send_to_discord(verse):
    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
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
