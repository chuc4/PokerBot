from player import Player
from card import Card
from deck import Deck
from announcer import Announcer
from server import Server
from leaderboard import Leaderboard
from pokerplayer import PokerPlayer
class PokerWrapper:
    def __init__(self):
        self.gameID=0
        self.gameStarted=False
        self.numPlayers=0
        self.hardBlind=0
        self.currentPot=0
        self.pokerUI=Announcer()
        self.gamedeck=Deck()
        self.communityDeck=[]
        self.participants=[]


    def removePlayer(self,id):
        for i in self.participants:
            if i.username()==id:
                self.participants.remove(i)
        self.numPlayers-=1

    def addplayer(self,player):
        self.participants.append(player)
        self.numPlayers+=1
    def printparticipants(self):
        for i in self.participants:
            print(i.username(),i.getGameBalance())

    def checkPlayerBalance(self):
        for i in self.participants:
            if i.getGameBalance()<=0:
                print(i.username(), "has left the table")
                self.participants.remove(i)
