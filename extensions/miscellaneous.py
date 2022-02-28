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
        """Chooses between multiple choices.
        Used in format: .choose a b c OR .choose "option a" "option b" "option c".
        """

        # Randomly choose one of the parameters
        await ctx.send(random.choice(choices))

    @commands.command(description="Beep boop bot becomes the beep to your boop")
    async def beep(self, ctx: commands.Context):
        """Replies with boop"""
        await ctx.send("boop")

    @commands.command(pass_context=True, description="For when you feel like living on the edge")
    async def russianroulette(self, ctx: commands.Context):
        """Has a 1/6 chance of kicking the user who used the command"""

        choice = random.randint(1, 6)

        # 5/6 chance, user wins
        if choice != 6:
            await ctx.send("You were lucky... This time ;)")
            return

        # 1/6 chance, user loses + gets kicked
        await ctx.send("Oops... You lost")
        await ctx.author.kick()

    @commands.command(description="Gets a random meme from Reddit")
    async def meme(self, ctx: commands.Context):
        """Sends a HerokuApp API request to get a meme from Reddit"""

        # Get a random meme
        content = get("https://meme-api.herokuapp.com/gimme").text
        data = json.loads(content,)

        # Create an embed
        meme = discord.Embed()
        meme.title = f"{data['title']}"
        meme.color = discord.Color(0x486572)
        meme.set_image(url=f"{data['url']}")

        await ctx.reply(embed=meme)


def setup(bot: commands.Bot):
    """Adds the 'Miscellaneous' cog to the bot"""
    bot.add_cog(Miscellaneous(bot))