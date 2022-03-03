import discord
import _chatbot
from discord.ext import commands


class ChatBot(commands.Cog):
    """Command/event category for the AI chatbot"""
    def __init__(self, bot: commands.Bot):
        self.chatbot = _chatbot.init_chatbot() # Initialise the chatbot model from the _chatbot module
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Gets a response from the AI chatbot when someone sends a message"""

        if message.author.bot:
            return # Do nothing if the bot sent the message

        # This is the equivalent of response_ = await self.chatbot.get_response, but
        # asyncio throws an exception when attempting to use a method within an
        # await statement
        response_ = self.chatbot.get_response(message.content)
        await message.channel.send(f"{message.author.mention}: {response_}")


def setup(bot: commands.Bot):
    """Adds the 'ChatBot' cog to the bot"""
    bot.add_cog(ChatBot(bot))
