import discord
from discord.ext import commands


async def sanction(
    ctx: commands.Context, punishment: str, member: discord.Member, reason=None
):
    """
    Utility function that kicks, bans, or softbans a member and sends a message.
    """
    if punishment == "ban":
        await member.ban()
        action = "permanently banned"

    if punishment == "softban":
        await member.ban()
        action = "temporarily banned"

    if punishment == "kick":
        await member.kick()
        action = "kicked"

    message = f"⚖️ **{ctx.author.name}** was {action}"
    message + "." if reason is None else f" for **{reason}**."

    embed = discord.Embed(title="🛠️ User Sanctioned", description=f"⚙️ {message}")
    await ctx.send(embed=embed)


async def lift_ban(ctx: commands.Context, ban_type: str, user: discord.User):
    """
    Utility function that unbans a member.
    """
    try:
        await ctx.guild.unban(user)

    except commands.UserNotFound:
        return await ctx.reply(f"❌ I couldn't find the user {user}.", delete_after=20)

    except discord.NotFound:
        return await ctx.reply(
            f"❌ Unbanning **{user}** was not possible. Please check that they are currently banned.",
            delete_after=20,
        )

    message = f":tools: {ctx.author.mention}: {user.name}'s {ban_type} ban was lifted."
    await ctx.send(message)
