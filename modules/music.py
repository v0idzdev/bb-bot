import discord
import discord.ext.commands as commands
import asyncio
import itertools

from async_timeout import timeout
from functools import partial
from youtube_dl import YoutubeDL


# |---------- CONFIG ----------|


COLOR = discord.Color(0x486572)

ytdl_options = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'before_options': '-nostdin',
    'options': '-vn'
}

ytdl = YoutubeDL(ytdl_options)


# |-------- EXCEPTIONS --------|


class VCError(commands.CommandError):
    """
    Exception class for connection errors.
    """


class InvalidVC(VCError):
    """
    Exception class for invalid VCs.
    """


# |----- YOUTUBEDL SOURCE -----|


class YTDLSource(discord.PCMVolumeTransformer):
    """
    Contains functionality/data relating to the YouTube download source.
    """
    def __init__(self, source, *, data, requester):
        super().__init__(source)

        self.requester = requester
        self.title = data.get("title")
        self.web_url = data.get("webpage_url")

    def __getitem__(self, item: str):
        return self.__getattribute__(item)

    @classmethod
    async def create_source(
        cls, ctx: commands.Context, search: str, *, loop: asyncio.AbstractEventLoop, download=False
    ):
        """
        Creates a source.

        ctx (Context):
            Command invocation context.

        search (str):
            The user's song search string.

        loop (AbstractEventLoop):
            The main event loop.

        download (bool):
            Whether to download the audio from YouTube or not.
        """
        loop = loop or asyncio.get_event_loop()

        to_run = partial(ytdl.extract_info, url=search, download=download)
        data = await loop.run_in_executor(None, to_run)

        if 'entries' in data: # Get the first item in a playlist
            data = data["entries"][0]

        await ctx.send(f':white_check_mark: [Added {data["title"]} to the Queue.]\n', delete_after=15)

        if download:
            source = ytdl.prepare_filename(data)
        else:
            return {'webpage_url': data['webpage_url'], 'requester': ctx.author, 'title': data['title']}

        return cls(discord.FFmpegPCMAudio(source), data=data, requester=ctx.author)

    @classmethod
    async def regather_stream(cls, data: dict, *, loop: asyncio.AbstractEventLoop):
        """
        Used to prepare a stream instead of downloading.

        data (dict):
            The data received from the YTDL source.

        loop (AbstractEventLoop):
            The main event loop.
        """
        loop = loop or asyncio.get_event_loop()
        requester = data['requester']

        to_run = partial(ytdl.extract_info, url=data['webpage_url'], download=False)
        data = await loop.run_in_executor(None, to_run)

        return cls(discord.FFmpegPCMAudio(data['url']), data=data, requester=requester)


# |------- MUSIC PLAYER -------|


class MusicPlayer:
    """
    Class assigned to each guild using the bot for music.

    Contains a queue and a loop.
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
            self.np = await self._channel.send(f'🔊 **Now Playing:** *{source.title}* requested by '
                + f'**{source.requester}**.')

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

         guild:
            The server to destroy the music player in and leave VCs in.
        """
        return self.bot.loop.create_task(self._cog.cleanup(guild))


# |-------- MUSIC COG ---------|


