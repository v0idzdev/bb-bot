import asyncio
import datetime
import functools

import discord
from discord.ext import commands


def session_check(coro):
    async def wrapper(self, *args, **kwargs):
        await self.require_session()
        return await coro(self, *args, **kwargs)
    return wrapper

def authorization_check(coro):
    async def wrapper(self, *args, **kwargs):
        if self.authorized and self.authorized['datetime'] < datetime.datetime.utcnow():
            await self.authorize()
        elif not self.authorized:
            await self.authorize()
        return await coro(self, *args, **kwargs) 
    return wrapper

def executor(func):
    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        partial = functools.partial(func, *args, **kwargs)
        return loop.run_in_executor(None, partial)
    return wrapper


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
