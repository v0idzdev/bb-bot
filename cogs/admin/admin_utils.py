import discord
import json

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


async def lift_ban(ctx: commands.Context, ban_type: str, user: discord.User):
    """
    Utility function that unbans a member.
    """
    message = f":tools: {ctx.author.mention}: {user.name}'s {ban_type} ban was lifted."

    await ctx.guild.unban(user)
    await ctx.send(message)


async def handle_id(interaction: discord.Interaction, server_id: str, blacklist: dict, filepath: str):
    """
    Checks if a server ID is in the blacklist, and deletes it if it is.

    Returns None if the ID is not found.
    """
    if server_id == id:
        del blacklist[server_id]

        with open(filepath, "w") as file:
            json.dump(blacklist, file, indent=4)

        return await interaction.message.channel.send(
            f":thumbsup: {interaction.message.author.mention}: The blacklist for this server"
            + f" has successfully been deleted."
        )
