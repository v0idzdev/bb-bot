import random
import discord
import json
from requests import get
from discord.ext import commands


class Miscellaneous(commands.Cog):
    """Command category for miscellaneous/dumb commands"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="choose", aliases=["ch"], description="For when you want an expert opinion on a serious matter")
    async def choose_(self, ctx: commands.Context, *choices: str):
        """Chooses between multiple choices.
        Used in format: .choose a b c OR .choose "option a" "option b" "option c".
        """

        # Randomly choose one of the parameters
        await ctx.send(random.choice(choices))

    @commands.command(name="beep", description="Beep boop bot becomes the beep to your boop")
    async def beep_(self, ctx: commands.Context):
        """Replies with boop"""
        await ctx.send("boop")

    @commands.command(name="russianroulette", aliases=["rr"],
        pass_context=True, description="For when you feel like living on the edge")
    async def russianroulette_(self, ctx: commands.Context):
        """Has a 1/6 chance of kicking the user who used the command"""

        choice = random.randint(1, 6)

        # 5/6 chance, user wins
        if choice != 6:
            await ctx.send("You were lucky... This time ;)")
            return

        # 1/6 chance, user loses + gets kicked
        await ctx.send("Oops... You lost")
        await ctx.author.kick()

    @commands.command(name="meme", aliases=["m"], description="Gets a random meme from Reddit")
    async def meme_(self, ctx: commands.Context):
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

    @commands.command(name="poll", pass_context=True, description="For when you want to get opinions")
    async def poll_(self, ctx: commands.Context, *poll):
        """Sends an embed that lets users vote on a topic via reactions.
        Currently, there are only two reactions: yes/no or for/against etc.
        """

        user_name = ctx.message.author.name # Get the sender's username

        embed = discord.Embed()
        embed.title = f"Poll by **{user_name}**"
        embed.description = " ".join(poll)
        embed.color = discord.Color(0x486572)

        msg = await ctx.channel.send(embed=embed)

        # Add the reactions for yes/no
        await msg.add_reaction("✔️")
        await msg.add_reaction("❌")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        """Checks reactions to polls.
        Updates the embed message with the number of 'yes' votes and the
        number of 'no' votes.
        """

        if user.id != self.bot.user.id: # If the user isn't a bot
            cached_messages = discord.utils.get(self.bot.cached_messages, id=reaction.message.id)

            # Loop over all the reactions in the bot's cache
            # Check if the user is an author, if the user's not a bot, and if the reaction emoji isn't one they used
            for react in cached_messages.reactions:
                if user in await react.users().flatten() and not user.bot and str(react) != str(reaction.emoji):
                    await cached_messages.remove_reaction(react.emoji, user)


def setup(bot: commands.Bot):
    """Adds the 'Miscellaneous' cog to the bot"""
    bot.add_cog(Miscellaneous(bot))