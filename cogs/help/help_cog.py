"""
Contains a embedded help command.
"""

import nextcord
import start
import sys

sys.path.append('../handlers')

from nextcord.ext import commands
from .help_command import HelpCommand


class HelpCommandCog(commands.Cog, name='Help'):
    """❓ Shows help information about commands."""
    def __init__(self, client: commands.Bot):
        self._current_help_command = client.help_command

        client.help_command = HelpCommand()
        client.help_command.cog = self

    def cog_unload(self):
        """Called when the cog is removed."""
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
        embed = nextcord.Embed(
            title="Beep Boop Bot Documentation",
            color=start.colour,
            url="https://github.com/matthewflegg/beepboop/blob/main/README.md",
            description="View the official commands list for Beep Boop Bot on GitHub.",
        )

        embed.set_author(
            name="Matthew Flegg",
            url="https://github.com/matthewflegg",
            icon_url="https://imagemagick.org/image/convex-hull.png",
        )

        embed.set_thumbnail(
            url="https://media.istockphoto.com/vectors/robot-avatar-icon-vector-id908807494?k=20&m=908807494&s=612x612&w=0&h=N050SIC8pgzsf_LaJT-ZyEE6HHMXLU5PYfMpixuinas="
        )

        embed.set_footer(
            text="Contribute to the open source Beep Boop Bot GitHub repository."
        )

        await ctx.send(embed=embed)


def setup(client: commands.Bot):
    """Registers the cog with the client."""
    client.add_cog(HelpCommandCog(client))


def teardown(client: commands.Bot):
    """Un-registers the cog with the client."""
    client.remove_cog(HelpCommandCog(client))

