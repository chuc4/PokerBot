import random 
import discord
import asyncio 

class Announcer:
    async def initiateGame(self, ctx):
        await ctx.send("WELCOME TO POKER BOT!")
        await ctx.send("If this is your first time with Poker Bot," + 
        " please type \'.create\'. Please type \'.help\' for the rules" + 
        " and betting system.")
    
    async def askBet(self, ctx):
        await ctx.send("What is the big blind (minimum bet) amount?")
    
    async def announceWinner(self, ctx, sorted_players, com_deck, currentPot):
        #sending community hands
        winner = sorted_players[0].username()
        self.showCommCards(com_deck)
        await ctx.send(winner + " has won, receiving " + str(currentPot))
            
    async def askMove(self, ctx, member, hasRaised, blind, bot):
        if hasRaised or blind:
            await ctx.send("{}, Would you like to call, raise, or fold?".format(member))
        else:
            await ctx.send("{}, Would you like to check, raise, or fold?".format(member))

    async def askBalance(self, ctx):
        await ctx.send("What should be the starting game balance of all players?")

    ####IMPORTANT: MUST USE asyncio.run(joinTimer) IN ORDER TO CALL THIS FUNCTION.####
    async def joinTimer(self, ctx):
        time = 30
        while time != 0:
            if time == 5: 
                await ctx.send("Entries close in 5 seconds.")
            time -= 1
            await asyncio.sleep(1)
    
    ####IMPORTANT: MUST USE asyncio.run(joinQueue) IN ORDER TO CALL THIS FUNCTION.####
    async def joinQueue(self, ctx):
        print("now running timer")
        await ctx.send("Please click on the green checkmark to join the game!")
        ##REQUIRES ON_EVENT() IMPLEMENTATION FOR CHECKMARK##
        await ctx.send("A timer will begin now. You will have 60 seconds to join the game.")
        await self.joinTimer()
        await ctx.send("Time is up. The game will be starting shortly...")

    async def showCards(self, ctx, hand):
        cards=""
        for card in hand:
            cards+=card.show()
        await ctx.send(cards)

    async def showCommCards(self, ctx, comm_deck):
        await ctx.send("**CURRENT COMMUNITY DECK**")
        commCards=""
        i=0
        for card in comm_deck:
            commCards+=card.show()
            i+=1
        for j in range(5-i):
            commCards+="<:back:867926963061411871>"
        await ctx.send(commCards)
    async def reportRaise(self, ctx, name, amount):
        await ctx.send(name + " has raised to " + amount + " <:chips:865450470671646760>!")

    async def reportCall(self, ctx, name):
        await ctx.send(name + " has called!")

    async def reportFold(self, ctx, name):
        await ctx.send(name + " has folded!")
    
    async def reportCheck(self, ctx, name):
        await ctx.send(name + " has checked!")

    async def showBalances(self, ctx, pkr_players):
        await ctx.send("CURRENT BALANCES:")
        for player in pkr_players:
            await ctx.send(player.username() + ": " + str(player.getGameBalance())+ " <:chips:865450470671646760>")
    
    async def showPlayer(self, ctx, game):
        embed = discord.Embed(title=game.competing[0].username(), 
        description="Balance: "+str(game.competing[0].getGameBalance())+" <:chips:865450470671646760>" + """
        In Pot: """ + str(game.competing[0]._inPot)+""" <:chips:865450470671646760>
        
        Current Pot: """+ str(game.currentPot),
        color=discord.Color.green())
        embed.set_thumbnail(url=game.competing[0]._user.avatar_url)
        await ctx.send(embed=embed)

    async def askLeave(self, ctx):
        await ctx.send("Thanks for playing Poker with us! Hope you stop by again soon!")
    
    async def resetGame(self, ctx):
        await ctx.send("*\n\n**A NEW GAME HAS STARTED**")