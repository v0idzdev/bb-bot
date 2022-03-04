import traceback
import discord
import math
import sys
from discord.ext import commands


class GenericErrorHandler(commands.Cog):
    """Generic error handler.
    Used if local (cog-specific) error handlers fail to catch exceptions.
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        """Generic command error handler."""
        if hasattr(ctx.command, "on_error"): # Don't override local errors
            return

        error = getattr(error, "original", error)

        if isinstance(error, commands.CommandNotFound):
            return

        if isinstance(error, commands.BotMissingPermissions): # Error handling for missing bot perms
            missing = [perm.replace("_", " ").replace("guild", "server").title() for perm in error.missing_perms]

            if len(missing) > 2:
                format_ = f"{'**, **'.join(missing[: -1])}, and {missing[-1]}"
            else:
                format_ = " and ".join(missing)

            message_ = f"I need the **{format_}** permission(s) to use this command."
            await ctx.send(message_)
            return

        if isinstance(error, commands.DisabledCommand): # Command is disabled
            await ctx.send("This command has been disabled.")
            return

        if isinstance(error, commands.CommandOnCooldown): # Command is currently on cooldown
            await ctx.send(f"This command is currently on cooldown. Try again in {math.ceil(error.retry_after)}s")
            return

        if isinstance(error, commands.MissingPermissions): # Error handling for missing user perms
            missing = [perm.replace("_", " ").replace("guild", "server").title() for perm in error.missing_perms]

            if len(missing) > 2:
                format_ = f"{'**, **'.join(missing[: -1])}, and {missing[-1]}"
            else:
                format_ = " and ".join(missing)

            message_ = f"You need the **{format_}** permission(s) to use this command."
            await ctx.send(message_)
            return

        if isinstance(error, commands.UserInputError): # If the bot receives bad input
            await ctx.send("Sorry, that input is invalid.")
            return

        if isinstance(error, commands.NoPrivateMessage): # If the user can't use the command in a DM
            try:
                await ctx.author.send("You can't use this command in private messages.")
            except discord.Forbidden:
                pass
            return

        print(f"Ignoring exceptions in command {ctx.command}", file=sys.stderr) # Print errors to stderr
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


def setup(bot: commands.Bot):
    """Adds the 'GenericErrorHandler' cog to the bot."""
    bot.add_cog(GenericErrorHandler(bot))