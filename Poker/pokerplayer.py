import asyncio
import discord
from Poker.deck import Deck
from Poker.card import Card



class PokerPlayer:
    def __init__(self, username, seatNumber, user, startBalance):
        self._user = user
        self._username = username
        self._seatNumber = seatNumber
        self._hand = []
        self._gameBalance = startBalance
        self._playerAction = 0
        self._inGame = True
        self._winCondition = [0]
        self._inPot=0

    '''DMs a players hand'''
    async def send_hand(self, bot):
        handString = ""
        await self._user.send("**Hand:**")
        for card in self._hand:
            handString += card.emote

        

        await self._user.send(handString)

    '''Returns the player's username'''
    def username(self):
        return self._username

    '''Returns the player's seatNumber'''
    def seatNumber(self):
        return self._seatNumber

    '''Returns the player's status'''
    def getStatus(self):
        return self._inGame

    '''Sets the player's status'''
    def setStatus(self, status):
        self._inGame = status

    '''Returns the player's action'''
    def getHand(self):
        return self._hand

    '''Adds a card to the player's hand.
       A player cannot have more than 2 cards.'''
    def addCard(self, c):
        if len(self._hand) < 2:
            self._hand.append(c)

    '''Returns the player's balance'''
    def getGameBalance(self):
        return self._gameBalance-self._inPot

    '''Sets the Poker Player's current balance.
       opType represents the type of operation.
       1 is for addition and 0 is for subtraction.
       The player's inGame status is set to False if 
       their balance hits 0'''
    def setBalance(self, opType, amount):
        if opType:
            self._gameBalance += amount
        else:
            if self._gameBalance > 0:
                current = self._gameBalance - amount
                self._gameBalance = current if (current > 0) else 0
                if self._gameBalance == 0:
                    self.setStatus(False)

    '''Returns the player's action'''
    def getAction(self):
        return self._playerAction

    '''Sets the player's action'''
    def setAction(self, action):
        self._playerAction = action

    '''Returns player's win condition'''
    def getWinCond(self):
        if self._winCondition[0] == 10:
            return "ROYAL FLUSH"
        elif self._winCondition[0] == 9:
            return "STRAIGHT FLUSH"
        elif self._winCondition[0] == 8:
            return "FOUR OF A KIND"
        elif self._winCondition[0] == 7:
            return "FULL HOUSE"
        elif self._winCondition[0] == 6:
            return "FLUSH"
        elif self._winCondition[0] == 5:
            return "STRAIGHT"
        elif self._winCondition[0] == 4:
            return "THREE OF A KIND"
        elif self._winCondition[0] == 3:
            return "TWO PAIR"
        elif self._winCondition[0] == 2:
            return "ONE PAIR"
        elif self._winCondition[0] == 1:
            return "HIGH CARD"