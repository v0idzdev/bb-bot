import discord
from discord.ext import commands


async def sanction(
    ctx: commands.Context, punishment: str, member: discord.Member, reason=None
):
    """
    Utility function that bans or kicks a member.
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

    for (
        message
    ) in (  # Generate the start of a message to send to the user and the server
        message_server := f":tools: **{ctx.author.name}** was {action}",
        message_member := f":x: You were {action} from **{ctx.guild.name}**",
    ):
        message += (
            "." if reason is None else f" for **{reason}**."
        )  # Then add the correct ending

    await ctx.send(message_server)
    await member.send(message_member)