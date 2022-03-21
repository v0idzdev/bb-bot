import nextcord
import nextcord.ext.commands as commands
import asyncio
import itertools
import start

from async_timeout import timeout
from .music_utils import YTDLSource, VCError, InvalidVC
from .music_player import MusicPlayer


class MusicCog(commands.Cog):
    """
    🎵 Class containing music related commands.
    """
    __slots__ = ("bot", "players")

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.players = {}

    async def cleanup(self, guild):
        """
        Destroys the music player and disconnects from a voice channel.
        """
        try:
            await guild.voice_client.disconnect()
        except AttributeError:
            pass

        try:
            del self.players[guild.id]
        except KeyError:
            pass

    async def __local_check(self, ctx: commands.Context):
        """
        Local check for all the commands in the cog.
        """
        if not ctx.guild:
            raise commands.NoPrivateMessage
        return True

    async def __error(self, ctx: commands.Context, error):
        """
        Error handler for all errors in this cog.
        """
        if isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.send(f':x: {ctx.author.mention}: You can\'t play music in a private message channel.')
            except nextcord.HTTPException:
                pass
        elif isinstance(error, InvalidVC):
            await ctx.send(f':x: {ctx.author.mention}: Couldn\'t connect to a VC.'
                + 'Please make sure you\'re in a VC or provide me with one.')

    def get_player(self, ctx: commands.Context):
        """
        Gets the guild player or makes a new one.
        """
        try:
            player = self.players[ctx.guild.id]
        except KeyError:
            player = MusicPlayer(ctx)
            self.players[ctx.guild.id] = player

        return player

    @commands.command(aliases=['join'])
    async def connect(self, ctx: commands.Context, *, channel: nextcord.VoiceChannel=None):
        """
        🎵 Joins a voice channel.

        Usage:
        ```
        ~join [channel]
        ```
        """
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                error_msg = f':x: {ctx.author.mention}: No channel to join. Specify a channel or join one yourself.'

                await ctx.send(error_msg)
                raise AttributeError(error_msg)

        vc = ctx.voice_client

        if vc:
            if vc.channel.id == channel.id:
                return
            try:
                await vc.move_to(channel)
            except asyncio.TimeoutError:
                raise VCError(f':x: {ctx.author.mention}: Moving to channel **{channel}** timed out.')
        else:
            try:
                await channel.connect()
            except asyncio.TimeoutError:
                raise VCError(f':x: {ctx.author.mention}: Connecting to channel **{channel}** timed out.')

        embed = nextcord.Embed(
            title=f'🔥 Connected to:',
            description=f'**{channel}**',
            color=start.colour
        )

        await ctx.send(embed=embed, delete_after=20)

    @commands.command(aliases=['p'])
    async def play(self, ctx: commands.Context, *, search: str):
        """
        🎵 Plays a song in a voice channel.

        Usage:
        ```
        ~play | ~p <song>
        ```
        """
        await ctx.trigger_typing()

        vc = ctx.voice_client

        if not vc:
            await ctx.invoke(self.connect)

        player = self.get_player(ctx)
        source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop, download=False)

        await player.queue.put(source)

    @commands.command(aliases=['ps'])
    async def pause(self, ctx: commands.Context):
        """
        🎵 Pauses the currently playing song.

        Usage:
        ```
        ~pause | ~ps
        ```
        """
        vc = ctx.voice_client

        if not vc or not vc.is_playing():
            return await ctx.send(f':x: {ctx.author.mention}: I\'m not currently playing anything.',
                delete_after=20
            )
        elif vc.is_paused():
            return

        vc.pause()

        embed = nextcord.Embed(
            title=f'⏸️ **{ctx.author}**: Paused the song.',
            color=start.colour
        )

        await ctx.send(embed=embed)

    @commands.command(aliases=['r'])
    async def resume(self, ctx: commands.Context):
        """
        🎵 Resumes the currently playing song.

        Usage:
        ```
        ~resume | ~r
        ```
        """
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send(f':x: {ctx.author.mention}: I\'m not currently playing anything.',
                delete_after=20
            )
        elif not vc.is_paused():
            return

        vc.resume()

        embed = nextcord.Embed(
            title=f'▶️ **{ctx.author}**: Resumed the song.',
            color=start.colour
        )

        await ctx.send(embed=embed)

    @commands.command(aliases=['s'])
    async def skip(self, ctx: commands.Context):
        """
        🎵 Skips the currently playing song.

        Usage:
        ```
        ~skip | ~s
        ```
        """
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send(f':x: {ctx.author.mention}: I\'m not currently playing anything.',
                delete_after=20
            )

        if vc.is_paused():
            pass
        elif not vc.is_playing():
            return

        vc.stop()

        embed = nextcord.Embed(
            title=f'⏭️ **{ctx.author}**: Skipped the song.',
            color=start.colour
        )

        await ctx.send(embed=embed)

    @commands.command(aliases=['q', 'songs'])
    async def queue(self, ctx: commands.Context):
        """
        🎵 Shows the current music queue.

        Usage:
        ```
        ~queue | ~q | ~songs
        ```
        """
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send(f':x: {ctx.author.mention}: I\'m not connected to VC.', delete_after=20)

        player = self.get_player(ctx)
        if player.queue.empty():
            return await ctx.send(f':x: {ctx.author.mention}: There are no more queued songs.')

        # Grab up to 5 entries from the queue...
        upcoming = list(itertools.islice(player.queue._queue, 0, 5))

        fmt = '\n\n'.join(f'➡️ **{i + 1}**: *{j["title"]}*' for i, j in enumerate(upcoming))
        embed = nextcord.Embed(
            title=f'Upcoming: {len(upcoming)} songs.',
            description=fmt,
            color=start.colour
        )

        await ctx.send(embed=embed)

    @commands.command(aliases=['np'])
    async def nowplaying(self, ctx: commands.Context):
        """
        🎵 Shows the song that's currently playing.

        Usage:
        ```
        ~nowplaying | ~np
        ```
        """
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send(f':x: {ctx.author.mention}: I\'m not currently playing anything.',
                delete_after=20
            )

        player = self.get_player(ctx)
        if not player.current:
            return await ctx.send(f':x: {ctx.author.mention}: I\'m not currently playing anything.')

        try:
            # Remove our previous now_playing message.
            await player.np.delete()
        except nextcord.HTTPException:
            pass

        embed = nextcord.Embed(
            title=f'🎵 **Now Playing:** *{vc.source.title}*',
            description=f'Requested by: **{vc.source.requester}**',
            color=start.colour
        )

        player.np = await ctx.send(embed=embed)

    @commands.command(aliases=['vol'])
    async def volume(self, ctx: commands.Context, *, vol: float):
        """
        🎵 Changes the music player's volume.

        Usage:
        ```
        ~volume | ~vol <volume>
        ```
        """
        vc: nextcord.VoiceProtocol = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send(f':x: {ctx.author.mention}: I\'m not connected to VC.', delete_after=20)

        if not 0 < vol < 101:
            return await ctx.send(f':x: {ctx.author.mention}: I can only set the volume between 1 and 100.')

        player = self.get_player(ctx)

        if vc.source:
            vc.source.volume = vol / 100

        player.volume = vol / 100

        embed = nextcord.Embed(
            title=f'🔊 **{ctx.author}**: Set the volume to *{vol}%*',
            color=start.colour
        )

        await ctx.send(embed=embed)

    @commands.command(aliases=["del"])
    async def stop(self, ctx: commands.Context):
        """
        🎵 Clears the queue and stops the music player.

        Usage:
        ```
        ~stop | ~del
        ```
        """
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send(f':x: {ctx.author.mention}: I\'m not currently playing anything.',
                delete_after=20
            )

        await self.cleanup(ctx.guild)


def setup(client: commands.Bot):
    """Registers the cog with the client."""
    client.add_cog(MusicCog(client))


def teardown(client: commands.Bot):
    """Un-registers the cog with the client."""
    client.remove_cog(MusicCog(client))