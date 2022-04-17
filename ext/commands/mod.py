"""
Module `mod` contains the `mod` cog/group, which implements
server moderation commands for BB.Bot.
"""
import asyncio
import discord
import datetime
import core

from enum import Enum, auto
from discord.ext import commands
from discord import app_commands
from typing import Optional


class TimeUnit(Enum):
    """
    Used with the `amount` parameter in certain commands to denote
    whether the user wants to ban another user for `amount` seconds,
    minutes, hours, or days.
    """
    SECONDS = auto()
    MINUTES = auto()
    HOURS = auto()
    DAYS = auto()


class Mod(commands.Cog, app_commands.Group, name="mod"):
    """
    ⚙️ Command group for server moderators and administrators.
    """
    def __init__(self, client: core.DiscordClient) -> None:
        self.client = client

    @app_commands.command()
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.cooldown(1, 5, key=lambda interaction: interaction.guild.id)
    async def purge(self, interaction: discord.Interaction, *, amount: int=6) -> None:
        """
        ⚙️ Clears a specified number of messages from a channel. Defaults to 6.
        """
        await interaction.response.defer()
        await interaction.channel.purge(limit=amount)

        embed = discord.Embed(
            title="⚙️ Messages Purged",
            description=f"💡 Number of Messages: **{amount}**.",
            timestamp=datetime.datetime.utcnow()
        )

        await interaction.followup.send(embed=embed)

    @app_commands.command()
    @app_commands.describe(
        member="❓ The member to temporarily mute.",
        timeunit="❓ Whether you want to mute them for a certain number of seconds, minutes, hours, or days.",
        amount="❓ The number of seconds, minutes, hours, or days to mute the member for.",
        reason="❓ The reason for temporarily muting the member."
    )
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.cooldown(1, 5, key=lambda interaction: interaction.guild.id)
    async def tempmute(
        self,
        interaction: discord.Interaction,
        *,
        member: discord.Member,
        timeunit: TimeUnit,
        amount: int,
        reason: Optional[str]=None
    ):
        """
        ⚙️ Mutes a member of a server for a specified amount of time.
        """
        await interaction.response.defer()
        guild = interaction.guild
        role = discord.utils.get(guild.roles, "Muted")
        await member.add_roles(role)

        for channel in guild.channels:
            await channel.set_permissions(
                role,
                speak=False,
                send_messages=False,
                read_message_history=False,
                read_messages=False
            )

        muted_embed = discord.Embed(
            title="⚙️ Member Muted",
            description=f"💡 Member: **{member.name}**.",
            timestamp=datetime.datetime.utcnow()
        )

        if reason:
            muted_embed.add_field(name="🖊️ Reason", value=reason, inline=False)

        muted_embed.add_field(name="⏳ Time", value=f"**{amount}**{str(timeunit)[0]}")
        await interaction.followup.send(embed=muted_embed)
        seconds_muted = amount

        if timeunit == TimeUnit.MINUTES:
            seconds_muted *= 60
        if timeunit == TimeUnit.HOURS:
            seconds_muted *= (60 * 60)
        if timeunit == TimeUnit.DAYS:
            seconds_muted *= (60 * 60 * 24)

        await asyncio.sleep(seconds_muted)
        await member.remove_roles(role)

        unmuted_embed = discord.Embed(
            title="⚙️ Member Unmuted",
            description=f"💡 Member: **{member.name}**.",
            timestamp=datetime.datetime.utcnow()
        )

        await interaction.followup.send(embed=unmuted_embed)

    @app_commands.command()
    @app_commands.describe(
        member="❓ The member to mute.",
        reason="❓ The reason for muting the member."
    )
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.cooldown(1, 5, key=lambda interaction: interaction.guild.id)
    async def mute(
        self,
        interaction: discord.Interaction,
        *,
        member: discord.Member,
        reason: Optional[str]=None
    ):
        """
        ⚙️ Mutes a member of a server until they are unmuted.
        """
        guild = interaction.guild
        muted_role = discord.utils.get(guild.roles, name="Muted")

        if not muted_role:
            muted_role = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(
                muted_role,
                speak=False,
                send_messages=False,
                read_message_history=False,
                read_messages=False
            )

        muted_embed = discord.Embed(
            title="⚙️ Member Muted",
            description=f"💡 Member: **{member.name}**.",
            timestamp=datetime.datetime.utcnow()
        )

        if reason:
            muted_embed.add_field(name="🖊️ Reason", value=reason, inline=False)

        await interaction.followup.send(embed=muted_embed)
        await member.add_roles(muted_role, reason=reason)

    @app_commands.command()
    @app_commands.describe(member="❓ The member to unmute.")
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.cooldown(1, 5, key=lambda interaction: interaction.guild.id)
    async def unmute(self, interaction: discord.Interaction, *, member: discord.Member):
        """
        ⚙️ Unmutes a member of a server.
        """
        await interaction.response.defer()
        muted_role = discord.utils.get(interaction.guild.roles, name="Muted")
        await member.remove_roles(muted_role)

        unmuted_embed = discord.Embed(
            title="⚙️ Member Unmuted",
            description=f"💡 Member: **{member.name}**.",
            timestamp=datetime.datetime.utcnow()
        )

        await interaction.followup.send(embed=unmuted_embed)

    @app_commands.command()
    @app_commands.describe(
        member="❓ The member to kick from the server.",
        reason="❓ The reason for kicking the member."
    )
    @app_commands.checks.has_permissions(kick_members=True)
    @app_commands.checks.cooldown(1, 5, key=lambda interaction: interaction.guild.id)
    async def kick(
        self,
        interaction: discord.Interaction,
        *,
        member: discord.Member,
        reason: Optional[str]=None
    ):
        """
        ⚙️ Kicks a member from a server.
        """
        await interaction.response.defer()
        guild = interaction.guild

        kicked_embed = discord.Embed(
            title="⚙️ Member Kicked",
            description=f"💡 Member: **{member.name}**.",
            timestamp=datetime.datetime.utcnow()
        )

        if reason:
            kicked_embed.add_field(name="🖊️ Reason", value=reason, inline=False)

        await interaction.followup.send(embed=kicked_embed)
        await guild.kick(member)

    @app_commands.command()
    @app_commands.describe(
        member="❓ The member to temporarily ban.",
        timeunit="❓ Whether you want to ban them for a certain number of seconds, minutes, hours, or days.",
        amount="❓ The number of seconds, minutes, hours, or days to ban the member for.",
        reason="❓ The reason for temporarily banning the member."
    )
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.checks.cooldown(1, 5, key=lambda interaction: interaction.guild.id)
    async def tempban(
        self,
        interaction: discord.Interaction,
        *,
        member: discord.Member,
        timeunit: TimeUnit,
        amount: int,
        reason: Optional[str]=None
    ):
        """
        ⚙️ Bans a member of a server for a specified amount of time.
        """
        await interaction.response.defer()
        guild = interaction.guild

        banned_embed = discord.Embed(
            title="⚙️ Member Banned",
            description=f"💡 Member: **{member.name}**.",
            timestamp=datetime.datetime.utcnow()
        )

        if reason:
            banned_embed.add_field(name="🖊️ Reason", value=reason, inline=False)

        banned_embed.add_field(name="⏳ Time", value=f"**{amount}**{str(timeunit)[0]}")
        await interaction.followup.send(embed=banned_embed)
        await guild.ban(member, reason=reason)
        seconds_banned = amount

        if timeunit == TimeUnit.MINUTES:
            seconds_banned *= 60
        if timeunit == TimeUnit.HOURS:
            seconds_banned *= (60 * 60)
        if timeunit == TimeUnit.DAYS:
            seconds_banned *= (60 * 60 * 24)

        await asyncio.sleep(seconds_banned)
        await guild.unban(user=member)

        unbanned_embed = discord.Embed(
            title="⚙️ Member Unbanned",
            description=f"💡 Member: **{member.name}**.",
            timestamp=datetime.datetime.utcnow()
        )

        await interaction.followup.send(embed=unbanned_embed)

    @app_commands.command()
    @app_commands.describe(
        member="❓ The member to ban.",
        reason="❓ The reason for banning the member."
    )
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.checks.cooldown(1, 5, key=lambda interaction: interaction.guild.id)
    async def ban(
        self,
        interaction: discord.Interaction,
        *,
        member: discord.Member,
        reason: Optional[str]=None
    ):
        """
        ⚙️ Mutes a member of a server until they are unmuted.
        """
        await interaction.response.defer()
        guild = interaction.guild

        banned_embed = discord.Embed(
            title="⚙️ Member Banned",
            description=f"💡 Member: **{member.name}**.",
            timestamp=datetime.datetime.utcnow()
        )

        if reason:
            banned_embed.add_field(name="🖊️ Reason", value=reason, inline=False)

        await interaction.followup.send(embed=banned_embed)
        await guild.ban(member, reason=reason)

    @app_commands.command()
    @app_commands.describe(member="❓ The member to unban.")
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.checks.cooldown(1, 5, key=lambda interaction: interaction.guild.id)
    async def unban(self, interaction: discord.Interaction, *, member: discord.Member):
        """
        ⚙️ Unbans a member of a server.
        """
        await interaction.response.defer()
        await interaction.guild.unban(member)

        unbanned_embed = discord.Embed(
            title="⚙️ Member Unmuted",
            description=f"💡 Member: **{member.name}**.",
            timestamp=datetime.datetime.utcnow()
        )

        await interaction.followup.send(embed=unbanned_embed)


async def setup(client: core.DiscordClient) -> None:
    """
    Registers the command group/cog with the discord client.
    All extensions must have a setup function.

    Params:
     - client: (DiscordClient): The client to register the cog with.
    """
    await client.add_cog(Mod(client))


async def setup(client: core.DiscordClient) -> None:
    """
    De-registers the command group/cog with the discord client.
    This is not usually needed, but is useful to have.

    Params:
     - client: (DiscordClient): The client to de-register the cog with.
    """
    await client.remove_cog(Mod(client))