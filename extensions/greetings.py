import discord
from discord.ext import commands


class Greetings(commands.Cog):
    """Command category for greeting commands."""
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Displays a welcome message when a member joins."""
        channel = member.guild.system_channel

        if channel is not None:
            await channel.send(f"👋 Welcome, **{member.mention}**!")

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        """Displays a goodbye message when a member leaves."""
        channel = member.guild.system_channel

        if channel is not None:
            await channel.send(f"👋 Goodbye, **{member.name}**.")

    @commands.command(name="hello", description="Says hello to a user, and hello again if they already used the command.")
    async def hello_(self, ctx: commands.Context, *, member: discord.Member=None):
        """Says hello to a user when a user uses .hello.
        Says hello again if the user uses the command more than once in a row.
        """

        member = member or ctx.author

        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send(f"Hello **{member.name}**!")
        else:
            await ctx.send(f"Hello again, **{member.name}**.")

        self._last_member = member


def setup(bot: commands.Bot):
    """Adds the Greetings cog to the bot."""
    bot.add_cog(Greetings(bot))