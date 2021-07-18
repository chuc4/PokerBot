from Poker.leaderboard import Leaderboard
import discord
from Poker.player import Player

class Server:
    def __init__(self, bot):
        self.bot=bot
        self.players = {}
        self.resets = 0
    
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

        
        
