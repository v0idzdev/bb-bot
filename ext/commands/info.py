"""
Module `info` contains the `info` cog/group, which implements
information commands for BB.Bot.
"""
import discord
import datetime
import core

from discord.ext import commands
from discord import app_commands
from typing import Optional


class Info(commands.Cog, app_commands.Group, name="info"):
    """
    💡 Provides infomation about servers, members, and more.
    """
    def __init__(self, client: core.DiscordClient) -> None:
        self.client = client
        super().__init__()

    @app_commands.command()
    @app_commands.describe(member="❓ The member to view the join date of.")
    async def joined(self, interaction: discord.Interaction, *, member: discord.Member) -> None:
        """
        💡 Shows a member's join date. If no member is specified, it shows yours.
        """
        if member is None:
            member = interaction.user

        date = member.joined_at.strftime("%d/%m/%Y")
        time = member.joined_at.strftime("%I:%M %p")

        joined_embed = discord.Embed(
            title="💡 Join Date",
            description=f"**`@{member.name}`** | **`{member.discriminator}`**.",
        ) \
            .add_field(name="⏳ Time", value=f"**{date}** | *{time}*.") \
            .set_author(icon_url=member.avatar.url or None, name=member.name)
        
        await interaction.response.send_message(embed=joined_embed, ephemeral=True)

    @app_commands.command()
    @app_commands.describe(member="❓ The member to view the top role of.")
    async def toprole(self, interaction: discord.Interaction, *, member: Optional[discord.Member]=None) -> None:
        """
        💡 Shows a member's top role. If no member is specified, it shows yours.
        """
        if member is None:
            member = interaction.user

        top_role_embed = discord.Embed(
            title="💡 Top Role",
            description=f"**`@{member.name}`** | **`{member.discriminator}`**.",
        ) \
            .add_field(name="🏷️ Role", value=f"*@{member.top_role.name}*") \
            .set_author(icon_url=member.avatar.url or None, name=member.name)
        
        await interaction.response.send_message(embed=top_role_embed, ephemeral=True)
    
    @app_commands.command()
    @app_commands.describe(member="❓ The member to view the permissions of.")
    async def perms(self, interaction: discord.Interaction, *, member: Optional[discord.Member]=None) -> None:
        """
        💡 Shows a member's perms. If no member is specified, it shows yours.
        """
        if member is None:
            member = interaction.user

        perms_embed = discord.Embed(
            title="💡 Permissions",
            description=f"**`@{member.name}`** | **`{member.discriminator}`**.",
        ) \
            .set_author(icon_url=member.avatar.url or None, name=member.name) \
            .add_field(
                name="💎 Perms",
                value="\u200b".join(f"`{perm}` " for perm, value in member.guild_permissions if value) or "..."
            )

        await interaction.response.send_message(embed=perms_embed, ephemeral=True)
    
    @app_commands.command()
    @app_commands.describe(member="❓ The member to view the avatar of.")
    async def avatar(self, interaction: discord.Interaction, *, member: Optional[discord.Member]=None) -> None:
        """ 
        💡 Shows a member's avatar. If no member is specified, it shows yours.
        """
        if member is None:
            member = interaction.user

        avatar_embed = discord.Embed(
            title="💡 Avatar",
            description=f"**`@{member.name}`** | **`{member.discriminator}`**.",
        ) \
            .set_image(url=member.avatar.url or None)
        
        await interaction.response.send_message(embed=avatar_embed, ephemeral=True)
        


async def setup(client: core.DiscordClient) -> None:
    """
    Registers the command group/cog with the discord client.
    All extensions must have a setup function.

    Params:
     - client: (DiscordClient): The client to register the cog with.
    """
    await client.add_cog(Info(client))


async def teardown(client: core.DiscordClient) -> None:
    """
    De-registers the command group/cog with the discord client.
    This is not usually needed, but is useful to have.

    Params:
     - client: (DiscordClient): The client to de-register the cog with.
    """
    await client.remove_cog(Info(client))