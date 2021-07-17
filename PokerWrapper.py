from player import Player
from card import Card

class PokerWrapper:
    def __init__(self):
        self.gameID
        self.gameStarted=False
        self.numPlayers=0
        self.hardBlind=0
        self.currentPot=0
        self.pokerUI
        self.gamedeck
        self.communityDeck
        self.participants