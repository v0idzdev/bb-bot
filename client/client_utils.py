import discord
from discord.ext import commands


def get_prefix(bot: commands.Bot, message: discord.Message):
    """
    Returns the client's command prefix.
    """
    return (
        "?" if bot.user.name == "BB.Bot | Dev" else "~"
    )  # Set the prefix to '?' if the bot is the development version
