from Poker.player import Player

class Server:
    def __init__(self):
        self.players = {}
        self.resets = 0
    
    def addPlayer(self, ctx):
        if ctx.author.id not in self.players:
            player = Player(ctx.author.name, 3000)
            self.players[ctx.author.id] = player
            return True
        else:
            return False
    
    async def getBalance(self, ctx):
        if ctx.author.id not in self.players:
            await ctx.send("You do not have an account! Use the .create command to create an account!")
            return None
        else:
            player = self.players[ctx.author.id]
            val=player.getBalance()
            return val
            # await ctx.send("You currently have " + str(player.getBalance()) + " chips!")
    
    def reset(self):
        for player in self.players:
            player.setBalance(3000)
        self.resets += 1
    
    def help(self):
        
        description="""**.create** - Create your profile for the server 
        **.p** - Create and play a game of Texas Hold'Em Poker
        **.balance** - Check to see how many chips you have
        **.top** - Check the leaderboards to see who is on top
        **.join** - Join an already existing Poker game
        **(Mods Only) .reset** - Reset the balances of everyone in the server"""
        return description
        
        
