"""
Contains miscellaneous commands to be used for fun.
"""

import datetime
import random
import re
import humanize
import discord
import requests

from typing import Optional
from discord.ext import commands
from utils import TwitchBroadcast, ViewYoutubeButton
from urllib import parse, request
from bs4 import BeautifulSoup

from ..misc_utils import fetch_from_youtube


class MiscCog(commands.Cog, name="Misc"):
    """
    🎲 Contains miscellaneous commands.
    """

    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command()
    async def twitch(self, ctx: commands.Context, *, name: str = None):
        """
        🎲 Shows information about a Twitch stream.

        ❓ This command is also available as a slash command.

        Usage:
        ```
        ~twitch <streamer name>
        ```
        Or:
        ```
        /twitch <streamer name>
        ```
        """
        if name is None:
            return await ctx.reply(
                f"❌ You need to specify a streamer name.", delete_after=20
            )

        client = self.client.twitch
        name = name.strip().lower()
        broadcaster_data = await client.connect("helix/users", login=name)
        broad_list = broadcaster_data["data"]

        if broad_list:
            broadcaster_id = broad_list[0]["id"]

            broadcaster_name = broad_list[0]["display_name"]
            json = await client.connect("helix/streams", user_id=str(broadcaster_id))

            if not json["data"]:
                return await ctx.reply(
                    f"❌ **{broadcaster_name}** isn't live.", delete_after=20
                )

            stream: TwitchBroadcast = await client.return_information(json)
            stream.thumbnail.seek(0)
            file = discord.File(fp=stream.thumbnail, filename="stream.png")

            game_cover = stream.game_image
            game_name = stream.game_name
            view_count = stream.viewer_count
            username = stream.username
            stream_title = stream.stream_title
            started_at = stream.started_at

            on_going_for = humanize.precisedelta(
                datetime.datetime.utcnow() - started_at, format="%0.0f"
            )

            embed = discord.Embed(
                title=stream_title,
                timestamp=datetime.datetime.utcnow(),
                url=stream.stream_url,
            )

            embed.set_image(url="attachment://stream.png")
            embed.set_thumbnail(url=game_cover)
            embed.add_field(name="Stream Time", value=on_going_for)
            embed.add_field(name="Username", value=username)
            embed.add_field(name="Viewer Count", value=view_count)
            embed.add_field(name="Category", value=game_name)

            return await ctx.send(embed=embed, file=file)

        return await ctx.reply(
            f":x: I couldn't find a streamer with the name '{name}'.", delete_after=20
        )

    @commands.command()
    async def choose(self, ctx: commands.Context, *choices: str):
        """
        🎲 Chooses a random option from a list of choices.

        ❓ This command is also available as a slash command.

        Usage:
        ```
        ~choose <...choices>
        ```
        Or:
        ```
        /choose <...choices>
        ```
        """
        # Display some error messages if the user's input is invalid.
        # This is because it's kinda awkward to do this in the on_command_error event.
        if len(choices) < 1:
            return await ctx.reply(
                f":x: You need to give me choices to choose from.", delete_after=20
            )
        if len(choices) == 1:
            return await ctx.reply(f":x: I need more than one choice!", delete_after=20)

        embed = discord.Embed(
            title=f"🎲 I Choose",
            description=f"```{random.choice(choices)}```",
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def meme(self, ctx: commands.Context):
        """
        🎲 Sends a random meme from Reddit.

        ❓ This command is also available as a slash command.

        Usage:
        ```
        ~meme
        ```
        Or:
        ```
        /meme
        ```
        """
        response = await self.client.session.get("https://meme-api.herokuapp.com/gimme")

        data = await response.json()
        meme = discord.Embed(title=str(data["title"]))
        meme.set_image(url=str(data["url"]))

        await ctx.reply(embed=meme)

    @commands.command()
    async def poll(self, ctx: commands.Context, *, poll: str):
        """
        🎲 Creates a simple yes or no poll.

        ❓ This command is also available as a slash command.

        Usage:
        ```
        ~poll <question> [...options]
        ```
        Or:
        ```
        /poll <question>
        ```
        """
        if not poll:
            return await ctx.reply(
                f":x: You need to specify a question.", delete_after=20
            )

        embed = discord.Embed(
            title=f"📢 Poll by **{ctx.author.name}**:",
            description=f"```❓ {' '.join(poll)}```\n",
        )

        embed.set_footer(text="Vote ✔️ Yes or ❌ No.")
        message = await ctx.send(embed=embed)

        await message.add_reaction("✔️")
        return await message.add_reaction("❌")

    @commands.command()
    async def echo(self, ctx: commands.Context, *, message: str):
        """
        🎲 Repeats what you say.

        ❓ This command is also available as a slash command.

        Usage:
        ```
        ~echo <message>
        ```
        Or:
        ```
        /echo <message>
        ```
        """
        if message is None:
            return await ctx.reply(
                f":x: You need to tell me what to say.", delete_after=20
            )

        await ctx.message.delete()
        await ctx.send(message)

    @commands.command()
    async def ping(self, ctx: commands.Context):
        """
        🎲 Shows your current latency.

        ❓ This command is also available as a slash command.

        Usage:
        ```
        ~ping
        ```
        Or:
        ```
        /ping
        ```
        """
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"⌛ Your ping is **{round(self.client.latency * 1000)}**ms.",
        )

        await ctx.send(embed=embed)

    @commands.command(aliases=["yt"])
    async def youtube(self, ctx: commands.Context, *, search: str = None):
        """
        🎲 Searches for a video on youtube and sends the link.

        ❓ This command is also available as a slash command.

        Usage:
        ```
        ~youtube <search>
        ```
        Or:
        ```
        /youtube <search>
        ```
        """
        if search is None:
            return await ctx.reply(
                f":x: You need to tell me what to search for.", delete_after=20
            )

        embed, url = await fetch_from_youtube(search)
        await ctx.send(embed=embed)

        # Ask if they would like to view the video in Discord
        embed = discord.Embed(
            title="🎲 View in Discord?",
            description="❓ Click View In Discord to view the video in this text channel.",
        )
        view = ViewYoutubeButton(url, ctx, timeout=60)
        view.message = await ctx.send(embed=embed, view=view)


async def setup(client: commands.Bot):
    """
    Registers the cog with the client.
    """
    await client.add_cog(MiscCog(client))


async def teardown(client: commands.Bot):
    """
    Un-registers the cog with the client.
    """
    await client.remove_cog(MiscCog(client))
