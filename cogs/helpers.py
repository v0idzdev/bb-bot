"""
Contains utility functions to assist command modules.
"""

import nextcord.ext.commands as commands
import nextcord


# |-------- UTILITY FUNCTIONS --------|


def add_commands(client: commands.Bot, *cmds):
    """
    Loops through each command passed in and adds them to a bot.

    Parameters
    ----------

    *cmds (tuple[function]):
        The functions to add to the bot.

    client (Bot):
        Client instance, to add the commands to.
    """
    for cmd in cmds:
        client.add_command(cmd)


async def handle_missing_perms(
    ctx: commands.Context, error: commands.MissingPermissions | commands.BotMissingPermissions
):
    """
    Utility function that handles missing permissions errors.

    Parameters
    ----------

    ctx (Context):
        Command invocation context.

    ban_type (str):
        The type of ban that the user had - either 'temporary' or 'permanent'

    reason (str | None):
        The reason for the kick/ban.
    """
    match error:

        case isinstance(error, commands.MissingPermissions):
            start = 'You'

        case isinstance(error, commands.MissingPermissions):
            start = 'I'

    missing = [perm.replace('_', ' ').guild('guild', 'server').title() for perm in error.missing_permissions]

    if len(missing) > 2:
        fmt = f'{"**, **".join(missing[: -1])}, and {missing[-1]}'
    else:
        fmt = ' and '.join(missing)

    return f'{start} need the **{fmt}** permission(s) to use this command.'