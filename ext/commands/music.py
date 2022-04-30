"""
Module `music` contains the `music` cog/group, which implements
music streaming commands for BB.Bot.
"""
import asyncio
import datetime
import itertools
import discord
import core

from discord.ext import commands
from discord import app_commands
from ext import utils
from ext.utils import music


class Music(commands.Cog, name="Music"):
    """
    🎵 Lets you stream music in a voice channel.
    """
    def __init__(self, client: core.DiscordClient):
        self.client = client
        self.players = {}
    
    async def cleanup(self, guild: discord.Guild):
        """
        Destroys the music player and disconnects from the voice
        channel the bot is currently playing music in.

        Params:
         - guild (discord.Guild): The guild the bot is playing in.
        """
        try:
            await guild.voice_client.disconnect()
        except AttributeError:
            pass

        try:
            del self.players[guild.id]
        except KeyError:
            pass
    
    async def __local_check(self, interaction: discord.Interaction):
        """
        Local check for all the commands in the cog. Checks if the
        command was used in a guild.

        Params:
         - ctx ()
        """
        if not interaction.guild:
            raise commands.NoPrivateMessage
        return True

    async def __error(self, interaction: discord.Interaction, error):
        """
        Error handler for all errors in this cog.
        """
        if isinstance(error, commands.NoPrivateMessage):
            try:
                error_embed = utils.create_error_embed("You can't play music in a DM channel.")
                await interaction.response.send_message(embed=error_embed, ephemeral=True)
            except discord.HTTPException:
                pass

        elif isinstance(error, music.InvalidVC):
            error_embed = utils.create_error_embed("Could not connect to a voice channel.")
            await interaction.response.send_message(embed=error_embed, ephemeral=True)

    def get_player(self, interaction: discord.Interaction):
        """
        Gets the guild player or makes a new one.
        """
        try:
            player = self.players[interaction.guild.id]
        except KeyError:
            player = music.MusicPlayer(interaction)
            self.players[interaction.guild.id] = player

        return player

    @app_commands.command()
    @app_commands.describe(channel="❓ The voice channel to join.")
    async def connect(
        self, interaction: discord.Interaction, *, channel: discord.VoiceChannel=None
    ):
        """
        🎵 Joins a voice channel.
        """
        if not channel:
            try:
                channel = interaction.user.voice.channel
            except AttributeError:
                error_embed = utils.create_error_embed("No channel to join.")
                return await interaction.response.send_message(embed=error_embed, ephemeral=True)

        vc = interaction.guild.voice_client

        if vc:
            if vc.channel.id == channel.id:
                return
            try:
                await vc.move_to(channel)
            except asyncio.TimeoutError:
                error_embed = utils.create_error_embed("Moving to channel **`channel`** timed out.")
                return await interaction.response.send_message(embed=error_embed, ephemeral=True)
        else:
            try:
                await channel.connect()
            except asyncio.TimeoutError:
                error_embed = utils.create_error_embed("Moving to channel **`channel`** timed out.")
                return await interaction.response.send_message(embed=error_embed, ephemeral=True)

        embed = discord.Embed(
            title=f"🎧 Successfully Connected",
            description=f"**`Channel: {channel}`**.",
            timestamp=datetime.datetime.utcnow(),
            color=self.client.theme,
        )
        embed.set_footer(text="❓ You can use /del to kick me at any time.")
        await interaction.response.send_message(embed=embed)

    @app_commands.command()
    @app_commands.describe(search="❓ The song to search YouTube for.")
    async def play(self, interaction: discord.Interaction, *, search: str):
        """
        🎵 Plays a song in a voice channel.
        """
        vc = interaction.guild.voice_client

        if not vc:
            await interaction.invoke(self.connect)

        player = self.get_player(interaction)
        source = await music.YTDLSource.create_source(
            interaction,
            search,
            loop=self.client.loop,
            download=False,
        )

        await player.queue.put(source)

    @app_commands.command()
    async def pause(self, interaction: discord.Interaction):
        """
        🎵 Pauses the currently playing song.
        """
        vc = interaction.guild.voice_client

        if not vc or not vc.is_playing():
            error_embed = utils.create_error_embed("I'm not currently playing anything.")
            return await interaction.response.send_message(embed=error_embed, ephemeral=True)
        elif vc.is_paused():
            return

        vc.pause()

        embed = discord.Embed(
            title=f"🎧 Paused",
            description=f"**Paused by `@{interaction.user.name}`** | **`{interaction.user.name}`**.",
            timestamp=datetime.datetime.utcnow(),
            color=self.client.theme,
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command()
    async def resume(self, interaction: discord.Interaction):
        """
        🎵 Resumes the currently playing song.
        """
        vc = interaction.guild.voice_client

        if not vc or not vc.is_connected():
            error_embed = utils.create_error_embed("I'm not currently playing anything.")
            return await interaction.response.send_message(embed=error_embed, ephemeral=True)

        elif not vc.is_paused():
            return

        vc.resume()

        embed = discord.Embed(
            title=f"🎧 Resumed",
            description=f"**Resumed by `@{interaction.user.name}`** | **`{interaction.user.name}`**.",
            timestamp=datetime.datetime.utcnow(),
            color=self.client.theme,
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command()
    async def skip(self, interaction: discord.Interaction):
        """
        🎵 Skips the currently playing song.
        """
        vc = interaction.guild.voice_client

        if not vc or not vc.is_connected():
            error_embed = utils.create_error_embed("I'm not currently playing anything.")
            return await interaction.response.send_message(embed=error_embed, ephemeral=True)

        if vc.is_paused():
            pass
        elif not vc.is_playing():
            return

        vc.stop()

        embed = discord.Embed(
            title=f"🎧 Skipped",
            description=f"**Skipped by `@{interaction.user.name}`** | **`{interaction.user.name}`**.",
            timestamp=datetime.datetime.utcnow(),
            color=self.client.theme,
        )

        await interaction.response.send_message.send(embed=embed)

    @app_commands.command()
    async def queue(self, interaction: discord.Interaction):
        """
        🎵 Shows the current music queue.
        """
        vc = interaction.guild.voice_client

        if not vc or not vc.is_connected():
            error_embed = utils.create_error_embed("I'm not currently playing anything.")
            return await interaction.response.send_message(embed=error_embed, ephemeral=True)

        player = self.get_player(interaction)
        if player.queue.empty():
            error_embed = utils.create_error_embed("There are no more queued songs.")
            return await interaction.response.send_message(embed=error_embed, ephemeral=True)

        upcoming = list(itertools.islice(player.queue._queue, 0, 5))

        fmt = "\n\n".join(
            f'➡️ **{i + 1}**: {song["title"]}' for i, song in enumerate(upcoming)
        )
        embed = discord.Embed(
            title=f"🎧 Music Queue",
            description=fmt,
            timestamp=datetime.datetime.utcnow(),
            color=self.client.theme,
        ) \
            .set_footer(text=f"❓ There are {len(upcoming)} songs queued.")

        await interaction.response.send_message.send(embed=embed)

    @app_commands.command()
    async def nowplaying(self, interaction: discord.Interaction):
        """
        🎵 Shows the song that's currently playing.
        """
        vc = interaction.guild.voice_client

        if not vc or not vc.is_connected():
            error_embed = utils.create_error_embed("I'm not currently playing anything.")
            return await interaction.response.send_message(embed=error_embed, ephemeral=True)

        player = self.get_player(interaction)
        if not player.current:
            error_embed = utils.create_error_embed("I'm not currently playing anything.")
            return await interaction.response.send_message(embed=error_embed, ephemeral=True)

        try:
            await player.np.delete()
        except discord.HTTPException:
            pass

        embed = discord.Embed(
            title=f"🎧 Now Playing",
            description=f"**Song: `{vc.source.title}`**\n**Requested by: **`{vc.source.requester.name}`**.",
            timestamp=datetime.datetime.utcnow(),
            color=self.client.theme,
        )

        player.np = await interaction.response.send_message(embed=embed)

    @app_commands.command()
    @app_commands.describe(vol="❓ The volume to play music at, as a percentage.")
    async def volume(self, interaction: discord.Interaction, *, vol: float):
        """
        🎵 Changes the music player's volume.
        Usage:
        ```
        ~volume | ~vol <volume>
        ```
        """
        vc: discord.VoiceProtocol = interaction.guild.voice_client

        if not vc or not vc.is_connected():
            error_embed = utils.create_error_embed("I'm not currently playing anything.")
            return await interaction.response.send_message(embed=error_embed, ephemeral=True)

        if not 0 < vol < 101:
            error_embed = utils.create_error_embed("I can only set the volume between 1 and 100.")
            return await interaction.response.send_message(embed=error_embed, ephemeral=True)

        player = self.get_player(interaction)

        if vc.source:
            vc.source.volume = vol / 100

        player.volume = vol / 100

        embed = discord.Embed(
            title="🎧 Volume Changed",
            description=f"**`{interaction.user.name}**` set the volume to `**{vol}%**`.",
            timestamp=datetime.datetime.utcnow(),
            color=self.client.theme,
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command()
    async def stop(self, interaction: discord.Interaction):
        """
        🎵 Clears the queue and stops the music player.
        """
        vc = interaction.guild.voice_client

        if not vc or not vc.is_connected():
            error_embed = utils.create_error_embed("I'm not currently playing anything.")
            return await interaction.response.send_message(embed=error_embed, ephemeral=True)

        await self.cleanup(interaction.guild)


async def setup(client: core.DiscordClient) -> None:
    """
    Registers the command group/cog with the discord client.
    All extensions must have a setup function.

    Params:
     - client: (DiscordClient): The client to register the cog with.
    """
    await client.add_cog(Music(client))


async def teardown(client: core.DiscordClient) -> None:
    """
    De-registers the command group/cog with the discord client.
    This is not usually needed, but is useful to have.

    Params:
     - client: (DiscordClient): The client to de-register the cog with.
    """
    await client.remove_cog(Music(client))
