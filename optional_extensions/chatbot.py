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

        if message.author == self.bot:
            return # Do nothing if the bot sent the message

        chatbot_ = self.chatbot # I have to do it this way because I can't use an object statement in an "await"
        response_ = await chatbot_.get_response(message.content)
        await message.channel.send(f"{message.author.mention}: {response_}")


def setup(bot: commands.Bot):
    """Adds the 'ChatBot' cog to the bot"""
    bot.add_cog(ChatBot(bot))
