from Poker.player import Player
from Poker.pokerplayer import PokerPlayer
from Poker.deck import Deck
from Poker.card import Card
from Poker.announcer import Announcer
from Poker.evalhand import EvaluateHand
import asyncio
import discord

class PokerWrapper:
    def __init__(self):
        self.gameID
        self.gameStarted=False
        self.numPlayers=0
        self.hardBlind=0
        self.currentPot=0
        self.pokerUI
        self.gamedeck = Deck()
        self.communityDeck=[]
        self.participants = []
        self.competing=[]
        self.startingBalance
    
    async def startGame(self, ctx):
        await Announcer.initiateGame(ctx)

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
                i=1
                async for user in reaction.users():
                    if user != bot.user:
                        self.participants.append(PokerPlayer(user.id, i))
                        i+=1
        if len(self.participants) < 3:
            await ctx.send("Not enough players")
            return False
        else:
            await ctx.send("Starting game with " + str(len(self.participants)) + " players")

    async def setBlind(self, ctx):

        def representsInt(s):
            try: 
                int(s)
                return True
            except ValueError:
                return False

        def verify(m):
            return m.author == ctx.message.author and representsInt(m.content)

        await Announcer.askBet(ctx)

        try:
            msg = await self.client.wait_for('message', check = verify, timeout = 30)
        except asyncio.TimeoutError:
            await ctx.send(f"Sorry, you took too long to type the blind")
            return False

        self.hardBlind = int(msg.content)

        #await Announcer.reportBet(ctx, blind)
        
    def setBalance(self, balance):
        self.startingBalance = balance
        for p in self.participants:
            p.setInitBalance(balance)

    def dealCards(self):
        self.gamedeck.shuffle()

        for p in self.participants:
            for i in range(2):
                c = self.gamedeck.drawCard()
                p.addCard(c)

    def checkPlayerBalance(self):
        for i in self.participants:
            if i.getGameBalance()<=0:
                print(i.username(), "has left the table")
                self.participants.remove(i)

    def removePlayer(self,id):
        for i in self.participants:
            if i.username()==id:
                self.participants.remove(i)
        self.numPlayers-=1

    def createCommDeck(self):
        i = 0
        for i in range(3):
            self.addCardtoComm()
        
    def addCardtoComm(self):
        self.communityDeck.append(self.gameDeck.drawCard())

    def findWinner(self):
        for x in self.competing:
            commAndHand = self.communityDeck+ x._hand
            Eval=EvaluateHand(commAndHand)
            x._winCondition=Eval.evaluate()
            print (x._winCondition)

        winningCond = max(x._winCondition[0] for x in self.participants)
        print(winningCond)
        compete=[]
        for x in self.participants:
            if x._winCondition[0]==winningCond:
                compete.append(x)
        winners=Eval.winning(compete,winningCond)
        for x in winners:
            print(x._username+": "+ x.getWinCond())

    def resetRound(self):
        self.gameStarted=False
        self.currentPot=0
        self.communityDeck.clear()
        self.gamedeck= Deck()
        self.numPlayers=len(self.participants)
