from Poker.player import Player
from Poker.pokerplayer import PokerPlayer
from Poker.deck import Deck
from Poker.card import Card
from Poker.announcer import Announcer
from Poker.evalhand import EvaluateHand
import asyncio
import discord
import math


class PokerWrapper:
    def __init__(self, bot):
        self.bot=bot
        self.gameID=0
        self.gameStarted = False
        self.numPlayers = 0
        self.hardBlind = 0
        self.smallBlind=0
        self.currentPot = 0
        self.pokerUI = Announcer()
        self.gameDeck = Deck()
        self.communityDeck = []
        self.participants = []
        self.competing = []
        self.joinQueue=[]
        self.leaveQueue=[]
        self.startingBalance = 0


    async def startGame(self, ctx):
        await self.pokerUI.initiateGame(ctx)

    async def setPlayers(self, ctx, bot):
        embed = discord.Embed(title="Poker: Texas hold 'em",
                              description="Starting Balance: "+str(self.startingBalance)+""" <:chips:865450470671646760>
        Min Bet: """+str(self.hardBlind)+""" <:chips:865450470671646760>
        \nReact to Join!""",
            color=discord.Color.green())

        message = await ctx.send(embed=embed)
        await message.add_reaction('✅')
        await asyncio.sleep(10)

        message = await ctx.fetch_message(message.id)

        for reaction in message.reactions:
            if reaction.emoji == '✅':
                i = 1
                async for user in reaction.users():
                    if user != bot.user:
                        newPlayer= PokerPlayer(user.name, i, user, self.startingBalance)
                        self.participants.append(newPlayer)
                        i += 1
        if len(self.participants) < 2:
            await ctx.send("Not enough players")
            return False
        else:
            await ctx.send("Starting game with " + str(len(self.participants)) + " players")

    def addPlayers(self):
        for newPlayer in self.joinQueue:
            self.participants.append(newPlayer)
        self.joinQueue.clear()

    def leaveGame(self, players):
        for x in self.leaveQueue:
            players[x._user.id].balance+= x.getGameBalance()-self.startingBalance
            self.participants.remove(x)
            
        self.leaveQueue.clear()

    async def setBlind(self, ctx, bot):

        def representsInt(s):
            try:
                int(s)
                return True
            except ValueError:
                return False

        def verify(m):
            return m.author == ctx.message.author and representsInt(m.content)

        await self.pokerUI.askBet(ctx)

        try:
            msg = await bot.wait_for('message', check=verify, timeout=30)
        except asyncio.TimeoutError:
            await ctx.send(f"Sorry, you took too long to type the blind")
            return False

        self.hardBlind = int(msg.content)
        self.smallBlind = math.floor(self.hardBlind/2)

        # await Announcer.reportBet(ctx, blind)

    async def setBalance(self, ctx):

        def representsInt(s):
            try: 
                int(s)
                return True
            except ValueError:
                return False

        def verify(m):
            return m.author == ctx.message.author and representsInt(m.content)

        await self.pokerUI.askBalance(ctx)

        try:
            msg = await self.bot.wait_for('message', check = verify, timeout = 30)
        except asyncio.TimeoutError:
            await ctx.send(f"Sorry, you took too long to type the balance")
            return False

        self.startingBalance = int(msg.content)


    async def dealCards(self, bot):
        self.gameDeck.shuffle()

        for p in self.participants:
            for i in range(2):
                c = self.gameDeck.drawCard()
                p.addCard(c)
            await p.send_hand(bot)
    
    def checkPlayerBalance(self):
        for i in self.participants:
            if i.getGameBalance() <= 0:
                print(i.username(), "has left the table")
                self.participants.remove(i)

    def playerFold(self, id):
        self.competing.pop(0)

    def removePlayer(self, id):
        for i in self.participants:
            if i.username() == id:
                self.participants.remove(i)
        self.numPlayers -= 1

    def createCommDeck(self):
        i = 0
        for i in range(3):
            self.addCardtoComm()

    def addCardtoComm(self):
        self.communityDeck.append(self.gameDeck.drawCard())

    def findWinner(self):
        Eval = EvaluateHand(self.communityDeck)
        for x in self.competing:
            commAndHand = self.communityDeck + x._hand
            Eval = EvaluateHand(commAndHand)
            x._winCondition = Eval.evaluate()
            print (x._username)

        winningCond = max(x._winCondition[0] for x in self.competing)
        compete = []
        for x in self.competing:
            if x._winCondition[0] == winningCond:
                compete.append(x)
        winners = Eval.winning(compete, winningCond)
        return winners

    def resetRound(self):
        self.gameStarted = False
        self.currentPot = 0
        self.communityDeck.clear()
        self.gameDeck = Deck()
        self.numPlayers = len(self.participants)
        temp = self.participants.pop(0)
        self.participants.append(temp)
        self.competing.clear()
        for x in self.participants:
            x._hand = []
            x._gameBalance=int(x._gameBalance-x._inPot)
            x._inPot=0
            

    async def setDealer(self, ctx):
        return
    
    async def takeBlinds(self, ctx):
        return