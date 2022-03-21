"""
Contains miscellaneous commands to be used for fun.
"""

import random
import nextcord
import json
import start
import requests

from nextcord.ext import commands


class MiscCog(commands.Cog):
    """🎲 Contains miscellaneous commands."""
    def __init__(self, client: commands.Bot):
        self.client = client


    @commands.command()
    async def choose(self, ctx: commands.Context, *choices: str):
        """
        🎲 Chooses a random option from a list of choices.

        Usage:
        ```
        ~choose [...choices]
        ```
        """
        await ctx.send(random.choice(choices))


    @commands.command()
    async def meme(self, ctx: commands.Context):
        """
        🎲 Sends a random meme from Reddit.

        Usage:
        ```
        ~meme
        ```
        """
        content = requests.get('https://meme-api.herokuapp.com/gimme').text
        data = json.loads(content, )

        meme = nextcord.Embed(
            title=str(data["title"]),
            color=start.colour
        )

        meme.set_image(url=str(data['url']))
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
        embed = nextcord.Embed(
            title=f'Poll by **{ctx.author.name}**:',
            color=start.colour,
            description=' '.join(poll)
        )

        message = await ctx.send(embed=embed)

        await message.add_reaction('✔️')
        await message.add_reaction('❌')


def setup(client: commands.Bot):
    """Registers the cog with the client."""
    client.add_cog(MiscCog(client))


def teardown(client: commands.Bot):
    """Un-registers the cog with the client."""
    client.remove_cog(MiscCog(client))

