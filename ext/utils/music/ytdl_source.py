"""
Module `ytdl_source` contains the class `YTDLSource`, which is
responsible for creating an audio source from a search term.
"""
import discord
import asyncio

from youtube_dl import YoutubeDL
from functools import partial
from discord.ext import commands
from ._config import ytdl_options

ytdl = YoutubeDL(ytdl_options)


class YTDLSource(discord.PCMVolumeTransformer):
    """
    Class `YTDLSource` overrides `discord.PCMVolumeTransformer`.
    It is responsible for creating an audio source.
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
        cls,
        interaction: discord.Interaction,
        search: str,
        *,
        loop: asyncio.AbstractEventLoop,
        download=False,
    ):
        """
        Creates a source.
        """
        loop = loop or asyncio.get_event_loop()

        to_run = partial(ytdl.extract_info, url=search, download=download)
        data = await loop.run_in_executor(None, to_run)

        if "entries" in data:
            data = data["entries"][0]

        embed = discord.Embed(
            title=f"🎧 Song Added to the Queue", description=f'🎹 {data["title"]}'
        )

        await interaction.response.send_message(embed=embed)

        if download:
            source = ytdl.prepare_filename(data)
        else:
            return {
                "webpage_url": data["webpage_url"],
                "requester": interaction.user,
                "title": data["title"],
            }

        return cls(discord.FFmpegPCMAudio(source), data=data, requester=interaction.user)

    @classmethod
    async def regather_stream(cls, data: dict, *, loop: asyncio.AbstractEventLoop):
        """
        Used to prepare a stream instead of downloading.
        """
        loop = loop or asyncio.get_event_loop()
        requester = data["requester"]

        to_run = partial(ytdl.extract_info, url=data["webpage_url"], download=False)
        data = await loop.run_in_executor(None, to_run)

        return cls(discord.FFmpegPCMAudio(data["url"]), data=data, requester=requester)