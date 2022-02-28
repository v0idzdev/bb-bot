import random
import discord
import json
from requests import get
from discord.ext import commands


class Miscellaneous(commands.Cog):
    """Command category for miscellaneous/dumb commands"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(description="For when you want an expert opinion on a serious matter")
    async def choose(self, ctx: commands.Context, *choices: str):
        """Chooses between multiple choices"""
        await ctx.send(random.choice(choices))

    @commands.command(description="Beep boop bot becomes the beep to your boop")
    async def beep(self, ctx: commands.Context):
        """Replies with boop"""
        await ctx.send("boop")

    @commands.command(pass_context=True, description="For when you feel like living on the edge")
    async def russianroulette(self, ctx: commands.Context):
        """Has a 1/6 chance of kicking the user who used the command"""

        choice = random.randint(1, 6)

        if choice != 6:
            await ctx.send("You were lucky... This time ;)")
            return

        # ! Currently, the bot doesn't actually kick anyone because the command hasn't been tested

        await ctx.send("Oops... You lost")
        await ctx.send(f"Pretending to kick **{ctx.author.name}** for debugging purposes")
        # await ctx.author.kick()

    @commands.command(description="Gets a random meme from Reddit")
    async def meme(self, ctx: commands.Context):
        """Sends a HerokuApp API request to get a meme from Reddit"""

        content = get("https://meme-api.herokuapp.com/gimme").text
        data = json.loads(content,)

        meme = discord.Embed()
        meme.title = f"{data['title']}"
        meme.color = discord.Color(0x486572)
        meme.set_image(url=f"{data['url']}")

        await ctx.reply(embed=meme)


def setup(bot):
    """Adds the 'Miscellaneous' cog to the bot"""
    bot.add_cog(Miscellaneous(bot))