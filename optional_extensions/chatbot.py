import os
from urllib import response
import requests
import discord

from discord.ext import commands
from prsaw import RandomStuff


class ChatBotError(commands.CommandInvokeError):
    """Custom exception class for the AI chatbot.
    Lets us know that this module cause the error
    """


class ChatBot(commands.Cog):
    """Optional module for AI chatbot features.
    To use this module, a user must create a channel called 'chat-bot'
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Responds to a message in a text channel and gets an AI response"""

        rs = RandomStuff()

        response = rs.get_ai_response(message.content)
        await message.channel.send(f"<@{message.author.id}>: {response}")