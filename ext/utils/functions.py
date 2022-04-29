"""
Module `functions` contains standalone utility functions to be
used in BB.Bot extensions. 
"""
import functools
from typing import Any, Callable, List
import discord
import datetime
import requests
import re

from bs4 import BeautifulSoup
from urllib import (
    parse,
    request
)


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


async def youtube_search_to_url(search_query: str) -> str:
    """
    Returns the first result in a Youtube search for a given
    query. 

    Params:
     - search_query (str): The search terms to use.
    
    Returns:
     - The URL of the first result found.
    """
    query = parse.urlencode({"search_query": search_query})
    content = request.urlopen("http://www.youtube.com/results?" + query)
    results = re.findall(r"watch\?v=(\S{11})", content.read().decode())
    return "https://www.youtube.com/watch?v=" + results[0]


async def youtube_url_to_title(url: str) -> str:
    """
    Returns the title of a Youtube video, given a video's URL.

    Params:
     - url (str): The URL of the Youtube video.
    
    Returns:
     - The title of the Youtube video.
    """
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, "html.parser")

    return "".join([t for t in soup.find("title")])


async def youtube_url_to_thumbnail(url: str) -> str:
    """
    Returns the thumbnail of a Youtube video, given a video's URL.

    Params:
     - url (str): The URL of the Youtube video.
    
    Returns:
     - A URL for the thumbnail of the Youtube video.
    """
    exp = r"^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*"
    s = re.findall(exp, url)[0][-1]
    return f"https://i.ytimg.com/vi/{s}/maxresdefault.jpg"