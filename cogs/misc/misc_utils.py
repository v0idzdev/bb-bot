import requests
import datetime
import discord
import re

from bs4 import BeautifulSoup
from urllib import parse, request


async def fetch_from_youtube(search: str):
    """
    Searches YouTube for a video and returns a url and an embed.
    """
    # Getting the link for the first search result
    query = parse.urlencode({"search_query": search})
    content = request.urlopen("http://www.youtube.com/results?" + query)
    results = re.findall(r"watch\?v=(\S{11})", content.read().decode())

    url = "https://www.youtube.com/watch?v=" + results[0]

    # Getting the title of the video
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, "html.parser")
    title = ""

    for title_ in soup.find_all("title"):
        title += title_.get_text()

    # Getting the thumbnail of the video
    exp = r"^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*"
    s = re.findall(exp, url)[0][-1]
    thumbnail = f"https://i.ytimg.com/vi/{s}/maxresdefault.jpg"

    # Creating the embed to send to the channel
    embed = discord.Embed(
        title="🎲 Found a Video",
        description=f"🔗 [{title}]({url})",
        timestamp=datetime.datetime.utcnow(),
    )
    embed.set_thumbnail(url=thumbnail)
    embed.set_footer(text=f"❓ Follow the link above to view the video.")

    return embed, url
