"""
Contains miscellaneous commands to be used for fun.
"""

import discord.ext.commands as commands
import modules.utilities.helpers as helpers
import random
import discord
import json
import requests


# |---------- COMMANDS ----------|


@commands.command()
async def choose(ctx: commands.Context, *choices: str):
    """
    Randomly chooses an option and sends it back.

    Parameters
    ----------

    ctx (Context):
        Command invocation context.

    *choices (str):
        The choices that the user gives the bot.
    """
    await ctx.send(random.choice(choices))


@commands.command()
async def meme(ctx: commands.Context):
    """
    Gets a meme from Reddit and sends it as an embed.

    Parameters
    ----------

    ctx (Context):
        Command invocation context.
    """
    content = requests.get('https://meme-api.herokuapp.com/gimme').text
    data = json.loads(content, )

    meme = discord.Embed(
        title=str(data["title"]),
        color=0x486572
    )

    meme.set_image(url=str(data['url']))
    await ctx.reply(embed=meme)


@commands.command()
async def poll(ctx: commands.Context, *poll: str):
    """
    Sends an embed that users can use reactions to vote on.

    Parameters
    ----------

    ctx (Context):
        Command invocation context.
    """
    embed = discord.Embed(
        title=f'Poll by **{ctx.author.name}**:',
        color=0x486572,
        description=' '.join(poll)
    )

    message = await ctx.send(embed=embed)

    await message.add_reaction(':heavy_check_mark:')
    await message.add_reaction(':x:')


# |----- REGISTERING MODULE -----|


def setup(client: commands.Bot):
    """Registers the functions in this module with the client.

    Parameters
    ----------

    client (Bot):
        Client instance, to add the commands to.
    """
    helpers.add_commands(client, choose, meme, poll)

