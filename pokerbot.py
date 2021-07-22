import asyncio
import discord
from discord.ext import commands
import time

from Poker.server import Server
from Poker.leaderboard import Leaderboard
from Poker.pokerwrapper import PokerWrapper



intents = discord.Intents.default()
intents.members = True
description = '''A bot to play Poker with.'''
bot = commands.Bot(command_prefix='.', description=description)
bot.remove_command('help')

def main():
    try:
        bot.run('ODYzMjAzODY1MjQzNjgwNzg4.YOjfPw.UKKwd0qMwzIk2dPgwZyXx4Eubxk')
    finally:
        print(f'End running at {time.asctime(time.localtime(time.time()))}')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('---------')

server_bot = Server(bot)
# leaderboard_bot = Leaderboard(bot)


@bot.command()
async def help(ctx):
    await server_bot.help(ctx)
    

@bot.command()
async def create(ctx):
    await server_bot.addPlayer(ctx)
        


@bot.command()
async def top(ctx):
    await server_bot.printLeaderboard(ctx)


@bot.command()
async def balance(ctx):
    await server_bot.getBalance(ctx)


@bot.command() 
async def p(ctx):
    # print(ctx.message.channel.id)
    # discord.utils.get(ctx.guild.channels, name=given_name)
    game = PokerWrapper(ctx.message.channel.id, bot)
    await game.startGame(ctx)
    await game.setBalance(ctx)
    await game.setBlind(ctx)
    await game.setPlayers(ctx)
    
        
        



if __name__ == '__main__':
    main()