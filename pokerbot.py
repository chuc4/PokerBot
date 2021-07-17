import asyncio
import discord
from discord.ext import commands
import time

from Poker.server import Server
from Poker.leaderboard import Leaderboard



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
        # print("hi")

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('---------')

server_bot = Server()
leaderboard_bot = Leaderboard()


@bot.command()
async def help(ctx):
    embed = discord.Embed(title="List of Commands", 
    description=server_bot.help(),
    color=0xffffff)
    embed.set_thumbnail(url="https://s.wsj.net/public/resources/images/JR-AA451_IFPOKE_GR_20191031164807.jpg")
    await ctx.send(embed=embed)
    

@bot.command()
async def create(ctx):
    if (server_bot.addPlayer(ctx)): 
        await ctx.send("You have created an account!")
        leaderboard_bot.addplayer(str(ctx.author.id))
        # leaderboard_bot.addplayer(str(str(ctx.author.name) + "#" + str(ctx.author.discriminator)))
    else: await ctx.send("You already created an account!")

@bot.command()
async def top(ctx):
    sort_byvalue= leaderboard_bot.getLeaderboard(ctx)
    leaderboard=""
    k=1
    for i in sort_byvalue:
        name = str(await bot.fetch_user(int(i[0])))
        leaderboard+= str(k)+". "+name+" - "+ str(i[1])+" <:chips:865450470671646760>\n"
        k+=1
    embed = discord.Embed(title=ctx.message.guild.name+" Leaderboard:",
    description=leaderboard,
    color=discord.Color.red())
    embed.set_thumbnail(url=ctx.message.guild.icon_url) 
    await ctx.send(embed=embed)



@bot.command()
async def balance(ctx):
    balance= await server_bot.getBalance(ctx)
    if (balance!=None):
        embed = discord.Embed(title=ctx.author.name+"'s Balance:", 
        description=str(balance)+" <:chips:865450470671646760>",
        color=discord.Color.green())
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)



@bot.command() 
async def p(ctx, *args):
    blind = 20
    startAmt = 1000

    if len(args)==2:
        blind = args[0]
        startAmt = args[1]
    
    embed = discord.Embed(title="Poker: Texas hold 'em", 
    description="Starting Balance: "+str(startAmt)+""" <:chips:865450470671646760>
    Min Bet: """+str(blind)+""" <:chips:865450470671646760> 
    \nReact to Join!""",
    color=discord.Color.green())
    players = []

    message = await ctx.send(embed=embed)
    await message.add_reaction('✅')
    await asyncio.sleep(10)

    message = await ctx.fetch_message(message.id)

    for reaction in message.reactions:
        if reaction.emoji == '✅':
            async for user in reaction.users():
                if user != bot.user:
                    players.append(user.mention)
    if len(players)<2:
        await ctx.send("Not enough players")
    else:
        await ctx.send(players)
        



if __name__ == '__main__':
    main()