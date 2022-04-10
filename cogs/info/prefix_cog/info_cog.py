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
    async def joined(self, ctx: commands.Context, *, member: discord.Member = None):
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
        await joined_callback(ctx, member)

    @commands.command()
    @commands.guild_only()
    async def toprole(self, ctx: commands.Context, *, member: discord.Member = None):
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
        await toprole_callback(ctx, member)

    @commands.command(alias=["perms"])
    @commands.guild_only()
    async def permissions(
        self, ctx: commands.Context, *, member: discord.Member = None
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
        await perms_callback(ctx, member)

    @commands.command()
    @commands.guild_only()
    async def botinfo(self, ctx: commands.Context):
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
        await botinfo_callback(ctx, self.client)

    @commands.command()
    async def avatar(self, ctx: commands.Context, *, member: discord.Member = None):
        """
        💡 Shows a member's avatar. If no member is specified, it shows yours.

        ❓ This will change depending on whether the bot is self-hosted.

        Usage:
        ```
        ~avatar [@member]
        ```
        Or:
        ```
        /avatar [@member]
        ```
        """
        await avatar_callback(ctx, member)


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
