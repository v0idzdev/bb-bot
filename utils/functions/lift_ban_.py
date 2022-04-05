import discord
from discord.ext import commands


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
