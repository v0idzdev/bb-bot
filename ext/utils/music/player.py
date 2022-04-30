"""
Module `player` contains class `MusicPlayer`, which is reponsible for
managing music streaming on a per-guild basis.
"""
import asyncio
import discord
import datetime

from ext import utils
from async_timeout import timeout
from discord.ext import commands
from .ytdl_source import YTDLSource


class MusicPlayer:
    """
    Class `MusicPlayer` is responsible for managing music streaming
    on a per-guild basis.
    """
    __slots__ = (
        "client",
        "_guild",
        "_channel",
        "_cog",
        "queue",
        "next",
        "current",
        "np",
        "volume",
    )

    def __init__(self, interaction: discord.Interaction):
        self.queue = asyncio.Queue()
        self.next = asyncio.Event()

        self.client = interaction.client
        self._guild = interaction.guild
        self._channel = interaction.channel
        self._cog = interaction.cog

        self.np = None  # Now playing message
        self.volume = 0.5
        self.current = None

        interaction.client.loop.create_task(self.player_loop())

    async def player_loop(self):
        """
        The main player loop.
        """
        await self.client.wait_until_ready()

        while not self.client.is_closed():
            self.next.clear()

            try:
                async with timeout(300):
                    source = await self.queue.get()
            except asyncio.TimeoutError:
                return self.destroy(self._guild)

            if not isinstance(source, YTDLSource):
                try:
                    source = await YTDLSource.regather_stream(
                        source, loop=self.client.loop
                    )
                except Exception as e:
                    error_embed = utils.create_error_embed("Sorry, I couldn't process your song.") \
                        .add_field(name="Error Details", value=[{e}])
                    await self._channel.send(embed=error_embed, ephemeral=True)
                    continue

            source.volume = self.volume
            self.current = source

            self._guild.voice_client.play(
                source,
                after=lambda _: self.client.loop.call_soon_threadsafe(self.next.set),
            )

            embed = discord.Embed(
                title=f"🎧 Now Playing",
                description=f"**Song: `{source.title}`**\n**Requested by: **`{source.requester.name}`**.",
                timestamp=datetime.datetime.utcnow(),
                color=self.client.theme,
            )

            self.np = await self._channel.send(embed=embed)

            await self.next.wait()

            try:
                source.cleanup()
            except ValueError as ex:
                error_embed = utils.create_error_embed("Discord.py encountered an internal error.") \
                        .add_field(name="Error Details", value=[{ex}])
                await self._channel.send(embed=error_embed, ephemeral=True)

            self.current = None

            try:
                await self.np.delete()
            except discord.HTTPException:
                pass

    def destroy(self, guild):
        """
        Disconnect and clean up the player.
        """
        return self.client.loop.create_task(self._cog.cleanup(guild))