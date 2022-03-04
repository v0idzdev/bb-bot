from datetime import datetime
import discord
import asyncio
import chatbot
from discord.ext import commands


class ChatBot(commands.Cog):
    """Command/event category for the AI chatbot."""
    def __init__(self, bot: commands.Bot):
        self.chatbot = chatbot.init_chatbot() # Initialise the chatbot model from the _chatbot module
        self.bot = bot
        self.enabled_channels = [] # A list of all the channels AI chat is enabled in (!!! THIS MIGHT BE DODGY !!!)
        self.time_enabled = None

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Gets a response from the AI chatbot when someone sends a message."""

        if message.author.bot or message.channel not in self.enabled_channels:
            return # Do nothing if the bot sent the message or if this isn't an enabled channel
        if message.created_at < self.time_enabled: # Ignore all messages before the chatbot was enabled
            return
        if message.content.startswith("."): # If the message is a command, ignore it
            return

        # Show 'bot is typing' for 2 seconds
        ctx = await self.bot.get_context(message)

        async with ctx.typing():
            await asyncio.sleep(2)

        # Get and send an AI response
        response_ = self.chatbot.get_response(message.content)
        await message.channel.send(f"{message.author.mention}: {response_}")

    @commands.command(name="aienable", aliases=["ai", "enableaichat"],
                      description="Enables AI chatbot responses to all messages within a channel."
                                + "Requires 'Manage channels' permissions.")
    @commands.has_permissions(manage_channels=True)
    async def enable_ai_chat(self, ctx: commands.Context):
        """Enables AI chatbot responses in a text channel."""

        # Add the channel to the list. Check in on_message if this is an enabled channel
        if ctx.channel not in self.enabled_channels: # Check if not already enabled
            self.enabled_channels.append(ctx.channel)
            self.time_enabled = datetime.now()

            await ctx.send("✅ Done! I will now use AI to respond to all messages in this channel.\n"
                         + "You can use .aidisable or .disableaichat to disable chatbot responses.")
        else:
            await ctx.send("❌ You've already enabled AI chat in this channel.")

    @enable_ai_chat.error
    async def enable_ai_chat_error(self, ctx: commands.Context, error):
        """Called when the enable AI chat command throws an error."""

        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You don't have permission to enable AI chat in this channel.")

    @commands.command(name="aidisable", aliases=["disableaichat"],
                      description="Disables AI chatbot responses to all messages within a channel."
                                + "Requires 'Manage channels' permissions.")
    @commands.has_permissions(manage_channels=True)
    async def disable_ai_chat(self, ctx: commands.Context):
        """Disables AI chatbot responses in a text channel."""

        if ctx.channel in self.enabled_channels: # If the channel is enabled, disable it
            self.enabled_channels.remove(ctx.channel)

            await ctx.send("✅ Done! I will no longer use AI to respond to all messages in this channel.\n"
                         + "You can use .aienable, .ai, or .enableaichat to enable chatbot responses.")
        else:
            await ctx.send("❌ You've already disabled AI chat in this channel.")

    @disable_ai_chat.error
    async def disable_ai_chat_error(self, ctx: commands.Context, error):
        """Called when the disable AI chat command throws an error."""

        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You don't have permission to disable AI chat in this channel.")


def setup(bot: commands.Bot):
    """Adds the ChatBot cog to the bot"""
    bot.add_cog(ChatBot(bot))