class Music(commands.Cog):
    """
    Class containing music related commands.
    """
    __slots__ = ("bot", "players")

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.players = {}

    async def cleanup(self, guild):
        """
        Destroys the music player and disconnects from a voice channel.

        guild:
            The server to destroy the music player in and leave VCs in.
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

        Parameters
        ----------

        ctx (Context):
            Command invocation context.
        """
        if not ctx.guild:
            raise commands.NoPrivateMessage
        return True

    async def __error(self, ctx: commands.Context, error):
        """
        Error handler for all errors in this cog.

        Parameters
        ----------

        ctx (Context):
            Command invocation context.

        error:
            The error that was raised.
        """
        if isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.send(f':x: {ctx.author.mention}: You can\'t play music in a private message channel.')
            except discord.HTTPException:
                pass
        elif isinstance(error, InvalidVC):
            await ctx.send(f':x: {ctx.author.mention}: Couldn\'t connect to a VC.'
                + 'Please make sure you\'re in a VC or provide me with one.')

    def get_player(self, ctx: commands.Context):
        """
        Gets the guild player or makes a new one.

        Parameters
        ----------

        ctx (Context):
            Command invocation context.
        """
        try:
            player = self.players[ctx.guild.id]
        except KeyError:
            player = MusicPlayer(ctx)
            self.players[ctx.guild.id] = player

        return player

    @commands.command(aliases=['join'])
    async def connect(self, ctx: commands.Context, *, channel: discord.VoiceChannel=None):
        """
        Connects to a voice channel.

        Parameters
        ----------

        ctx (Context):
            Command invocation context.

        channel (VoiceChannel):
            The voice channel to join.
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

        await ctx.send(f'Connected to: **{channel}**', delete_after=20)

    @commands.command(aliases=['p'])
    async def play(self, ctx: commands.Context, *, search: str):
        """
        Requests a song and add it to the queue.

        Tries to join a valid voice channel if the bot isn't already in one, and
        uses YTDL to automatically search a song.

        Parameters
        ----------

        ctx (Context):
            Command invocation context.

        search (str):
            The song to search for.
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
        Pauses the currently playing song.

        Parameters
        ----------

        ctx (Context):
            Command invocation context.
        """
        vc = ctx.voice_client

        if not vc or not vc.is_playing():
            return await ctx.send(f':x: {ctx.author.mention}: I\'m not currently playing anything.',
                delete_after=20
            )
        elif vc.is_paused():
            return

        vc.pause()
        await ctx.send(f'**{ctx.author}**: Paused the song')

    @commands.command(aliases=['r'])
    async def resume(self, ctx: commands.Context):
        """
        Resumes a paused song.

        Parameters
        ----------

        ctx (Context):
            Command invocation context.
        """
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send(f':x: {ctx.author.mention}: I\'m not currently playing anything.',
                delete_after=20
            )
        elif not vc.is_paused():
            return

        vc.resume()
        await ctx.send(f':track_next: **{ctx.author}**: Resumed the song.')

    @commands.command(aliases=['s'])
    async def skip(self, ctx: commands.Context):
        """
        Skips a song.

        Parameters
        ----------

        ctx (Context):
            Command invocation context.
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
        await ctx.send(f':track_next: **{ctx.author}**: Skipped the song.')

    @commands.command(aliases=['q', 'songs'])
    async def queue(self, ctx: commands.Context):
        """
        Shows the queue of upcoming songs.

        Parameters
        ----------

        ctx (Context):
            Command invocation context.
        """
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send(f':x: {ctx.author.mention}: I\'m not connected to VC.', delete_after=20)

        player = self.get_player(ctx)
        if player.queue.empty():
            return await ctx.send(f':x: {ctx.author.mention}: There are no more queued songs.')

        # Grab up to 5 entries from the queue...
        upcoming = list(itertools.islice(player.queue._queue, 0, 5))

        fmt = '\n'.join(f':headphones: **{i + 1}**: *{j["title"]}*' for i, j in enumerate(upcoming))
        embed = discord.Embed(title=f'Upcoming - Next {len(upcoming)}', description=fmt)

        await ctx.send(embed=embed)

    @commands.command(aliases=['np'])
    async def nowplaying(self, ctx: commands.Context):
        """
        Displays information about the song that's currently playing.

        Parameters
        ----------

        ctx (Context):
            Command invocation context.
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
        except discord.HTTPException:
            pass

        player.np = await ctx.send(f':musical_note: **Now Playing:** *{vc.source.title}* '
            f'requested by **{vc.source.requester}**')

    @commands.command(aliases=["vol"])
    async def volume(self, ctx: commands.Context, *, vol: float):
        """
        Changes the music player's volume.

        Parameters
        ----------

        ctx (Context):
            Command invocation context.

        vol (float):
            The volume to set the music player to.
        """
        vc: discord.VoiceProtocol = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send(f':x: {ctx.author.mention}: I\'m not connected to VC.', delete_after=20)

        if not 0 < vol < 101:
            return await ctx.send(f':x: {ctx.author.mention}: I can only set the volume between 1 and 100.')

        player = self.get_player(ctx)

        if vc.source:
            vc.source.volume = vol / 100

        player.volume = vol / 100
        await ctx.send(f":sound: **{ctx.author}**: Set the volume to *{vol}%*")

    @commands.command(aliases=["del"])
    async def stop(self, ctx: commands.Context):
        """
        Stops the currently playing song and destroy the player.

        Parameters
        ----------

        ctx (Context):
            Command invocation context.
        """
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send(f':x: {ctx.author.mention}: I\'m not currently playing anything.',
                delete_after=20
            )

        await self.cleanup(ctx.guild)


# |---- REGISTERING MODULE ----|


def setup(client: commands.Bot):
    """
    Registers the music cog with the bot.

    Parameters
    ----------

    client (Bot):
        The bot to add the commands to.
    """
    client.add_cog(Music(client))