import discord

from client import Client
from discord.ext import commands
from discord import app_commands


class InfoCog(commands.Cog, name="Info"):
    """
    💡 Commands that provide info and stats.
    """

    def __init__(self, client: Client) -> None:
        self.client = client

    @app_commands.command()
    @app_commands.describe(member="💡 Choose a user to display information about.")
    async def joined(
        self, interaction: discord.Interaction, *, member: discord.Member = None
    ):
        """
        💡 Shows when you joined the server.

        ❓ If no member is specified, the bot will show when you joined.

        Usage:
        ```
        ~joined [@member]
        ```
        """
        await interaction.response.defer()

        if member is None:  # if no user is provided, show info about the member
            member = interaction.user

        embed = discord.Embed(
            title=f"💡 Join Date",
            description=f"👋🏻 **{member.joined_at}**",
        )

        embed.set_author(icon_url=member.avatar.url, name=member.display_name)
        await interaction.followup.send(embed=embed, ephemeral=True)

    @app_commands.command()
    @app_commands.describe(member="💡 Choose a user to display information about.")
    async def toprole(
        self, interaction: discord.Interaction, *, member: discord.Member = None
    ):
        """
        💡 Shows the top role for a member.

        ❓ If no member is specified, the bot will show your top role.

        Usage:
        ```
        ~joined [@member]
        ```
        """
        await interaction.response.defer()

        if member is None:
            member = interaction.user

        embed = discord.Embed(
            title=f"💡 Top Role",
            description=f"🌟 **{member.top_role.name}**",
        )

        embed.set_author(icon_url=member.avatar.url, name=member.display_name)
        await interaction.followup.send(embed=embed, ephemeral=True)

    @app_commands.command()
    @app_commands.describe(member="💡 Choose a user to display information about.")
    async def permissions(
        self, interaction: discord.Interaction, *, member: discord.Member = None
    ):
        """
        💡 Shows the top role for a member.

        ❓ If no member is specified, the bot will show your top role.

        Usage:
        ```
        ~joined [@member]
        ```
        """
        await interaction.response.defer()

        if member is None:
            member = interaction.user

        perms = "\n".join(
            f"`{perm}` " for perm, value in member.guild_permissions if value
        )

        embed = discord.Embed(
            title=f"💡 Permissions",
            description=perms,
        )

        embed.set_author(icon_url=member.avatar.url, name=member.display_name)
        await interaction.followup.send(embed=embed, ephemeral=True)


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
