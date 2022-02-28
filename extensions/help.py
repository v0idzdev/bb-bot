import discord
from discord.ext import commands


class Help(commands.Cog):
    """Command category for help commands"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(description="Generates an embed that links to the Beep Boop Bot documentation")
    async def docs(self, ctx: commands.Context):
        """Creates an embed that links to the docs page"""

        embed = discord.Embed()
        embed.title = "Beep Boop Bot Documentation"
        embed.url = "https://github.com/matthewflegg/beepboop/blob/main/README.md"
        embed.description="📃 See the official documentation for Beep Boop Bot on GitHub"
        embed.color=discord.Color(0x486572)
        embed.author.name="Matthew Flegg"
        embed.author.url="https://github.com/matthewflegg"
        embed.author.icon_url="https://imagemagick.org/image/convex-hull.png"
        embed.set_thumbnail(url="https://media.istockphoto.com/vectors/robot-avatar-icon-vector-id908807494?k=20&m=908807494&s=612x612&w=0&h=N050SIC8pgzsf_LaJT-ZyEE6HHMXLU5PYfMpixuinas=")
        embed.set_footer(text="📙 Contribute to the open source Beep Boop Bot GitHub repository")

        await ctx.send(embed=embed)


def setup(bot):
    """Adds the 'Help' cog to the bot"""
    bot.add_cog(Help(bot))