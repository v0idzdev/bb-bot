"""
Contains all of the errors that the client will handle.

This is a global error handler and does not override local
error handlers.
"""

import discord.ext.commands as commands
import discord.ui as UI
import helpers
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
    message = f':x: {ctx.author.mention}'

    match error.__class__:

        case commands.CommandNotFound:
            message += 'That command does not exist.'

        case commands.BotMissingPermissions:
            message += await helpers.handle_missing_perms(ctx, error)

        case commands.MissingPermissions:
            message += await helpers.handle_missing_perms(ctx, error)

        case commands.DisabledCommand:
            message += 'This command has been disabled.'

        case commands.CommandOnCooldown:
            message += 'This command is on cooldown. Try again after ' \
                + f'{math.ceil(error.retry_after)}s.'

        case commands.UserInputError:
            message += 'Sorry, that input is invalid.'

        case commands.NoPrivateMessage:
            try:
                message += 'You can\'t use this command in private messages.'

            except discord.Forbidden:
                return

        case _:
            print(f'Ignoring exceptions in command {ctx.command}.', file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

            return

    button_continue = UI.Button(label='OK', style=discord.ButtonStyle.green)
    button_docspage = UI.Button(label='Help',
        url='https://github.com/matthewflegg/beepboop/blob/main/README.md',
    )

    button_continue.callback = lambda interaction: \
        (await interaction.message.delete(delay=3) for _ in '_').__anext__()

    view = UI.View()
    view.add_item(button_continue)
    view.add_item(button_docspage)

    return await ctx.send(message, view=view)


# |----- REGISTERING MODULE -----|


def setup(client: commands.Bot):
    """
    Registers the functions in this module with the client.

    Parameters
    ----------

    client (Bot):
        Client instance, to add the commands to.
    """
    client.add_listener(on_command_error, on_command_error.__name__)