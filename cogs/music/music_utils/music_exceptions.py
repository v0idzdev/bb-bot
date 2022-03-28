from discord.ext import commands


class VCError(commands.CommandError):
    """
    Exception class for connection errors.
    """


class InvalidVC(VCError):
    """
    Exception class for invalid VCs.
    """
