"""
Contains a embedded help command.
"""

import sys
import discord

from discord.ext import commands
from .help_command import HelpCommand

sys.path.append("../handlers")


class HelpCommandCog(commands.Cog, name="Help"):
    """
    ❓ Shows help information about commands.
    """

    def __init__(self, client: commands.Bot):
        self.client = client
        self._current_help_command = client.help_command
        client.help_command = HelpCommand()
        client.help_command.cog = self

    async def cog_unload(self):
        """
        Called when the cog is removed.
        """
        self.client.help_command = self._current_help_command

    @commands.command()
    async def docs(self, ctx: commands.Context):
        """
        Sends a link to the documentation.

        Usage:
        ```
        ~docs
        ```
        """
        embed = discord.Embed(
            title="Beep Boop Bot Documentation",
            url="https://github.com/matthewflegg/beepboop/blob/main/README.md",
            description="View the official commands list for Beep Boop Bot on GitHub.",
        )

        embed.set_author(
            name="Matthew Flegg",
            url="https://github.com/matthewflegg",
            icon_url="https://imagemagick.org/image/convex-hull.png",
        )

        embed.set_footer(
            text="Contribute to the open source Beep Boop Bot GitHub repository."
        )

        await ctx.send(embed=embed)


async def setup(client: commands.Bot):
    """
    Registers the cog with the client.
    """
    await client.add_cog(HelpCommandCog(client))


async def teardown(client: commands.Bot):
    """
    Un-registers the cog with the client.
    """
    await client.remove_cog(HelpCommandCog(client))
