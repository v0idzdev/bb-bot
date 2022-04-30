"""
Module `mod` contains the `mod` cog/group, which implements
server moderation commands for BB.Bot.
"""
import asyncio
import discord
import datetime
import core
import enum

from ext import utils
from discord.ext import commands
from discord import app_commands
from typing import Optional


class TimeUnit(enum.Enum):
    """
    Used with the `amount` parameter in certain commands to denote
    whether the user wants to ban another user for `amount` seconds,
    minutes, hours, or days.
    """
    Seconds = 1
    Minutes = 2
    Hours = 3
    Days = 4


class Mod(commands.Cog, name="Moderation"):
    """
    ⚙️ Lets server admins & mods manage their server.
    """
    mute = app_commands.Group(name="mute", description="❓ Mutes a member of a server.")
    ban = app_commands.Group(name="ban", description="❓ Bans a member of a server.")

    def __init__(self, client: core.DiscordClient) -> None:
        self.client = client
        super().__init__()

    @app_commands.command()
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.cooldown(1, 5, key=lambda interaction: interaction.guild.id)
    async def purge(self, interaction: discord.Interaction, *, amount: int=6) -> None:
        """
        ⚙️ Clears a specified number of messages from a channel. Defaults to 6.
        """
        if amount <= 0:
            error_embed = utils.create_error_embed("You can only clear one or more messages.")
            await interaction.response.send_message(embed=error_embed, ephemeral=True)

        await interaction.channel.purge(limit=amount)

        embed = discord.Embed(
            title="⚙️ Messages Purged",
            description=f"**Number of Messages: {amount}**.",
            timestamp=datetime.datetime.utcnow(),
            color=self.client.theme,
        )   

        await interaction.response.send_message(embed=embed)

    @mute.command()
    @app_commands.describe(
        member="❓ The member to temporarily mute.",
        timeunit="❓ Whether you want to mute them for a certain number of seconds, minutes, hours, or days.",
        amount="❓ The number of seconds, minutes, hours, or days to mute the member for.",
        reason="❓ The reason for temporarily muting the member."
    )
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.cooldown(1, 5, key=lambda interaction: interaction.guild.id)
    async def temporarily(
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
        guild = interaction.guild
        muted_role = discord.utils.get(guild.roles, name="Muted")

        if not muted_role:
            muted_role = await guild.create_role(name="Muted")

        await member.add_roles(muted_role)

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
            description=f"**`@{member.name}`** | **`{member.discriminator}`**.",
            timestamp=datetime.datetime.utcnow(),
            color=self.client.theme,
        ) \
            .set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url) \
            .add_field(name="⏳ Time", value=f"**{amount}** {str(timeunit.name)}.") \
            .add_field(name="🖊️ Reason", value=reason or "...")

        await interaction.response.send_message(embed=muted_embed)
        seconds_muted = amount

        if timeunit == TimeUnit.Minutes:
            seconds_muted *= 60
        if timeunit == TimeUnit.Hours:
            seconds_muted *= (60 * 60)
        if timeunit == TimeUnit.Days:
            seconds_muted *= (60 * 60 * 24)

        await asyncio.sleep(seconds_muted)
        await member.remove_roles(muted_role)

        unmuted_embed = discord.Embed(
            title="⚙️ Member Unmuted",
            description=f"**`@{member.name}`** | **`{member.discriminator}`**.",
            timestamp=datetime.datetime.utcnow(),
            color=self.client.theme,
        ) \
            .set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)

        await interaction.followup.send(embed=unmuted_embed)

    @mute.command()
    @app_commands.describe(
        member="❓ The member to mute.",
        reason="❓ The reason for muting the member."
    )
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.cooldown(1, 5, key=lambda interaction: interaction.guild.id)
    async def permanently(
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
            description=f"**`@{member.name}`** | **`{member.discriminator}`**.",
            timestamp=datetime.datetime.utcnow(),
            color=self.client.theme,
        ) \
            .set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url) \
            .add_field(name="🖊️ Reason", value=reason or "...")

        await interaction.response.send_message(embed=muted_embed)
        await member.add_roles(muted_role, reason=reason)

    @app_commands.command()
    @app_commands.describe(member="❓ The member to unmute.")
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.cooldown(1, 5, key=lambda interaction: interaction.guild.id)
    async def unmute(self, interaction: discord.Interaction, *, member: discord.Member):
        """
        ⚙️ Unmutes a member of a server.
        """
        muted_role = discord.utils.get(interaction.guild.roles, name="Muted")
        await member.remove_roles(muted_role)

        unmuted_embed = discord.Embed(
            title="⚙️ Member Unmuted",
            description=f"**`@{member.name}`** | **`{member.discriminator}`**.",
            timestamp=datetime.datetime.utcnow(),
            color=self.client.theme,
        ) \
            .set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)

        await interaction.response.send_message(embed=unmuted_embed)

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
        guild = interaction.guild

        kicked_embed = discord.Embed(
            title="⚙️ Member Kicked",
            description=f"**`@{member.name}`** | **`{member.discriminator}`**.",
            timestamp=datetime.datetime.utcnow(),
            color=self.client.theme,
        ) \
            .set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url) \
            .add_field(name="🖊️ Reason", value=reason or "...") \

        await interaction.response.send_message(embed=kicked_embed)
        await guild.kick(member)

    @ban.command()
    @app_commands.describe(
        member="❓ The member to temporarily ban.",
        timeunit="❓ Whether you want to ban them for a certain number of seconds, minutes, hours, or days.",
        amount="❓ The number of seconds, minutes, hours, or days to ban the member for.",
        reason="❓ The reason for temporarily banning the member."
    )
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.checks.cooldown(1, 5, key=lambda interaction: interaction.guild.id)
    async def temporarily(
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
        guild = interaction.guild

        banned_embed = discord.Embed(
            title="⚙️ Member Banned",
            description=f"**`@{member.name}`** | **`{member.discriminator}`**.",
            timestamp=datetime.datetime.utcnow(),
            color=self.client.theme,
        ) \
            .set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url) \
            .add_field(name="⏳ Time", value=f"**{amount}** {str(timeunit.name)}.") \
            .add_field(name="🖊️ Reason", value=reason or "...")

        await interaction.response.send_message(embed=banned_embed)
        await guild.ban(member, reason=reason)
        seconds_banned = amount

        if timeunit == TimeUnit.Minutes:
            seconds_banned *= 60
        if timeunit == TimeUnit.Hours:
            seconds_banned *= (60 * 60)
        if timeunit == TimeUnit.Days:
            seconds_banned *= (60 * 60 * 24)

        await asyncio.sleep(seconds_banned)
        await guild.unban(user=member)

        unbanned_embed = discord.Embed(
            title="⚙️ Member Unbanned",
            description=f"**`@{member.name}`** | **`{member.discriminator}`**.",
            timestamp=datetime.datetime.utcnow(),
            color=self.client.theme,
        ) \
            .set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)

        await interaction.followup.send(embed=unbanned_embed)

    @ban.command()
    @app_commands.describe(
        member="❓ The member to ban.",
        reason="❓ The reason for banning the member."
    )
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.checks.cooldown(1, 5, key=lambda interaction: interaction.guild.id)
    async def permanently(
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

        banned_embed = discord.Embed(
            title="⚙️ Member Banned",
            description=f"**`@{member.name}`** | **`{member.discriminator}`**.",
            timestamp=datetime.datetime.utcnow(),
            color=self.client.theme,
        ) \
            .set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url) \
            .add_field(name="🖊️ Reason", value=reason or "...")

        await interaction.response.send_message(embed=banned_embed)
        await guild.ban(member, reason=reason)

    @app_commands.command()
    @app_commands.describe(member="❓ The member to unban.")
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.checks.cooldown(1, 5, key=lambda interaction: interaction.guild.id)
    async def unban(self, interaction: discord.Interaction, *, member: discord.Member):
        """
        ⚙️ Unbans a member of a server.
        """
        await interaction.guild.unban(member)

        unbanned_embed = discord.Embed(
            title="⚙️ Member Unbanned",
            description=f"**`@{member.name}`** | **`{member.discriminator}`**.",
            timestamp=datetime.datetime.utcnow(),
            color=self.client.theme,
        ) \
            .set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)

        await interaction.response.send_message(embed=unbanned_embed)


async def setup(client: core.DiscordClient) -> None:
    """
    Registers the command group/cog with the discord client.
    All extensions must have a setup function.

    Params:
     - client: (DiscordClient): The client to register the cog with.
    """
    await client.add_cog(Mod(client))


async def teardown(client: core.DiscordClient) -> None:
    """
    De-registers the command group/cog with the discord client.
    This is not usually needed, but is useful to have.

    Params:
     - client: (DiscordClient): The client to de-register the cog with.
    """
    await client.remove_cog(Mod(client))