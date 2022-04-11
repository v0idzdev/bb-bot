"""
Contains all of the errors that the client will handle.

This is a global error handler and does not override local
error handlers.
"""

import discord
import traceback
import math
import sys

from discord.ext import commands
from discord import app_commands

class ErrorHandler(commands.Cog):
    """
    Manages global errors that are otherwise not locally handled.
    """

    def __init__(self, client: commands.Bot):
        self.client = client

    async def handle_missing_perms(
        self,
        ctx: commands.Context,
        error: commands.MissingPermissions | commands.BotMissingPermissions,
    ):
        """
        Utility function that handles missing permissions errors.
        """
        match error:

            case isinstance(error, commands.MissingPermissions):
                start = "You"

            case isinstance(error, commands.MissingPermissions):
                start = "I"

        missing = [
            perm.replace("_", " ").guild("guild", "server").title()
            for perm in error.missing_permissions
        ]

        if len(missing) > 2:
            fmt = f'{"**, **".join(missing[: -1])}, and {missing[-1]}'
        else:
            fmt = " and ".join(missing)

        return f"{start} need the **{fmt}** permission(s) to use this command."

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        """
        Handles errors raised by commands that are not locally handled.
        """
        if hasattr(ctx.command, "on_error"):
            return

        error = getattr(error, "original", error)
        message = f":x: "

        if isinstance(error, commands.CommandNotFound):
            message += "That command does not exist."

        elif isinstance(error, commands.BotMissingPermissions) or isinstance(error, commands.MissingPermissions):
            message += await self.handle_missing_perms(ctx, error)

        elif isinstance(error, commands.DisabledCommand):
            message += "This command has been disabled."

        elif isinstance(error, commands.CommandOnCooldown):
            message += f"This command is on cooldown. Try again after {math.ceil(error.retry_after)} seconds.."

        elif isinstance(error, commands.UserInputError):
            message += "Sorry, that input is invalid."

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                message += "You can't use this command in private messages."
            except discord.Forbidden:
                return

        else:
            print(f"Ignoring exceptions in command {ctx.command}.", file=sys.stderr)
            traceback.print_exception(
                type(error), error, error.__traceback__, file=sys.stderr
            )

            return

        return await ctx.reply(message, delete_after=20)


async def setup(client: commands.Bot):
    """
    Registers the cog with the client.
    """
    await client.add_cog(ErrorHandler(client))


async def teardown(client: commands.Bot):
    """
    Un-registers the cog with the client.
    """
    await client.remove_cog(ErrorHandler(client))
