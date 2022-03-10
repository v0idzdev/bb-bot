import discord
import asyncio

from discord.ext import commands
from typing import Optional # Lets us use Optional[type] for keyword args


class AdminCommandError(Exception):
    """
    Custom exception class for admin command errors.
    """


class Admin(commands.Cog):
    """
    Extension for admin-related commands.
    """
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(aliases=['b'])
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context, user: discord.Member, *, reason: Optional[str]=None):
        """
        Bans a user from a server.

        PARAMETERS
        ----------

        ctx (commands.Context): Command invocation context.
        user (discord.Member): The Discord user to ban from the server
        reason (str): The specified reason for the ban. Defaults to None.
        """
        # if ctx.message.author == self.client.user:
        #     return

        await ctx.guild.ban(user, reason=reason) # Ban the user in the server
        message = f':loudspeaker: You have been banned from **{ctx.guild.name}**' # Default message to DM to the user

        # If the sender didn't give a reason, just add a full stop at the end of the message
        # Else, add the reason at the end of the message
        if reason is None:
            message += '.'
        else:
            message += f'for **{reason}**.'

        # Send a message to the channel the command was used in, saying the user was banned
        await ctx.send(f':tools: **{user.name} has been successfully banned.')
        return await ctx.author.send(message) # DM the banned user the message

    @ban.error
    async def ban_error(self, ctx: commands.Context, error: Exception):
        """
        Handles errors raised in the ban method.

        PARAMETERS
        ----------

        ctx (commands.Context): Command invocation context.
        error (Exception): The error that was raised.
        """
        message = f':x: {ctx.author.mention}: ' # This will be the start of the error message we send

        # Check for missing perms and missing parameter exceptions and add the
        # appropriate string to the end of the message.
        #
        # If none of the below exceptions were raised, send a default error message
        if isinstance(error, commands.MissingPermissions):
            message += 'You aren\'t allowed to ban members.'
        elif isinstance(error, commands.MissingRequiredArgument):
            message += 'Please specify a user to ban.'
        else:
            message += 'Sorry, an unknown error occurred.'

        # Print the traceback and send the error message
        print(error.__traceback__)
        return await ctx.send(message)

    @commands.command(aliases=['k'])
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx: commands.Context, user: discord.Member, *, reason: Optional[str]=None):
        """
        Kicks a user from a server.

        PARAMETERS
        ----------

        ctx (commands.Context): Command invocation context.
        user (discord.Member): The Discord user to kick from the server
        reason (str): The specified reason for the kick. Defaults to None.
        """
        await ctx.guild.kick(user, reason=reason) # Kicks the user in the server
        message = f':loudspeaker: You have been kicked from **{ctx.guild.name}**' # Default message to DM to the user

        # If the sender didn't give a reason, just add a full stop at the end of the message
        # Else, add the reason at the end of the message
        if reason is None:
            message += '.'
        else:
            message += f'for **{reason}**.'

        # Send a message to the channel the command was used in, saying the user was kicked
        await ctx.send(f':tools: **{user.name} has been successfully kicked.')
        return await ctx.author.send(message) # DM the banned user the message

    @kick.error
    async def kick_error(self, ctx: commands.Context, error: Exception):
        """
        Handles errors raised in the kick method.

        PARAMETERS
        ----------

        ctx (commands.Context): Command invocation context.
        error (Exception): The error that was raised.
        """
        message = f':x: {ctx.author.mention}: ' # This will be the start of the error message we send

        # Check for missing perms and missing parameter exceptions and add the
        # appropriate string to the end of the message.
        #
        # If none of the below exceptions were raised, send a default error message
        if isinstance(error, commands.MissingPermissions):
            message += 'You aren\'t allowed to kick members.'
        elif isinstance(error, commands.MissingRequiredArgument):
            message += 'Please specify a user to kick.'
        else:
            message += 'Sorry, an unknown error occurred.'

        # Print the traceback and send the error message
        print(error.__traceback__)
        return await ctx.send(message)


