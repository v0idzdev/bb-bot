"""
Module `general` contains standalone utility functions to be
used in BB.Bot extensions. These utilities are used in many
extensions, hence, 'general'.
"""
import discord
import datetime
import requests
import re

from bs4 import BeautifulSoup
from urllib import (
    parse,
    request
)

from typing import Any, Callable, List


def create_error_embed(message: str) -> discord.Embed:
    """
    This function formats a command invocation error message
    using an embed with a title and timestamp. It then sends
    the message using `interaction.response.send_message`.

    Params:
     - message (str): The error message to format using a `discord.Embed`.

    Returns:
     - A formatted `discord.Embed` containing the error message.
    """
    return discord.Embed(
        title=f"❌ An Error Occurred",
        description=f"🏷️ {message}",
        timestamp=datetime.datetime.utcnow(),
        color=discord.Color.red(),
    )