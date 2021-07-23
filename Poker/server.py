from Poker.leaderboard import Leaderboard
from Poker.pokerwrapper import PokerWrapper
from Poker.announcer import Announcer
import discord
from Poker.player import Player

class Server:
    def __init__(self, bot):
        self.bot=bot
        self.players = {}
        self.resets = 0
        self.announcerUI = Announcer()
    
    async def addPlayer(self, ctx):
        if ctx.author.id not in self.players:
            player = Player(ctx.author.id, 3000)
            self.players[ctx.author.id] = player
            await ctx.send("You have created an account!")
            return True
        else:
            await ctx.send("You already created an account!")
            return False
    
    async def getBalance(self, ctx):
        if ctx.author.id not in self.players:
            await ctx.send("You do not have an account! Use the .create command to create an account!")
        else:
            player = self.players[ctx.author.id]
            balance=player.getBalance()
            embed = discord.Embed(title=ctx.author.name+"'s Balance:", 
            description=str(balance)+" <:chips:865450470671646760>",
            color=discord.Color.green())
            embed.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

    
    def reset(self):
        for player in self.players:
            player.setBalance(3000)
        self.resets += 1
    
    async def help(self, ctx):

        embed = discord.Embed(title="List of Commands", 
        description="""**.create** - Create your profile for the server 
        **.p** - Create and play a game of Texas Hold'Em Poker
        **.balance** - Check to see how many chips you have
        **.top** - Check the leaderboards to see who is on top
        **.join** - Join an already existing Poker game
        **(Mods Only) .reset** - Reset the balances of everyone in the server""",
        color=0xffffff)
        embed.set_thumbnail(url="https://s.wsj.net/public/resources/images/JR-AA451_IFPOKE_GR_20191031164807.jpg")
        await ctx.send(embed=embed)
        
    async def printLeaderboard(self, ctx):
        sort_byvalue=sorted(self.players.items(),key=lambda x:x[1].balance,reverse=True)
        leaderboard=""
        k=1
        for i in sort_byvalue:
            name = str(await self.bot.fetch_user(i[1].id))
            leaderboard+= str(k)+". "+name+" - "+ str(i[1].balance)+" <:chips:865450470671646760>\n"
            k+=1
        embed = discord.Embed(title=ctx.message.guild.name+" Leaderboard:",
        description=leaderboard,
        color=discord.Color.red())
        embed.set_thumbnail(url=ctx.message.guild.icon_url) 
        await ctx.send(embed=embed)

    # def validate_game(ctx): #check if in game in channel is in progress
    #     return

    def validate_game(self, ctx): #check if in game in channel is in progress
        return

    async def initiateGame(self, ctx, id, bot):
        new_game = PokerWrapper(id,bot)
        await self.startGame(ctx, new_game, bot)
        await self.join(ctx, new_game, bot)
        await self.startRounds(ctx, new_game, bot)
        await self.findWinner(ctx, new_game)
        await self.resetRound(ctx, new_game, bot)
    
    async def redoGame(self, ctx, game, bot):
        await self.startGame(ctx, game)
        await self.join(ctx, game, bot)
        await self.startRounds(ctx, game, bot)
        await self.findWinner(ctx, game)
        await self.resetRound(ctx, game, bot)

    async def startGame(self, ctx, game, bot):
        self.validate_game(ctx)
        await game.startGame(ctx)
        await game.setBlind(ctx, bot)
        await game.setBalance(ctx) #change this function later

    
    async def join(self, ctx, game, bot):
        await game.setPlayers(ctx, bot)
        """
        - 
        """
    
    async def startRounds(self, ctx, game, bot):
        await game.dealCards(bot) #needs to send dm's
        game.setDealer(ctx) #needs to be implemented
        game.takeBlinds(ctx) #needs to be implemented
        await self.flop(ctx, game)
        # self.nextTurns()
        await self.turn(ctx, game)
        # self.nextTurns()
        await self.river(ctx, game)
        # self.nextTurns()
    
    async def flop(self, ctx, game):
        game.createCommDeck()
        commDeck = game.communityDeck
        await self.announcerUI.showCommCards(ctx, commDeck)

    def nextTurns(self, pool, message): 
        while len(pool) != 0:
            hasRaised = False
            i = 0
            for i in range(len(pool)):
                self.announcer.askMove(pool[i].getHand(), hasRaised)
                format_msg = message.content.lower().strip().split()
                pool[i].setAction(format_msg)
                if format_msg == "raise":
                    self.announcer.reportRaise(pool[i].username, format_msg[1]) 
                    hasRaised = True
                    temp = pool.pop(i)
                    pool.append(temp)
                if format_msg == "call": 
                    self.announcer.reportCall(pool[i].username)
                    i += 1
                if format_msg == "check":
                    self.announcer.reportCheck(pool[i].username)
                    i += 1
                if format_msg == "fold":
                    self.announcer.reportFold(pool[i].username)
                    self.pokerWrapper.removePlayer(message.author.id)
                    pool.pop(i)
    
    async def turn(self, ctx, game):
        game.addCardtoComm()
        commDeck = game.communityDeck
        await game.pokerUI.showCommCards(ctx, commDeck)
    
    async def river(self, ctx, game):
        game.addCardtoComm()
        commDeck = game.communityDeck
        await game.pokerUI.showCommCards(ctx, commDeck)
    
    async def findWinner(self, ctx, game):
        winners = game.findWinner() #needs to return a list of winners
        for x in winners:
            await ctx.send(x._username+": " + x.getWinCond())
        #announce the winner(s) of the game

    async def resetRound(self, ctx, game, bot):
        await game.pokerUI.askLeave() #needs to be implemented
        await self.join(ctx, game, bot)
        game.resetRound()
        await self.redoGame(ctx, game, bot)
