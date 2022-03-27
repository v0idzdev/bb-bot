"""
Contains miscellaneous commands to be used for fun.
"""

import datetime
import random
import humanize

import discord
from discord.ext import commands
from utils.models import TwitchBroadcast


class MiscCog(commands.Cog, name="Misc"):
    """
    🎲 Contains miscellaneous commands.
    """

    def __init__(self, client: commands.Bot):
        self.client = client

    # @commands.command()
    # async def twitch(self, ctx: commands.Context, *, name: str):
    #     """
    #     🎲 Shows information about a Twitch streamer.

    #     Usage:
    #     ```
    #     ~twitch <streamer name>
    #     ```
    #     """
    #     client = self.client.twitch
    #     name = name.lower()
    #     broadcaster_data = await client.connect("helix/users", login=name)
    #     broad_list = broadcaster_data['data']

    #     if broad_list:
    #         broadcaster_id = broad_list[0]['id']

    #         broadcaster_name = broad_list[0]['display_name']
    #         json = await client.connect('helix/streams', user_id=str(broadcaster_id))

    #         if not json['data']:
    #             return await ctx.send(f"{broadcaster_name} isn't live")

    #         stream: TwitchBroadcast = await client.return_information(json)
    #         stream.thumbnail.seek(0)
    #         file = discord.File(fp=stream.thumbnail, filename="stream.png")

    #         game_cover = stream.game_image
    #         game_name = stream.game_name
    #         view_count = stream.viewer_count
    #         username = stream.username
    #         stream_title = stream.stream_title
    #         started_at = stream.started_at

    #         on_going_for = humanize.precisedelta(datetime.datetime.utcnow() - started_at, format="%0.0f")

    #         embed = discord.Embed(title=stream_title, color=self.client.theme, timestamp=datetime.datetime.utcnow(), url=stream.stream_url)

    #         embed.set_image(url="attachment://stream.png")
    #         embed.set_thumbnail(url=game_cover)
    #         embed.add_field(name="Stream Time", value=on_going_for)
    #         embed.add_field(name="Username", value=username)
    #         embed.add_field(name="Viewer Count", value=view_count)
    #         embed.add_field(name="Category", value=game_name)

    #         return await ctx.send(embed=embed, file=file)

    #     return await ctx.send(f"{name} isn't a valid streamer's name")

    @commands.command()
    async def choose(self, ctx: commands.Context, *choices: str):
        """
        🎲 Chooses a random option from a list of choices.

        Usage:
        ```
        ~choose <...choices>
        ```
        """
        # Display some error messages if the user's input is invalid.
        # This is because it's kinda awkward to do this in the on_command_error event.
        if len(choices) < 1:
            return await ctx.send(f':x: {ctx.author.mention}: You need to give me choices to choose from.')
        if len(choices) == 1:
            return await ctx.send(f':x: {ctx.author.mention}: I need more than one choice!')

        embed = discord.Embed(title=f'🎲 I choose {random.choice(choices)}')
        await ctx.send(embed=embed)

    @commands.command()
    async def meme(self, ctx: commands.Context):
        """
        🎲 Sends a random meme from Reddit.

        Usage:
        ```
        ~meme
        ```
        """
        response = await self.client.session.get("https://meme-api.herokuapp.com/gimme")
        data = await response.json()
        meme = discord.Embed(title=str(data["title"]), color=self.client.theme)
        meme.set_image(url=str(data["url"]))
        await ctx.reply(embed=meme)

    @commands.command()
    async def poll(self, ctx: commands.Context, *poll: str):
        """
        🎲 Creates a simple yes or no poll.

        Usage:
        ```
        ~poll [question]
        ```
        """
        embed = discord.Embed(
            title=f"Poll by **{ctx.author.name}**:",
            color=self.client.theme,
            description=" ".join(poll),
        )

        message = await ctx.send(embed=embed)

        await message.add_reaction("✔️")
        await message.add_reaction("❌")


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
