"""
Contains all of the errors that the client will handle.

This is a global error handler and does not override local
error handlers.
"""

import discord.ext.commands as commands
import modules.utilities.helpers as helpers
import discord
import traceback
import math
import sys


# |-------- ERROR HANDLER --------|


async def on_command_error(ctx: commands.Context, error):
    """
    Handles errors raised by commands that are not locally handled.

    Called when a command throws an exception.

    Parameters
    ----------

    ctx (Context):
        Command invocation context.

    error:
        The command error that was raised.
    """
    if hasattr(ctx.command, 'on_error'):
        return

    error = getattr(error, 'original', error)
    message = ':x: '

    match True:

        case isinstance(error, commands.CommandNotFound):
            return

        case isinstance(error, commands.BotMissingPermissions):
            message += await helpers.handle_missing_perms(ctx, error)

        case isinstance(error, commands.MissingPermissions):
            message += await helpers.handle_missing_perms(ctx, error)

        case isinstance(error, commands.DisabledCommand):
            message += 'This command has been disabled.'

        case isinstance(error, commands.CommandOnCooldown):
            message += 'This command is on cooldown. Try again after' \
                + f'{math.ceil(error.retry_after)}s.'

        case isinstance(error, commands.UserInputError):
            message += 'Sorry, that input is invalid.'

        case isinstance(error, commands.UserInputError):
            try:
                message += 'You can\'t use this command in private messages.'

            except discord.Forbidden:
                return

        case _:
            print(f'Ignoring exceptions in command {ctx.command}', file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

            return

    await ctx.send(message)