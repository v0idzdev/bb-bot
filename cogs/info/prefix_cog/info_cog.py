import discord

from client import Client
from discord import app_commands

from ..info_commands import *


class InfoCog(commands.Cog, name="Info"):
    """
    💡 Commands that provide info and stats.
    """

    def __init__(self, client: Client) -> None:
        self.client = client

    @commands.command()
    @commands.guild_only()
    async def joined(
        self, interaction: discord.Interaction, *, member: discord.Member = None
    ):
        """
        💡 Shows when a member joined the server.

        ❓ If no member is specified, the bot will show when you joined.

        Usage:
        ```
        ~joined [@member]
        ```
        Or:
        ```
        /joined [@member]
        ```
        """
        await joined_callback(interaction, member)

    @commands.command()
    @commands.guild_only()
    async def toprole(
        self, interaction: discord.Interaction, *, member: discord.Member = None
    ):
        """
        💡 Shows the top role for a member.

        ❓ If no member is specified, the bot will show your top role.

        Usage:
        ```
        ~toprole [@member]
        ```
        Or:
        ```
        /toprole [@member]
        ```
        """
        await toprole_callback(interaction, member)

    @commands.command(alias=["perms"])
    @commands.guild_only()
    async def permissions(
        self, interaction: discord.Interaction, *, member: discord.Member = None
    ):
        """
        💡 Shows the permissions for a member.

        ❓ If no member is specified, the bot will show your permissions.

        Usage:
        ```
        ~permissions | ~perms [@member]
        ```
        Or:
        ```
        /permissions [@member]
        ```
        """
        await perms_callback(interaction, member)

    @commands.command()
    @commands.guild_only()
    async def botinfo(self, interaction: discord.Interaction):
        """
        💡 Shows information about the bot.

        ❓ This will change depending on whether the bot is self-hosted.

        Usage:
        ```
        ~botinfo [@member]
        ```
        Or:
        ```
        /botinfo [@member]
        ```
        """
        await botinfo_callback(interaction, self.client)



async def setup(client: commands.Bot):
    """
    Registers the cog with the client.
    """
    await client.add_cog(InfoCog(client))


async def teardown(client: commands.Bot):
    """
    Un-registers the cog with the client.
    """
    await client.remove_cog(InfoCog(client))
