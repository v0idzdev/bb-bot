import discord
import youtube_dl
from youtube_search import YoutubeSearch
from discord.ext import commands


class Music(commands.Cog):
    """Command category for music commands"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._queue = []

    @commands.command(aliases=["j"], description="Brings Beep Boop Bot into the VC you're in")
    async def join(self, ctx: commands.Context):
        """Brings the bot into a VC.
        If the user of the command isn't in a VC, it sends a message
        saying 'You're not in a VC, join one and try again'.
        """

        if ctx.author.voice is None: # If the user isn't in a VC
            await ctx.send("You're not in a VC, join one and try again")

        vc = ctx.author.voice.channel

        if ctx.voice_client is None: # If the bot isn't in a VC
            await vc.connect()
        else: # Else if it is, move it to the one the user is in
            await ctx.voice_client.move_to(vc)

    @commands.command(aliases=["d"], description="Disconnects Beep Boop Bot from your VC channel")
    async def disconnect(self, ctx: commands.Context):
        """Disconnects the bot from the VC the user's in"""
        await ctx.voice_client.disconnect()

    @commands.command(aliases=["p"], description="Plays a song.")
    async def play(self, ctx: commands.Context, song: str):
        """Plays a song from YouTube if the bot is in a VC"""

        vc = ctx.voice_client

        if vc.is_playing():
            await ctx.send("I'm already playing a song. \nAdding [{name}] to the queue")
            self._queue.append(song)
            return

        if ctx.voice_client is None: # Check if the bot's currently in VC
            await ctx.send("I'm not in a voice channel, use .join or .j to put me in one")
            return

        results = YoutubeSearch(song, max_results=1).to_dict()
        name = results[0]["title"]

        url_suffix = results[0]["url_suffix"]
        url = "https://youtube.com" + url_suffix

        embed = discord.Embed()
        embed.title = f"▶️ Now playing:"
        embed.description = f"[{name}] {url}"
        embed.color = discord.Color(0x486572)

        YDL_OPTIONS = {'format': 'bestaudio'}

        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            URL = info['formats'][0]['url']

        vc.play(discord.FFmpegPCMAudio(URL))
        await ctx.send(embed=embed)


        # if ctx.voice_client is None: # Check if the bot's currently in VC
        #     await ctx.send("I'm not in a voice channel, use .join or .j to put me in one")
        #     return

        # ctx.voice_client.stop()

        # # Options for streaming
        # YTDL_OPTIONS = {"format": "bestaudio"}
        # FFMPEG_OPTIONS = {
        #     "before_options": "-reconnect 1 reconnect_streamed 1 -reconnect_delay_max 5",
        #     "options": "vn"
        # }

        # vc = ctx.voice_client

        # with youtube_dl.YoutubeDL(YTDL_OPTIONS) as ydl:
        #     info = ydl.extract_info(url, download=False)
        #     _url = info["formats"][0]["url"]

        #     source = await discord.FFmpegOpusAudio.from_probe(_url, **FFMPEG_OPTIONS)
        #     vc.play(source) # Play the song in VC
        #     await ctx.send(f"▶️ Now playing: **{info['title']}**")

    @commands.command(aliases=["s"], description="Pauses a song")
    async def pause(self, ctx: commands.Context):
        """Pauses the music steam"""
        await ctx.voice_client.pause()
        await ctx.send("⏸️ Paused **{info['title']}**")

    @commands.command(aliases=["r"], description="Resumes a song")
    async def resume(self, ctx: commands.Context):
        """Resumes the music steam"""
        await ctx.voice_client.resume()
        await ctx.send("▶️ Resuming **{info['title']}**")


def setup(bot: commands.Bot):
    """Adds the 'Help' cog to the bot"""
    bot.add_cog(Music(bot))