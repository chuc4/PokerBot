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
            
    async def askMove(self, ctx, hand):
        await ctx.send("Here is your hand:")
        for card in hand:
            card.show()
        await ctx.send("Would you like to call, raise, or fold?")

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

    async def showCards(self, ctx, seat, pkr_players):
        play_hand = pkr_players[seat-1].getHand()
        await ctx.send("Your current hand:")
        for card in play_hand:
            card.show()

    async def showCommCards(self, ctx, comm_deck):
        await ctx.send("CURRENT COMMUNITY DECK")
        for card in comm_deck:
            card.show()
            
    async def reportRaise(self, ctx, seat, pkr_players):
        await ctx.send(pkr_players[seat-1].username() + " has raised!")

    async def reportCall(self, ctx, seat, pkr_players):
        await ctx.send(pkr_players[seat-1].username() + " has called!")

    async def reportFold(self, ctx, seat, pkr_players):
        await ctx.send(pkr_players[seat-1].username() + " has folded!")

    async def showBalances(self, ctx, pkr_players):
        await ctx.send("CURRENT BALANCES:")
        for player in pkr_players:
            ctx.send(player.username() + ": " + player.getGameBalance())

    async def askLeave(self, ctx):
        await ctx.send("Thanks for playing Poker with us! Hope you stop by again soon!")
    
    async def resetGame(self, ctx):
        await ctx.send("A new game will be starting soon. Resetting...")