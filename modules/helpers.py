"""
Contains utility functions to assist command modules.
"""

import discord.ext.commands as commands
import discord


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


async def sanction(
    ctx: commands.Context, punishment: str, member: discord.Member, reason=None
):
    """
    Utility function that bans or kicks a member.

    Parameters
    ----------

    ctx (Context):
        Command invocation context.

    punishment (str):
        Either 'kick'/'ban' depending on the sanction.

    reason (str | None):
        The reason for the kick/ban.
    """
    match punishment:

        case "ban":
            await member.ban()
            action = "permanently banned"

        case "softban":
            await member.ban()
            action = "temporarily banned"

        case "kick":
            await member.kick()
            action = "kicked"

    message_server = f":tools: **{ctx.author.name}** was {action}"
    message_member = f":x: You were {action} from **{ctx.guild.name}**"

    for message in (message_server, message_member):
        message += "." if reason is None else f" for **{reason}**."

    await ctx.send(message_server)
    await member.send(message_member)


async def lift_ban(ctx: commands.Context, ban_type: str, user: discord.User):
    """
    Utility function that unbans a member.

    Outputs an appropriate message depending on whether the ban
    was permanent or temporary.

    Parameters
    ----------

    ctx (Context):
        Command invocation context.

    ban_type (str):
        The type of ban that the user had - either 'temporary' or 'permanent'

    reason (str | None):
        The reason for the kick/ban.
    """
    message = f":tools: {ctx.author.mention}: {user.name}'s {ban_type} ban was lifted."

    await ctx.guild.unban(user)
    await ctx.send(message)


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