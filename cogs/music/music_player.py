import asyncio

import discord
from async_timeout import timeout
from discord.ext import commands

from .music_utils import YTDLSource


class MusicPlayer:
    """
    Class assigned to each guild using the bot for music.
    """
    __slots__ = ('bot', '_guild', '_channel', '_cog', 'queue', 'next', 'current', 'np', 'volume')

    def __init__(self, ctx: commands.Context):
        self.queue = asyncio.Queue()
        self.next = asyncio.Event()

        self.bot = ctx.bot
        self._guild = ctx.guild
        self._channel = ctx.channel
        self._cog = ctx.cog

        self.np = None # Now playing message
        self.volume = .5
        self.current = None

        ctx.bot.loop.create_task(self.player_loop())

    async def player_loop(self):
        """
        The main player loop.
        """
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            self.next.clear()

            try:
                # Wait for the next song. If we timeout, cancel player and dc
                async with timeout(300):  # Wait 5 mins
                    source = await self.queue.get()
            except asyncio.TimeoutError:
                return self.destroy(self._guild)

            if not isinstance(source, YTDLSource):
                # Source was probably not downloaded
                # So we should regather
                try:
                    source = await YTDLSource.regather_stream(source, loop=self.bot.loop)
                except Exception as e:
                    await self._channel.send(f':x: Sorry, I couldn\'t process your song.\n'
                        + f'\n[{e}]\n')
                    continue

            source.volume = self.volume
            self.current = source

            self._guild.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))

            embed = discord.Embed(
                title=f'🎵 **Now Playing:** *{source.title}*',
                description=f'Requested by: **{source.requester}**',
                color=self.client.theme
            )

            self.np = await self._channel.send(embed=embed)

            await self.next.wait()

            # Make sure the FFmpeg process is cleaned up.
            source.cleanup()
            self.current = None

            try:
                # We are no longer playing this song...
                await self.np.delete()
            except discord.HTTPException:
                pass

    def destroy(self, guild):
        """
        Disconnect and clean up the player.
        """
        return self.bot.loop.create_task(self._cog.cleanup(guild))
