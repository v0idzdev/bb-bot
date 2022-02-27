import discord
import os

from discord.ext import commands, tasks
from dotenv import load_dotenv
from random import randint, random

load_dotenv(".env")

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"--- Username: {bot.user.name}")
    print(f"--- Bot ID: {bot.user.id}")


@bot.command(description="For when you want an expert opinion on a serious matter")
async def choose(ctx, *choices: str):
    """Chooses between multiple choices"""
    await ctx.send(random.choice(choices))


@bot.command(description="Beep boop bot becomes the beep to your boop")
async def beep(ctx):
    """Replies with boop"""
    await ctx.send("boop")


# @bot.group(pass_context=True, description="For when you feel like living on the edge")
@bot.command(pass_context=True, description="For when you feel like living on the edge")
async def russianroulette(ctx):
    """Has a 1/6 chance of kicking the user who used the command"""

    # await ctx.send(f"{ctx.author.name}, are you sure you want to play russian roulette?"
    #     + "There will be a 1/6 chance that you get kicked. (yes/no)")

    # ! Remove when uncommenting the "!russianroulette subcommands"
    choice = randint(1, 6)

    if choice != 6:
          await ctx.send("You were lucky... This time ;)")
          return

    ctx.send("Oops... You lost")
    await ctx.send("***Uhhh pretend they actually get kicked this is just for testing lol***")

# @russianroulette.command(pass_context=True)
# async def yes(ctx):
#     """A subcommand for [prefix]russianroulette - run if user types [prefix]yes"""
#     choice = randint(1, 6)

#     if choice != 6:
#         await ctx.send("You were lucky... This time ;)")
#         return

#     ctx.send("Oops... You lost")
#     await ctx.send("***Uhhh pretend they actually get kicked this is just for testing lol***")
#     # await ctx.author.kick()

# @russianroulette.command(pass_context=True)
# async def no(ctx):
#     """A subcommand for [prefix]russianroulette - run if user types [prefix]no"""
#     await ctx.send("Ok lol, I guess you don't like living on the edge :(")


TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)
