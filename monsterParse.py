import requests
import json


def parseCard():
    monsterLink = "https://storage.googleapis.com/mirubot/paddata/processed/na_cards.json"

    loadSite = requests.get(monsterLink)
    cards = json.loads(loadSite.text)

    for card in cards:
        print(type(card['card']['card_id']))


parseCard()