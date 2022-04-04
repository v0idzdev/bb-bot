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

    message = f":tools: **{ctx.author.name}** was {action}"
    message += "." if reason is None else f" for **{reason}**."

    embed = discord.Embed(title="🛠️ User Sanctioned", description=f"⚙️ {message}")
    await ctx.send(embed=embed)
