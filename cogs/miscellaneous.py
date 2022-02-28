import random
from discord.ext import commands


class Miscellaneous(commands.Cog):
    """Command category for miscellaneous/dumb commands"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="For when you want an expert opinion on a serious matter")
    async def choose(self, ctx, *choices: str):
        """Chooses between multiple choices"""
        await ctx.send(random.choice(choices))

    @commands.command(description="Beep boop bot becomes the beep to your boop")
    async def beep(self, ctx):
        """Replies with boop"""
        await ctx.send("boop")

    @commands.command(pass_context=True, description="For when you feel like living on the edge")
    async def russianroulette(self, ctx):
        """Has a 1/6 chance of kicking the user who used the command"""

        choice = random.randint(1, 6)

        if choice != 6:
            await ctx.send("You were lucky... This time ;)")
            return

        # ! Currently, the bot doesn't actually kick anyone because the command hasn't been tested

        ctx.send("Oops... You lost")
        await ctx.send(f"Pretending to kick {ctx.author.name} for debugging purposes")
        # await ctx.author.kick()


def setup(bot):
    """Adds the 'Miscellaneous' cog to the bot"""
    bot.add_cog(Miscellaneous(bot))