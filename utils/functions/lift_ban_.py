import discord
from discord.ext import commands


async def lift_ban(ctx: commands.Context, ban_type: str, user: discord.User):
    """
    Utility function that unbans a member.
    """
    message = f":tools: {ctx.author.mention}: {user.name}'s {ban_type} ban was lifted."

    await ctx.guild.unban(user)
    await ctx.send(message)
